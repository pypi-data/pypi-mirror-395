# src/jules_cli/git/vcs.py

import os
import time
import hashlib
import requests
from slugify import slugify
from ..utils.commands import run_cmd
from ..utils.exceptions import GitError
from ..utils.config import config

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def git_current_branch() -> str:
    code, out, _ = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if code != 0:
        raise GitError("Failed to get current branch.")
    return out.strip()

def git_is_clean() -> bool:
    code, out, _ = run_cmd(["git", "status", "--porcelain"])
    if code != 0:
        raise GitError("Failed to get git status.")
    return not out.strip()

def git_get_remote_repo_info():
    """
    Tries to get (owner, repo) from git remote origin.
    """
    code, out, _ = run_cmd(["git", "remote", "get-url", "origin"])
    if code != 0:
        return None, None
    
    url = out.strip()
    # Remove .git suffix if present
    if url.endswith(".git"):
        url = url[:-4]
        
    # Handle SSH: git@github.com:owner/repo
    if "github.com:" in url:
        part = url.split("github.com:")[-1]
    # Handle HTTPS: https://github.com/owner/repo
    elif "github.com/" in url:
        part = url.split("github.com/")[-1]
    else:
        return None, None
        
    if "/" not in part:
        return None, None
        
    parts = part.split("/", 1)
    return parts[0], parts[1]

def git_create_branch_and_commit(
    commit_message: str = "jules: automated fix",
    branch_type: str = "feature",
):

    summary = commit_message.split("\n")[0]
    slug = slugify(summary)

    # Add a short hash to prevent branch name collisions
    short_hash = hashlib.sha1(str(time.time()).encode()).hexdigest()[:6]

    branch_name = f"{branch_type}/{slug}-{short_hash}"

    code, _, err = run_cmd(["git", "checkout", "-b", branch_name], capture=False)
    if code != 0:
        raise GitError(f"Failed to create branch: {err}")
    code, _, err = run_cmd(["git", "add", "-A"], capture=False)
    if code != 0:
        raise GitError(f"Failed to add files: {err}")
    code, _, err = run_cmd(["git", "commit", "-m", commit_message], capture=False)
    if code != 0:
        raise GitError(f"Failed to commit changes: {err}")


def git_push_branch(branch_name: str):
    code, _, err = run_cmd(["git", "push", "-u", "origin", branch_name], capture=False)
    if code != 0:
        raise GitError(f"Failed to push branch: {err}")

def github_create_pr(
    owner: str,
    repo: str,
    head: str,
    base: str = "main",
    title: str = None,
    body: str = None,
    draft: bool = False,
    labels: list = None,
    reviewers: list = None,
    assignees: list = None,
):
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise GitError("GITHUB_TOKEN not set; cannot create PR automatically.")
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}
    data = {
        "head": head,
        "base": base,
        "title": title or "Automated fix from Jules CLI",
        "body": body or "",
        "draft": draft,
    }

    if labels:
        data["labels"] = labels
    if reviewers:
        data["reviewers"] = reviewers
    if assignees:
        data["assignees"] = assignees

    resp = requests.post(url, headers=headers, json=data, timeout=30)
    if resp.status_code >= 400:
        raise GitError(f"GitHub PR creation failed {resp.status_code}: {resp.text}")
    return resp.json()