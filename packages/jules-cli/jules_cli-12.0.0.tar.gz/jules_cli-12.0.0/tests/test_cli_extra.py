# tests/test_cli_extra.py

from unittest.mock import patch
from typer.testing import CliRunner
from jules_cli.cli import app
from jules_cli.utils.exceptions import JulesError

runner = CliRunner()

def test_auto_command():
    with patch('jules_cli.cli.auto_fix_command') as mock_auto_fix_command, \
         patch('jules_cli.cli.check_env'), \
         patch('jules_cli.cli.init_db'):
        result = runner.invoke(app, ["auto"])
        assert result.exit_code == 0
        mock_auto_fix_command.assert_called_once()

def test_session_list_command():
    with patch('jules_cli.cli.cmd_session_list') as mock_cmd_session_list, \
         patch('jules_cli.cli.check_env'), \
         patch('jules_cli.cli.init_db'):
        result = runner.invoke(app, ["session", "list"])
        assert result.exit_code == 0
        mock_cmd_session_list.assert_called_once()

def test_session_show_command():
    with patch('jules_cli.cli.cmd_session_show') as mock_cmd_session_show, \
         patch('jules_cli.cli.check_env'), \
         patch('jules_cli.cli.init_db'):
        result = runner.invoke(app, ["session", "show", "123"])
        assert result.exit_code == 0
        mock_cmd_session_show.assert_called_once_with('123')

def test_commit_command():
    with patch('jules_cli.cli.cmd_commit_and_push') as mock_cmd_commit_and_push, \
         patch('jules_cli.cli.check_env'), \
         patch('jules_cli.cli.init_db'):
        result = runner.invoke(app, ["commit"])
        assert result.exit_code == 0
        mock_cmd_commit_and_push.assert_called_once()

def test_push_command():
    with patch('jules_cli.cli.git_current_branch', return_value='my-branch') as mock_git_current_branch, \
         patch('jules_cli.cli.git_push_branch') as mock_git_push_branch, \
         patch('jules_cli.cli.check_env'), \
         patch('jules_cli.cli.init_db'):
        result = runner.invoke(app, ["push"])
        assert result.exit_code == 0
        mock_git_current_branch.assert_called_once()
        mock_git_push_branch.assert_called_once_with('my-branch')

def test_doctor_command():
    with patch('jules_cli.cli.run_doctor_command') as mock_run_doctor_command, \
         patch('jules_cli.cli.check_env'), \
         patch('jules_cli.cli.init_db'):
        result = runner.invoke(app, ["doctor"])
        assert result.exit_code == 0
        mock_run_doctor_command.assert_called_once()

def test_main_jules_error():
    with patch('jules_cli.cli.check_env', side_effect=JulesError("test error")) as mock_check_env, \
         patch('jules_cli.cli.init_db'), \
         patch('jules_cli.cli.logger') as mock_logger:
        result = runner.invoke(app, ["task", "foo"])
        assert result.exit_code == 1
        mock_check_env.assert_called_once()
        mock_logger.error.assert_called_once()
        assert "test error" in str(mock_logger.error.call_args)
