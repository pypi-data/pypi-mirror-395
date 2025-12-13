import argparse
from ara_cli.commands.command import Command
from ara_cli.error_handler import AraError


class AgentRunCommand(Command):
    def __init__(self, chat_instance, args):
        self.chat_instance = chat_instance
        self.args = args
        self.parser = self._create_parser()

    def _create_parser(self):
        """Creates and configures the argument parser."""
        parser = argparse.ArgumentParser(
            prog="AGENT_RUN",
            description="Run a binary agent.",
            add_help=False,  # We handle help manually
        )
        parser.add_argument("agent_name", nargs="?",
                            help="The name of the agent to run.")
        parser.add_argument("-b", "--base-dir", dest="base_dir",
                            help="Specify the base directory for the agent.")
        parser.add_argument("-r", "--requirements", dest="requirements",
                            action="append", help="Specify a requirements file or directory.")
        parser.add_argument("-h", "--help", action="store_true",
                            help="Show this help message.")
        return parser

    def _handle_help(self, arg_list):
        """Handles the --help flag for the agent command."""
        agent_name = next(
            (arg for arg in arg_list if not arg.startswith('-')), None)

        if agent_name:
            try:
                self.chat_instance.agent_manager.run_agent(
                    agent_name, ["--help"])
            except SystemExit:
                pass  # Common with argparse's --help
            except Exception:
                print(f"Displaying built-in help for {agent_name}:\n")
                self.parser.print_help()
        else:
            self.parser.print_help()
        return True

    def _prepare_agent_args(self, parsed_args, unknown_args):
        """Prepares the arguments to be passed to the agent."""
        agent_args = list(unknown_args)

        if parsed_args.base_dir:
            print(f"Using base directory: {parsed_args.base_dir}")
            agent_args.extend(["--base-dir", parsed_args.base_dir])

        if parsed_args.requirements:
            print(f"Requirements Paths ({len(parsed_args.requirements)}):")
            for req_path in parsed_args.requirements:
                print(f"  - {req_path}")
                agent_args.extend(["--requirements", req_path])

        elif self.chat_instance.source_artefact_path:
            print(
                f"INFO: Automatically passing source artefact to agent: {self.chat_instance.source_artefact_path}")
            agent_args.insert(0, self.chat_instance.source_artefact_path)
            agent_args.insert(0, "-r")

        return agent_args

    def _run_agent(self, parsed_args, unknown_args):
        """Runs the agent with the prepared arguments."""
        if not parsed_args.agent_name:
            raise AraError("Usage: AGENT_RUN <agent_name> [args...]")

        agent_name = parsed_args.agent_name
        agent_args = self._prepare_agent_args(parsed_args, unknown_args)

        self.chat_instance.agent_manager.run_agent(agent_name, agent_args)

    def execute(self):
        """
        Parses arguments and runs a binary agent, handling help requests and errors.
        """
        try:
            arg_list = self.args.split()
            if "-h" in arg_list or "--help" in arg_list:
                self._handle_help(arg_list)
                return

            parsed_args, unknown_args = self.parser.parse_known_args(arg_list)
            self._run_agent(parsed_args, unknown_args)

        except SystemExit:
            # Argparse may exit, which is fine.
            pass
        except AraError as e:
            raise e
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
