# src/jules_cli/commands/commit.py

from ..git.vcs import git_create_branch_and_commit, git_push_branch, git_current_branch
from ..utils.logging import logger

def cmd_commit_and_push(
    commit_message: str = "chore: automated changes from Jules",
    branch_type: str = "feature",
):
    try:
        git_create_branch_and_commit(
            commit_message=commit_message,
            branch_type=branch_type,
        )
    except Exception as e:
        logger.error("Failed to commit: %s", e)
        return {"status": "error", "message": f"Failed to commit: {e}"}

    branch = git_current_branch()

    try:
        git_push_branch(branch)
        logger.info(f"Pushed branch {branch}")
        return {"status": "success", "branch": branch}
    except Exception as e:
        logger.error("Failed to push automatically: %s", e)
        logger.info(f"Run: git push origin {branch}")
        return {"status": "error", "message": f"Failed to push: {e}", "branch": branch}
