"""Main CLI entry point for lyzr-kit."""

import typer

from lyzr_kit.commands.agent import app as agent_app
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


if __name__ == "__main__":
    app()
