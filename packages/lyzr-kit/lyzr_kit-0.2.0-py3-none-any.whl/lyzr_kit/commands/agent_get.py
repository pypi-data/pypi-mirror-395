"""Agent get command implementation."""

import typer
from rich.status import Status

from lyzr_kit.commands._auth_helper import require_auth
from lyzr_kit.commands._console import console
from lyzr_kit.commands._resolver import resolve_builtin_agent_id
from lyzr_kit.storage import StorageManager, get_next_local_serial
from lyzr_kit.utils.auth import AuthConfig
from lyzr_kit.utils.platform import PlatformClient, PlatformError


def _generate_default_agent_id(auth: AuthConfig, resource_name: str) -> str:
    """Generate default agent ID from user_id, org_id and resource name.

    Format: <user_id_suffix>-<org_id_suffix>-<resource_name>
    """
    parts = []

    if auth.user_id:
        user_id = auth.user_id
        if user_id.startswith("mem_"):
            user_id = user_id[4:]
        user_suffix = user_id[:8] if len(user_id) >= 8 else user_id
        parts.append(user_suffix)

    if auth.org_id:
        org_id = auth.org_id
        org_suffix = org_id[:8] if len(org_id) >= 8 else org_id
        parts.append(org_suffix)

    parts.append(resource_name)
    return "-".join(parts)


def get_agent(source_id: str, new_id: str | None = None) -> None:
    """Clone agent to agents/<new-id>.yaml and create on platform."""
    auth = require_auth()
    storage = StorageManager()

    # Resolve source_id (could be serial number or agent ID)
    # For 'get' command, we only look up built-in agents
    resolved_source_id = resolve_builtin_agent_id(source_id, storage)
    if resolved_source_id is None:
        raise typer.Exit(1)

    # Generate default ID
    default_id = _generate_default_agent_id(auth, resolved_source_id)

    # Prompt for new_id if not provided
    if new_id is None:
        new_id = console.input(
            f"[cyan]Enter ID for your new agent[/cyan] [dim](default: {default_id})[/dim]: "
        ).strip()
        if not new_id:
            new_id = default_id

    # Check if new_id conflicts with existing agents
    if storage.agent_exists(new_id):
        console.print(f"[red]Error: ID '{new_id}' already exists[/red]")
        console.print("[dim]Re-run the command with a different ID[/dim]")
        raise typer.Exit(1)

    # Get source agent
    agent = storage.get_agent(resolved_source_id)
    if not agent:
        console.print(f"[red]Error: Source agent '{source_id}' not found[/red]")
        console.print("[dim]Run 'lk agent ls' to see available agents[/dim]")
        raise typer.Exit(1)

    # Update agent ID and serial
    agent.id = new_id
    agent.serial = get_next_local_serial()

    # Create agent on platform
    try:
        with Status("[bold cyan]Creating agent on platform...[/bold cyan]", console=console):
            platform = PlatformClient(auth)
            response = platform.create_agent(agent)

            agent.is_active = True
            agent.endpoint = response.endpoint
            agent.platform_agent_id = response.agent_id
            agent.platform_env_id = response.env_id
            agent.marketplace_app_id = response.app_id

    except PlatformError as e:
        console.print(f"[red]Platform Error:[/red] {e}")
        raise typer.Exit(1) from None

    # Save to local
    path = storage.save_agent(agent)

    console.print(f"[green]Agent '{new_id}' created successfully![/green]")
    console.print(f"[dim]Agent ID:[/dim] {response.agent_id}")
    console.print(f"[dim]Platform URL:[/dim] {response.platform_url}")
    if response.chat_url:
        console.print(f"[dim]Chat URL:[/dim] {response.chat_url}")
    console.print(f"[dim]API Endpoint:[/dim] {agent.endpoint}")
    console.print(f"[dim]Local config:[/dim] {path}")
    if response.app_id:
        console.print(f"[dim]Marketplace App:[/dim] {response.app_id}")
