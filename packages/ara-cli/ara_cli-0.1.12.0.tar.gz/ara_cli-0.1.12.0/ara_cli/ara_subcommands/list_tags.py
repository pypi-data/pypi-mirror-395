import typer
from typing import Optional
from .common import ClassifierEnum, MockArgs, ClassifierOption
from ara_cli.ara_command_action import list_tags_action


def list_tags_main(
    json_output: bool = typer.Option(False, "-j", "--json/--no-json", help="Output tags as JSON"),
    include_classifier: Optional[ClassifierEnum] = ClassifierOption("Show tags for an artefact type", "--include-classifier"),
    exclude_classifier: Optional[ClassifierEnum] = ClassifierOption("Show tags for an artefact type", "--exclude-classifier"),
    filtered_extra_column: bool = typer.Option(False, "--filtered-extra-column", help="Filter tags for extra column")
):
    """Show tags."""
    args = MockArgs(
        json=json_output,
        include_classifier=include_classifier.value if include_classifier else None,
        exclude_classifier=exclude_classifier.value if exclude_classifier else None,
        filtered_extra_column=filtered_extra_column
    )
    list_tags_action(args)


def register(parent: typer.Typer):
    help_text = "Show tags"
    parent.command(name="list-tags", help=help_text)(list_tags_main)
