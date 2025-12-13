# src/jules_cli/commands/task.py

from typing import Optional
from ..core.api import pick_source_for_repo, create_session, poll_for_result, list_sources
from ..state import _state
from ..utils.logging import logger
from ..utils.branch import generate_branch_name
from ..utils.config import config
import json

def run_task(
    user_prompt: str,
    repo_dir_name: Optional[str] = None,
    automation_mode: Optional[str] = "AUTO_CREATE_PR",
    auto: bool = False,
    timeout: Optional[int] = None,  # <-- Added parameter
):
    if repo_dir_name is None:
        repo_dir_name = config.get_nested("core", "default_repo")
        if not repo_dir_name:
            raise RuntimeError("No repository specified. Use --repo or set default_repo in your config.")
    # pick source
    source_obj = pick_source_for_repo(repo_dir_name)
    if not source_obj:
        available = [s.get("name") for s in list_sources()]
        raise RuntimeError(f"No source matched repo '{repo_dir_name}'. Available: {available}")
    source_name = source_obj["name"]
    owner = source_obj["githubRepo"]["owner"]
    repo = source_obj["githubRepo"]["repo"]
    logger.info(f"Using Jules source: {source_name} (repo {owner}/{repo})")

    # create session
    logger.info("Creating Jules session...")
    branch_name = generate_branch_name(user_prompt)
    starting_branch = config.get_nested("core", "default_branch", "main")
    sess = create_session(prompt=user_prompt, source_name=source_name, starting_branch=starting_branch,
                          title="Jules CLI interactive", automation_mode=automation_mode, branch_name=branch_name)
    _state["current_session"] = sess
    sid = sess.get("id")
    if not sid:
        raise RuntimeError(f"Failed to create session: {sess}")
    
    # Use provided timeout or fall back to config default (which poll_for_result handles if None passed, but we want explicit control here)
    poll_timeout = timeout if timeout is not None else config.get_nested("core", "api_timeout", 120)

    logger.info(f"Session created: {sid}. Polling for result (timeout={poll_timeout}s)...")
    result = poll_for_result(sid, timeout=poll_timeout) # <-- Pass timeout here
    _state["last_result"] = result
    _state["repo_source"] = source_name
    _state["repo_owner"] = owner
    _state["repo_name"] = repo
    logger.info("Result received: %s", result["type"])
    if result["type"] == "patch":
        logger.info("Patch available in last_result['patch']. Use `apply` to apply locally.")
    elif result["type"] == "pr":
        pr = result.get("pr")
        logger.info("PR artifact: %s", json.dumps(pr, indent=2))
    elif result["type"] == "message":
        message = result.get("message")
        logger.info(f"Jules message: {message}")
    elif result["type"] == "plan":
        plan = result.get("plan")
        logger.info(f"Jules plan generated:")
        for step in plan.get("steps", []):
            logger.info(f"- {step.get('title')}: {step.get('description')}")
        logger.info("Use `jules approve` to approve the plan or `jules reject` to reject it.")
    elif result["type"] == "session_status":
        status = result["status"]
        session = result["session"]
        logger.info(f"Jules session {session['id']} reached state: {status}")
        if status == "COMPLETED":
            logger.info("Session completed without generating specific artifacts.")
        elif status == "FAILED":
            logger.error("Session failed.")
        elif status == "CANCELLED":
            logger.warning("Session cancelled.")
        elif status == "PLANNING":
            logger.info("Session is in PLANNING state. Jules is likely waiting for further instructions.")
        else:
            logger.info(f"Session in unexpected state: {status}")
    return result