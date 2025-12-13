# src/jules_cli/git/vcs.py

import os
import time
import hashlib
import requests
from slugify import slugify
from ..utils.commands import run_cmd
from ..utils.exceptions import GitError
from ..utils.config import config

# Note: GITHUB_TOKEN is now retrieved dynamically inside functions to support keyring/config updates.

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
    Tries to get (owner, repo, platform) from git remote origin.
    Returns (owner, repo, platform) where platform is 'github', 'gitlab', or 'bitbucket'.
    """
    code, out, _ = run_cmd(["git", "remote", "get-url", "origin"])
    if code != 0:
        return None, None, None
    
    url = out.strip()
    # Remove .git suffix if present
    if url.endswith(".git"):
        url = url[:-4]

    platform = "github"
    part = ""

    # Normalize SSH to HTTPS-like format for easier parsing
    if "git@" in url:
        # git@github.com:owner/repo
        # git@gitlab.com:owner/repo
        # git@bitbucket.org:owner/repo
        if ":" in url:
            domain_part = url.split(":", 1)[0] # git@github.com
            if "@" in domain_part:
                domain = domain_part.split("@")[-1]
            else:
                domain = domain_part # unexpected

            part = url.split(":", 1)[-1]

            if "gitlab" in domain:
                platform = "gitlab"
            elif "bitbucket" in domain:
                platform = "bitbucket"
            else:
                platform = "github"
        else:
             return None, None, None
    else:
        # HTTPS
        if "gitlab.com" in url:
            platform = "gitlab"
            if "gitlab.com/" in url:
                part = url.split("gitlab.com/")[-1]
        elif "bitbucket.org" in url:
            platform = "bitbucket"
            if "bitbucket.org/" in url:
                part = url.split("bitbucket.org/")[-1]
        elif "github.com" in url:
            platform = "github"
            if "github.com/" in url:
                part = url.split("github.com/")[-1]
        else:
            # Try to guess based on structure if unknown domain?
            # For now assume failure or default to github if it looks like one
            return None, None, None
        
    if "/" not in part:
        return None, None, None
        
    parts = part.split("/", 1)
    return parts[0], parts[1], platform

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
    github_token = config.get_secret("GITHUB_TOKEN")
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

def gitlab_create_mr(
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
    gitlab_token = config.get_secret("GITLAB_TOKEN")
    if not gitlab_token:
        raise GitError("GITLAB_TOKEN not set; cannot create MR automatically.")

    # Encode project path (owner/repo -> owner%2Frepo)
    project_path = f"{owner}/{repo}".replace("/", "%2F")
    url = f"https://gitlab.com/api/v4/projects/{project_path}/merge_requests"
    headers = {"PRIVATE-TOKEN": gitlab_token}

    data = {
        "source_branch": head,
        "target_branch": base,
        "title": title or "Automated fix from Jules CLI",
        "description": body or "",
    }

    # GitLab doesn't have a simple 'draft' bool in create, usually prefix title with "Draft: "
    if draft:
        data["title"] = "Draft: " + data["title"]

    if labels:
        data["labels"] = ",".join(labels)
    if reviewers:
        data["reviewer_ids"] = reviewers # Note: needs IDs, not names usually. Keeping simplistic for now.
    if assignees:
        data["assignee_ids"] = assignees # Note: needs IDs.

    resp = requests.post(url, headers=headers, json=data, timeout=30)
    if resp.status_code >= 400:
        raise GitError(f"GitLab MR creation failed {resp.status_code}: {resp.text}")
    return resp.json()

def bitbucket_create_pr(
    owner: str,
    repo: str,
    head: str,
    base: str = "main",
    title: str = None,
    body: str = None,
    draft: bool = False, # Bitbucket Cloud doesn't strictly have drafts like GitHub
    labels: list = None,
    reviewers: list = None,
    assignees: list = None,
):
    # Bitbucket uses App Passwords for Basic Auth usually (username:app_password)
    # We expect BITBUCKET_TOKEN to be "username:app_password" or just the token if using OAuth (but CLI usually uses Basic)
    bitbucket_creds = config.get_secret("BITBUCKET_TOKEN")
    if not bitbucket_creds:
        raise GitError("BITBUCKET_TOKEN not set; cannot create PR automatically.")

    if ":" in bitbucket_creds:
        username, password = bitbucket_creds.split(":", 1)
        auth = (username, password)
    else:
        # Assume it's a bearer token? Or maybe just fail. Let's try Basic with user from config?
        # For simplicity, assume token is full credential or bearer.
        # But requests auth is easiest with tuple.
        # If it is just a token, maybe Bearer?
        auth = None
        # But we need auth. Let's raise if not formatted or handle Bearer.
        # If it doesn't contain colon, assume it is a Bearer token.
        pass

    url = f"https://api.bitbucket.org/2.0/repositories/{owner}/{repo}/pullrequests"
    headers = {"Content-Type": "application/json"}

    if ":" not in bitbucket_creds:
         headers["Authorization"] = f"Bearer {bitbucket_creds}"
         auth = None

    data = {
        "title": title or "Automated fix from Jules CLI",
        "description": body or "",
        "source": {
            "branch": {
                "name": head
            }
        },
        "destination": {
            "branch": {
                "name": base
            }
        }
    }

    if reviewers:
        # Bitbucket expects uuids for reviewers usually.
        pass

    resp = requests.post(url, headers=headers, json=data, auth=auth, timeout=30)
    if resp.status_code >= 400:
        raise GitError(f"Bitbucket PR creation failed {resp.status_code}: {resp.text}")
    return resp.json()
