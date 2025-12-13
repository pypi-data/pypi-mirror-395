import base64
from os.path import exists, join
import os
from os import makedirs
from re import findall
import re
import shutil
import glob
import logging
import warnings
from io import StringIO
from contextlib import redirect_stderr
from langfuse import Langfuse
from langfuse.api.resources.commons.errors import Error as LangfuseError, NotFoundError
import litellm
from ara_cli.classifier import Classifier
from ara_cli.artefact_creator import ArtefactCreator
from ara_cli.template_manager import TemplatePathManager
from ara_cli.ara_config import ConfigManager
from ara_cli.file_lister import generate_markdown_listing


class LLMSingleton:
    _instance = None
    _default_model = None
    _extraction_model = None
    langfuse = None

    def __init__(self, default_model_id, extraction_model_id):
        config = ConfigManager().get_config()
        default_config_data = config.llm_config.get(str(default_model_id))

        if not default_config_data:
            raise ValueError(
                f"No configuration found for the default model: {default_model_id}"
            )
        self.default_config_params = default_config_data.model_dump(exclude_none=True)

        extraction_config_data = config.llm_config.get(str(extraction_model_id))
        if not extraction_config_data:
            raise ValueError(
                f"No configuration found for the extraction model: {extraction_model_id}"
            )
        self.extraction_config_params = extraction_config_data.model_dump(
            exclude_none=True
        )

        langfuse_public_key = os.getenv("ARA_CLI_LANGFUSE_PUBLIC_KEY")
        langfuse_secret_key = os.getenv("ARA_CLI_LANGFUSE_SECRET_KEY")
        langfuse_host = os.getenv("LANGFUSE_HOST")

        captured_stderr = StringIO()
        with redirect_stderr(captured_stderr):
            self.langfuse = Langfuse(
                public_key=langfuse_public_key,
                secret_key=langfuse_secret_key,
                host=langfuse_host,
            )

        # Check if there was an authentication error
        stderr_output = captured_stderr.getvalue()
        if "Authentication error" in stderr_output:
            warnings.warn(
                "Invalid Langfuse credentials - prompt tracing disabled and using default prompts. "
                "Set environment variables 'ARA_CLI_LANGFUSE_PUBLIC_KEY', 'ARA_CLI_LANGFUSE_SECRET_KEY', "
                "'LANGFUSE_HOST' and restart application to use Langfuse capabilities",
                UserWarning,
            )

        LLMSingleton._default_model = default_model_id
        LLMSingleton._extraction_model = extraction_model_id
        LLMSingleton._instance = self

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            config = ConfigManager().get_config()
            default_model = config.default_llm
            if not default_model:
                if not config.llm_config:
                    raise ValueError(
                        "No LLM configurations are defined in the configuration file."
                    )
                default_model = next(iter(config.llm_config))

            extraction_model = getattr(config, "extraction_llm", default_model)
            if not extraction_model:
                extraction_model = default_model

            cls(default_model, extraction_model)
        return cls._instance

    @classmethod
    def get_config_by_purpose(cls, purpose="default"):
        """
        purpose= 'default' or 'extraction'
        """
        instance = cls.get_instance()
        if purpose == "extraction":
            return instance.extraction_config_params.copy()
        return instance.default_config_params.copy()

    @classmethod
    def set_default_model(cls, model_name):
        """Sets the default language model for the current session."""
        cls.get_instance()
        if model_name == cls._default_model:
            return cls._instance
        cls(model_name, cls._extraction_model)
        return cls._instance

    @classmethod
    def set_extraction_model(cls, model_name):
        """Sets the extraction language model for the current session."""
        cls.get_instance()
        if model_name == cls._extraction_model:
            return cls._instance
        cls(cls._default_model, model_name)
        return cls._instance

    @classmethod
    def get_default_model(cls):
        """Gets the default model name stored in the singleton instance."""
        if cls._instance is None:
            cls.get_instance()
        return cls._default_model

    @classmethod
    def get_extraction_model(cls):
        """Gets the extraction model name stored in the singleton instance."""
        if cls._instance is None:
            cls.get_instance()
        return cls._extraction_model


def write_string_to_file(filename, string, mode):
    with open(filename, mode, encoding="utf-8") as file:
        file.write(f"\n{string}\n")
    return file


