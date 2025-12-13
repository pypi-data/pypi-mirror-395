import typer
from .common import ClassifierEnum, MockArgs, ClassifierArgument
from ara_cli.ara_command_action import classifier_directory_action


def classifier_directory_main(
    classifier: ClassifierEnum = ClassifierArgument("Classifier of the artefact type")
):
    """Print the ara subdirectory for an artefact classifier."""
    args = MockArgs(classifier=classifier.value)
    classifier_directory_action(args)


def register(parent: typer.Typer):
    help_text = "Print the ara subdirectory for an artefact classifier"
    parent.command(name="classifier-directory", help=help_text)(classifier_directory_main)
