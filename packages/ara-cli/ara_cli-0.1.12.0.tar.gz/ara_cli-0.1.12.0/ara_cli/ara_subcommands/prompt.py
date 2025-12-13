import typer
from typing import Optional, List
from .common import ClassifierEnum, MockArgs, ClassifierArgument, ArtefactNameArgument, ChatNameArgument
from ara_cli.ara_command_action import prompt_action


def prompt_init(
    classifier: ClassifierEnum = ClassifierArgument("Classifier of the artefact"),
    parameter: str = ArtefactNameArgument("Name of artefact data directory")
):
    """Initialize a macro prompt."""
    args = MockArgs(
        classifier=classifier.value,
        parameter=parameter,
        steps="init"
    )
    prompt_action(args)


def prompt_load(
    classifier: ClassifierEnum = ClassifierArgument("Classifier of the artefact"),
    parameter: str = ArtefactNameArgument("Name of artefact data directory")
):
    """Load selected templates."""
    args = MockArgs(
        classifier=classifier.value,
        parameter=parameter,
        steps="load"
    )
    prompt_action(args)


def prompt_send(
    classifier: ClassifierEnum = ClassifierArgument("Classifier of the artefact"),
    parameter: str = ArtefactNameArgument("Name of artefact data directory")
):
    """Send configured prompt to LLM."""
    args = MockArgs(
        classifier=classifier.value,
        parameter=parameter,
        steps="send"
    )
    prompt_action(args)


def prompt_load_and_send(
    classifier: ClassifierEnum = ClassifierArgument("Classifier of the artefact"),
    parameter: str = ArtefactNameArgument("Name of artefact data directory")
):
    """Load templates and send prompt to LLM."""
    args = MockArgs(
        classifier=classifier.value,
        parameter=parameter,
        steps="load-and-send"
    )
    prompt_action(args)


def prompt_extract(
    classifier: ClassifierEnum = ClassifierArgument("Classifier of the artefact"),
    parameter: str = ArtefactNameArgument("Name of artefact data directory"),
    write: bool = typer.Option(False, "-w", "--write", help="Overwrite existing files without using LLM for merging")
):
    """Extract LLM response and save to disk."""
    args = MockArgs(
        classifier=classifier.value,
        parameter=parameter,
        steps="extract",
        write=write
    )
    prompt_action(args)


def prompt_update(
    classifier: ClassifierEnum = ClassifierArgument("Classifier of the artefact"),
    parameter: str = ArtefactNameArgument("Name of artefact data directory")
):
    """Update artefact config prompt files."""
    args = MockArgs(
        classifier=classifier.value,
        parameter=parameter,
        steps="update"
    )
    prompt_action(args)


def prompt_chat(
    classifier: ClassifierEnum = ClassifierArgument("Classifier of the artefact"),
    parameter: str = ArtefactNameArgument("Name of artefact data directory"),
    chat_name: Optional[str] = ChatNameArgument("Optional name for a specific chat", None),
    reset: Optional[bool] = typer.Option(None, "-r", "--reset/--no-reset", help="Reset the chat file if it exists"),
    output_mode: bool = typer.Option(False, "--out", help="Output the contents of the chat file instead of entering interactive chat mode"),
    append: Optional[List[str]] = typer.Option(None, "--append", help="Append strings to the chat file"),
    restricted: Optional[bool] = typer.Option(None, "--restricted/--no-restricted", help="Start with a limited set of commands")
):
    """Start chat mode for the artefact."""
    args = MockArgs(
        classifier=classifier.value,
        parameter=parameter,
        steps="chat",
        chat_name=chat_name,
        reset=reset,
        output_mode=output_mode,
        append=append,
        restricted=restricted
    )
    prompt_action(args)


def prompt_init_rag(
    classifier: ClassifierEnum = ClassifierArgument("Classifier of the artefact"),
    parameter: str = ArtefactNameArgument("Name of artefact data directory")
):
    """Initialize RAG prompt."""
    args = MockArgs(
        classifier=classifier.value,
        parameter=parameter,
        steps="init-rag"
    )
    prompt_action(args)


def register(parent: typer.Typer):
    prompt_app = typer.Typer(
        help="Base command for prompt interaction mode",
        add_completion=False  # Disable completion on subcommand
    )
    prompt_app.command("init")(prompt_init)
    prompt_app.command("load")(prompt_load)
    prompt_app.command("send")(prompt_send)
    prompt_app.command("load-and-send")(prompt_load_and_send)
    prompt_app.command("extract")(prompt_extract)
    prompt_app.command("update")(prompt_update)
    prompt_app.command("chat")(prompt_chat)
    prompt_app.command("init-rag")(prompt_init_rag)
    parent.add_typer(prompt_app, name="prompt")
