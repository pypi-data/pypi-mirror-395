import typer
import os
from typing import Optional
from os import getenv
from ara_cli.version import __version__
from ara_cli import error_handler
from ara_cli.ara_subcommands.create import register as register_create_cli
from ara_cli.ara_subcommands.delete import register as register_delete_cli
from ara_cli.ara_subcommands.rename import register as register_rename_cli
from ara_cli.ara_subcommands.list import register as register_list_cli
from ara_cli.ara_subcommands.list_tags import register as register_list_tags_cli
from ara_cli.ara_subcommands.prompt import register as register_prompt_cli
from ara_cli.ara_subcommands.chat import register as register_chat_cli
from ara_cli.ara_subcommands.template import register as register_template_cli
from ara_cli.ara_subcommands.fetch_templates import register as register_fetch_templates_cli
from ara_cli.ara_subcommands.fetch_scripts import register as register_fetch_scripts_cli
from ara_cli.ara_subcommands.fetch_agents import register as register_fetch_agents_cli
from ara_cli.ara_subcommands.fetch import register as register_fetch
from ara_cli.ara_subcommands.read import register as register_read_cli
from ara_cli.ara_subcommands.reconnect import register as register_reconnect_cli
from ara_cli.ara_subcommands.read_status import register as register_read_status_cli
from ara_cli.ara_subcommands.read_user import register as register_read_user_cli
from ara_cli.ara_subcommands.set_status import register as register_set_status_cli
from ara_cli.ara_subcommands.set_user import register as register_set_user_cli
from ara_cli.ara_subcommands.classifier_directory import register as register_classifier_directory_cli
from ara_cli.ara_subcommands.scan import register as register_scan_cli
from ara_cli.ara_subcommands.autofix import register as register_autofix_cli
from ara_cli.ara_subcommands.extract import register as register_extract_cli
from ara_cli.ara_subcommands.load import register as register_load_cli

from ara_cli.directory_navigator import DirectoryNavigator


def version_callback(value: bool):
    if value:
        typer.echo(f"ara {__version__}")
        raise typer.Exit()


def is_debug_mode_enabled():
    """Check if debug mode is enabled via environment variable."""
    return getenv('ARA_DEBUG', '').lower() in ('1', 'true', 'yes')


def configure_debug_mode(debug: bool, env_debug_mode: bool):
    """Configure debug mode based on arguments and environment."""
    if debug or env_debug_mode:
        error_handler.debug_mode = True


def check_ara_directory_exists():
    """Check if ara directory exists or if we're inside ara directory tree."""
    return DirectoryNavigator.find_ara_directory_root() is not None


def prompt_create_ara_directory():
    """Prompt user to create ara directory and create it if confirmed."""
    # Print the prompt message
    print("No 'ara' directory found. Create one in the current directory? (Y/n)",
          end=" ", flush=True)

    # Read user input
    try:
        response = input().strip()
    except (EOFError, KeyboardInterrupt):
        typer.echo("\nOperation cancelled.")
        raise typer.Exit(1)

    if response.lower() in ('y', 'yes', ''):
        current_dir = os.getcwd()
        ara_path = os.path.join(current_dir, 'ara')

        # Create ara directory structure
        subdirectories = [
            'businessgoals',
            'capabilities',
            'epics',
            'examples',
            'features',
            'keyfeatures',
            'tasks',
            'userstories',
            'vision'
        ]

        try:
            # Create main ara directory
            os.makedirs(ara_path, exist_ok=True)

            # Create subdirectories for artefact types
            for subdir in subdirectories:
                os.makedirs(os.path.join(ara_path, subdir), exist_ok=True)

            # Create .araconfig directory
            araconfig_path = os.path.join(ara_path, '.araconfig')
            os.makedirs(araconfig_path, exist_ok=True)

            # Create default ara_config.json using ConfigManager
            from ara_cli.ara_config import ConfigManager, ARAconfig
            config_file_path = os.path.join(araconfig_path, 'ara_config.json')

            # Reset ConfigManager to ensure clean state
            ConfigManager.reset()

            # Create default config and save it
            default_config = ARAconfig()
            from ara_cli.ara_config import save_data
            save_data(config_file_path, default_config)

            typer.echo(f"Created ara directory structure at {ara_path}")
            typer.echo(f"Created default configuration at {config_file_path}")
            return True

        except OSError as e:
            typer.echo(f"Error creating ara directory: {e}", err=True)
            raise typer.Exit(1)
        except Exception as e:
            typer.echo(f"Error creating configuration file: {e}", err=True)
            raise typer.Exit(1)
    else:
        typer.echo("Ara directory creation cancelled.")
        raise typer.Exit(0)


def requires_ara_directory():
    """Check if ara directory exists and prompt to create if not."""
    if not check_ara_directory_exists():
        return prompt_create_ara_directory()
    return True


