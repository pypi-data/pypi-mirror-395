import typer
from .common import ClassifierEnum, MockArgs, ClassifierArgument, ArtefactNameArgument
from ara_cli.ara_command_action import rename_action


def rename_main(
    classifier: ClassifierEnum = ClassifierArgument("Classifier of the artefact"),
    parameter: str = ArtefactNameArgument("Filename of artefact"),
    aspect: str = typer.Argument(help="New artefact name and new data directory name")
):
    """Rename a classified artefact and its data directory."""
    args = MockArgs(
        classifier=classifier.value,
        parameter=parameter,
        aspect=aspect
    )
    rename_action(args)


def register(parent: typer.Typer):
    help_text = "Rename a classified artefact and its data directory"
    parent.command(name="rename", help=help_text)(rename_main)
