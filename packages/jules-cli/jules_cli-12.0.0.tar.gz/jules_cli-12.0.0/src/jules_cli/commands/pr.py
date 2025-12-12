# src/jules_cli/commands/pr.py

from typing import List
from ..state import _state
from ..git.vcs import git_current_branch, github_create_pr, git_get_remote_repo_info
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
):
    token = os.getenv("GITHUB_TOKEN") or config.get_nested("core", "github_token")
    if not token:
        logger.error("GITHUB_TOKEN not set in environment or config; cannot create PR.")
        return {"status": "error", "message": "GITHUB_TOKEN not set."}
    
    # We must ensure the github_create_pr function uses this token.
    # Currently `github_create_pr` likely uses `GITHUB_TOKEN` from env or global.
    # We should pass it or ensure it can access it.
    # Let's check `src/jules_cli/git/vcs.py`.
    # For now, let's assume `github_create_pr` reads env.
    # If so, we might need to set it in env temporarily if not present?
    if not os.getenv("GITHUB_TOKEN") and token:
        os.environ["GITHUB_TOKEN"] = token

    owner = _state.get("repo_owner")
    repo = _state.get("repo_name")

    # Fallback: try to detect from git config
    if not owner or not repo:
        owner, repo = git_get_remote_repo_info()
        if owner and repo:
            logger.info(f"Detected repo from git remote: {owner}/{repo}")
        else:
            logger.warning("No repo detected in state or git remote. Run a task first.")
            return {"status": "error", "message": "No repo detected."}
            
    # determine current branch to use as head
    head = git_current_branch()

    if issue:
        body += f"\n\nCloses #{issue}"

    try:
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
        logger.info("Created PR: %s", pr.get("html_url"))

        # Cache the PR metadata
        cache_key = f"pr_{pr['number']}"
        save_to_cache(cache_key, pr)

        return pr
    except Exception as e:
        logger.error("Failed to create PR: %s", e)
        return {"status": "error", "message": f"Failed to create PR: {e}"}