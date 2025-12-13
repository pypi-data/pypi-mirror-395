"""Main CLI entry point for lyzr-kit."""

import typer

from lyzr_kit.commands.agent import app as agent_app
from lyzr_kit.commands.agent_chat import chat_with_agent
from lyzr_kit.commands.agent_get import get_agent
from lyzr_kit.commands.agent_list import list_agents
from lyzr_kit.commands.agent_set import set_agent
from lyzr_kit.commands.auth import auth as auth_command
from lyzr_kit.commands.feature import app as feature_app
from lyzr_kit.commands.tool import app as tool_app

app = typer.Typer(
    name="lk",
    help="Lyzr Kit - Manage AI agents, tools, and features",
    no_args_is_help=True,
)

# Register subcommands
app.add_typer(agent_app, name="agent", help="Manage agents")
app.add_typer(agent_app, name="a", hidden=True)  # Shorthand

app.add_typer(tool_app, name="tool", help="Manage tools")
app.add_typer(tool_app, name="t", hidden=True)  # Shorthand

app.add_typer(feature_app, name="feature", help="Manage features")
app.add_typer(feature_app, name="f", hidden=True)  # Shorthand

app.command(name="auth")(auth_command)


# Default agent commands at root level (agent resource is optional)
@app.command("ls")
@app.command("list", hidden=True)
def ls() -> None:
    """List all agents (built-in + cloned). Same as 'lk agent ls'."""
    list_agents()


@app.command("get")
def get(
    source_id: str = typer.Argument(..., help="Built-in agent ID or serial number"),
    new_id: str = typer.Argument(None, help="New ID for the cloned agent"),
) -> None:
    """Clone a built-in agent. Same as 'lk agent get'."""
    get_agent(source_id, new_id)


@app.command("set")
def set_cmd(
    identifier: str = typer.Argument(..., help="Local agent ID or serial number"),
) -> None:
    """Update a local agent on platform. Same as 'lk agent set'."""
    set_agent(identifier)


@app.command("chat")
def chat(
    identifier: str = typer.Argument(..., help="Local agent ID or serial number"),
) -> None:
    """Start interactive chat session. Same as 'lk agent chat'."""
    chat_with_agent(identifier)


if __name__ == "__main__":
    app()