def read_string_from_file(path):
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()
    return text


def _is_valid_message(message: dict) -> bool:
    """
    Checks if a message in a prompt is valid (i.e., not empty).
    It handles both string content and list content (for multimodal inputs).
    """
    content = message.get("content")

    if isinstance(content, str):
        return content.strip() != ""

    if isinstance(content, list):
        # For multimodal content, check if there's at least one non-empty text part.
        return any(
            item.get("type") == "text" and item.get("text", "").strip() != ""
            for item in content
        )

    return False


def _norm(p: str) -> str:
    """Normalize slashes and collapse .. segments."""
    return os.path.normpath(p) if p else p


def resolve_existing_path(rel_or_abs_path: str, anchor_dir: str) -> str:
    """
    Resolve a potentially relative path to an existing absolute path.

    Strategy:
    - If already absolute and exists -> return it.
    - Else, try from the anchor_dir.
    - Else, walk up parent directories from anchor_dir and try joining at each level.
    - If nothing is found, return the normalized original (will fail later with clear message).
    """
    if not rel_or_abs_path:
        return rel_or_abs_path

    candidate = _norm(rel_or_abs_path)

    if os.path.isabs(candidate) and os.path.exists(candidate):
        return candidate

    anchor_dir = os.path.abspath(anchor_dir or os.getcwd())

    # Try from anchor dir directly
    direct = _norm(os.path.join(anchor_dir, candidate))
    if os.path.exists(direct):
        return direct

    # Walk parents
    cur = anchor_dir
    prev = None
    while cur and cur != prev:
        test = _norm(os.path.join(cur, candidate))
        if os.path.exists(test):
            return test
        prev = cur
        cur = os.path.dirname(cur)

    # Give back normalized candidate; open() will raise, but at least path is clean
    return candidate


def send_prompt(prompt, purpose="default"):
    """Prepares and sends a prompt to the LLM, streaming the response."""
    chat_instance = LLMSingleton.get_instance()
    config_parameters = chat_instance.get_config_by_purpose(purpose)
    model_info = config_parameters.get("model", "unknown_model")

    with LLMSingleton.get_instance().langfuse.start_as_current_span(
        name="send_prompt"
    ) as span:
        span.update_trace(
            input={"prompt": prompt, "purpose": purpose, "model": model_info}
        )

        config_parameters.pop("provider", None)

        filtered_prompt = [msg for msg in prompt if _is_valid_message(msg)]

        completion = litellm.completion(
            **config_parameters, messages=filtered_prompt, stream=True
        )
        response_text = ""
        try:
            for chunk in completion:
                chunk_content = chunk.choices[0].delta.content
                if chunk_content:
                    response_text += chunk_content
                yield chunk

            # Update Langfuse span with success output
            span.update(
                output={
                    "success": True,
                    "response_length": len(response_text),
                    "response": response_text,
                }
            )

        except Exception as e:
            # Update Langfuse span with error details
            span.update(output={"error": str(e)}, level="ERROR")
            raise


def describe_image(image_path: str) -> str:
    """
    Send an image to the LLM and get a text description.

    Args:
        image_path: Path to the image file

    Returns:
        Text description of the image
    """
    with LLMSingleton.get_instance().langfuse.start_as_current_span(
        name="ara-cli/describe-image"
    ) as span:
        span.update_trace(input={"image_path": image_path})

        try:
            langfuse_prompt = LLMSingleton.get_instance().langfuse.get_prompt(
                "ara-cli/describe-image"
            )
            describe_image_prompt = (
                langfuse_prompt.prompt if langfuse_prompt.prompt else None
            )
        except (LangfuseError, NotFoundError, Exception) as e:
            logging.info(f"Could not fetch Langfuse prompt: {e}")
            describe_image_prompt = None

        # Fallback to default prompt if Langfuse prompt is not available
        if not describe_image_prompt:
            logging.info("Using default describe-image prompt.")
            describe_image_prompt = (
                "Please describe this image in detail. If it contains text, transcribe it exactly. "
                "If it's a diagram or chart, explain its structure and content. If it's a photo or illustration, "
                "describe what you see."
            )

        # Resolve and read the image
        resolved_image_path = resolve_existing_path(image_path, os.getcwd())
        with open(resolved_image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        # Determine image type
        image_extension = os.path.splitext(resolved_image_path)[1].lower()
        mime_type = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".bmp": "image/bmp",
        }.get(image_extension, "image/png")

        # Create message with image
        message = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": describe_image_prompt,
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{base64_image}"},
                },
            ],
        }

        # Get response from LLM using the extraction model purpose
        response_text = ""
        for chunk in send_prompt([message], purpose="extraction"):
            chunk_content = chunk.choices[0].delta.content
            if chunk_content:
                response_text += chunk_content

        response_text = response_text.strip()

        span.update(
            output={
                "success": True,
                "description_length": len(response_text),
                "response": response_text,
            }
        )

        return response_text


