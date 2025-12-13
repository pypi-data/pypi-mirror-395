#!/usr/bin/env python3
# src/jules_cli/cli.py

"""
Jules Interactive CLI
"""
import os
import typer
from typer import Context
from typing_extensions import Annotated
from importlib import metadata

from .commands.auto import auto_fix_command
from .commands.task import run_task
from .commands.refactor import run_refactor
from .commands.testgen import run_testgen
from .commands.session import cmd_session_list, cmd_session_show
from .commands.history import cmd_history_list, cmd_history_view
from .commands.apply import cmd_apply
from .commands.config import config_app
from .commands.auth import auth_app
from .commands.commit import cmd_commit_and_push
from .commands.pr import cmd_create_pr
from .commands.doctor import run_doctor_command
from .commands.stage import cmd_stage
from .commands.plan import cmd_approve, cmd_reject
from .commands.workspace import app as workspace_app
from .commands.suggest import cmd_suggest
from .commands.interact import cmd_interact
from .commands.init import cmd_init
from .commands.upgrade import upgrade_app
from .commands.hooks import install_hooks
from .tui.app import JulesTui
from .db import init_db, add_history_record
from .git.vcs import git_push_branch, git_current_branch
from .state import _state
from .utils.environment import check_env
from .utils.logging import logger, setup_logging
from .utils.exceptions import JulesError
from .utils.config import config
from .utils.output import print_json
from .utils.decorators import with_output_handling, record_history
from .banner import print_logo

app = typer.Typer(
    help="Jules Interactive CLI — fully immersive developer assistant.",
    add_completion=True,
    no_args_is_help=True,
    rich_markup_mode="markdown",
)

session_app = typer.Typer(name="session", help="Manage sessions.")
history_app = typer.Typer(name="history", help="View session history.")
pr_app = typer.Typer(name="pr", help="Manage pull requests.")
hooks_app = typer.Typer(name="hooks", help="Manage local git hooks.")

app.add_typer(session_app)
app.add_typer(history_app)
app.add_typer(pr_app)
app.add_typer(workspace_app)
app.add_typer(config_app)
app.add_typer(auth_app)
app.add_typer(upgrade_app)
app.add_typer(hooks_app)

def load_plugins():
    for entry_point in metadata.entry_points(group="jules.plugins"):
        plugin = entry_point.load()
        if isinstance(plugin, typer.Typer):
            app.add_typer(plugin, name=entry_point.name)
        else:
            app.command(entry_point.name)(plugin)

@app.callback()
def main(
    ctx: typer.Context,
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging."),
    verbose: bool = typer.Option(False, "--verbose", help="Enable verbose logging."),
    no_color: bool = typer.Option(False, "--no-color", help="Disable colored output."),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format."),
    pretty: bool = typer.Option(False, "--pretty", help="Pretty-print JSON output."),
):
    """
    Main entry point for the Jules CLI.
    Initializes logging, checks the environment, and sets up the database.
    """
    print_logo()
    _state["json_output"] = json_output
    _state["pretty"] = pretty
    """
    Jules CLI
    """
    log_level = config.get("log_level", "INFO").upper()
    if debug:
        log_level = "DEBUG"
    elif verbose:
        log_level = "VERBOSE"

    color_mode = config.get("color_mode", "auto")
    use_color = not no_color and color_mode != "off"

    setup_logging(level=log_level, color=use_color)

    # Skip environment and DB checks for the 'doctor', 'auth', and 'init' commands
    if ctx.invoked_subcommand not in ["doctor", "auth", "init"]:
        try:
            check_env()
        except JulesError as e:
            logger.error(e)
            raise typer.Exit(code=1)

        try:
            init_db()
        except Exception as e:
            logger.error("Failed to initialize database: %s", e)
            raise typer.Exit(code=1)


@app.command()
@with_output_handling
def auto(
    runner: str = typer.Option(
        "pytest",
        "--runner",
        "-r",
        help="Test runner to use (pytest, unittest, nose2).",
    ),
    detect_flaky: bool = typer.Option(
        False,
        "--detect-flaky",
        help="Attempt to detect flaky tests by re-running failures.",
    ),
):
    """
    Run tests and auto-fix failures.
    """
    return auto_fix_command(runner=runner, detect_flaky=detect_flaky)

@app.command()
@with_output_handling
@record_history(prompt_template="generate {test_type} tests for {file_path}", status="testgen_run")
def testgen(
    file_path: str,
    test_type: str = typer.Option(
        "missing",
        "--type",
        "-t",
        help="Type of tests to generate (e.g., missing, edge-case, async, error-path).",
    ),
):
    """
    Generate tests for a given file.
    """
    return run_testgen(file_path, test_type=test_type)

@app.command()
@with_output_handling
@record_history(prompt_arg_name="instruction", status="refactor_run")
def refactor(instruction: str):
    """
    Run a repository-wide refactor.
    """
    return run_refactor(instruction)

@app.command()
@with_output_handling
@record_history(prompt_arg_name="prompt", status="task_run")
def task(prompt: str):
    """
    Ask Jules to perform an arbitrary dev task (bugfix/refactor/tests/docs).
    """
    return run_task(prompt)

@app.command()
@with_output_handling
def approve(session_id: str = typer.Argument(None, help="Session ID to approve (optional if recent session exists)")):
    """
    Approve the plan for the current or specified session.
    """
    return cmd_approve(session_id)

