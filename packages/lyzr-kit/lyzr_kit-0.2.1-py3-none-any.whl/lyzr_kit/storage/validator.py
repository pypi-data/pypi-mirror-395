"""Validation utilities for agents folder structure and files."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml
from pydantic import ValidationError

from lyzr_kit.schemas.agent import Agent


@dataclass
class ValidationIssue:
    """Represents a validation issue found during folder/file validation."""

    issue_type: str  # "nested_folder", "invalid_extension", "invalid_yaml", "invalid_schema"
    path: Path
    message: str
    hint: str


@dataclass
class ValidationResult:
    """Result of validating a resource folder."""

    is_valid: bool
    issues: list[ValidationIssue] = field(default_factory=list)

    # Categorized issues for easy access
    nested_folders: list[Path] = field(default_factory=list)
    invalid_extensions: list[Path] = field(default_factory=list)
    invalid_yaml_files: list[Path] = field(default_factory=list)
    invalid_schema_files: list[Path] = field(default_factory=list)


def validate_agents_folder(local_path: Path) -> ValidationResult:
    """Validate the agents folder structure and files.

    Performs three checks:
    1. Folder structure - no nested folders allowed (flat structure only)
    2. File extensions - only .yaml files allowed
    3. Schema validation - all YAML files must follow the Agent schema

    Args:
        local_path: Path to the project directory.

    Returns:
        ValidationResult with all issues found.
    """
    agents_dir = local_path / "agents"
    result = ValidationResult(is_valid=True)

    # If agents folder doesn't exist or isn't a directory, nothing to validate
    if not agents_dir.exists() or not agents_dir.is_dir():
        return result

    try:
        # Check 1: Detect nested folders (flat structure required)
        for item in agents_dir.iterdir():
            if item.is_dir():
                issue = ValidationIssue(
                    issue_type="nested_folder",
                    path=item,
                    message=f"Nested folder detected: {item.name}/",
                    hint=f"Remove or move the folder '{item.name}' outside of agents/",
                )
                result.issues.append(issue)
                result.nested_folders.append(item)

        # Check 2: Detect non-YAML files
        for item in agents_dir.iterdir():
            if item.is_file() and not item.name.endswith(".yaml"):
                issue = ValidationIssue(
                    issue_type="invalid_extension",
                    path=item,
                    message=f"Invalid file extension: {item.name}",
                    hint=f"Remove '{item.name}' - only .yaml files are allowed in agents/",
                )
                result.issues.append(issue)
                result.invalid_extensions.append(item)

        # Check 3: Validate YAML files against Agent schema
        for yaml_file in agents_dir.glob("*.yaml"):
            validation_issue = _validate_agent_yaml(yaml_file)
            if validation_issue:
                result.issues.append(validation_issue)
                if validation_issue.issue_type == "invalid_yaml":
                    result.invalid_yaml_files.append(yaml_file)
                elif validation_issue.issue_type == "invalid_schema":
                    result.invalid_schema_files.append(yaml_file)

    except OSError:
        # Handle filesystem errors gracefully
        return result

    result.is_valid = len(result.issues) == 0
    return result


def _validate_agent_yaml(yaml_file: Path) -> ValidationIssue | None:
    """Validate a single YAML file against the Agent schema."""
    try:
        with open(yaml_file) as f:
            data = yaml.safe_load(f)

        if data is None:
            return ValidationIssue(
                issue_type="invalid_yaml",
                path=yaml_file,
                message=f"Empty YAML file: {yaml_file.name}",
                hint=f"Delete '{yaml_file.name}' or add valid agent configuration",
            )

        Agent.model_validate(data)
        return None

    except yaml.YAMLError as e:
        return ValidationIssue(
            issue_type="invalid_yaml",
            path=yaml_file,
            message=f"Invalid YAML syntax in {yaml_file.name}: {e}",
            hint=f"Fix YAML syntax in '{yaml_file.name}' or delete and re-clone",
        )

    except ValidationError as e:
        error_fields = [err["loc"][0] for err in e.errors() if err.get("loc")]
        error_summary = ", ".join(str(f) for f in error_fields[:3])
        if len(error_fields) > 3:
            error_summary += f" (+{len(error_fields) - 3} more)"

        return ValidationIssue(
            issue_type="invalid_schema",
            path=yaml_file,
            message=f"Schema validation failed for {yaml_file.name}: {error_summary}",
            hint=f"Delete '{yaml_file.name}' and re-clone with 'lk agent get'",
        )


def validate_agent_yaml_file(
    yaml_path: Path,
) -> tuple[Agent | None, ValidationError | None, str | None]:
    """Validate an agent YAML file and return the agent or errors.

    Returns:
        Tuple of (agent, validation_error, yaml_error_message).
        - If valid: (Agent, None, None)
        - If schema invalid: (None, ValidationError, None)
        - If YAML invalid: (None, None, error_message)
    """
    try:
        with open(yaml_path) as f:
            data = yaml.safe_load(f)

        if data is None:
            return None, None, f"Empty YAML file: {yaml_path.name}"

        agent = Agent.model_validate(data)
        return agent, None, None

    except yaml.YAMLError as e:
        return None, None, f"Invalid YAML syntax: {e}"

    except ValidationError as e:
        return None, e, None


def format_schema_errors(error: ValidationError, agent_id: str) -> str:
    """Format Pydantic validation errors for detailed user display."""
    lines = [f"[red]Error: Agent '{agent_id}' has invalid schema.[/red]", ""]

    lines.append("[yellow]Expected fields:[/yellow]")
    lines.append("  - id (required): string, 3-50 chars")
    lines.append("  - name (required): string, 1-100 chars")
    lines.append('  - category (required): "chat" or "qa"')
    lines.append("  - model (required): object with provider, name, credential_id")
    lines.append("")

    lines.append("[yellow]Your file is missing or has invalid:[/yellow]")
    for err in error.errors():
        loc = ".".join(str(x) for x in err["loc"])
        msg = err["msg"]
        err_type = err["type"]

        if err_type == "missing":
            lines.append(f"  - {loc}: field required")
        else:
            lines.append(f"  - {loc}: {msg}")

    lines.append("")
    lines.append(f"[dim]Fix the YAML file and re-run 'lk agent set {agent_id}'[/dim]")

    return "\n".join(lines)


def format_validation_errors(result: ValidationResult) -> str:
    """Format validation errors for display to the user."""
    if result.is_valid:
        return ""

    lines = ["[red]Validation errors found in agents/:[/red]", ""]

    if result.nested_folders:
        lines.append("[yellow]Nested folders (flat structure required):[/yellow]")
        for folder in result.nested_folders:
            lines.append(f"  - {folder.name}/")
        lines.append("[dim]Hint: Remove these folders from agents/[/dim]")
        lines.append("")

    if result.invalid_extensions:
        lines.append("[yellow]Invalid file extensions (only .yaml allowed):[/yellow]")
        for file in result.invalid_extensions:
            lines.append(f"  - {file.name}")
        lines.append("[dim]Hint: Remove these files from agents/[/dim]")
        lines.append("")

    if result.invalid_yaml_files:
        lines.append("[yellow]Invalid YAML syntax:[/yellow]")
        for file in result.invalid_yaml_files:
            lines.append(f"  - {file.name}")
        lines.append("[dim]Hint: Fix syntax or delete and re-clone with 'lk agent get'[/dim]")
        lines.append("")

    if result.invalid_schema_files:
        lines.append("[yellow]Invalid agent schema:[/yellow]")
        for file in result.invalid_schema_files:
            lines.append(f"  - {file.name}")
        lines.append("[dim]Hint: Delete and re-clone with 'lk agent get <source> <new-id>'[/dim]")
        lines.append("")

    return "\n".join(lines)
