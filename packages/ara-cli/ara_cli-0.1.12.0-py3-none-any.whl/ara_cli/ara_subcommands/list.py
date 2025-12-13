import typer
from ara_cli.error_handler import AraError
from typing import Optional, List, Tuple
from .common import MockArgs
from ara_cli.ara_command_action import list_action
from ara_cli.completers import complete_classifier, complete_artefact_name


def _classifier_completer(incomplete: str):
    """Simple wrapper for classifier completion for include/exclude options."""
    yield from complete_classifier(incomplete)


def contextual_option_completer(ctx: typer.Context, args: list[str], incomplete: str):
    """
    Provides completions for options that take multiple arguments (like --branch).
    Due to observed environmental limitations where `args` is always empty,
    this completer will currently only offer generic classifier completions.
    """
    yield from complete_classifier(incomplete)


def _validate_extension_options(
    include_extension: Optional[List[str]], exclude_extension: Optional[List[str]]
) -> None:
    """Validate that include and exclude extension options are mutually exclusive."""
    if include_extension and exclude_extension:
        raise AraError(
            "--include-extension/-i and --exclude-extension/-e are mutually exclusive"
        )


def _validate_exclusive_options(
    branch: Optional[Tuple[str, str]],
    children: Optional[Tuple[str, str]],
    data: Optional[Tuple[str, str]],
) -> None:
    """Validate that branch, children, and data options are mutually exclusive."""
    exclusive_options = [branch, children, data]
    non_none_options = [opt for opt in exclusive_options if opt is not None]
    if len(non_none_options) > 1:
        raise AraError("--branch, --children, and --data are mutually exclusive")


def list_main(
    ctx: typer.Context,
    include_content: Optional[List[str]] = typer.Option(
        None,
        "-I",
        "--include-content",
        help="filter for files which include given content",
    ),
    exclude_content: Optional[List[str]] = typer.Option(
        None,
        "-E",
        "--exclude-content",
        help="filter for files which do not include given content",
    ),
    include_tags: Optional[List[str]] = typer.Option(
        None, "--include-tags", help="filter for files which include given tags"
    ),
    exclude_tags: Optional[List[str]] = typer.Option(
        None, "--exclude-tags", help="filter for files which do not include given tags"
    ),
    include_extension: Optional[List[str]] = typer.Option(
        None,
        "-i",
        "--include-extension",
        "--include-classifier",
        help="list of extensions to include in listing",
        autocompletion=_classifier_completer,
    ),
    exclude_extension: Optional[List[str]] = typer.Option(
        None,
        "-e",
        "--exclude-extension",
        "--exclude-classifier",
        help="list of extensions to exclude from listing",
        autocompletion=_classifier_completer,
    ),
    branch: Optional[Tuple[str, str]] = typer.Option(
        None,
        "-b",
        "--branch",
        help="List artefacts in the parent chain (classifier artefact_name)",
        autocompletion=contextual_option_completer,
    ),
    children: Optional[Tuple[str, str]] = typer.Option(
        None,
        "-c",
        "--children",
        help="List child artefacts (classifier artefact_name)",
        autocompletion=contextual_option_completer,
    ),
    data: Optional[Tuple[str, str]] = typer.Option(
        None,
        "-d",
        "--data",
        help="List file in the data directory (classifier artefact_name)",
        autocompletion=contextual_option_completer,
    ),
):
    """List files with optional tags.

    Examples:
        ara list --data feature my_feature --include-extension .md
        ara list --include-extension .feature
        ara list --children userstory my_story
        ara list --branch userstory my_story --include-extension .businessgoal
        ara list --include-content "example content" --include-extension .task
    """
    _validate_extension_options(include_extension, exclude_extension)
    _validate_exclusive_options(branch, children, data)

    args = MockArgs(
        include_content=include_content,
        exclude_content=exclude_content,
        include_tags=include_tags,
        exclude_tags=exclude_tags,
        include_extension=include_extension,
        exclude_extension=exclude_extension,
        branch_args=tuple(branch) if branch else (None, None),
        children_args=tuple(children) if children else (None, None),
        data_args=tuple(data) if data else (None, None),
    )

    list_action(args)


def register(parent: typer.Typer):
    help_text = "List files with optional tags"
    parent.command(name="list", help=help_text)(list_main)
