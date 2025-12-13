import typer
from typing import Optional, List
from .common import ClassifierEnum, MockArgs, ClassifierArgument, ArtefactNameArgument
from ara_cli.ara_command_action import read_action


def read_main(
    classifier: ClassifierEnum = ClassifierArgument("Classifier of the artefact type", default=None),
    parameter: str = ArtefactNameArgument("Filename of artefact", default=None),
    include_content: Optional[List[str]] = typer.Option(None, "-I", "--include-content", help="filter for files which include given content"),
    exclude_content: Optional[List[str]] = typer.Option(None, "-E", "--exclude-content", help="filter for files which do not include given content"),
    include_tags: Optional[List[str]] = typer.Option(None, "--include-tags", help="filter for files which include given tags"),
    exclude_tags: Optional[List[str]] = typer.Option(None, "--exclude-tags", help="filter for files which do not include given tags"),
    include_extension: Optional[List[str]] = typer.Option(None, "-i", "--include-extension", "--include-classifier", help="list of extensions to include in listing"),
    exclude_extension: Optional[List[str]] = typer.Option(None, "-e", "--exclude-extension", "--exclude-classifier", help="list of extensions to exclude from listing"),
    branch: bool = typer.Option(False, "-b", "--branch", help="Output the contents of artefacts in the parent chain"),
    children: bool = typer.Option(False, "-c", "--children", help="Output the contents of child artefacts")
):
    """Reads contents of artefacts."""
    # Handle mutually exclusive options
    if branch and children:
        typer.echo("Error: --branch and --children are mutually exclusive", err=True)
        raise typer.Exit(1)

    read_mode = None
    if branch:
        read_mode = "branch"
    elif children:
        read_mode = "children"

    args = MockArgs(
        classifier=classifier.value if classifier else None,
        parameter=parameter,
        include_content=include_content,
        exclude_content=exclude_content,
        include_tags=include_tags,
        exclude_tags=exclude_tags,
        include_extension=include_extension,
        exclude_extension=exclude_extension,
        read_mode=read_mode
    )
    read_action(args)


def register(parent: typer.Typer):
    help_text = "Reads contents of artefacts"
    parent.command(name="read", help=help_text)(read_main)
