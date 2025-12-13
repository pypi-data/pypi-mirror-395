import typer
from .common import ClassifierEnum, MockArgs, ClassifierArgument
from ara_cli.ara_command_action import template_action


def template_main(
    classifier: ClassifierEnum = ClassifierArgument("Classifier of the artefact type")
):
    """Outputs a classified ara template in the terminal."""
    args = MockArgs(classifier=classifier.value)
    template_action(args)


def register(parent: typer.Typer):
    help_text = "Outputs a classified ara template in the terminal"
    parent.command(name="template", help=help_text)(template_main)
