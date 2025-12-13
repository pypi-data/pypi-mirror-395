import os
import pty
import sys
import stat
from ara_cli.error_handler import AraError


class AgentProcessManager:
    """
    Manages the lifecycle of binary, interactive agents.
    This manager is designed to run agents that require full TTY control,
    handing over the terminal to the agent process until it exits.
    """

    def __init__(self, chat_instance=None):
        self.chat_instance = chat_instance
        self.agent_process = None

    def get_agent_path(self, agent_name):
        """
        Constructs the full path to the agent binary by reliably finding
        the project root.
        """
        if not self.chat_instance:
            raise AraError("Chat instance is not available to find project root.")

        base_dir = self.chat_instance._find_project_root()
        if not base_dir:
            raise AraError(
                "Could not find project root from chat instance. Is this a valid ara project?"
            )

        return os.path.join(base_dir, "ara", ".araconfig", "agents", agent_name)

    def _ensure_executable(self, agent_path):
        """
        Validates existence and ensures the binary is executable.
        """
        if (agent_path != "--help") and (not os.path.exists(agent_path)):
            raise AraError(f"Agent binary not found at: {agent_path}")

        if not os.path.isfile(agent_path):
            raise AraError(f"Agent path does not point to a file: {agent_path}")

        if not os.access(agent_path, os.X_OK):
            try:
                os.chmod(agent_path, os.stat(agent_path).st_mode | stat.S_IEXEC)
                print(f"Made agent binary executable: {agent_path}")
            except Exception as e:
                raise AraError(
                    f"Agent binary is not executable and could not be changed: {agent_path}. Error: {e}"
                )

    def _print_session_banner(self, agent_name, is_start=True):
        """
        Handles UI printing for start and end of sessions.
        """
        print("\n" + "=" * 50)
        if is_start:
            print(f"Starting interactive agent: {agent_name}")
            print("You are now in an interactive session with the agent.")
            print(
                "To exit, use the agent's own exit command (e.g., '/quit', '/exit', or Ctrl+C)."
            )
            print("You will be returned to the 'ara>' prompt after the agent exits.")
        else:
            print("Returned to ara-cli prompt.")
        print("=" * 50 + ("\n" if is_start else ""))

        sys.stdout.flush()
        sys.stderr.flush()

    def _handle_process_exit(self, agent_name, return_code):
        """
        Analyzes the exit status code from pty.spawn.
        """
        print("\n" + "=" * 50)
        if os.WIFEXITED(return_code):
            exit_code = os.WEXITSTATUS(return_code)
            status_msg = (
                f"Agent '{agent_name}' finished successfully."
                if exit_code == 0
                else f"Agent '{agent_name}' exited with code: {exit_code}."
            )
            print(status_msg)
        elif os.WIFSIGNALED(return_code):
            signal_num = os.WTERMSIG(return_code)
            print(f"Agent '{agent_name}' terminated by signal: {signal_num}.")
        else:
            print(
                f"Agent '{agent_name}' exited with an unexpected status: {return_code}."
            )

    def run_agent(self, agent_name, agent_args):
        """
        Finds, validates, and runs a binary agent using a pseudo-terminal (pty).
        Refactored to maintain low CCN.
        """
        agent_path = self.get_agent_path(agent_name)

        # Validation Logic Extracted
        self._ensure_executable(agent_path)

        command = [agent_path] + agent_args

        # UI Logic Extracted
        self._print_session_banner(agent_name, is_start=True)

        try:
            # Execution Logic
            return_code = pty.spawn(command)

            # Exit Status Logic Extracted
            self._handle_process_exit(agent_name, return_code)

        except FileNotFoundError:
            raise AraError(f"Failed to execute. Command not found: {agent_path}")
        except Exception as e:
            raise AraError(f"An error occurred while trying to run the agent: {e}")
        finally:
            self._print_session_banner(agent_name, is_start=False)

    def cleanup_agent_process(self):
        """
        Placeholder for cleanup.
        """
        if hasattr(self, "chat_instance") and self.chat_instance:
            self.chat_instance.prompt = "ara> "
        pass
