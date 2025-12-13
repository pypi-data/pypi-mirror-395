import os
from ara_cli.commands.command import Command


def list_available_binary_agents(chat_instance):
    """Helper to list executable files in the agents directory."""
    try:
        base_dir = chat_instance._find_project_root()
        if not base_dir:
            return []  # Can't find project root

        agents_dir = os.path.join(base_dir, "ara", ".araconfig", "agents")
        if not os.path.isdir(agents_dir):
            return []

        available_agents = []
        for f in os.listdir(agents_dir):
            path = os.path.join(agents_dir, f)
            if os.path.isfile(path) and os.access(path, os.X_OK):
                available_agents.append(f)
        return available_agents
    except Exception:
        return []  # Fail silently


class ListAgentsCommand(Command):
    def __init__(self, chat_instance):
        self.chat_instance = chat_instance

    def execute(self):
        """Lists all available executable binary agents."""
        print("Searching for available agents in 'ara/.araconfig/agents/'...")
        available_agents = list_available_binary_agents(self.chat_instance)
        if available_agents:
            print("\nAvailable binary agents:")
            for agent in available_agents:
                print(f"  - {agent}")
        else:
            print("No executable binary agents found.")
