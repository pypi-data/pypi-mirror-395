# tests/test_cli.py

import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock

from jules_cli.cli import app
from jules_cli.utils.exceptions import JulesError

runner = CliRunner()

@pytest.fixture(autouse=True)
def mock_dependencies():
    with patch("jules_cli.cli.check_env") as mock_check_env, \
         patch("jules_cli.cli.init_db") as mock_init_db, \
         patch("jules_cli.cli.setup_logging") as mock_setup_logging, \
         patch("jules_cli.cli.auto_fix_command") as mock_auto_fix_command, \
         patch("jules_cli.cli.run_task") as mock_run_task, \
         patch("jules_cli.cli.cmd_session_list") as mock_cmd_session_list, \
         patch("jules_cli.cli.cmd_session_show") as mock_cmd_session_show, \
         patch("jules_cli.cli.cmd_history_list") as mock_cmd_history_list, \
         patch("jules_cli.cli.cmd_history_view") as mock_cmd_history_view, \
         patch("jules_cli.cli.cmd_apply") as mock_cmd_apply, \
         patch("jules_cli.cli.cmd_commit_and_push") as mock_cmd_commit_and_push, \
         patch("jules_cli.cli.git_current_branch") as mock_git_current_branch, \
         patch("jules_cli.cli.git_push_branch") as mock_git_push_branch, \
         patch("jules_cli.cli.cmd_create_pr") as mock_cmd_create_pr, \
         patch("jules_cli.cli.cmd_stage") as mock_cmd_stage, \
         patch("jules_cli.cli.run_doctor_command") as mock_run_doctor_command, \
         patch("jules_cli.cli.add_history_record") as mock_add_history_record, \
         patch("jules_cli.cli.print_json") as mock_print_json:
        yield {
            "mock_check_env": mock_check_env,
            "mock_init_db": mock_init_db,
            "mock_setup_logging": mock_setup_logging,
            "mock_auto_fix_command": mock_auto_fix_command,
            "mock_run_task": mock_run_task,
            "mock_cmd_session_list": mock_cmd_session_list,
            "mock_cmd_session_show": mock_cmd_session_show,
            "mock_cmd_history_list": mock_cmd_history_list,
            "mock_cmd_history_view": mock_cmd_history_view,
            "mock_cmd_apply": mock_cmd_apply,
            "mock_cmd_commit_and_push": mock_cmd_commit_and_push,
            "mock_git_current_branch": mock_git_current_branch,
            "mock_git_push_branch": mock_git_push_branch,
            "mock_cmd_create_pr": mock_cmd_create_pr,
            "mock_cmd_stage": mock_cmd_stage,
            "mock_run_doctor_command": mock_run_doctor_command,
            "mock_add_history_record": mock_add_history_record,
            "mock_print_json": mock_print_json,
        }

def test_main_debug_verbose_no_color_options(mock_dependencies):
    result = runner.invoke(app, ["--debug", "--verbose", "--no-color", "doctor"])
    assert result.exit_code == 0
    mock_dependencies["mock_setup_logging"].assert_called_with(level="DEBUG", color=False)

def test_main_json_pretty_options(mock_dependencies):
    mock_dependencies["mock_run_doctor_command"].return_value = {"status": "ok"}
    result = runner.invoke(app, ["--json", "--pretty", "doctor"])
    assert result.exit_code == 0
    mock_dependencies["mock_print_json"].assert_called_once_with({"status": "ok"}, pretty=True)

# @pytest.mark.xfail(reason="ValueError: I/O operation on closed file. in CliRunner")
# def test_main_jules_error_during_check_env(mock_dependencies, caplog):
#     mock_dependencies["mock_check_env"].side_effect = JulesError("Env check failed")
#     result = runner.invoke(app, ["auto"], catch_exceptions=False)
#     assert result.exit_code == 1
#     assert "Env check failed" in caplog.text

# @pytest.mark.xfail(reason="ValueError: I/O operation on closed file. in CliRunner")
# def test_main_exception_during_init_db(mock_dependencies, caplog):
#     mock_dependencies["mock_init_db"].side_effect = Exception("DB init failed")
#     result = runner.invoke(app, ["auto"], catch_exceptions=False)
#     assert result.exit_code == 1
#     assert "Failed to initialize database: DB init failed" in caplog.text

def test_auto_command_json_output(mock_dependencies):
    mock_dependencies["mock_auto_fix_command"].return_value = {"status": "fixed"}
    result = runner.invoke(app, ["--json", "auto"])
    assert result.exit_code == 0
    mock_dependencies["mock_print_json"].assert_called_once_with({"status": "fixed"}, pretty=False)

