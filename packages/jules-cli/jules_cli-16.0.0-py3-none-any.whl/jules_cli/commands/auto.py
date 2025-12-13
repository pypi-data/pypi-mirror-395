# src/jules_cli/commands/auto.py

from ..testing.runner import run_tests
from .task import run_task
from ..utils.logging import logger
from ..utils.config import config
from typing import Optional

def auto_fix_command(repo_dir_name: Optional[str] = None, runner: str = "pytest", detect_flaky: bool = False):
    if repo_dir_name is None:
        repo_dir_name = config.get_nested("core", "default_repo")
        if not repo_dir_name:
            raise RuntimeError(
                "No repository specified. Please use the --repo option or set a default_repo in your config file."
            )

    # run tests
    code, out, err = run_tests(runner=runner, detect_flaky=detect_flaky)
    if code == 0:
        logger.info("🎉 All tests passed. Nothing to do.")
        return {"status": "success", "message": "All tests passed."}
    failure_text = out + "\n" + err
    run_task(prompt_from_failure(failure_text, runner), repo_dir_name=repo_dir_name, auto=True)
    return {"status": "running", "message": "Attempting to fix failed tests."}

def prompt_from_failure(failure_text: str, runner: str) -> str:
    return (
        f"You are Jules, an automated debugging assistant. I will paste {runner} output. "
        "Produce a minimal, correct fix and include any new tests required. "
        "Return changes as changeSet.gitPatch.unidiffPatch or create a PR artifact. "
        f"{runner} output:\n" + failure_text
    )
