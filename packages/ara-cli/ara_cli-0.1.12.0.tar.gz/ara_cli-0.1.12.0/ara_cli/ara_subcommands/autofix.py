import typer
from .common import MockArgs
from ara_cli.ara_command_action import autofix_action


def autofix_main(
    single_pass: bool = typer.Option(False, "--single-pass", help="Run the autofix once for every scanned file"),
    deterministic: bool = typer.Option(False, "-d", "--deterministic", help="Run only deterministic fixes e.g Title-FileName Mismatch fix"),
    non_deterministic: bool = typer.Option(False, "-nd", "--non-deterministic", help="Run only non-deterministic fixes")
):
    """Fix ARA tree with llm models for scanned artefacts with ara scan command."""
    if deterministic and non_deterministic:
        typer.echo("Error: --deterministic and --non-deterministic are mutually exclusive", err=True)
        raise typer.Exit(1)
    
    args = MockArgs(
        single_pass=single_pass,
        deterministic=deterministic,
        non_deterministic=non_deterministic
    )
    autofix_action(args)


def register(parent: typer.Typer):
    help_text = "Fix ARA tree with llm models for scanned artefacts"
    parent.command(name="autofix", help=help_text)(autofix_main)
