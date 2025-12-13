# tests/test_cli_coverage.py

import pytest
from typer.testing import CliRunner
from jules_cli.cli import app
from unittest.mock import patch, MagicMock
from typer import Exit
from jules_cli.utils.exceptions import JulesError

runner = CliRunner()

@pytest.fixture(autouse=True)
def mock_logger():
    """Mock the logger to prevent I/O on closed files."""
    with patch("jules_cli.cli.logger") as mock1, \
         patch("jules_cli.utils.logging.logger") as mock2:
        yield mock1

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
def test_cli_base_help(mock_init, mock_check, mock_logger):
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Jules Interactive CLI" in result.stdout

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
def test_cli_invalid_command(mock_init, mock_check, mock_logger):
    result = runner.invoke(app, ["invalid-cmd"])
    assert result.exit_code == 2
    assert "No such command" in result.stdout or "No such command" in result.stderr

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
def test_cli_check_env_failure(mock_init, mock_check, mock_logger):
    # Simulate check_env failing with JulesError
    mock_check.side_effect = JulesError("Env check failed")

    result = runner.invoke(app, ["auto"])
    assert result.exit_code == 1
    # logger.error is called
    mock_logger.error.assert_called()

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
def test_cli_init_db_failure(mock_init, mock_check, mock_logger):
    mock_init.side_effect = Exception("DB init failed")
    result = runner.invoke(app, ["auto"])
    assert result.exit_code == 1
    mock_logger.error.assert_called()
    args, _ = mock_logger.error.call_args
    assert "Failed to initialize database" in args[0]

# @pytest.mark.xfail(reason="ValueError: I/O operation on closed file with CliRunner")
# @patch("jules_cli.cli.check_env")
# @patch("jules_cli.cli.init_db")
# @patch("jules_cli.cli.setup_logging")
# @patch("jules_cli.commands.auto.run_pytest")
# def test_cli_verbose(mock_run_pytest, mock_setup_logging, mock_init, mock_check, mock_logger):
#     mock_run_pytest.return_value = (0, "ok", "")
#     result = runner.invoke(app, ["--verbose", "auto"])
#     mock_setup_logging.assert_called_with(level="VERBOSE", color=True)

# @pytest.mark.xfail(reason="ValueError: I/O operation on closed file with CliRunner")
# @patch("jules_cli.cli.check_env")
# @patch("jules_cli.cli.init_db")
# @patch("jules_cli.cli.setup_logging")
# @patch("jules_cli.commands.auto.run_pytest")
# def test_cli_debug(mock_run_pytest, mock_setup_logging, mock_init, mock_check, mock_logger):
#     mock_run_pytest.return_value = (0, "ok", "")
#     result = runner.invoke(app, ["--debug", "auto"])
#     mock_setup_logging.assert_called_with(level="DEBUG", color=True)

# @pytest.mark.xfail(reason="ValueError: I/O operation on closed file with CliRunner")
# @patch("jules_cli.cli.check_env")
# @patch("jules_cli.cli.init_db")
# @patch("jules_cli.cli.setup_logging")
# @patch("jules_cli.commands.auto.run_pytest")
# def test_cli_no_color(mock_run_pytest, mock_setup_logging, mock_init, mock_check, mock_logger):
#     mock_run_pytest.return_value = (0, "ok", "")
#     result = runner.invoke(app, ["--no-color", "auto"])
#     mock_setup_logging.assert_called_with(level="INFO", color=False)
