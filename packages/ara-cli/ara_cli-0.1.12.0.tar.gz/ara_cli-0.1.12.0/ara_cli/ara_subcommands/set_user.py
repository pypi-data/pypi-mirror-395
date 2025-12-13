import typer
from .common import ClassifierEnum, MockArgs, ClassifierArgument, ArtefactNameArgument
from ara_cli.ara_command_action import set_user_action


def set_user_main(
    classifier: ClassifierEnum = ClassifierArgument("Classifier of the artefact type, typically 'task'"),
    parameter: str = ArtefactNameArgument("Name of the task artefact"),
    new_user: str = typer.Argument(help="New user to assign to the task")
):
    """Set the user of a task."""
    args = MockArgs(
        classifier=classifier.value,
        parameter=parameter,
        new_user=new_user
    )
    set_user_action(args)


def register(parent: typer.Typer):
    help_text = "Set the user of a task"
    parent.command(name="set-user", help=help_text)(set_user_main)
