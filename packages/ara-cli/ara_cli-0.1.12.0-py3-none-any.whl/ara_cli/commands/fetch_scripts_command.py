import os
import shutil
from ara_cli.commands.command import Command
from ara_cli.ara_config import ConfigManager
from ara_cli.directory_navigator import DirectoryNavigator

class FetchScriptsCommand(Command):
    def __init__(self, output=None):
        self.output = output or print
        self.config = ConfigManager.get_config()

    def execute(self):
        navigator = DirectoryNavigator()
        original_directory = os.getcwd()
        navigator.navigate_to_target()
        os.chdir('..')

        global_scripts_dir = self._get_global_scripts_dir()
        global_scripts_config_dir = self._get_global_scripts_config_dir()

        if not os.path.exists(global_scripts_dir):
            self.output("Global scripts directory not found.")
            os.chdir(original_directory)
            return

        if not os.path.exists(global_scripts_config_dir):
            os.makedirs(global_scripts_config_dir)

        for item in os.listdir(global_scripts_dir):
            source = os.path.join(global_scripts_dir, item)
            destination = os.path.join(global_scripts_config_dir, item)
            if os.path.isfile(source):
                shutil.copy2(source, destination)
                self.output(f"Copied {item} to global scripts directory.")

        os.chdir(original_directory)

    def _get_global_scripts_dir(self):
        base_path = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(base_path, "templates", "global-scripts")

    def _get_global_scripts_config_dir(self):
        return os.path.join(self.config.local_prompt_templates_dir, "global-scripts")
