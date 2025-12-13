import typer
from .common import ClassifierEnum, MockArgs, ClassifierArgument, ArtefactNameArgument
from ara_cli.ara_command_action import delete_action


def delete_main(
    classifier: ClassifierEnum = ClassifierArgument("Classifier of the artefact to be deleted"),
    parameter: str = ArtefactNameArgument("Filename of artefact"),
    force: bool = typer.Option(False, "-f", "--force", help="ignore nonexistent files and arguments, never prompt")
):
    """Delete an artefact file including its data directory."""
    args = MockArgs(
        classifier=classifier.value,
        parameter=parameter,
        force=force
    )
    delete_action(args)


def register(parent: typer.Typer):
    help_text = "Delete an artefact file including its data directory"
    parent.command(name="delete", help=help_text)(delete_main)
