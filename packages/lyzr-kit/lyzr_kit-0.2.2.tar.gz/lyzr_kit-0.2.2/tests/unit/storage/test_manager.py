"""Unit tests for storage manager."""

from pathlib import Path

from lyzr_kit.storage.manager import StorageManager
from lyzr_kit.schemas.agent import Agent


class TestStorageManagerLoadAgent:
    """Tests for StorageManager._load_agent method."""

    def test_load_agent_returns_none_for_invalid_yaml(self):
        """_load_agent should return None for invalid YAML."""
        storage = StorageManager()

        # Create invalid YAML file
        agents_dir = Path.cwd() / ".local-kit" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        invalid_file = agents_dir / "invalid-agent.yaml"
        invalid_file.write_text("invalid: yaml: content: [")

        # Should return None, not raise
        result = storage._load_agent(invalid_file)
        assert result is None

    def test_load_agent_returns_none_for_invalid_schema(self):
        """_load_agent should return None for valid YAML but invalid schema."""
        storage = StorageManager()

        # Create YAML with missing required fields
        agents_dir = Path.cwd() / ".local-kit" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        invalid_file = agents_dir / "bad-schema.yaml"
        invalid_file.write_text("some_field: value\n")

        # Should return None (validation fails)
        result = storage._load_agent(invalid_file)
        assert result is None


class TestStorageManagerSaveAgent:
    """Tests for StorageManager.save_agent method."""

    def test_save_agent_converts_datetime_to_iso(self):
        """save_agent should convert datetime fields to ISO format."""
        from datetime import datetime

        from lyzr_kit.schemas.agent import ModelConfig

        storage = StorageManager()

        agent = Agent(
            id="test-agent",
            name="Test Agent",
            category="chat",
            created_at=datetime(2024, 1, 15, 10, 30, 0),
            model=ModelConfig(provider="openai", name="gpt-4", credential_id="cred-1"),
        )

        path = storage.save_agent(agent)
        content = path.read_text()

        # Should contain ISO format datetime
        assert "2024-01-15" in content
        assert "10:30:00" in content


class TestStorageManagerListAgents:
    """Tests for StorageManager.list_agents method."""

    def test_list_agents_returns_tuples_with_source(self):
        """list_agents should return tuples of (agent, source)."""
        storage = StorageManager()
        agents = storage.list_agents()

        # Should return list of tuples
        assert len(agents) > 0
        for item in agents:
            assert isinstance(item, tuple)
            assert len(item) == 2
            agent, source = item
            assert isinstance(agent, Agent)
            assert source in ("built-in", "local")

    def test_list_agents_builtin_agents_have_builtin_source(self):
        """Built-in agents should have 'built-in' source."""
        storage = StorageManager()
        agents = storage.list_agents()

        # Find chat-agent (should be built-in)
        chat_agents = [(a, s) for a, s in agents if a.id == "chat-agent"]
        assert len(chat_agents) == 1
        agent, source = chat_agents[0]
        assert source == "built-in"


class TestStorageManagerAgentExists:
    """Tests for StorageManager.agent_exists method."""

    def test_agent_exists_returns_true_for_builtin(self):
        """agent_exists should return True for built-in agents."""
        storage = StorageManager()
        assert storage.agent_exists("chat-agent") is True
        assert storage.agent_exists("qa-agent") is True

    def test_agent_exists_returns_false_for_nonexistent(self):
        """agent_exists should return False for non-existent agents."""
        storage = StorageManager()
        assert storage.agent_exists("nonexistent-agent-xyz") is False

    def test_agent_exists_returns_true_for_local(self):
        """agent_exists should return True for local agents."""
        from lyzr_kit.schemas.agent import ModelConfig

        storage = StorageManager()

        # Create a local agent
        agent = Agent(
            id="local-test-agent",
            name="Local Test Agent",
            category="chat",
            model=ModelConfig(provider="openai", name="gpt-4", credential_id="cred-1"),
        )
        storage.save_agent(agent)

        # Should now exist
        assert storage.agent_exists("local-test-agent") is True
