import os
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from jules_cli.cli import app

runner = CliRunner()

def test_init_command_creates_config(tmp_path):
    # Mock config path to use tmp_path
    config_path = tmp_path / "config.toml"

    # Mock setup_logging to prevent global state modification
    # Mock logger in the command module to verify calls without stream issues
    with patch("jules_cli.utils.config.DEFAULT_CONFIG_PATH", str(config_path)), \
         patch("jules_cli.utils.config.config.path", str(config_path)), \
         patch("jules_cli.commands.init.cmd_doctor") as mock_doctor, \
         patch("jules_cli.cli.check_env"), \
         patch("jules_cli.cli.init_db"), \
         patch("jules_cli.cli.print_logo"), \
         patch("jules_cli.utils.logging.setup_logging"), \
         patch("jules_cli.commands.init.logger") as mock_logger:

         # Prepare inputs: API Key, Github Token, Default Repo, Default Branch
         inputs = "test-api-key\ntest-github-token\nmy-repo\nmain\n"

         result = runner.invoke(app, ["init"], input=inputs)

         assert result.exit_code == 0
         # assert "Jules Initialization Wizard" in result.stdout # Removed as we mock logger
         
         # Verify logger was called
         mock_logger.info.assert_any_call("Welcome to the Jules CLI Initialization Wizard! 🚀")

         # Verify config file was created/updated
         assert config_path.exists()
         content = config_path.read_text()
         assert 'default_repo = "my-repo"' in content
         assert 'default_branch = "main"' in content
         assert 'jules_api_key = "test-api-key"' in content

         # Verify doctor was called
         mock_doctor.assert_called_once()
