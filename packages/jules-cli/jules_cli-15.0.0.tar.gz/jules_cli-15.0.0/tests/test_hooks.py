import pytest
import os
from unittest.mock import patch, mock_open
from typer.testing import CliRunner
from jules_cli.cli import app

runner = CliRunner()

def test_hooks_command_exists():
    # This test verifies the command is available in the CLI
    # We need to mock check_env to avoid exit due to missing API key
    with patch("jules_cli.cli.check_env") as mock_check:
        result = runner.invoke(app, ["hooks", "--help"])
        assert result.exit_code == 0
        assert "install" in result.stdout

def test_install_hooks_content():
    # We want to verify the content written to .pre-commit-config.yaml
    m = mock_open()
    with patch("builtins.open", m), patch("os.path.exists", return_value=False):
        from jules_cli.commands.hooks import install_hooks
        install_hooks()

        m.assert_called_with(".pre-commit-config.yaml", "w")
        handle = m()

        # Collect all written content
        written_content = "".join([call.args[0] for call in handle.write.call_args_list])

        assert "repos:" in written_content
        assert "jules-suggest" in written_content # checking for hook id
