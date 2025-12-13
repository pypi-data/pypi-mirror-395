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
    """List available agents."""
    list_agents()


@app.command("get")
def get(
    source_id: str = typer.Argument(..., help="Built-in agent ID or serial (#)"),
    new_id: str = typer.Argument(None, help="Your new agent ID"),
) -> None:
    """Deploy an agent from built-in templates."""
    get_agent(source_id, new_id)


@app.command("set")
def set_cmd(
    identifier: str = typer.Argument(..., help="Your agent ID or serial (#)"),
) -> None:
    """Push local changes to platform."""
    set_agent(identifier)


@app.command("chat")
def chat(
    identifier: str = typer.Argument(..., help="Your agent ID or serial (#)"),
) -> None:
    """Chat with an agent."""
    chat_with_agent(identifier)
