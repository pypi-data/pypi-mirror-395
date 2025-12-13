import typer
from typing import Optional, List
from .common import MockArgs, ChatNameArgument
from ara_cli.ara_command_action import chat_action


def chat_main(
    chat_name: Optional[str] = ChatNameArgument("Optional name for a specific chat. Pass the .md file to continue an existing chat", None),
    reset: Optional[bool] = typer.Option(None, "-r", "--reset/--no-reset", help="Reset the chat file if it exists"),
    output_mode: bool = typer.Option(False, "--out", help="Output the contents of the chat file instead of entering interactive chat mode"),
    append: Optional[List[str]] = typer.Option(None, "--append", help="Append strings to the chat file"),
    restricted: Optional[bool] = typer.Option(None, "--restricted/--no-restricted", help="Start with a limited set of commands")
):
    """Command line chatbot. Chat control with SEND/s | RERUN/r | QUIT/q"""
    args = MockArgs(
        chat_name=chat_name,
        reset=reset,
        output_mode=output_mode,
        append=append,
        restricted=restricted
    )
    chat_action(args)


def register(parent: typer.Typer):
    help_text = "Command line chatbot. Chat control with SEND/s | RERUN/r | QUIT/q"
    parent.command(name="chat", help=help_text)(chat_main)
