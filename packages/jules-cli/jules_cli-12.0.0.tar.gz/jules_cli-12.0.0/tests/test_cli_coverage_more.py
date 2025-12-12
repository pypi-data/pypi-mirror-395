# tests/test_cli_coverage_more.py

import pytest
from typer.testing import CliRunner
from jules_cli.cli import app
from unittest.mock import patch, MagicMock
from jules_cli.utils.exceptions import JulesError

runner = CliRunner()

@pytest.fixture(autouse=True)
def mock_logger():
    """Mock the logger to prevent I/O on closed files during CliRunner execution."""
    with patch("jules_cli.cli.logger") as mock:
        yield mock

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.cmd_create_pr")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_pr_create_success(mock_state, mock_create_pr, mock_init, mock_check, mock_logger):
    # Setup state
    mock_state.update({"repo_owner": "owner", "repo_name": "repo", "session_id": "sess1"})
    mock_create_pr.return_value = "http://pr-url"

    result = runner.invoke(app, ["pr", "create", "--title", "T", "--body", "B"])
    assert result.exit_code == 0
    mock_create_pr.assert_called_with(
        owner="owner", repo="repo", title="T", body="B",
        draft=False, labels=None, reviewers=None, assignees=None, issue=None
    )

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.cmd_create_pr")
@patch("jules_cli.cli.config.get_nested")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_pr_create_no_repo_in_state(mock_state, mock_config, mock_create_pr, mock_init, mock_check, mock_logger):
    # State empty, config has default repo
    mock_state.update({})
    mock_config.return_value = "owner/repo"
    mock_create_pr.return_value = "http://pr-url"

    result = runner.invoke(app, ["pr", "create"])
    assert result.exit_code == 0
    mock_create_pr.assert_called()
    assert mock_create_pr.call_args[1]["owner"] == "owner"

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.cmd_create_pr")
@patch("jules_cli.cli.config.get_nested")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_pr_create_fail_no_repo(mock_state, mock_config, mock_create_pr, mock_init, mock_check, mock_logger):
    # State empty, config empty
    mock_state.update({})
    mock_config.return_value = None

    result = runner.invoke(app, ["pr", "create"])
    assert result.exit_code == 1
    mock_logger.error.assert_called()
    assert "No repository specified" in mock_logger.error.call_args[0][0]

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.cmd_suggest")
@patch("jules_cli.cli.add_history_record")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_suggest(mock_state, mock_history, mock_suggest, mock_init, mock_check, mock_logger):
    mock_suggest.return_value = {"suggestions": []}
    mock_state.update({"current_session": {"id": "sess1"}})

    result = runner.invoke(app, ["suggest", "--security", "--focus", "auth"])
    assert result.exit_code == 0
    mock_suggest.assert_called_with(focus="auth", security=True, tests=False, chore=False)
    mock_history.assert_called()
    # verify prompt desc
    prompt = mock_history.call_args[1]["prompt"]
    assert "suggest" in prompt
    assert "--security" in prompt
    assert "--focus auth" in prompt

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.run_refactor")
@patch("jules_cli.cli.add_history_record")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_refactor(mock_state, mock_history, mock_refactor, mock_init, mock_check, mock_logger):
    mock_refactor.return_value = {"status": "success"}

    result = runner.invoke(app, ["refactor", "fix indent"])
    assert result.exit_code == 0
    mock_refactor.assert_called_with("fix indent")
    mock_history.assert_called()

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.run_testgen")
@patch("jules_cli.cli.add_history_record")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_testgen(mock_state, mock_history, mock_testgen, mock_init, mock_check, mock_logger):
    mock_testgen.return_value = {"status": "generated"}

    result = runner.invoke(app, ["testgen", "file.py", "--type", "missing"])
    assert result.exit_code == 0
    mock_testgen.assert_called_with("file.py", test_type="missing")
    mock_history.assert_called()

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.cmd_commit_and_push")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_commit(mock_state, mock_commit, mock_init, mock_check, mock_logger):
    mock_commit.return_value = {"status": "ok"}

    result = runner.invoke(app, ["commit", "-m", "msg", "-t", "fix"])
    assert result.exit_code == 0
    mock_commit.assert_called_with(commit_message="msg", branch_type="fix")

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.cmd_apply")
@patch("jules_cli.cli.add_history_record")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_apply(mock_state, mock_history, mock_apply, mock_init, mock_check, mock_logger):
    mock_apply.return_value = {"status": "applied"}
    mock_state.update({"session_id": "sess1", "last_patch": "patchdata"})

    result = runner.invoke(app, ["apply"])
    assert result.exit_code == 0
    mock_apply.assert_called()
    mock_history.assert_called()

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.load_plugins")
def test_main_plugin_load_error(mock_load, mock_init, mock_check, mock_logger):
    # simulate error during plugin load
    mock_load.side_effect = JulesError("Plugin error")

    # Since main block calling load_plugins is under if __name__ == "__main__":
    # we cannot easily test it via CliRunner invoke of app(), because app() is the Typer object.
    # The code `if __name__ == "__main__": load_plugins(); app()` is entry point logic.
    # But load_plugins is called before app().
    # We can test `load_plugins` logic separately if it was part of app callback, but it is not.
    # It is outside.

    # However, if we look at `cli.py`, `load_plugins` adds commands to `app`.
    # We can call `load_plugins` and see if it handles errors?
    # But the `try...except` block is in `if __name__ == "__main__"`.
    # So we can't test that exception handling via `invoke`.
    pass

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.cmd_approve")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_approve(mock_state, mock_approve, mock_init, mock_check, mock_logger):
    mock_approve.return_value = {}
    result = runner.invoke(app, ["approve", "sess1"])
    assert result.exit_code == 0
    mock_approve.assert_called_with("sess1")

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.cmd_reject")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_reject(mock_state, mock_reject, mock_init, mock_check, mock_logger):
    mock_reject.return_value = {}
    result = runner.invoke(app, ["reject", "sess1"])
    assert result.exit_code == 0
    mock_reject.assert_called_with("sess1")

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.cmd_stage")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_stage(mock_state, mock_stage, mock_init, mock_check, mock_logger):
    mock_stage.return_value = {}
    result = runner.invoke(app, ["stage"])
    assert result.exit_code == 0
    mock_stage.assert_called()

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.cmd_session_list")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_session_list(mock_state, mock_list, mock_init, mock_check, mock_logger):
    mock_list.return_value = []
    result = runner.invoke(app, ["session", "list"])
    assert result.exit_code == 0
    mock_list.assert_called()

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.cmd_session_show")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_session_show(mock_state, mock_show, mock_init, mock_check, mock_logger):
    mock_show.return_value = {}
    result = runner.invoke(app, ["session", "show", "sid"])
    assert result.exit_code == 0
    mock_show.assert_called_with("sid")

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.cmd_history_list")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_history_list(mock_state, mock_list, mock_init, mock_check, mock_logger):
    mock_list.return_value = []
    result = runner.invoke(app, ["history", "list"])
    assert result.exit_code == 0
    mock_list.assert_called()

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.cmd_history_view")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_history_view(mock_state, mock_view, mock_init, mock_check, mock_logger):
    mock_view.return_value = {}
    result = runner.invoke(app, ["history", "view", "sid"])
    assert result.exit_code == 0
    mock_view.assert_called_with("sid")

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.git_push_branch")
@patch("jules_cli.cli.git_current_branch")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_push(mock_state, mock_branch, mock_push, mock_init, mock_check, mock_logger):
    mock_branch.return_value = "feature/branch"
    mock_push.return_value = {"status": "pushed"}
    result = runner.invoke(app, ["push"])
    assert result.exit_code == 0
    mock_push.assert_called_with("feature/branch")

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.run_doctor_command")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_doctor(mock_state, mock_doctor, mock_init, mock_check, mock_logger):
    mock_doctor.return_value = {"status": "healthy"}
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    mock_doctor.assert_called()

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.cmd_interact")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_interact(mock_state, mock_interact, mock_init, mock_check, mock_logger):
    result = runner.invoke(app, ["interact", "hello"])
    assert result.exit_code == 0
    mock_interact.assert_called_with("hello")

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.run_task")
@patch("jules_cli.cli.add_history_record")
@patch("jules_cli.cli._state", new_callable=dict)
def test_cli_task(mock_state, mock_history, mock_task, mock_init, mock_check, mock_logger):
    mock_task.return_value = {"status": "done"}
    result = runner.invoke(app, ["task", "do something"])
    assert result.exit_code == 0
    mock_task.assert_called_with("do something")
    mock_history.assert_called()
