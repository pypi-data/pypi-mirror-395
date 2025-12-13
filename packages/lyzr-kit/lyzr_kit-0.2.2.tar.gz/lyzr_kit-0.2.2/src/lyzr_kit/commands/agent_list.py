"""Agent list command implementation."""

from pathlib import Path

import typer
from rich.table import Table

from lyzr_kit.commands._console import console
from lyzr_kit.storage import StorageManager, format_validation_errors, validate_agents_folder


def list_agents() -> None:
    """List all agents (built-in + local)."""
    storage = StorageManager()

    # Validate agents folder structure first
    validation_result = validate_agents_folder(Path(storage.local_path))
    if not validation_result.is_valid:
        console.print(format_validation_errors(validation_result))
        raise typer.Exit(1)

    agents = storage.list_agents()

    # Separate built-in and local agents
    builtin_agents = [(a, s) for a, s in agents if s == "built-in"]
    local_agents = [(a, s) for a, s in agents if s == "local"]

    # Built-in agents table
    console.print()
    builtin_table = Table(title="Built-in Agents", title_style="bold cyan")
    builtin_table.add_column("#", style="dim", justify="right")
    builtin_table.add_column("ID", style="cyan")
    builtin_table.add_column("NAME", style="white")
    builtin_table.add_column("CATEGORY", style="magenta")
    builtin_table.add_column("ENDPOINT", style="dim")

    if builtin_agents:
        for agent, _ in builtin_agents:
            serial_str = str(agent.serial) if agent.serial is not None else "?"
            builtin_table.add_row(
                serial_str,
                agent.id,
                agent.name,
                agent.category,
                "-",
            )
    else:
        builtin_table.add_row("-", "[dim]No built-in agents[/dim]", "", "", "")

    console.print(builtin_table)

    # Local agents table
    console.print()
    local_table = Table(title="Your Agents", title_style="bold green")
    local_table.add_column("#", style="dim", justify="right")
    local_table.add_column("ID", style="cyan")
    local_table.add_column("NAME", style="white")
    local_table.add_column("CATEGORY", style="magenta")
    local_table.add_column("ENDPOINT", style="dim")

    if local_agents:
        for agent, _ in local_agents:
            serial_str = str(agent.serial) if agent.serial is not None else "?"
            endpoint = agent.endpoint if agent.endpoint else "-"
            local_table.add_row(
                serial_str,
                agent.id,
                agent.name,
                agent.category,
                endpoint,
            )
    else:
        local_table.add_row("-", "[dim]No local agents yet[/dim]", "", "", "")
        console.print(local_table)
        console.print("[dim]Run 'lk agent get <#> [new-id]' to clone a built-in agent[/dim]")
        return

    console.print(local_table)
