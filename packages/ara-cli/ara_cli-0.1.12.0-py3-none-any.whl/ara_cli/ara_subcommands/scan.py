import typer
from .common import MockArgs
from ara_cli.ara_command_action import scan_action


def scan_main():
    """Scan ARA tree for incompatible artefacts."""
    args = MockArgs()
    scan_action(args)


def register(parent: typer.Typer):
    help_text = "Scan ARA tree for incompatible artefacts"
    parent.command(name="scan", help=help_text)(scan_main)
