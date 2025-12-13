# src/jules_cli/commands/refactor.py

from typing import Optional
from ..core.api import pick_source_for_repo, create_session, poll_for_result, list_sources, send_message
from ..state import _state
from ..utils.logging import logger
from ..utils.config import config
from ..utils.branch import generate_branch_name
import json

def run_refactor(
    instruction: str,
    repo_dir_name: Optional[str] = None,
    automation_mode: Optional[str] = "AUTO_CREATE_PR",
    plan: Optional[list[str]] = None,
) -> dict:
    """
    Runs a repository-wide refactor.

    Args:
        instruction: The refactoring instruction.
        repo_dir_name: The name of the repository to refactor.
        automation_mode: The automation mode to use.
        plan: An optional multi-step plan to execute.

    Returns:
        The result of the refactoring session.
    """
    if repo_dir_name is None:
        repo_dir_name = config.get_nested("core", "default_repo")
        if not repo_dir_name:
            raise RuntimeError(
                "No repository specified. Please use the --repo option or set a default_repo in your config file."
            )

    # pick source
    source_obj = pick_source_for_repo(repo_dir_name)
    if not source_obj:
        available = [s.get("name") for s in list_sources()]
        raise RuntimeError(
            f"Could not find a matching repository for '{repo_dir_name}'. Available repositories: {', '.join(available)}"
        )
    source_name = source_obj["name"]
    owner = source_obj["githubRepo"]["owner"]
    repo = source_obj["githubRepo"]["repo"]
    logger.info(f"Using Jules source: {source_name} (repo {owner}/{repo})")

    # create session
    logger.info("Creating Jules refactor session...")
    branch_name = generate_branch_name(instruction, branch_type="refactor")
    starting_branch = config.get_nested("core", "default_branch", "main")
    sess = create_session(prompt=instruction, source_name=source_name, starting_branch=starting_branch,
                          title=f"Jules CLI refactor: {instruction[:50]}", automation_mode=automation_mode, branch_name=branch_name)
    _state["current_session"] = sess
    sid = sess.get("id")
    if not sid:
        raise RuntimeError(f"Failed to create session: {sess}")
    logger.info(f"Session created: {sid}.")

    if plan is None:
        logger.info("Generating a plan...")
        send_message(sid, "generate a plan for this refactor")
        result = poll_for_result(sid)
        plan = result.get("plan")
        if not plan:
            raise RuntimeError("Failed to generate a plan.")
        logger.info("Plan generated: %s", json.dumps(plan, indent=2))

    for step in plan:
        logger.info("Executing step: %s", step)
        send_message(sid, step)
        result = poll_for_result(sid)
        if result["type"] == "patch":
            logger.info("Patch available in last_result['patch']. Use `apply` to apply locally.")
            # In a real implementation, we would apply the patch here.
            # For now, we'll just store it.
            _state["last_result"] = result
        elif result["type"] == "pr":
            pr = result.get("pr")
            logger.info("PR artifact: %s", json.dumps(pr, indent=2))
            # In a real implementation, we would handle the PR here.
            # For now, we'll just store it.
            _state["last_result"] = result
            break

    logger.info("Refactor finished.")
    result = _state.get("last_result", {})
    _state["repo_source"] = source_name
    _state["repo_owner"] = owner
    _state["repo_name"] = repo
    logger.info("Result received: %s", result["type"])
    if result["type"] == "patch":
        logger.info("Patch available in last_result['patch']. Use `apply` to apply locally.")
    elif result["type"] == "pr":
        pr = result.get("pr")
        logger.info("PR artifact: %s", json.dumps(pr, indent=2))
    return result
