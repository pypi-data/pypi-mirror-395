# src/jules_cli/commands/config.py

import typer
import json
import ast
from ..utils.config import config
from ..utils.logging import logger

config_app = typer.Typer(name="config", help="Manage CLI configuration.")

@config_app.command("list")
def list_config():
    """
    List the entire configuration.
    """
    typer.echo(json.dumps(config.data, indent=2))

@config_app.command("get")
def get_config(key: str):
    """
    Get a configuration value by key (e.g., 'core.default_repo').
    """
    val = config.get_from_path(key)
    if val is None:
        logger.warning(f"Key '{key}' not found.")
    else:
        if isinstance(val, (dict, list)):
            typer.echo(json.dumps(val, indent=2))
        else:
            typer.echo(val)

@config_app.command("set")
def set_config(key: str, value: str):
    """
    Set a configuration value (e.g., 'core.api_timeout 120').
    Automatically infers boolean, integer, list, and dict types.
    """
    # Infer type
    real_value = value
    try:
        # Try to parse as a python literal (bool, int, float, list, dict)
        real_value = ast.literal_eval(value)
    except (ValueError, SyntaxError):
        # If it fails, treat as a string
        # Handle simple boolean strings that literal_eval might miss if lowercase?
        # ast.literal_eval('true') fails, 'True' works.
        if value.lower() == "true":
            real_value = True
        elif value.lower() == "false":
            real_value = False
        else:
            real_value = value

    try:
        config.set_value(key, real_value)
        logger.info(f"Set '{key}' to '{real_value}'")
    except Exception as e:
        logger.error(f"Failed to set config: {e}")
        raise typer.Exit(code=1)

@config_app.command("set-repo")
def set_repo(repo_name: str):
    """
    Sets the default repository (shortcut for 'set core.default_repo').
    """
    if "/" not in repo_name:
        logger.error("Invalid repository format. Please use 'owner/repo'.")
        raise typer.Exit(code=1)
    
    set_config("core.default_repo", repo_name)
