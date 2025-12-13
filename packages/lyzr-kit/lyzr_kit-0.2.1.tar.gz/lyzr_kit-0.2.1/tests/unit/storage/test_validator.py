"""Unit tests for storage validator."""

from pathlib import Path

from pydantic import ValidationError

from lyzr_kit.storage.validator import (
    ValidationResult,
    format_schema_errors,
    format_validation_errors,
    validate_agent_yaml_file,
    validate_agents_folder,
)
from lyzr_kit.schemas.agent import Agent


class TestValidateAgentsFolder:
    """Tests for validate_agents_folder function."""

    def test_valid_empty_folder(self):
        """Empty agents folder should be valid."""
        # ..local-kit/agents doesn't exist yet
        result = validate_agents_folder(Path.cwd() / "..local-kit")
        assert result.is_valid is True
        assert len(result.issues) == 0

    def test_valid_with_yaml_files(self):
        """Folder with valid YAML files should be valid."""
        agents_dir = Path.cwd() / ".local-kit" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        # Create valid agent YAML
        valid_yaml = agents_dir / "test-agent.yaml"
        valid_yaml.write_text("""
id: test-agent
name: Test Agent
category: chat
model:
  provider: openai
  name: gpt-4
  credential_id: cred-1
""")

        result = validate_agents_folder(Path.cwd() / ".local-kit")
        assert result.is_valid is True
        assert len(result.issues) == 0

    def test_detects_nested_folders(self):
        """Should detect nested folders as invalid."""
        agents_dir = Path.cwd() / ".local-kit" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        # Create nested folder
        nested_dir = agents_dir / "nested-folder"
        nested_dir.mkdir()

        result = validate_agents_folder(Path.cwd() / ".local-kit")
        assert result.is_valid is False
        assert len(result.nested_folders) == 1
        assert result.nested_folders[0].name == "nested-folder"

    def test_detects_multiple_nested_folders(self):
        """Should detect all nested folders."""
        agents_dir = Path.cwd() / ".local-kit" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        # Create multiple nested folders
        (agents_dir / "folder1").mkdir()
        (agents_dir / "folder2").mkdir()

        result = validate_agents_folder(Path.cwd() / ".local-kit")
        assert result.is_valid is False
        assert len(result.nested_folders) == 2

    def test_detects_invalid_file_extensions(self):
        """Should detect non-YAML files as invalid."""
        agents_dir = Path.cwd() / ".local-kit" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        # Create invalid files
        (agents_dir / "readme.txt").write_text("some text")
        (agents_dir / "config.json").write_text("{}")

        result = validate_agents_folder(Path.cwd() / ".local-kit")
        assert result.is_valid is False
        assert len(result.invalid_extensions) == 2

    def test_detects_invalid_yaml_syntax(self):
        """Should detect YAML files with invalid syntax."""
        agents_dir = Path.cwd() / ".local-kit" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        # Create invalid YAML
        invalid_yaml = agents_dir / "broken.yaml"
        invalid_yaml.write_text("invalid: yaml: content: [")

        result = validate_agents_folder(Path.cwd() / ".local-kit")
        assert result.is_valid is False
        assert len(result.invalid_yaml_files) == 1
        assert result.invalid_yaml_files[0].name == "broken.yaml"

    def test_detects_empty_yaml_file(self):
        """Should detect empty YAML files as invalid."""
        agents_dir = Path.cwd() / ".local-kit" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        # Create empty YAML
        empty_yaml = agents_dir / "empty.yaml"
        empty_yaml.write_text("")

        result = validate_agents_folder(Path.cwd() / ".local-kit")
        assert result.is_valid is False
        assert len(result.invalid_yaml_files) == 1

    def test_detects_invalid_schema(self):
        """Should detect YAML files that don't match Agent schema."""
        agents_dir = Path.cwd() / ".local-kit" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        # Create YAML with missing required fields
        invalid_schema = agents_dir / "bad-schema.yaml"
        invalid_schema.write_text("""
some_field: value
other_field: 123
""")

        result = validate_agents_folder(Path.cwd() / ".local-kit")
        assert result.is_valid is False
        assert len(result.invalid_schema_files) == 1
        assert result.invalid_schema_files[0].name == "bad-schema.yaml"

    def test_detects_all_issue_types(self):
        """Should detect all types of issues in one validation."""
        agents_dir = Path.cwd() / ".local-kit" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        # Create nested folder
        (agents_dir / "nested").mkdir()

        # Create invalid extension file
        (agents_dir / "readme.txt").write_text("text")

        # Create invalid YAML
        (agents_dir / "broken.yaml").write_text("invalid: yaml: [")

        # Create invalid schema
        (agents_dir / "bad-schema.yaml").write_text("field: value")

        result = validate_agents_folder(Path.cwd() / ".local-kit")
        assert result.is_valid is False
        assert len(result.nested_folders) == 1
        assert len(result.invalid_extensions) == 1
        assert len(result.invalid_yaml_files) == 1
        assert len(result.invalid_schema_files) == 1


