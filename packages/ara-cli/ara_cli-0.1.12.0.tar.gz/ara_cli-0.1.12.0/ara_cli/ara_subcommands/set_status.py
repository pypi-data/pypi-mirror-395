import typer
from .common import ClassifierEnum, MockArgs, ClassifierArgument, ArtefactNameArgument, StatusArgument
from ara_cli.ara_command_action import set_status_action


def set_status_main(
    classifier: ClassifierEnum = ClassifierArgument("Classifier of the artefact type, typically 'task'"),
    parameter: str = ArtefactNameArgument("Name of the task artefact"),
    new_status: str = StatusArgument("New status to set for the task")
):
    """Set the status of a task."""
    args = MockArgs(
        classifier=classifier.value,
        parameter=parameter,
        new_status=new_status
    )
    set_status_action(args)


def register(parent: typer.Typer):
    help_text = "Set the status of a task"
    parent.command(name="set-status", help=help_text)(set_status_main)
