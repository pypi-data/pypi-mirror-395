from unittest.mock import MagicMock, patch
from typer.testing import CliRunner
from jules_cli.cli import app

runner = CliRunner()

@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.setup_logging")
def test_tui_command_exists(mock_setup_logging, mock_check_env, mock_init_db):
    """Test that the 'jules tui' command exists and is registered."""
    result = runner.invoke(app, ["tui", "--help"])
    assert result.exit_code == 0
    assert "Launch the Jules TUI" in result.stdout or "tui" in result.stdout

@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.setup_logging")
@patch("jules_cli.cli.JulesTui")
def test_tui_command_execution(mock_app_class, mock_setup_logging, mock_check_env, mock_init_db):
    """Test that invoking 'jules tui' runs the Textual app."""
    # Setup mock
    mock_app_instance = MagicMock()
    mock_app_class.return_value = mock_app_instance

    # Run command
    result = runner.invoke(app, ["tui"])

    # Assert
    assert result.exit_code == 0
    mock_app_class.assert_called_once()
    mock_app_instance.run.assert_called_once()
