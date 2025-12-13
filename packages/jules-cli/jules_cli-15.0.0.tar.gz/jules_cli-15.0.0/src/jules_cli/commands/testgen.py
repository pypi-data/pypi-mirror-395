# src/jules_cli/commands/testgen.py

from typing import Optional
from ..core.api import pick_source_for_repo, create_session, poll_for_result, list_sources
from ..state import _state
from ..utils.logging import logger
from ..utils.config import config
from ..utils.branch import generate_branch_name
import json

def run_testgen(
    file_path: str,
    repo_dir_name: Optional[str] = None,
    automation_mode: Optional[str] = "AUTO_CREATE_PR",
    test_type: str = "missing",
) -> dict:
    """
    Generates tests for a given file.

    Args:
        file_path: The path to the file to generate tests for.
        repo_dir_name: The name of the repository to generate tests in.
        automation_mode: The automation mode to use.
        test_type: The type of tests to generate.

    Returns:
        The result of the test generation session.
    """
    if repo_dir_name is None:
        repo_dir_name = config.get_nested("core", "default_repo")
        if not repo_dir_name:
            raise RuntimeError(
                "No repository specified. Please use the --repo option or set a default_repo in your config file."
            )

    prompt = f"Generate {test_type} tests for the file: {file_path}"

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
    logger.info("Creating Jules testgen session...")
    branch_name = generate_branch_name(f"tests for {file_path}", branch_type="fix")
    starting_branch = config.get_nested("core", "default_branch", "main")
    sess = create_session(prompt=prompt, source_name=source_name, starting_branch=starting_branch,
                          title=f"Jules CLI testgen: {file_path}", automation_mode=automation_mode, branch_name=branch_name)
    _state["current_session"] = sess
    sid = sess.get("id")
    if not sid:
        raise RuntimeError(f"Failed to create session: {sess}")
    logger.info(f"Session created: {sid}. Polling for result...")
    result = poll_for_result(sid)
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
    return result
