import typer
from .common import MockArgs
from ara_cli.ara_command_action import extract_action


def extract_main(
    filename: str = typer.Argument(help="Input file to extract from"),
    force: bool = typer.Option(False, "-f", "--force", help="Answer queries with yes when extracting"),
    write: bool = typer.Option(False, "-w", "--write", help="Overwrite existing files without using LLM for merging")
):
    """Extract blocks of marked content from a given file."""
    args = MockArgs(
        filename=filename,
        force=force,
        write=write
    )
    extract_action(args)


def register(parent: typer.Typer):
    help_text = "Extract blocks of marked content from a given file"
    parent.command(name="extract", help=help_text)(extract_main)
