import os
import requests
from tqdm import tqdm
from ara_cli.commands.command import Command
from ara_cli.directory_navigator import DirectoryNavigator


class FetchAgentsCommand(Command):
    """Command to fetch binary agents from a remote URL.

    This command downloads a binary agent from a hardcoded URL and
    saves it to the project's ara/.araconfig/agents/ directory.
    """

    AGENT_URL = "https://s3-public.talsen.team/so-agents/feature-creation"

    def __init__(self, output=None):
        """Initialize the FetchAgentsCommand.

        Parameters
        ----------
        output : callable, optional
            Output function for displaying messages. Defaults to print.
        """
        self.output = output or print

    def execute(self):
        """Execute the fetch-agents command.

        Downloads a binary agent from a remote URL and saves it to the
        project's .araconfig/agents directory.
        """
        navigator = DirectoryNavigator()
        original_directory = os.getcwd()

        try:
            # Navigate to ara directory
            navigator.navigate_to_target()

            dest_dir = self._get_project_agents_dir()
            os.makedirs(dest_dir, exist_ok=True)

            agent_name = self.AGENT_URL.split('/')[-1]
            dest_path = os.path.join(dest_dir, agent_name)

            self.output(f"Downloading agent from {self.AGENT_URL}...")

            response = requests.get(self.AGENT_URL, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

            with open(dest_path, 'wb') as f:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    f.write(data)

            progress_bar.close()

            if total_size != 0 and progress_bar.n != total_size:
                raise Exception("ERROR, something went wrong during download")

            # Make the binary executable
            os.chmod(dest_path, 0o755)

            self.output(f"Downloaded {agent_name} to ara/.araconfig/agents/")
            self.output(
                "Binary agents fetched successfully to ara/.araconfig/agents/")

        except requests.exceptions.RequestException as e:
            self.output(f"Error downloading agent: {e}")
        finally:
            # Return to original directory
            os.chdir(original_directory)

    def _get_project_agents_dir(self):
        """Get the path to the project agents directory.

        Returns
        -------
        str
            Path to ara/.araconfig/agents directory.
        """
        return os.path.join(".araconfig", "agents")

