# src/jules_cli/commands/workspace.py


import typer
import yaml
import subprocess
from pathlib import Path
import shlex
from ..utils.logging import logger

app = typer.Typer(name="workspace", help="Manage workspaces.")

@app.command("run")
def run(command: str):
    """
    Run a command in each repository defined in the workspace.yaml file.
    """
    workspace_file = Path("workspace.yaml")
    if not workspace_file.exists():
        logger.error("Error: workspace.yaml not found.")
        raise typer.Exit(code=1)

    with open(workspace_file, "r") as f:
        workspace_data = yaml.safe_load(f)

    if "repos" not in workspace_data:
        logger.error("Error: workspace.yaml is missing the 'repos' key.")
        raise typer.Exit(code=1)

    for repo in workspace_data["repos"]:
        repo_path = Path(repo["name"])
        if not repo_path.exists() or not repo_path.is_dir():
            logger.warning(f"Warning: Repository '{repo['name']}' not found. Skipping.")
            continue

        logger.info(f"Running command in '{repo['name']}': {command}")
        subprocess.run(shlex.split(command), cwd=str(repo_path), check=True)
