import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from jules_cli.cli import app

runner = CliRunner()

def test_completion_options_are_present():
    """
    Test that tab completion options are enabled in the CLI.
    This test is expected to FAIL initially because add_completion is currently False.
    """
    # specific mocks to avoid environment checks and side effects
    with patch("jules_cli.cli.check_env"), \
         patch("jules_cli.cli.init_db"), \
         patch("jules_cli.cli.setup_logging"), \
         patch("jules_cli.cli.load_plugins"):

        result = runner.invoke(app, ["_completion", "bash"])
        result = runner.invoke(app, ["--show-completion", "bash"])
        assert result.exit_code == 0
        assert "complete -o default -F" in result.stdout # A common pattern in bash completion scripts
