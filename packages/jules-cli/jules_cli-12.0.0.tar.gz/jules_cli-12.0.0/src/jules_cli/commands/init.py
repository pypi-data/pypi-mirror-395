import typer
import os
from ..utils.config import config, DEFAULT_CONFIG_PATH
from ..utils.logging import logger
from ..commands.doctor import cmd_doctor

def cmd_init():
    """
    Interactive wizard to set up Jules CLI.
    """
    logger.info("Welcome to the Jules CLI Initialization Wizard! 🚀")

    # 1. Ask for API Key
    api_key = typer.prompt("Enter your Jules API Key", default=os.getenv("JULES_API_KEY", ""), show_default=False)

    # 2. Ask for GitHub Token
    github_token = typer.prompt("Enter your GitHub Token", default=os.getenv("GITHUB_TOKEN", ""), show_default=False)

    # 3. Default Repo
    default_repo = typer.prompt("Enter default repository (e.g. owner/repo)", default=config.get_nested("core", "default_repo", ""))

    # 4. Default Branch
    default_branch = typer.prompt("Enter default branch", default=config.get_nested("core", "default_branch", "main"))

    # Update config object
    if "core" not in config.data:
        config.data["core"] = {}

    config.data["core"]["default_repo"] = default_repo
    config.data["core"]["default_branch"] = default_branch

    if api_key:
        config.data["core"]["jules_api_key"] = api_key
    if github_token:
        config.data["core"]["github_token"] = github_token

    config.save()
    logger.info(f"Configuration saved to {config.path}")

    # 5. Run Doctor
    logger.info("Running system checks...")
    cmd_doctor()