@app.command()
@with_output_handling
def reject(session_id: str = typer.Argument(None, help="Session ID to reject (optional if recent session exists)")):
    """
    Reject the plan for the current or specified session.
    """
    return cmd_reject(session_id)

@session_app.command("list")
@with_output_handling
def session_list():
    """
    List sessions.
    """
    return cmd_session_list()

@session_app.command("show")
@with_output_handling
def session_show(session_id: str):
    """
    Show session details.
    """
    return cmd_session_show(session_id)

@history_app.command("list")
@with_output_handling
def history_list():
    """
    List all sessions.
    """
    return cmd_history_list()

@history_app.command("view")
@with_output_handling
def history_view(session_id: str):
    """
    Show session details by id.
    """
    return cmd_history_view(session_id)

@app.command()
@with_output_handling
def apply():
    """
    Apply last patch received.
    """
    result = cmd_apply()
    if _state.get("session_id"):
        add_history_record(session_id=_state.get("session_id"), patch=_state.get("last_patch"), status="patched")
    return result

@app.command()
@with_output_handling
def commit(
    commit_message: str = typer.Option(
        "chore: automated changes from Jules",
        "--message",
        "-m",
        help="Commit message.",
    ),
    branch_type: str = typer.Option(
        "feature",
        "--type",
        "-t",
        help="Branch type (e.g., fix, feature, chore).",
    ),
):
    """
    Commit & create branch after apply (if patch applied locally).
    """
    return cmd_commit_and_push(commit_message=commit_message, branch_type=branch_type)

@app.command()
@with_output_handling
def push():
    """
    Push branch to origin.
    """
    branch = git_current_branch()
    return git_push_branch(branch)

@pr_app.command("create")
@with_output_handling
def pr_create(
    title: str = typer.Option("Automated fix from Jules CLI", "--title", "-t", help="PR title."),
    body: str = typer.Option("Auto PR", "--body", "-b", help="PR body."),
    draft: bool = typer.Option(False, "--draft", help="Create a draft PR."),
    labels: str = typer.Option(None, "--labels", "-l", help="Comma-separated labels."),
    reviewers: str = typer.Option(None, "--reviewers", "-r", help="Comma-separated reviewers."),
    assignees: str = typer.Option(None, "--assignees", "-a", help="Comma-separated assignees."),
    issue: int = typer.Option(None, "--issue", "-i", help="Linked issue number."),
):
    """
    Create a PR/MR for GitHub, GitLab, or Bitbucket. Auto-detects platform.
    """
    pr_url = cmd_create_pr(
        title=title,
        body=body,
        draft=draft,
        labels=labels.split(",") if labels else None,
        reviewers=reviewers.split(",") if reviewers else None,
        assignees=assignees.split(",") if assignees else None,
        issue=issue,
    )

    if isinstance(pr_url, dict) and "status" in pr_url and pr_url["status"] == "error":
        raise typer.Exit(code=1)

    url = "unknown"
    if isinstance(pr_url, str):
        url = pr_url
    elif "html_url" in pr_url: url = pr_url["html_url"]
    elif "web_url" in pr_url: url = pr_url["web_url"]
    elif "links" in pr_url and "html" in pr_url["links"]: url = pr_url["links"]["html"]["href"]

    if _state.get("session_id"):
        add_history_record(session_id=_state.get("session_id"), pr_url=url, status="pr_created")
    return {"pr_url": url}

@hooks_app.command("install")
def hooks_install():
    """
    Install Jules pre-commit hooks.
    """
    install_hooks()


@app.command()
@with_output_handling
def stage():
    """
    Interactively stage changes.
    """
    return cmd_stage()

@app.command()
@with_output_handling
def doctor():
    """
    Run environment validation checks.
    """
    return run_doctor_command()

@app.command(name="init")
def init():
    """
    Interactive wizard to set up Jules CLI.
    """
    cmd_init()

@app.command()
@with_output_handling
def suggest(
    focus: str = typer.Option(None, "--focus", "-f", help="Limit suggestions to a specific area."),
    security: bool = typer.Option(False, "--security", help="Focus on security vulnerabilities (OWASP, secrets)."),
    tests: bool = typer.Option(False, "--tests", help="Focus on generating missing tests and improving coverage."),
    chore: bool = typer.Option(False, "--chore", help="Focus on maintenance, dependencies, and cleanup."),
):
    """
    Proactively scan the codebase and suggest improvements.
    """
    result = cmd_suggest(focus=focus, security=security, tests=tests, chore=chore)
    
    sess = _state.get("current_session")
    session_id = sess.get("id") if sess else os.urandom(8).hex()
    _state["session_id"] = session_id

    # Construct a descriptive prompt string for history
    prompt_desc = "jules suggest"
    if security: prompt_desc += " --security"
    if tests: prompt_desc += " --tests"
    if chore: prompt_desc += " --chore"
    if focus: prompt_desc += f" --focus {focus}"

    add_history_record(session_id=session_id, prompt=prompt_desc, status="suggest_run")
    
    return result

@app.command()
def interact(prompt: str):
    """
    Start an interactive chat session with Jules.
    """
    cmd_interact(prompt)

@app.command()
def tui():
    """
    Launch the Jules TUI.
    """
    app = JulesTui()
    app.run()


if __name__ == "__main__":
    try:
        load_plugins()
        app()
    except JulesError as e:
        logger.error(e)
        raise typer.Exit(code=1)
    except Exception as e:
        logger.critical("Fatal error: %s", e)
        raise typer.Exit(code=1)
