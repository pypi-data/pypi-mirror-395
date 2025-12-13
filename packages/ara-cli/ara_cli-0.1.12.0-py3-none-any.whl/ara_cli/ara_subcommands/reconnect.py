import typer
from typing import Optional
from .common import ClassifierEnum, MockArgs, ClassifierArgument, ArtefactNameArgument, ParentNameArgument
from ara_cli.ara_command_action import reconnect_action


def reconnect_main(
    classifier: ClassifierEnum = ClassifierArgument("Classifier of the artefact type"),
    parameter: str = ArtefactNameArgument("Filename of artefact"),
    parent_classifier: ClassifierEnum = ClassifierArgument("Classifier of the parent artefact type"),
    parent_name: str = ParentNameArgument("Filename of parent artefact"),
    rule: Optional[str] = typer.Option(None, "-r", "--rule", help="Rule for connection")
):
    """Connect an artefact to a parent artefact."""
    args = MockArgs(
        classifier=classifier.value,
        parameter=parameter,
        parent_classifier=parent_classifier.value,
        parent_name=parent_name,
        rule=rule
    )
    reconnect_action(args)


def register(parent: typer.Typer):
    help_text = "Connect an artefact to a parent artefact"
    parent.command(name="reconnect", help=help_text)(reconnect_main)
