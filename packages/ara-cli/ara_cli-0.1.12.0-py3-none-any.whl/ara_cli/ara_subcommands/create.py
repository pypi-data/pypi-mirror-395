import typer
from typing import Optional
from .common import (
    ClassifierEnum, AspectEnum, MockArgs,
    ClassifierArgument, ArtefactNameArgument, ParentNameArgument, AspectArgument
)
from ara_cli.ara_command_action import create_action


def create_contributes_to(
    ctx: typer.Context,
    parent_classifier: ClassifierEnum = ClassifierArgument("Classifier of the parent"),
    parent_name: str = ParentNameArgument("Name of a parent artefact"),
    rule: Optional[str] = typer.Option(None, "-r", "--rule", help="Rule for contribution")
):
    """Create an artefact that contributes to a parent artefact."""
    # Get classifier and parameter from parent context
    parent_params = ctx.parent.params
    classifier = parent_params['classifier']
    parameter = parent_params['parameter']

    args = MockArgs(
        classifier=classifier,
        parameter=parameter,
        option="contributes-to",
        parent_classifier=parent_classifier.value,
        parent_name=parent_name,
        rule=rule
    )
    create_action(args)


def create_aspect(
    ctx: typer.Context,
    aspect: AspectEnum = AspectArgument("Adds additional specification breakdown aspects")
):
    """Create an artefact with additional specification breakdown aspects."""
    # Get classifier and parameter from parent context
    parent_params = ctx.parent.params
    classifier = parent_params['classifier']
    parameter = parent_params['parameter']

    args = MockArgs(
        classifier=classifier,
        parameter=parameter,
        option="aspect",
        aspect=aspect.value
    )
    create_action(args)


def create_main(
    ctx: typer.Context,
    classifier: ClassifierEnum = ClassifierArgument("Classifier that also serves as file extension"),
    parameter: str = ArtefactNameArgument("Artefact name that serves as filename")
):
    """Create a classified artefact with data directory."""
    if ctx.invoked_subcommand is None:
        args = MockArgs(
            classifier=classifier.value,
            parameter=parameter,
            option=None
        )
        create_action(args)


def register(parent: typer.Typer):
    create_app = typer.Typer(
        help="Create a classified artefact with data directory",
        add_completion=False  # Disable completion on subcommand
    )
    create_app.command("contributes-to")(create_contributes_to)
    create_app.command("aspect")(create_aspect)
    create_app.callback(invoke_without_command=True)(create_main)
    parent.add_typer(create_app, name="create")
