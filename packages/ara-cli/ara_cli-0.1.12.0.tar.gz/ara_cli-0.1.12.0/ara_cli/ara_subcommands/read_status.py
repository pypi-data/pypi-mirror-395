import typer
from .common import ClassifierEnum, MockArgs, ClassifierArgument, ArtefactNameArgument
from ara_cli.ara_command_action import read_status_action


def read_status_main(
    classifier: ClassifierEnum = ClassifierArgument("Classifier of the artefact type"),
    parameter: str = ArtefactNameArgument("Filename of artefact")
):
    """Read status of an artefact by checking its tags."""
    args = MockArgs(
        classifier=classifier.value,
        parameter=parameter
    )
    read_status_action(args)


def register(parent: typer.Typer):
    help_text = "Read status of an artefact by checking its tags"
    parent.command(name="read-status", help=help_text)(read_status_main)
