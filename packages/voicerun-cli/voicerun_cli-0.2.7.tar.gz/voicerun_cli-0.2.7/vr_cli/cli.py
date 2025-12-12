import typer

from .commands.agent import app as agent_app
from .commands.auth import app as auth_app
from .commands.context import app as context_app
from .commands.user import app as user_app

app = typer.Typer(
    help="VoiceRun CLI to interact with the VoiceRun API.",
    add_completion=True,
)
app.add_typer(auth_app, help="Authentication commands.")
app.add_typer(user_app, help="User commands.")
app.add_typer(agent_app, help="Manage agents, their functions, and environments.")
app.add_typer(context_app, name="context", help="Manage API context for different environments.")

if __name__ == "__main__":
    app()
