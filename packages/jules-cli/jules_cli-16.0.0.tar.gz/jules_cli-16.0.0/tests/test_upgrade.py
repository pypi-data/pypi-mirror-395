from unittest.mock import MagicMock, patch
import sys
import pytest
from typer.testing import CliRunner
from jules_cli.cli import app
from jules_cli.commands import upgrade

runner = CliRunner()

@pytest.fixture(autouse=True)
def mock_logger():
    """Mock the logger to prevent I/O on closed files."""
    with patch("jules_cli.cli.logger") as mock1, \
         patch("jules_cli.utils.logging.logger") as mock2, \
         patch("jules_cli.commands.upgrade.logger") as mock3:
        yield mock1

@pytest.fixture
def mock_get():
    with patch("requests.get") as mock:
        yield mock

@pytest.fixture
def mock_version():
    with patch("importlib.metadata.version") as mock:
        yield mock

@pytest.fixture
def mock_check_call():
    with patch("subprocess.check_call") as mock:
        yield mock

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.setup_logging")
def test_upgrade_no_update(mock_setup_logging, mock_init_db, mock_check_env, mock_get, mock_version, mock_check_call):
    # Mock current version
    mock_version.return_value = "1.0.0"

    # Mock PyPI response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"info": {"version": "1.0.0"}}
    mock_get.return_value = mock_response

    result = runner.invoke(app, ["upgrade"])

    assert result.exit_code == 0
    assert "You are using the latest version" in result.stdout
    mock_check_call.assert_not_called()

@patch("jules_cli.cli.check_env")
@patch("jules_cli.cli.init_db")
@patch("jules_cli.cli.setup_logging")
def test_upgrade_available(mock_setup_logging, mock_init_db, mock_check_env, mock_get, mock_version, mock_check_call):
    # Mock current version
    mock_version.return_value = "1.0.0"

    # Mock PyPI response with newer version
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"info": {"version": "2.0.0"}}
    mock_get.return_value = mock_response

    # Mock user input to confirm upgrade (if we add confirmation later)
    # For now, let's assume it proceeds or we can pass -y if implemented.
    # The prompt didn't specify interaction, so let's assume auto or simple.

    result = runner.invoke(app, ["upgrade"])

    assert result.exit_code == 0
    assert "New version available: 2.0.0" in result.stdout
    assert "Upgrading jules-cli..." in result.stdout
    mock_check_call.assert_called_with(
        [sys.executable, "-m", "pip", "install", "--upgrade", "jules-cli"]
    )
