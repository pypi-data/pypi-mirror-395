import re
import json
import os
import json_repair
from markdown_it import MarkdownIt
from ara_cli.prompt_handler import send_prompt, get_file_content
from ara_cli.classifier import Classifier
from ara_cli.directory_navigator import DirectoryNavigator
from ara_cli.artefact_models.artefact_mapping import title_prefix_to_artefact_class


def _find_extract_token(tokens):
    """Find the first token that needs to be processed."""
    for token in tokens:
        if token.type == 'fence' and token.content.strip().startswith("# [x] extract"):
            return token
    return None


def _extract_file_path(content_lines):
    """Extract file path from content lines."""
    if not content_lines:
        return None
    file_path_search = re.search(r"# filename: (.+)", content_lines[0])
    return file_path_search.group(1).strip() if file_path_search else None


def _find_artefact_class(content_lines):
    """Find the appropriate artefact class from content lines."""
    for line in content_lines[:2]:
        words = line.strip().split(' ')
        if not words:
            continue
        first_word = words[0]
        if first_word in title_prefix_to_artefact_class:
            return title_prefix_to_artefact_class[first_word]
    return None


def _process_file_extraction(file_path, code_content, force, write, original_cwd):
    """Process file extraction logic."""
    print(f"Filename extracted: {file_path}")
    # Make the path absolute based on the original CWD
    absolute_file_path = os.path.join(original_cwd, file_path)
    handle_existing_file(absolute_file_path, code_content, force, write)


def _process_artefact_extraction(artefact_class, content_lines, force, write):
    """Process artefact extraction logic."""
    artefact = artefact_class.deserialize('\n'.join(content_lines))
    serialized_artefact = artefact.serialize()

    original_directory = os.getcwd()
    directory_navigator = DirectoryNavigator()
    directory_navigator.navigate_to_target()

    artefact_path = artefact.file_path
    directory = os.path.dirname(artefact_path)
    os.makedirs(directory, exist_ok=True)
    handle_existing_file(artefact_path, serialized_artefact, force, write)

    os.chdir(original_directory)


def _perform_extraction_for_block(source_lines, block_start, block_end, force, write, original_cwd):
    """Helper function to process a single, identified block."""
    original_block_text = '\n'.join(source_lines[block_start:block_end + 1])
    block_content_lines = source_lines[block_start + 1:block_end]
    block_content = '\n'.join(block_content_lines)

    block_lines = block_content.split('\n')
    content_lines_after_extract = block_lines[1:]

    file_path = _extract_file_path(content_lines_after_extract)

    if file_path:
        code_content = '\n'.join(content_lines_after_extract[1:])
        _process_file_extraction(file_path, code_content, force, write, original_cwd)
    else:
        artefact_class = _find_artefact_class(content_lines_after_extract)
        if artefact_class:
            _process_artefact_extraction(artefact_class, content_lines_after_extract, force, write)
        else:
            print("No filename or valid artefact found, skipping processing for this block.")
            return None, None

    modified_block_text = original_block_text.replace("# [x] extract", "# [v] extract", 1)
    return original_block_text, modified_block_text


class FenceDetector:
    """Helper class to detect and match fence blocks."""
    
    def __init__(self, source_lines):
        self.source_lines = source_lines
    
    def is_extract_fence(self, line_num):
        """Check if line is a fence with extract marker."""
        line = self.source_lines[line_num]
        stripped_line = line.strip()
        
        is_fence = stripped_line.startswith('```') or stripped_line.startswith('~~~')
        if not is_fence:
            return False
            
        if not (line_num + 1 < len(self.source_lines)):
            return False
            
        return self.source_lines[line_num + 1].strip().startswith("# [x] extract")
    
    def find_matching_fence_end(self, start_line):
        """Find the matching end fence for a given start fence."""
        fence_line = self.source_lines[start_line]
        indentation = len(fence_line) - len(fence_line.lstrip())
        stripped_fence_line = fence_line.strip()
        fence_char = stripped_fence_line[0]
        fence_length = len(stripped_fence_line) - len(stripped_fence_line.lstrip(fence_char))

        for i in range(start_line + 1, len(self.source_lines)):
            scan_line = self.source_lines[i]
            stripped_scan_line = scan_line.strip()

            if not stripped_scan_line or stripped_scan_line[0] != fence_char:
                continue
            
            if not all(c == fence_char for c in stripped_scan_line):
                continue

            candidate_indentation = len(scan_line) - len(scan_line.lstrip())
            candidate_length = len(stripped_scan_line)
            
            if candidate_length == fence_length and candidate_indentation == indentation:
                return i
        
        return -1


def _process_document_blocks(source_lines, force, write, original_cwd):
    """Process all extract blocks in the document."""
    fence_detector = FenceDetector(source_lines)
    replacements = []
    line_num = 0
    
    while line_num < len(source_lines):
        if not fence_detector.is_extract_fence(line_num):
            line_num += 1
            continue

        block_start_line = line_num
        block_end_line = fence_detector.find_matching_fence_end(block_start_line)
        
        if block_end_line != -1:
            print(f"Block found and processed starting on line {block_start_line + 1}.")
            original, modified = _perform_extraction_for_block(
                source_lines, block_start_line, block_end_line, force, write, original_cwd
            )
            if original and modified:
                replacements.append((original, modified))
            line_num = block_end_line + 1
        else:
            line_num += 1
    
    return replacements