def append_headings(classifier, param, heading_name):
    sub_directory = Classifier.get_sub_directory(classifier)

    artefact_data_path = _norm(
        f"ara/{sub_directory}/{param}.data/{classifier}.prompt_log.md"
    )

    # Check if the file exists, and if not, create an empty file
    if not os.path.exists(artefact_data_path):
        with open(artefact_data_path, "w", encoding="utf-8") as file:
            file.write("")

    content = read_string_from_file(artefact_data_path)
    pattern = r"## {}_(\d+)".format(heading_name)
    matches = findall(pattern, content)

    max_number = 1
    if matches:
        max_number = max(map(int, matches)) + 1
    heading = f"## {heading_name}_{max_number}"

    write_string_to_file(artefact_data_path, heading, "a")


def write_prompt_result(classifier, param, text):
    sub_directory = Classifier.get_sub_directory(classifier)
    artefact_data_path = _norm(
        f"ara/{sub_directory}/{param}.data/{classifier}.prompt_log.md"
    )
    write_string_to_file(artefact_data_path, text, "a")


def prompt_data_directory_creation(classifier, parameter):
    sub_directory = Classifier.get_sub_directory(classifier)
    prompt_data_path = _norm(f"ara/{sub_directory}/{parameter}.data/prompt.data")
    if not exists(prompt_data_path):
        makedirs(prompt_data_path)
    return prompt_data_path