def test_task_command_json_output_and_history(mock_dependencies):
    mock_dependencies["mock_run_task"].return_value = {"result": "task_done"}
    result = runner.invoke(app, ["--json", "task", "test prompt"])
    assert result.exit_code == 0
    mock_dependencies["mock_run_task"].assert_called_once_with("test prompt")
    mock_dependencies["mock_add_history_record"].assert_called_once()
    mock_dependencies["mock_print_json"].assert_called_once_with({"result": "task_done"}, pretty=False)

def test_session_list_command_json_output(mock_dependencies):
    mock_dependencies["mock_cmd_session_list"].return_value = {"sessions": []}
    result = runner.invoke(app, ["--json", "session", "list"])
    assert result.exit_code == 0
    mock_dependencies["mock_print_json"].assert_called_once_with({"sessions": []}, pretty=False)

def test_session_show_command_json_output(mock_dependencies):
    mock_dependencies["mock_cmd_session_show"].return_value = {"session_id": "123"}
    result = runner.invoke(app, ["--json", "session", "show", "123"])
    assert result.exit_code == 0
    mock_dependencies["mock_print_json"].assert_called_once_with({"session_id": "123"}, pretty=False)

def test_history_list_command_json_output(mock_dependencies):
    mock_dependencies["mock_cmd_history_list"].return_value = {"history": []}
    result = runner.invoke(app, ["--json", "history", "list"])
    assert result.exit_code == 0
    mock_dependencies["mock_print_json"].assert_called_once_with({"history": []}, pretty=False)

def test_history_view_command_json_output(mock_dependencies):
    mock_dependencies["mock_cmd_history_view"].return_value = {"history_item": {}}
    result = runner.invoke(app, ["--json", "history", "view", "abc"])
    assert result.exit_code == 0
    mock_dependencies["mock_print_json"].assert_called_once_with({"history_item": {}}, pretty=False)

def test_apply_command_json_output_and_history(mock_dependencies):
    mock_dependencies["mock_cmd_apply"].return_value = {"status": "applied"}
    with patch("jules_cli.cli._state", {"session_id": "test_session", "last_patch": "test_patch"}):
        result = runner.invoke(app, ["--json", "apply"])
        assert result.exit_code == 0
        mock_dependencies["mock_add_history_record"].assert_called_once_with(
            session_id="test_session", patch="test_patch", status="patched"
        )
        mock_dependencies["mock_print_json"].assert_called_once_with({"status": "applied"}, pretty=False)

def test_commit_command_json_output(mock_dependencies):
    mock_dependencies["mock_cmd_commit_and_push"].return_value = {"status": "committed"}
    result = runner.invoke(app, ["--json", "commit"])
    assert result.exit_code == 0
    mock_dependencies["mock_print_json"].assert_called_once_with({"status": "committed"}, pretty=False)

def test_push_command_json_output(mock_dependencies):
    mock_dependencies["mock_git_current_branch"].return_value = "main"
    mock_dependencies["mock_git_push_branch"].return_value = {"status": "pushed"}
    result = runner.invoke(app, ["--json", "push"])
    assert result.exit_code == 0
    mock_dependencies["mock_print_json"].assert_called_once_with({"status": "pushed"}, pretty=False)

def test_pr_create_command_json_output_and_history(mock_dependencies):
    mock_dependencies["mock_cmd_create_pr"].return_value = "http://pr_url"
    with patch("jules_cli.cli._state", {"session_id": "test_session"}):
        result = runner.invoke(app, ["--json", "pr", "create"])
        assert result.exit_code == 0
        mock_dependencies["mock_add_history_record"].assert_called_once_with(
            session_id="test_session", pr_url="http://pr_url", status="pr_created"
        )
        mock_dependencies["mock_print_json"].assert_called_once_with({"pr_url": "http://pr_url"}, pretty=False)

def test_stage_command_json_output(mock_dependencies):
    mock_dependencies["mock_cmd_stage"].return_value = {"status": "staged"}
    result = runner.invoke(app, ["--json", "stage"])
    assert result.exit_code == 0
    mock_dependencies["mock_print_json"].assert_called_once_with({"status": "staged"}, pretty=False)

def test_doctor_command_json_output(mock_dependencies):
    mock_dependencies["mock_run_doctor_command"].return_value = {"status": "healthy"}
    result = runner.invoke(app, ["--json", "doctor"])
    assert result.exit_code == 0
    mock_dependencies["mock_print_json"].assert_called_once_with({"status": "healthy"}, pretty=False)

def test_main_use_color_true(mock_dependencies):
    with patch("jules_cli.cli.config") as mock_config:
        mock_config.get.side_effect = lambda key, default: "auto" if key == "color_mode" else default
        result = runner.invoke(app, ["doctor"])
        assert result.exit_code == 0
        mock_dependencies["mock_setup_logging"].assert_called_with(level="INFO", color=True)
