import sys
import typer
import requests
import subprocess
import importlib.metadata
from packaging import version
from ..utils.logging import logger

upgrade_app = typer.Typer(name="upgrade", help="Self-update the Jules CLI.")

@upgrade_app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
):
    """
    Check for updates and upgrade Jules CLI if a new version is available.
    """
    if ctx.invoked_subcommand is not None:
        return

    try:
        current_version_str = importlib.metadata.version("jules-cli")
        current_version = version.parse(current_version_str)

        logger.info(f"Current version: {current_version}")

        # Check PyPI
        response = requests.get("https://pypi.org/pypi/jules-cli/json", timeout=10)
        response.raise_for_status()
        data = response.json()
        latest_version_str = data["info"]["version"]
        latest_version = version.parse(latest_version_str)

        if latest_version > current_version:
            typer.echo(f"New version available: {latest_version}")
            typer.echo("Upgrading jules-cli...")

            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--upgrade", "jules-cli"]
            )
            typer.echo(f"Successfully upgraded to version {latest_version}!")
        else:
            typer.echo(f"You are using the latest version ({current_version}).")

    except Exception as e:
        logger.error(f"Failed to check for updates: {e}")
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)
