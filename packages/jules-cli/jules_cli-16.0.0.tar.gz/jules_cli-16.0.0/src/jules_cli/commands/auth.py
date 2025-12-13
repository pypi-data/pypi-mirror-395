import typer
import keyring
from getpass import getpass
from ..utils.logging import logger
from ..utils.config import config

auth_app = typer.Typer(name="auth", help="Manage authentication.")

@auth_app.command("login")
def login():
    """
    Interactively set API keys securely.
    """
    typer.echo("Please enter your Jules API Key (input hidden):")
    api_key = typer.prompt("Jules API Key", hide_input=True)

    typer.echo("Please enter your GitHub Token (input hidden):")
    github_token = typer.prompt("GitHub Token", hide_input=True)

    try:
        keyring.set_password("jules-cli", "JULES_API_KEY", api_key)
        keyring.set_password("jules-cli", "GITHUB_TOKEN", github_token)

        # We also want to clear them from config if they were there in plain text?
        # For now, let's just say we saved them.

        typer.echo("Credentials saved securely in system keyring.")
    except Exception as e:
        logger.error(f"Failed to save credentials: {e}")
        raise typer.Exit(code=1)