def get_file_content(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def initialize_prompt_templates(classifier, parameter):
    prompt_data_path = prompt_data_directory_creation(classifier, parameter)
    prompt_log_path = os.path.dirname(prompt_data_path)

    template_path = os.path.join(os.path.dirname(__file__), "templates")
    artefact_creator = ArtefactCreator()
    artefact_creator.create_artefact_prompt_files(
        prompt_log_path, template_path, classifier
    )

    generate_config_prompt_template_file(prompt_data_path, "config.prompt_templates.md")

    # Mark the relevant artefact in the givens list
    generate_config_prompt_givens_file(
        prompt_data_path,
        "config.prompt_givens.md",
        artefact_to_mark=f"{parameter}.{classifier}",
    )

    # Only once (was duplicated before)
    generate_config_prompt_global_givens_file(
        prompt_data_path, "config.prompt_global_givens.md"
    )


def write_template_files_to_config(template_type, config_file, base_template_path):
    template_path = os.path.join(base_template_path, template_type)
    for root, _, files in os.walk(template_path):
        for file in sorted(files):
            config_file.write(f"  - [] {template_type}/{file}\n")


def load_selected_prompt_templates(classifier, parameter):
    sub_directory = Classifier.get_sub_directory(classifier)
    prompt_data_path = _norm(f"ara/{sub_directory}/{parameter}.data/prompt.data")
    config_file_path = os.path.join(prompt_data_path, "config.prompt_templates.md")

    if not os.path.exists(config_file_path):
        print("WARNING: config.prompt_templates.md does not exist.")
        return

    with open(config_file_path, "r", encoding="utf-8") as config_file:
        content = config_file.read()

    global_base_template_path = TemplatePathManager.get_template_base_path()
    local_base_template_path = ConfigManager.get_config().local_prompt_templates_dir

    markdown_items = extract_and_load_markdown_files(config_file_path)

    # Ensure the prompt archive directory exists
    prompt_archive_path = os.path.join(prompt_data_path, "prompt.archive")
    if not os.path.exists(prompt_archive_path):
        os.makedirs(prompt_archive_path)
        print(f"Created archive directory: {prompt_archive_path}")

    for item in markdown_items:
        if item.startswith("custom-prompt-modules"):
            source_path = os.path.join(local_base_template_path, item)
            target_path = os.path.join(prompt_data_path, os.path.basename(item))
        elif item.startswith("prompt-modules"):
            source_path = os.path.join(global_base_template_path, item)
            target_path = os.path.join(prompt_data_path, os.path.basename(item))
        else:
            print(f"WARNING: Unrecognized template type for item {item}.")
            continue

        move_and_copy_files(source_path, prompt_data_path, prompt_archive_path)


def find_files_with_endings(directory, endings):
    """
    this function finds only files in the given directory it does not iterate recursively over sub directories
    """

    # Create an empty dictionary to store files according to their endings
    files_by_ending = {ending: [] for ending in endings}

    files = [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]
    # Walk through the files list
    for file in files:
        # Check each file to see if it ends with one of the specified endings
        for ending in endings:
            if file.endswith(ending):
                # If it does, append the file to the corresponding list
                files_by_ending[ending].append(file)
                break  # Move to the next file after finding a matching ending

    # Collect and sort files by the order of their endings, flatten the dictionary values into a list
    sorted_files = []
    for ending in endings:
        sorted_files.extend(files_by_ending[ending])

    return sorted_files


def move_and_copy_files(source_path, prompt_data_path, prompt_archive_path):
    """
    method detects existing prompt templates in the prompt.data directory and move them to the prompt.archive directory before new prompt templates are loaded in the prompt.data directory. So it is guaranteed, that only one .rules.md, .commands.md and .intention.md exists in the prompt.data directory
    """
    if os.path.exists(source_path):
        file_name = os.path.basename(source_path)

        # Check the name ending and extension of source path
        endings = [".blueprint.md", ".commands.md", ".rules.md", ".intention.md"]
        if any(file_name.endswith(ext) for ext in endings):
            for ext in endings:
                if file_name.endswith(ext):
                    # Define glob pattern to match all files with the same ending in the prompt_data_path
                    glob_pattern = os.path.join(prompt_data_path, f"*{ext}")

                    # Move all existing files with the same ending to the prompt_archive_path
                    for existing_file in glob.glob(glob_pattern):
                        archived_file_path = os.path.join(
                            prompt_archive_path, os.path.basename(existing_file)
                        )
                        shutil.move(existing_file, archived_file_path)
                        print(
                            f"Moved existing prompt-module: {os.path.basename(existing_file)} to prompt.archive"
                        )

                    # Copy the source_path file to the prompt_data_path directory
                    target_path = os.path.join(prompt_data_path, file_name)
                    shutil.copy(source_path, target_path)
                    print(f"Loaded new prompt-module: {os.path.basename(target_path)}")

        else:
            print(
                f"File name {file_name} does not end with one of the specified patterns, skipping move and copy."
            )
    else:
        print(f"WARNING: template {source_path} does not exist.")


def extract_and_load_markdown_files(md_prompt_file_path):
    """
    Extracts markdown files paths based on checked items and constructs proper paths
    respecting markdown header hierarchy. **Returns normalized relative paths**
    (not resolved), and resolution happens later relative to the config file dir.
    """
    header_stack = []
    path_accumulator = []
    with open(md_prompt_file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip().startswith("#"):
                level = line.count("#")
                header = line.strip().strip("#").strip()
                # Adjust the stack based on the current header level
                current_depth = len(header_stack)
                if level <= current_depth:
                    header_stack = header_stack[: level - 1]
                header_stack.append(header)
            elif "[x]" in line:
                relative_path = line.split("]")[-1].strip()
                # Use os.path.join for OS-safe joining, then normalize
                full_rel_path = os.path.join(*header_stack, relative_path) if header_stack else relative_path
                path_accumulator.append(_norm(full_rel_path))
    return path_accumulator


def load_givens(file_path):
    """
    Reads marked givens from a config markdown and returns:
      - combined markdown content (including code fences / images)
      - a list of image data dicts for the multimodal message
    Paths inside the markdown are resolved robustly relative to the config file directory (and its parents).
    """
    content = ""
    image_data_list = []
    markdown_items = extract_and_load_markdown_files(file_path)

    if not markdown_items:
        return "", []

    content = "### GIVENS\n\n"

    anchor_dir = os.path.dirname(os.path.abspath(file_path))

    for item in markdown_items:
        resolved = resolve_existing_path(item, anchor_dir)
        # Keep the listing line readable, show the original relative item
        content += item + "\n"

        ext = os.path.splitext(resolved)[1].lower()

        # Image branch
        if ext in (".png", ".jpeg", ".jpg", ".gif", ".bmp"):
            with open(resolved, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")

            mime_type = {
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".gif": "image/gif",
                ".bmp": "image/bmp",
            }.get(ext, "image/png")

            image_data_list.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{base64_image}"},
                }
            )
            # Also embed inline for the prompt markdown (use png as a neutral default for data URI)
            content += f"![{item}](data:{mime_type};base64,{base64_image})\n"

        else:
            # Check if the item specifies line ranges: e.g. "[10:20,25:30] filePath"
            match = re.match(r".*?\[(\d+:\d+(?:,\s*\d+:\d+)*)\]\s+(.+)", item)
            if match:
                line_ranges, file_name = match.groups()
                resolved_sub = resolve_existing_path(file_name, anchor_dir)
                content += "```\n"
                content += get_partial_file_content(resolved_sub, line_ranges) + "\n"
                content += "```\n\n"
            else:
                content += "```\n"
                content += get_file_content(resolved) + "\n"
                content += "```\n\n"

    return content, image_data_list


def get_partial_file_content(file_name, line_ranges):
    """
    Reads specific lines from a file based on the line ranges provided.

    Args:
    file_name (str): The path to the file (absolute or relative, already resolved by caller).
    line_ranges (str): A string representing the line ranges to read, e.g., '10:20,25:30'.

    Returns:
    str: The content of the specified lines.
    """
    line_ranges = line_ranges.strip("[]").split(",")
    lines_to_read = []
    for line_range in line_ranges:
        start, end = map(int, line_range.split(":"))
        lines_to_read.extend(range(start, end + 1))

    partial_content = []
    with open(file_name, "r", encoding="utf-8") as file:
        for i, line in enumerate(file, 1):
            if i in lines_to_read:
                partial_content.append(line)

    return "".join(partial_content)


def collect_file_content_by_extension(prompt_data_path, extensions):
    combined_content = ""
    image_data_list = []
    for ext in extensions:
        files = find_files_with_endings(prompt_data_path, [ext])
        for file_name in files:
            file_path = join(prompt_data_path, file_name)
            if ext in [".prompt_givens.md", ".prompt_global_givens.md"]:
                givens, image_data = load_givens(file_path)
                combined_content += givens
                image_data_list.extend(image_data)
            else:
                combined_content += get_file_content(file_path) + "\n\n"
    return combined_content, image_data_list


def prepend_system_prompt(message_list):
    try:
        langfuse_prompt = LLMSingleton.get_instance().langfuse.get_prompt(
            "ara-cli/system-prompt"
        )
        system_prompt = langfuse_prompt.prompt if langfuse_prompt.prompt else None
    except (LangfuseError, NotFoundError, Exception) as e:
        logging.info(f"Could not fetch Langfuse system prompt: {e}")
        system_prompt = None

    # Fallback to default prompt if Langfuse prompt is not available
    if not system_prompt:
        logging.info("Using default system prompt.")
        system_prompt = "You are a helpful assistant that can process both text and images."

    # Prepend the system prompt
    system_prompt_message = {"role": "system", "content": system_prompt}

    message_list.insert(0, system_prompt_message)
    return message_list


def append_images_to_message(message, image_data_list):
    """
    Appends image data list to a single message dict (NOT to a list).
    """
    logger = logging.getLogger(__name__)

    logger.debug(
        f"append_images_to_message called with image_data_list length: {len(image_data_list) if image_data_list else 0}"
    )

    if not image_data_list:
        logger.debug("No images to append, returning original message")
        return message

    message_content = message.get("content")
    logger.debug(f"Original message content: {message_content}")

    if isinstance(message_content, str):
        message["content"] = [{"type": "text", "text": message_content}]

    if isinstance(message["content"], list):
        message["content"].extend(image_data_list)
    else:
        # If somehow content is not list or str, coerce to list
        message["content"] = [{"type": "text", "text": str(message_content)}] + image_data_list

    logger.debug(f"Updated message content with {len(image_data_list)} images")

    return message


def create_and_send_custom_prompt(classifier, parameter):
    sub_directory = Classifier.get_sub_directory(classifier)
    prompt_data_path = _norm(f"ara/{sub_directory}/{parameter}.data/prompt.data")
    prompt_file_path_markdown = join(prompt_data_path, f"{classifier}.prompt.md")

    extensions = [
        ".blueprint.md",
        ".rules.md",
        ".prompt_givens.md",
        ".prompt_global_givens.md",
        ".intention.md",
        ".commands.md",
    ]
    combined_content_markdown, image_data_list = collect_file_content_by_extension(
        prompt_data_path, extensions
    )

    with open(prompt_file_path_markdown, "w", encoding="utf-8") as file:
        file.write(combined_content_markdown)

    prompt = read_string_from_file(prompt_file_path_markdown)
    append_headings(classifier, parameter, "prompt")
    write_prompt_result(classifier, parameter, prompt)

    # Build message and append images correctly (fixed)
    message = {"role": "user", "content": combined_content_markdown}
    message = append_images_to_message(message, image_data_list)
    message_list = [message]

    append_headings(classifier, parameter, "result")

    artefact_data_path = _norm(
        f"ara/{sub_directory}/{parameter}.data/{classifier}.prompt_log.md"
    )
    with open(artefact_data_path, "a", encoding="utf-8") as file:
        for chunk in send_prompt(message_list):
            chunk_content = chunk.choices[0].delta.content
            if not chunk_content:
                continue
            file.write(chunk_content)
            file.flush()


def generate_config_prompt_template_file(
    prompt_data_path, config_prompt_templates_name
):
    config_prompt_templates_path = os.path.join(
        prompt_data_path, config_prompt_templates_name
    )
    # Use instance method consistently
    config = ConfigManager().get_config()
    global_prompt_template_path = TemplatePathManager.get_template_base_path()
    dir_list = ["ara/.araconfig/custom-prompt-modules"] + [
        f"{os.path.join(global_prompt_template_path,'prompt-modules')}"
    ]
    file_list = ["*.blueprint.md", "*.rules.md", "*.intention.md", "*.commands.md"]

    print(f"used {dir_list} for prompt templates file listing")
    generate_markdown_listing(dir_list, file_list, config_prompt_templates_path)


def generate_config_prompt_givens_file(
    prompt_data_path, config_prompt_givens_name, artefact_to_mark=None
):
    config_prompt_givens_path = os.path.join(
        prompt_data_path, config_prompt_givens_name
    )
    config = ConfigManager().get_config()
    dir_list = (
        ["ara"]
        + [path for d in config.ext_code_dirs for path in d.values()]
        + [config.doc_dir]
        + [config.glossary_dir]
    )

    print(f"used {dir_list} for prompt givens file listing")
    generate_markdown_listing(
        dir_list, config.ara_prompt_given_list_includes, config_prompt_givens_path
    )

    # If an artefact is specified, mark it with [x]
    if artefact_to_mark:
        print(
            f"artefact {artefact_to_mark} marked in related config.prompt_givens.md per default"
        )

        # Read the generated file content
        with open(config_prompt_givens_path, "r", encoding="utf-8") as file:
            markdown_listing = file.readlines()

        updated_listing = []
        for line in markdown_listing:
            # Use a regular expression to match the exact string
            if re.search(r"\b" + re.escape(artefact_to_mark) + r"\b", line):
                line = line.replace("[]", "[x]")
            updated_listing.append(line)

        # Write the updated listing back to the file
        with open(config_prompt_givens_path, "w", encoding="utf-8") as file:
            file.write("".join(updated_listing))


def generate_config_prompt_global_givens_file(
    prompt_data_path, config_prompt_givens_name, artefact_to_mark=None
):
    from ara_cli.global_file_lister import generate_global_markdown_listing

    config_prompt_givens_path = os.path.join(
        prompt_data_path, config_prompt_givens_name
    )
    config = ConfigManager().get_config()

    if not hasattr(config, "global_dirs") or not config.global_dirs:
        return

    dir_list = [path for d in config.global_dirs for path in d.values()]
    print(
        f"used {dir_list} for global prompt givens file listing with absolute paths"
    )
    generate_global_markdown_listing(
        dir_list, config.ara_prompt_given_list_includes, config_prompt_givens_path
    )