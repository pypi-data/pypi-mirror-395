"""Core storage manager for lyzr-kit resources."""

from pathlib import Path

import yaml

from lyzr_kit.schemas.agent import Agent

# Built-in resources bundled with the package
COLLECTION_DIR = Path(__file__).parent.parent / "collection"


class StorageManager:
    """Manages storage for agents, tools, and features."""

    def __init__(
        self,
        builtin_path: str | Path | None = None,
        local_path: str | Path | None = None,
    ) -> None:
        """Initialize storage manager.

        Args:
            builtin_path: Path to built-in resources. Defaults to package collection.
            local_path: Path to local resources. Defaults to current working directory.
        """
        self.builtin_path = Path(builtin_path) if builtin_path else COLLECTION_DIR
        try:
            self.local_path = Path(local_path) if local_path else Path.cwd()
        except (FileNotFoundError, OSError):
            self.local_path = Path(".")

    def _ensure_local_dir(self, resource_type: str) -> Path:
        """Ensure local directory exists for resource type."""
        path = self.local_path / resource_type
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _list_yaml_files(self, directory: Path) -> list[Path]:
        """List all YAML files in a directory."""
        if not directory.exists() or not directory.is_dir():
            return []
        try:
            return list(directory.glob("*.yaml"))
        except OSError:
            return []

    def _load_agent(self, path: Path) -> Agent | None:
        """Load an agent from a YAML file."""
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
            return Agent.model_validate(data)
        except Exception:
            return None

    def list_agents(self) -> list[tuple[Agent, str]]:
        """List all agents from built-in and local directories.

        Returns:
            List of tuples containing (agent, source) where source is
            "built-in" or "local". Sorted by serial number.
        """
        agents: list[tuple[Agent, str]] = []

        # Built-in agents
        builtin_dir = self.builtin_path / "agents"
        for yaml_file in self._list_yaml_files(builtin_dir):
            agent = self._load_agent(yaml_file)
            if agent:
                agents.append((agent, "built-in"))

        # Local agents
        local_dir = self.local_path / "agents"
        for yaml_file in self._list_yaml_files(local_dir):
            agent = self._load_agent(yaml_file)
            if agent:
                agents.append((agent, "local"))

        # Sort: built-in first (by serial), then local (by serial)
        def sort_key(item: tuple[Agent, str]) -> tuple[int, int]:
            agent, source = item
            serial = agent.serial if agent.serial is not None else 999999
            # Built-in = 0, local = 1 (so built-in comes first)
            source_order = 0 if source == "built-in" else 1
            return (source_order, serial)

        agents.sort(key=sort_key)
        return agents

    def get_agent(self, agent_id: str) -> Agent | None:
        """Get an agent by ID from local or built-in directory.

        Searches all YAML files and matches by the 'id' field inside the file.
        Local agents take precedence over built-in agents.
        """
        # Check local first
        local_dir = self.local_path / "agents"
        for yaml_file in self._list_yaml_files(local_dir):
            agent = self._load_agent(yaml_file)
            if agent and agent.id == agent_id:
                return agent

        # Check built-in
        builtin_dir = self.builtin_path / "agents"
        for yaml_file in self._list_yaml_files(builtin_dir):
            agent = self._load_agent(yaml_file)
            if agent and agent.id == agent_id:
                return agent

        return None

    def save_agent(self, agent: Agent) -> Path:
        """Save an agent to local directory.

        Adds a comment warning not to modify the serial number.
        """
        self._ensure_local_dir("agents")
        path = self.local_path / "agents" / f"{agent.id}.yaml"

        data = agent.model_dump(exclude_none=True, exclude_unset=False)
        # Convert datetime to ISO format string
        for key in ["created_at", "updated_at"]:
            if key in data and data[key] is not None:
                data[key] = data[key].isoformat()

        with open(path, "w") as f:
            f.write("# WARNING: Do NOT modify the 'serial' field below\n")
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

        return path

    def agent_exists_local(self, agent_id: str) -> bool:
        """Check if agent exists in local directory."""
        local_dir = self.local_path / "agents"
        for yaml_file in self._list_yaml_files(local_dir):
            agent = self._load_agent(yaml_file)
            if agent and agent.id == agent_id:
                return True
        return False

    def agent_exists(self, agent_id: str) -> bool:
        """Check if agent exists in built-in or local directory."""
        if self.agent_exists_local(agent_id):
            return True

        builtin_dir = self.builtin_path / "agents"
        for yaml_file in self._list_yaml_files(builtin_dir):
            agent = self._load_agent(yaml_file)
            if agent and agent.id == agent_id:
                return True

        return False