def _apply_replacements(content, replacements):
    """Apply all replacements to the content."""
    updated_content = content
    for original, modified in replacements:
        updated_content = updated_content.replace(original, modified, 1)
    return updated_content


def _setup_working_directory(relative_to_ara_root):
    """Setup working directory and return original cwd."""
    cwd = os.getcwd()
    if relative_to_ara_root:
        navigator = DirectoryNavigator()
        navigator.navigate_to_target()
        os.chdir('..')
    return cwd


def extract_responses(document_path, relative_to_ara_root=False, force=False, write=False):
    print(f"Starting extraction from '{document_path}'")
    
    try:
        with open(document_path, 'r', encoding='utf-8', errors='replace') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{document_path}'. Skipping extraction.")
        return

    original_cwd = _setup_working_directory(relative_to_ara_root)
    
    source_lines = content.split('\n')
    replacements = _process_document_blocks(source_lines, force, write, original_cwd)
    
    updated_content = _apply_replacements(content, replacements)

    os.chdir(original_cwd)
    with open(document_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

    if replacements:
        print(f"End of extraction. Found and processed {len(replacements)} blocks in '{os.path.basename(document_path)}'.")


def modify_and_save_file(response, file_path):
    print(f"Debug: Modifying and saving file {file_path}")
    try:
        response_data = json_repair.loads(response)
        filename_from_response = response_data['filename']
        print(f"""Found in JSON merge response {response[:200]} ...
        the file {filename_from_response}
        loaded as this content string: 
        {response_data['content'][:100]} ...
        """)

        if filename_from_response != file_path:
            user_decision = prompt_user_decision("Filename does not match, overwrite? (y/n): ")
            if user_decision.lower() not in ['y', 'yes']:
                print("Debug: User chose not to overwrite")
                print("Skipping block.")
                return

        with open(file_path, 'w', encoding='utf-8', errors='replace') as file:
            file.write(response_data['content'])
        
        relative_path = os.path.relpath(file_path)
        print(f"File {relative_path} updated successfully.")
    except json.JSONDecodeError as ex:
        print(f"ERROR: Failed to decode JSON response: {ex}")


def prompt_user_decision(prompt):
    return input(prompt)


def determine_should_create(skip_query=False):
    if skip_query:
        return True
    user_decision = prompt_user_decision("File does not exist. Create? (y/n): ")
    if user_decision.lower() in ['y', 'yes']:
        return True
    return False


def create_file_if_not_exist(filename, content, skip_query=False):
    try:
        if not os.path.exists(filename):
            if determine_should_create(skip_query):
                # Ensure the directory exists
                dir_name = os.path.dirname(filename)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)

                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(content)
                    print(f"File {filename} created successfully.")
            else:
                print("Automatic file creation skipped by user.")

    except OSError as e:
        print(f"Error: {e}")
        print(f"Failed to create file {filename} due to an OS error")


def create_prompt_for_file_modification(content_str, filename):
    if not os.path.exists(filename):
        print(f"WARNING: {filename} for merge prompt creation does not exist.")
        return

    content_of_existing_file = json.dumps(get_file_content(filename))
    content = json.dumps(content_str)

    prompt_text = f"""
    * given this new_content: 
    ```
    {content}
    ```
    * and given this existing file {filename}
    ```
    {content_of_existing_file}
    ```
    * Merge the new content into {filename}.
    * Include only the provided information; do not add any new details.
    * Use the following JSON format for the prompt response of the merged file:
    {{
        "filename": "path/filename.filextension",
        "content":  "full content of the modified file in valid json format"
    }}
    """

    # print(f"Debug: modification prompt created: {prompt_text}")

    return prompt_text


def handle_existing_file(filename, block_content, skip_query=False, write=False):
    if not os.path.isfile(filename):
        print(f"File {filename} does not exist, attempting to create")
        # Ensure directory exists before writing
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)
        create_file_if_not_exist(filename, block_content, skip_query)

    elif write:
        print(f"File {filename} exists. Overwriting without LLM merge as requested.")
        try:
            directory = os.path.dirname(filename)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(filename, 'w', encoding='utf-8', errors='replace') as file:
                file.write(block_content)
            print(f"File {filename} overwritten successfully.")
        except OSError as e:
            print(f"Error: {e}")
            print(f"Failed to overwrite file {filename} due to an OS error")
    else:
        print(f"File {filename} exists, creating modification prompt")
        prompt_text = create_prompt_for_file_modification(block_content, filename)
        if prompt_text is None:
            return

        messages = [{"role": "user", "content": prompt_text}]
        response = ""

        for chunk in send_prompt(messages, purpose='extraction'):
            content = chunk.choices[0].delta.content
            if content:
                response += content
        modify_and_save_file(response, filename)


def extract_and_save_prompt_results(classifier, param, write=False):
    sub_directory = Classifier.get_sub_directory(classifier)
    prompt_log_file = f"ara/{sub_directory}/{param}.data/{classifier}.prompt_log.md"
    print(f"Extract marked sections from: {prompt_log_file}")

    extract_responses(prompt_log_file, relative_to_ara_root=True, write=write)