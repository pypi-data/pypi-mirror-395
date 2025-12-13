from os.path import join
import os
import shutil
from ara_cli.commands.command import Command
from ara_cli.ara_config import ConfigManager
from ara_cli.template_manager import TemplatePathManager


class FetchTemplatesCommand(Command):
    def __init__(self, output=None):
        self.output = output or print

    def execute(self):
        config = ConfigManager().get_config()
        prompt_templates_dir = config.local_prompt_templates_dir
        template_base_path = TemplatePathManager.get_template_base_path()
        global_prompt_templates_path = join(
            template_base_path, "prompt-modules")

        subdirs = ["commands", "rules", "intentions", "blueprints"]

        os.makedirs(join(prompt_templates_dir,
                    "global-prompt-modules"), exist_ok=True)
        for subdir in subdirs:
            target_dir = join(prompt_templates_dir,
                              "global-prompt-modules", subdir)
            source_dir = join(global_prompt_templates_path, subdir)
            os.makedirs(target_dir, exist_ok=True)
            for item in os.listdir(source_dir):
                source = join(source_dir, item)
                target = join(target_dir, item)
                shutil.copy2(source, target)

        custom_prompt_templates_subdir = config.custom_prompt_templates_subdir
        local_prompt_modules_dir = join(
            prompt_templates_dir, custom_prompt_templates_subdir)
        os.makedirs(local_prompt_modules_dir, exist_ok=True)
        for subdir in subdirs:
            os.makedirs(join(local_prompt_modules_dir, subdir), exist_ok=True)
