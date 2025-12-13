import typer
from ara_cli.commands.fetch_templates_command import FetchTemplatesCommand
from ara_cli.commands.fetch_scripts_command import FetchScriptsCommand
from ara_cli.commands.fetch_agents_command import FetchAgentsCommand


def register(app: typer.Typer):
    @app.command(name="fetch", help="Fetch templates, scripts, or agents. If no flags provided, fetches all.")
    def fetch(
        templates: bool = typer.Option(
            False, "--templates", "-t", help="Fetch prompt templates only."),
        scripts: bool = typer.Option(
            False, "--scripts", "-s", help="Fetch scripts only."),
        agents: bool = typer.Option(
            False, "--agents", "-a", help="Fetch agents only."),
    ):

        if not any([templates, scripts, agents]):
            templates = True
            scripts = True
            agents = True
            typer.echo("Fetching all resources (templates, scripts, agents)...")

        if templates:
            typer.echo("Fetching templates...")
            command = FetchTemplatesCommand()
            command.execute()

        if scripts:
            typer.echo("Fetching scripts...")
            command = FetchScriptsCommand()
            command.execute()

        if agents:
            typer.echo("Fetching agents...")
            command = FetchAgentsCommand()
            command.execute()
