# src/jules_cli/commands/pr.py

from typing import List, Optional
from ..state import _state
from ..git.vcs import (
    git_current_branch,
    github_create_pr,
    gitlab_create_mr,
    bitbucket_create_pr,
    git_get_remote_repo_info
)
import os
from ..utils.logging import logger
from ..utils.config import config
from ..cache import save_to_cache

def cmd_create_pr(
    title: str = "Automated fix from Jules CLI",
    body: str = "Auto PR",
    draft: bool = False,
    labels: List[str] = None,
    reviewers: List[str] = None,
    assignees: List[str] = None,
    issue: int = None,
    platform: Optional[str] = None,
    owner: Optional[str] = None,
    repo: Optional[str] = None,
):
    detected_platform = None

    # If owner/repo not provided, try state, then git remote, then config default
    if not owner or not repo:
        owner = _state.get("repo_owner")
        repo = _state.get("repo_name")

        if not owner or not repo:
            # Try git remote
            owner_git, repo_git, platform_git = git_get_remote_repo_info()
            if owner_git and repo_git:
                owner = owner_git
                repo = repo_git
                detected_platform = platform_git
                logger.info(f"Detected repo from git remote: {owner}/{repo} on {detected_platform}")
            else:
                # Fallback to default config
                default_repo = config.get_nested("core", "default_repo")
                if default_repo and "/" in default_repo:
                    owner, repo = default_repo.split("/", 1)
                    logger.info(f"Using default repo from config: {owner}/{repo}")
                else:
                    logger.warning("No repo detected in state, git remote, or config.")
                    return {"status": "error", "message": "No repo detected."}

    # Use detected platform if not provided
    if not platform:
        platform = detected_platform or "github" # Default to github if fallback or manually set

    # determine current branch to use as head
    try:
        head = git_current_branch()
    except Exception:
        # If not in a git repo (e.g. using default_repo config), we might need a head branch name.
        # But if we are not in git, we can't create a PR from local changes easily unless we pushed differently.
        # Assuming we are in a git repo or the user knows what they are doing.
        # If git_current_branch fails, we probably can't proceed unless 'head' was passed as arg (not currently supported in signature)
        logger.error("Could not determine current branch. Are you in a git repository?")
        return {"status": "error", "message": "Could not determine current branch."}

    if issue:
        body += f"\n\nCloses #{issue}"

    try:
        if platform == "github":
            token = config.get_secret("GITHUB_TOKEN") or config.get_nested("core", "github_token")
            if not token:
                logger.error("GITHUB_TOKEN not set.")
                return {"status": "error", "message": "GITHUB_TOKEN not set."}

            pr = github_create_pr(
                owner,
                repo,
                head=head,
                base="main",
                title=title,
                body=body,
                draft=draft,
                labels=labels,
                reviewers=reviewers,
                assignees=assignees,
            )
            logger.info("Created GitHub PR: %s", pr.get("html_url"))

        elif platform == "gitlab":
            pr = gitlab_create_mr(
                owner,
                repo,
                head=head,
                base="main",
                title=title,
                body=body,
                draft=draft,
                labels=labels,
                reviewers=reviewers,
                assignees=assignees,
            )
            logger.info("Created GitLab MR: %s", pr.get("web_url"))

        elif platform == "bitbucket":
            pr = bitbucket_create_pr(
                owner,
                repo,
                head=head,
                base="main",
                title=title,
                body=body,
                draft=draft,
                labels=labels,
                reviewers=reviewers,
                assignees=assignees,
            )
            logger.info("Created Bitbucket PR: %s", pr.get("links", {}).get("html", {}).get("href"))

        else:
            logger.error(f"Unsupported platform: {platform}")
            return {"status": "error", "message": f"Unsupported platform: {platform}"}

        # Cache the PR metadata
        if isinstance(pr, dict):
            # Try to get ID or number
            pr_id = pr.get("number") or pr.get("iid") or pr.get("id")
            cache_key = f"pr_{platform}_{pr_id}"
            save_to_cache(cache_key, pr)

        return pr
    except Exception as e:
        logger.error("Failed to create PR/MR: %s", e)
        return {"status": "error", "message": f"Failed to create PR: {e}"}