class TestFormatValidationErrors:
    """Tests for format_validation_errors function."""

    def test_empty_result_returns_empty_string(self):
        """Valid result should return empty string."""
        result = ValidationResult(is_valid=True)
        output = format_validation_errors(result)
        assert output == ""

    def test_formats_nested_folders(self):
        """Should format nested folder errors."""
        result = ValidationResult(is_valid=False)
        result.nested_folders = [Path(".local-kit/agents/nested")]
        result.issues = [None]  # type: ignore  # Just to make is_valid=False work

        output = format_validation_errors(result)
        assert "Nested folders" in output
        assert "nested" in output

    def test_formats_invalid_extensions(self):
        """Should format invalid extension errors."""
        result = ValidationResult(is_valid=False)
        result.invalid_extensions = [Path(".local-kit/agents/readme.txt")]
        result.issues = [None]  # type: ignore

        output = format_validation_errors(result)
        assert "Invalid file extensions" in output
        assert "readme.txt" in output

    def test_formats_invalid_yaml(self):
        """Should format invalid YAML errors."""
        result = ValidationResult(is_valid=False)
        result.invalid_yaml_files = [Path(".local-kit/agents/broken.yaml")]
        result.issues = [None]  # type: ignore

        output = format_validation_errors(result)
        assert "Invalid YAML syntax" in output
        assert "broken.yaml" in output

    def test_formats_invalid_schema(self):
        """Should format invalid schema errors."""
        result = ValidationResult(is_valid=False)
        result.invalid_schema_files = [Path(".local-kit/agents/bad.yaml")]
        result.issues = [None]  # type: ignore

        output = format_validation_errors(result)
        assert "Invalid agent schema" in output
        assert "bad.yaml" in output


class TestValidateAgentYamlFile:
    """Tests for validate_agent_yaml_file function."""

    def test_returns_agent_for_valid_yaml(self):
        """Should return Agent for valid YAML file."""
        agents_dir = Path.cwd() / ".local-kit" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        valid_yaml = agents_dir / "valid-agent.yaml"
        valid_yaml.write_text("""
id: valid-agent
name: Valid Agent
category: chat
model:
  provider: openai
  name: gpt-4
  credential_id: cred-1
""")

        agent, schema_error, yaml_error = validate_agent_yaml_file(valid_yaml)

        assert agent is not None
        assert agent.id == "valid-agent"
        assert schema_error is None
        assert yaml_error is None

    def test_returns_yaml_error_for_invalid_syntax(self):
        """Should return yaml error for invalid YAML syntax."""
        agents_dir = Path.cwd() / ".local-kit" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        invalid_yaml = agents_dir / "broken.yaml"
        invalid_yaml.write_text("invalid: yaml: [")

        agent, schema_error, yaml_error = validate_agent_yaml_file(invalid_yaml)

        assert agent is None
        assert schema_error is None
        assert yaml_error is not None
        assert "Invalid YAML syntax" in yaml_error

    def test_returns_schema_error_for_invalid_schema(self):
        """Should return schema error for invalid Agent schema."""
        agents_dir = Path.cwd() / ".local-kit" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        bad_schema = agents_dir / "bad-schema.yaml"
        bad_schema.write_text("field: value\nother: 123\n")

        agent, schema_error, yaml_error = validate_agent_yaml_file(bad_schema)

        assert agent is None
        assert schema_error is not None
        assert yaml_error is None

    def test_returns_yaml_error_for_empty_file(self):
        """Should return yaml error for empty YAML file."""
        agents_dir = Path.cwd() / ".local-kit" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        empty_yaml = agents_dir / "empty.yaml"
        empty_yaml.write_text("")

        agent, schema_error, yaml_error = validate_agent_yaml_file(empty_yaml)

        assert agent is None
        assert schema_error is None
        assert yaml_error is not None
        assert "Empty YAML file" in yaml_error


class TestFormatSchemaErrors:
    """Tests for format_schema_errors function."""

    def test_formats_missing_field_errors(self):
        """Should format missing required field errors."""
        # Trigger a validation error by validating invalid data
        try:
            Agent.model_validate({"field": "value"})
        except ValidationError as e:
            output = format_schema_errors(e, "test-agent")

        assert "invalid schema" in output
        assert "Expected fields:" in output
        assert "Your file is missing" in output
        assert "id" in output or "name" in output or "category" in output

    def test_includes_agent_id(self):
        """Should include agent ID in error message."""
        try:
            Agent.model_validate({})
        except ValidationError as e:
            output = format_schema_errors(e, "my-custom-agent")

        assert "my-custom-agent" in output

    def test_includes_fix_hint(self):
        """Should include hint to fix and re-run command."""
        try:
            Agent.model_validate({})
        except ValidationError as e:
            output = format_schema_errors(e, "test-agent")

        assert "Fix the YAML file" in output
        assert "lk agent set test-agent" in output
