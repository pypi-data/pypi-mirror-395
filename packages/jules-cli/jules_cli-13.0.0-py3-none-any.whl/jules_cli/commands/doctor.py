# src/jules_cli/commands/doctor.py

import os
import json
import shutil
import socket
import importlib.metadata
from ..utils.logging import logger
from ..utils.config import DEFAULT_CONFIG_PATH, config
from ..utils.commands import run_cmd
from ..git.vcs import git_get_remote_repo_info

def check_jules_api_key():
    return "JULES_API_KEY is set." if os.getenv("JULES_API_KEY") else "JULES_API_KEY is not set."

def check_git_installed():
    return "Git is installed." if shutil.which("git") else "Git is not installed."

def check_patch_installed():
    return "patch is installed." if shutil.which("patch") else "patch is not installed."

def check_repo_is_clean():
    code, out, _ = run_cmd(["git", "status", "--porcelain"])
    return "Git repository is clean." if code == 0 and not out.strip() else "Git repository has uncommitted changes."

def check_internet_connectivity():
    try:
        socket.create_connection(("8.8.8.8", 53))
        return "Internet connectivity is available."
    except OSError:
        return "No internet connectivity."

def check_github_token():
    return "GITHUB_TOKEN is set." if os.getenv("GITHUB_TOKEN") else "GITHUB_TOKEN is not set (optional)."

def check_config_file():
    return f"Config file found at {DEFAULT_CONFIG_PATH}." if os.path.exists(DEFAULT_CONFIG_PATH) else "Config file not found."

def check_dependencies():
    """
    Check if all dependencies from requirements.txt are installed.
    """
    try:
        with open("requirements.txt") as f:
            requirements = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return "Could not find requirements.txt."

    missing = []
    for req in requirements:
        try:
            importlib.metadata.version(req)
        except importlib.metadata.PackageNotFoundError:
            missing.append(req)

    if not missing:
        return "All dependencies are installed."
    else:
        return f"Missing dependencies: {', '.join(missing)}"

def check_configured_repo():
    owner, repo = git_get_remote_repo_info()
    if owner and repo:
        return f"Configured repository: {owner}/{repo}"
    else:
        return "No repository configured or detected from git remote."

def run_doctor_command():
    checks = {
        "JULES_API_KEY": check_jules_api_key(),
        "Git": check_git_installed(),
        "patch": check_patch_installed(),
        "Repo Status": check_repo_is_clean(),
        "Internet": check_internet_connectivity(),
        "GitHub Token": check_github_token(),
        "Config File": check_config_file(),
        "Dependencies": check_dependencies(),
        "Configured Repository": check_configured_repo(),
    }

    logger.info("Jules Environment Doctor")
    for check, result in checks.items():
        logger.info(f"- {check}: {result}")
    return checks

cmd_doctor = run_doctor_command