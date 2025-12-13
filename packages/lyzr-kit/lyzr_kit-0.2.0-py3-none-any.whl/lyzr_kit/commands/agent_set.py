"""Agent set command implementation."""

from pathlib import Path

import typer
from rich.status import Status

from lyzr_kit.commands._auth_helper import require_auth
from lyzr_kit.commands._console import console
from lyzr_kit.commands._resolver import resolve_local_agent_id
from lyzr_kit.storage import StorageManager, format_schema_errors, validate_agent_yaml_file
from lyzr_kit.utils.auth import STUDIO_BASE_URL
from lyzr_kit.utils.platform import PlatformClient, PlatformError


def set_agent(identifier: str) -> None:
    """Update agent on platform from agents/<id>.yaml.

    Args:
        identifier: Agent ID or serial number.
    """
    auth = require_auth()
    storage = StorageManager()

    # Resolve identifier (could be serial number or agent ID)
    # For 'set' command, we only look up local agents
    agent_id = resolve_local_agent_id(identifier, storage)
    if agent_id is None:
        raise typer.Exit(1)

    # Check if exists in local (by filename)
    yaml_path = Path(storage.local_path) / "agents" / f"{agent_id}.yaml"
    if not yaml_path.exists():
        console.print(f"[red]Error: Agent '{agent_id}' not found in agents/[/red]")
        console.print("[dim]Run 'lk agent get' first to clone the agent[/dim]")
        raise typer.Exit(1)

    # Load and validate with detailed error messages
    agent, schema_error, yaml_error = validate_agent_yaml_file(yaml_path)

    if yaml_error:
        console.print(f"[red]Error: {yaml_error}[/red]")
        console.print(f"[dim]Fix the YAML file and re-run 'lk agent set {agent_id}'[/dim]")
        raise typer.Exit(1)

    if schema_error:
        console.print(format_schema_errors(schema_error, agent_id))
        raise typer.Exit(1)

    if not agent:
        console.print(f"[red]Error: Failed to load agent '{agent_id}'[/red]")
        raise typer.Exit(1)

    # Detect if ID in YAML differs from filename and conflicts
    if agent.id != agent_id and storage.agent_exists(agent.id):
        console.print(f"[red]Error: ID '{agent.id}' already exists[/red]")
        console.print("[dim]Update the ID in the YAML file and re-run the command[/dim]")
        raise typer.Exit(1)

    # Check if agent has platform IDs
    if not agent.platform_agent_id or not agent.platform_env_id:
        console.print(f"[red]Error: Agent '{agent_id}' has no platform IDs[/red]")
        console.print("[dim]This agent may have been created before platform integration.[/dim]")
        console.print(f"[dim]Delete agents/{agent_id}.yaml and run 'lk agent get' again.[/dim]")
        raise typer.Exit(1)

    # Update agent on platform
    try:
        with Status("[bold cyan]Updating agent on platform...[/bold cyan]", console=console):
            platform = PlatformClient(auth)
            response = platform.update_agent(
                agent=agent,
                agent_id=agent.platform_agent_id,
                env_id=agent.platform_env_id,
            )
            agent.endpoint = response.endpoint

    except PlatformError as e:
        console.print(f"[red]Platform Error:[/red] {e}")
        raise typer.Exit(1) from None

    # Save updated agent
    path = storage.save_agent(agent)

    console.print(f"[green]Agent '{agent_id}' updated successfully![/green]")
    console.print(f"[dim]Agent ID:[/dim] {response.agent_id}")
    console.print(f"[dim]Platform URL:[/dim] {response.platform_url}")
    if agent.marketplace_app_id:
        chat_url = f"{STUDIO_BASE_URL}/agent/{agent.marketplace_app_id}/"
        console.print(f"[dim]Chat URL:[/dim] {chat_url}")
    console.print(f"[dim]API Endpoint:[/dim] {agent.endpoint}")
    console.print(f"[dim]Local config:[/dim] {path}")
