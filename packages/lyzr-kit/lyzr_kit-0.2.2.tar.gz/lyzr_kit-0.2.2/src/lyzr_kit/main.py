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


if __name__ == "__main__":
    app()
