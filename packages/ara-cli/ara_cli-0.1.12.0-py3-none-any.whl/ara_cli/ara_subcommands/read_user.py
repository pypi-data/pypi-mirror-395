import typer
from .common import ClassifierEnum, MockArgs, ClassifierArgument, ArtefactNameArgument
from ara_cli.ara_command_action import read_user_action


def read_user_main(
    classifier: ClassifierEnum = ClassifierArgument("Classifier of the artefact type"),
    parameter: str = ArtefactNameArgument("Filename of artefact")
):
    """Read user of an artefact by checking its tags."""
    args = MockArgs(
        classifier=classifier.value,
        parameter=parameter
    )
    read_user_action(args)


def register(parent: typer.Typer):
    help_text = "Read user of an artefact by checking its tags"
    parent.command(name="read-user", help=help_text)(read_user_main)
