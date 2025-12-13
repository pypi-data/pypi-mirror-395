
import os
import glob
from ara_cli.template_manager import TemplatePathManager
from ara_cli.ara_config import ConfigManager
from ara_cli.directory_navigator import DirectoryNavigator


class TemplateLoader:
    """Handles template loading logic shared between CLI and chat commands"""

    def __init__(self, chat_instance=None):
        self.chat_instance = chat_instance

    def load_template(self, template_name: str, template_type: str, chat_file_path: str, default_pattern: str | None = None) -> bool:
        if not template_name:
            if default_pattern:
                return self.load_template_from_prompt_data(template_type, default_pattern, chat_file_path)
            else:
                print(f"A template name is required for template type '{template_type}'.")
                return False
        return self.load_template_from_global_or_local(template_name, template_type, chat_file_path)

    def get_plural_template_type(self, template_type: str) -> str:
        """Determines the plural form of a template type."""
        plurals = {"commands": "commands", "rules": "rules"}
        return plurals.get(template_type, f"{template_type}s")

    def load_template_from_global_or_local(self, template_name: str, template_type: str, chat_file_path: str) -> bool:
        """Load template from global or local directories"""
        plural = self.get_plural_template_type(template_type)

        if template_name.startswith("global/"):
            return self._load_global_template(template_name, template_type, plural, chat_file_path)
        else:
            return self._load_local_template(template_name, template_type, plural, chat_file_path)

    def _choose_file_for_cli(self, files: list[str], pattern: str) -> str | None:
        """CLI-compatible file selection method"""
        if len(files) <= 1:
            return files[0] if files else None

        if pattern in ["*", "global/*"] or "*" in pattern:
            files.sort()
            print("Multiple files found:")
            for i, file in enumerate(files):
                print(f"{i + 1}: {os.path.basename(file)}")

            try:
                choice = input("Please choose a file to load (enter number): ")
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(files):
                    return files[choice_index]
                else:
                    print("Invalid choice. Aborting load.")
                    return None
            except (ValueError, KeyboardInterrupt):
                print("Invalid input. Aborting load.")
                return None
        else:
            return files[0]

    def _load_global_template(self, template_name: str, template_type: str, plural: str, chat_file_path: str) -> bool:
        """Load template from global directory"""
        directory = f"{TemplatePathManager.get_template_base_path()}/prompt-modules/{plural}/"
        template_file = template_name.removeprefix("global/")
        file_pattern = os.path.join(directory, template_file)
        matching_files = glob.glob(file_pattern)

        if not matching_files:
            print(f"No {template_type} template '{template_file}' found in global templates.")
            return False

        # Choose file based on context
        if self.chat_instance:
            file_path = self.chat_instance.choose_file_to_load(matching_files, template_file)
        else:
            file_path = self._choose_file_for_cli(matching_files, template_file)

        if file_path is None:
            return False

        return self._load_file_to_chat(file_path, template_type, chat_file_path)

    def _load_local_template(self, template_name: str, template_type: str, plural: str, chat_file_path: str) -> bool:
        """Load template from local custom directory"""
        ara_config = ConfigManager.get_config()
        navigator = DirectoryNavigator()

        original_directory = os.getcwd()
        navigator.navigate_to_target()
        local_templates_path = ara_config.local_prompt_templates_dir
        os.chdir("..")
        local_templates_path = os.path.join(os.getcwd(), local_templates_path)
        os.chdir(original_directory)

        custom_prompt_templates_subdir = ara_config.custom_prompt_templates_subdir
        template_directory = f"{local_templates_path}/{custom_prompt_templates_subdir}/{plural}"
        file_pattern = os.path.join(template_directory, template_name)
        matching_files = glob.glob(file_pattern)

        if not matching_files:
            print(f"No {template_type} template '{template_name}' found in local templates.")
            return False

        # Choose file based on context
        if self.chat_instance:
            file_path = self.chat_instance.choose_file_to_load(matching_files, template_name)
        else:
            file_path = self._choose_file_for_cli(matching_files, template_name)

        if file_path is None:
            return False

        return self._load_file_to_chat(file_path, template_type, chat_file_path)

    def load_template_from_prompt_data(self, template_type: str, default_pattern: str, chat_file_path: str) -> bool:
        """Load template from prompt.data directory with selection"""
        directory_path = os.path.join(os.path.dirname(chat_file_path), "prompt.data")
        file_pattern = os.path.join(directory_path, default_pattern)
        matching_files = glob.glob(file_pattern)

        if not matching_files:
            print(f"No {template_type} file found in prompt.data directory.")
            return False

        # Choose file based on context
        if self.chat_instance:
            file_path = self.chat_instance.choose_file_to_load(matching_files, default_pattern)
        else:
            file_path = self._choose_file_for_cli(matching_files, "*")

        if file_path is None:
            return False

        return self._load_file_to_chat(file_path, template_type, chat_file_path)

    def _load_file_to_chat(self, file_path: str, template_type: str, chat_file_path: str) -> bool:
        """Load a file into the chat file"""
        if self.chat_instance:
            # Use chat instance methods
            self.chat_instance.add_prompt_tag_if_needed(chat_file_path)
            if self.chat_instance.load_file(file_path):
                print(f"Loaded {template_type} from {os.path.basename(file_path)} into {os.path.basename(chat_file_path)}")
                return True
        else:
            # Direct file loading for CLI usage
            try:
                with open(file_path, 'r', encoding='utf-8') as template_file:
                    template_content = template_file.read().replace('\r\n', '\n')

                # Add prompt tag if needed
                self._add_prompt_tag_if_needed(chat_file_path)

                # Append template content with newlines for separation
                with open(chat_file_path, 'a', encoding='utf-8') as chat_file:
                    chat_file.write(f"\n{template_content}\n")

                print(f"Loaded {template_type} from {os.path.basename(file_path)} into {os.path.basename(chat_file_path)}")
                return True
            except Exception as e:
                print(f"Error loading {template_type} from {file_path}: {e}")
                return False

        return False

    def _add_prompt_tag_if_needed(self, chat_file_path: str):
        """Add prompt tag if needed for CLI usage"""
        from ara_cli.chat import Chat

        with open(chat_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        prompt_tag = f"# {Chat.ROLE_PROMPT}:"
        if Chat.get_last_role_marker(lines) == prompt_tag:
            return

        append = prompt_tag
        if lines:
            last_line = lines[-1].strip()
            if last_line != "" and last_line != '\n':
                append = f"\n{append}"

        with open(chat_file_path, 'a', encoding='utf-8') as file:
            file.write(append)

    def _find_project_root(self, start_path: str) -> str | None:
        """
        Finds the project root by searching for an 'ara' directory,
        starting from the given path and moving upwards.
        """
        current_dir = start_path
        while True:
            if os.path.isdir(os.path.join(current_dir, 'ara')):
                return current_dir
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:  # Reached the filesystem root
                return None
            current_dir = parent_dir

    def _gather_templates_from_path(self, search_path: str, templates_set: set, prefix: str = ""):
        """
        Scans a given path for items and adds them to the provided set,
        optionally prepending a prefix.
        """
        if not os.path.isdir(search_path):
            return
        for path in glob.glob(os.path.join(search_path, '*')):
            templates_set.add(f"{prefix}{os.path.basename(path)}")

    def get_available_templates(self, template_type: str, context_path: str) -> list[str]:
        """
        Scans for available global and project-local custom templates.
        This method safely searches for template files without changing the
        current directory, making it safe for use in autocompleters.
        Args:
            template_type: The type of template to search for (e.g., 'rules').
            context_path: The directory path to start the search for project root from.
        Returns:
            A sorted list of unique template names. Global templates are
            prefixed with 'global/'.
        """
        plural_type = self.get_plural_template_type(template_type)
        templates = set()

        # 1. Find Global Templates
        try:
            global_base_path = TemplatePathManager.get_template_base_path()
            global_template_dir = os.path.join(global_base_path, "prompt-modules", plural_type)
            self._gather_templates_from_path(global_template_dir, templates, prefix="global/")
        except Exception:
            pass  # Silently ignore if global templates are not found

        # 2. Find Local Custom Templates
        try:
            project_root = self._find_project_root(context_path)
            if project_root:
                config = ConfigManager.get_config()
                local_templates_base = os.path.join(project_root, config.local_prompt_templates_dir)
                custom_dir = os.path.join(local_templates_base, config.custom_prompt_templates_subdir, plural_type)
                self._gather_templates_from_path(custom_dir, templates)
        except Exception:
            pass  # Silently ignore if local templates cannot be resolved

        return sorted(list(templates))