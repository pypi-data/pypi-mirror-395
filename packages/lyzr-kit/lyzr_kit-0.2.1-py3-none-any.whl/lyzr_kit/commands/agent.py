"""Agent CLI commands - combines all agent subcommands."""

import typer

from lyzr_kit.commands.agent_chat import chat_with_agent
from lyzr_kit.commands.agent_get import get_agent
from lyzr_kit.commands.agent_list import list_agents
from lyzr_kit.commands.agent_set import set_agent

app = typer.Typer(no_args_is_help=True)


@app.command("ls")
@app.command("list", hidden=True)
def ls() -> None:
    """List all agents (built-in + cloned)."""
    list_agents()


@app.command("get")
def get(
    source_id: str = typer.Argument(..., help="Built-in agent ID or serial number"),
    new_id: str = typer.Argument(None, help="New ID for the cloned agent"),
) -> None:
    """Clone a built-in agent to agents/<new-id>.yaml and create on platform."""
    get_agent(source_id, new_id)


@app.command("set")
def set_cmd(
    identifier: str = typer.Argument(..., help="Local agent ID or serial number"),
) -> None:
    """Update a local agent on platform from agents/<id>.yaml."""
    set_agent(identifier)


@app.command("chat")
def chat(
    identifier: str = typer.Argument(..., help="Local agent ID or serial number"),
) -> None:
    """Start interactive chat session with a local agent."""
    chat_with_agent(identifier)
