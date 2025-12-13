import os
import subprocess
from ara_cli.chat_script_runner.script_finder import ScriptFinder
from ara_cli.chat_script_runner.script_lister import ScriptLister

class ScriptRunner:
    def __init__(self, chat_instance):
        self.chat_instance = chat_instance
        self.script_finder = ScriptFinder()
        self.script_lister = ScriptLister()

    def run_script(self, script_name: str):
        script_path = self.script_finder.find_script(script_name)
        if not script_path:
            return f"Script '{script_name}' not found."

        try:
            result = subprocess.run(
                ["python", script_path],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error running script: {e}\n{e.stderr}"

    def get_available_scripts(self):
        return self.script_lister.get_all_scripts()

    def get_global_scripts(self):
        return self.script_lister.get_global_scripts()
