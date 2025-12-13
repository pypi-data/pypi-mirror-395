from ara_cli.chat_script_runner.script_lister import ScriptLister

class ScriptCompleter:
    def __init__(self):
        self.script_lister = ScriptLister()

    def __call__(self, text, line, begidx, endidx):
        if line.startswith("rpy global/"):
            return self._complete_global_scripts(text)
        
        return self._complete_all_scripts(text)

    def _complete_all_scripts(self, text):
        all_scripts = self.script_lister.get_all_scripts()
        if not text:
            return all_scripts
        return [s for s in all_scripts if s.startswith(text)]

    def _complete_global_scripts(self, text):
        global_scripts = self.script_lister.get_global_scripts()
        if not text:
            return global_scripts
        return [s for s in global_scripts if s.startswith(text)]
