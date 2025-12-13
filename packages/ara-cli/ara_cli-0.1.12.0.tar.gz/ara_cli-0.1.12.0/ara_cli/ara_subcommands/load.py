import typer
from .common import TemplateTypeEnum, MockArgs, TemplateTypeArgument, ChatNameArgument
from ara_cli.ara_command_action import load_action


def create_template_name_completer():
    """Create a template name completer that can access the template_type context."""
    def completer(incomplete: str) -> list[str]:
        # This is a simplified version - in practice, you'd need to access
        # the template_type from the current command context
        from ara_cli.template_loader import TemplateLoader
        import os

        # For all template types since we can't easily get context in typer
        all_templates = []
        for template_type in ['rules', 'intention', 'commands', 'blueprint']:
            try:
                loader = TemplateLoader()
                templates = loader.get_available_templates(template_type, os.getcwd())
                all_templates.extend(templates)
            except Exception:
                continue

        return [t for t in all_templates if t.startswith(incomplete)]
    return completer


def load_main(
    chat_name: str = ChatNameArgument("Name of the chat file to load template into (without extension)"),
    template_type: TemplateTypeEnum = TemplateTypeArgument("Type of template to load"),
    template_name: str = typer.Argument(
        "",
        help="Name of the template to load. Supports wildcards and 'global/' prefix",
        autocompletion=create_template_name_completer()
    )
):
    """Load a template into a chat file."""
    args = MockArgs(
        chat_name=chat_name,
        template_type=template_type.value,
        template_name=template_name
    )
    load_action(args)


def register(parent: typer.Typer):
    help_text = "Load a template into a chat file"
    parent.command(name="load", help=help_text)(load_main)
