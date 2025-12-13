# src/jules_cli/commands/stage.py


from ..utils.commands import run_cmd_interactive
from ..utils.logging import logger
from ..git.vcs import git_is_clean

def cmd_stage():
    """
    Run git add -p to interactively stage changes.
    """
    if git_is_clean():
        logger.info("No changes to stage.")
        return {"status": "success", "message": "No changes."}

    logger.info("Starting interactive staging session...")
    try:
        run_cmd_interactive(["git", "add", "-p"])
        logger.info("Interactive staging session finished.")
        return {"status": "success"}
    except Exception as e:
        logger.error("Failed to run interactive staging: %s", e)
        return {"status": "error", "message": str(e)}