def create_app():
    app = typer.Typer(
        help="""The ara cli terminal tool is a management tool for classified ara artefacts.

Valid classified artefacts are: businessgoal, vision, capability, keyfeature, feature, epic, userstory, example, feature, task.

The default ara directory structure of classified artefact of the ara cli tool is:
.
└── ara
   ├── businessgoals
   ├── capabilities
   ├── epics
   ├── examples
   ├── features
   ├── keyfeatures
   ├── tasks
   ├── userstories
   └── vision

ara artefact handling examples:
  > create a new artefact for e.g. a feature:                                        ara create feature {feature_name}
  > create a new artefact for e.g. a feature that contributes to an userstory:       ara create feature {feature_name} contributes-to userstory {story_name}
  > read an artefact and return the content as terminal output, for eg. of a task:   ara read task {task_name}
  > read an artefact and its full chain of contributions to its parents and return
    the content as terminal output, for eg. of a task:                               ara read task {task_name} --branch
  > delete an artefact for e.g. feature:                                             ara delete feature {feature_name}
  > rename artefact and artefact data directory for e.g. a feature:                  ara rename feature {initial_feature_name} {new_feature_name}
  > create additional templates for a specific aspect (valid aspects are: customer,
    persona, concept, technology) related to an existing artefact like a feature:    ara create feature {feature_name} aspect {aspect_name}
  > list artefact data with .md file extension                                       ara list --data {classifier} {artefact_name} --include-extension .md
  > list artefact data with .md and .json file extensions                            ara list --data {classifier} {artefact_name} --include-extension .md .json
  > list everything but userstories                                                  ara list --exclude-extension .userstory
  > list all existing features:                                                      ara list --include-extension .feature
  > list all child artefacts contributing value to a parent artefact:                ara list --include-content "Contributes to {name_of_parent_artefact} {ara classifier_of_parent_artefact}"
  > list tasks which contain 'example content'                                       ara list --include-extension .task --include-content "example content"
  > list children artefacts of a userstory                                           ara list --children userstory {name_of_userstory}
  > list parent artefacts of a userstory                                             ara list --branch userstory {name_of_userstory}
  > list parent businessgoal artefact of a userstory                                 ara list --branch userstory {name_of_userstory} --include-extension .businessgoal
  > print any artefact template for e.g. a feature file template in the terminal:    ara template feature

ara prompt templates examples:
 > get and copy all prompt templates (blueprints, rules, intentions, commands
   in the ara/.araconfig/global-prompt-modules directory:                            ara fetch-templates

ara chat examples:
  > chat with ara and save the default chat.md file in the working directory:        ara chat
  > chat with ara and save the default task_chat.md file in the task.data directory: ara prompt chat task {task_name}

  > initialize a macro prompt for a task:                                            ara prompt init task {task_name}
  > load selected templates in config_prompt_templates.md for the task {task_name}:  ara prompt load task {task_name}
  > create and send configured prompt of the task {task_name} to the configured LLM: ara prompt send task {task_name}
  > extract the selected LLM response in task.exploration.md and save to disk:       ara prompt extract task {task_name}
        """,
        no_args_is_help=True,
        add_completion=True,
        rich_markup_mode="rich"
    )

    @app.callback(invoke_without_command=True)
    def main(
        ctx: typer.Context,
        version: Optional[bool] = typer.Option(
            None, "--version", "-v",
            callback=version_callback,
            is_eager=True,
            help="Show version and exit"
        ),
        debug: bool = typer.Option(
            False, "--debug",
            help="Enable debug mode for detailed error output"
        )
    ):
        """The ara cli terminal tool is a management tool for classified ara artefacts."""
        debug_mode = is_debug_mode_enabled()
        configure_debug_mode(debug, debug_mode)

        # Only show help if no subcommand is invoked
        if ctx.invoked_subcommand is None:
            ctx.get_help()
            ctx.exit()

        # Check for ara directory before executing any command
        # Skip check for commands that don't require ara directory
        commands_requiring_ara = {
            'create', 'delete', 'rename', 'list', 'list-tags', 'prompt',
            'read', 'reconnect', 'read-status', 'read-user', 'set-status',
            'set-user', 'scan', 'autofix'
        }

        if ctx.invoked_subcommand in commands_requiring_ara:
            requires_ara_directory()

    # Register all commands
    register_create_cli(app)
    register_delete_cli(app)
    register_rename_cli(app)
    register_list_cli(app)
    register_list_tags_cli(app)
    register_prompt_cli(app)
    register_chat_cli(app)
    register_template_cli(app)
    register_fetch_templates_cli(app)
    register_fetch_scripts_cli(app)
    register_fetch_agents_cli(app)
    register_fetch(app)
    register_read_cli(app)
    register_reconnect_cli(app)
    register_read_status_cli(app)
    register_read_user_cli(app)
    register_set_status_cli(app)
    register_set_user_cli(app)
    register_classifier_directory_cli(app)
    register_scan_cli(app)
    register_autofix_cli(app)
    register_extract_cli(app)
    register_load_cli(app)

    return app


def cli():
    app = create_app()
    try:
        app()
    except KeyboardInterrupt:
        typer.echo("\n[INFO] Operation cancelled by user", err=True)
        raise typer.Exit(130)  # Standard exit code for Ctrl+C
    except Exception as e:
        error_handler.handle_error(e, context="cli")


if __name__ == "__main__":
    cli()
