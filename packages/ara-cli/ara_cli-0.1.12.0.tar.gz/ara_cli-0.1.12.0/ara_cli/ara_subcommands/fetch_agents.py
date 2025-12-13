import typer
from ara_cli.commands.fetch_agents_command import FetchAgentsCommand


def register(app: typer.Typer):
    """Register the fetch-agents command with the typer app."""
    @app.command(name="fetch-agents", help="Fetch binary agents from templates to project.", deprecated=True)
    def fetch_agents():
        """Fetch binary agents from ara_cli/templates/agents to ara/.araconfig/agents."""
        typer.secho(
            "WARNING: 'fetch-agents' is deprecated. Please use 'ara fetch --agents' or just 'ara fetch' instead.",
            fg=typer.colors.YELLOW,
            err=True
        )
        command = FetchAgentsCommand()
        command.execute()
