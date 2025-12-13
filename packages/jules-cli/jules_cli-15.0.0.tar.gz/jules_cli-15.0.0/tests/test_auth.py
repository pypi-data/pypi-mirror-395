from unittest.mock import MagicMock, patch
import pytest
from typer.testing import CliRunner
from jules_cli.cli import app
from jules_cli.utils.config import Config
from jules_cli.utils.logging import logger

runner = CliRunner()

@pytest.fixture
def mock_keyring():
    with patch("jules_cli.commands.auth.keyring") as mock:
        yield mock

@pytest.fixture
def mock_config_get_secret():
    with patch("jules_cli.utils.config.Config.get_secret") as mock:
        yield mock

def test_auth_login(mock_keyring):
    # Simulate user input
    input_str = "test-api-key\ntest-github-token\n"

    # Ensure no previous handlers interfere
    logger.handlers = []

    # Invoke via main app
    result = runner.invoke(app, ["auth", "login"], input=input_str)

    if result.exit_code != 0:
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
        print(f"Exception: {result.exception}")

    assert result.exit_code == 0
    assert "Credentials saved securely" in result.stdout

    # Verify keyring calls
    mock_keyring.set_password.assert_any_call("jules-cli", "JULES_API_KEY", "test-api-key")
    mock_keyring.set_password.assert_any_call("jules-cli", "GITHUB_TOKEN", "test-github-token")

def test_config_get_secret_keyring():
    with patch("jules_cli.utils.config.keyring") as mock_keyring_mod:
        mock_keyring_mod.get_password.return_value = "secret-value"

        # Create a config instance (data doesn't matter for secret retrieval if keyring works)
        cfg = Config({}, "dummy_path")

        # We need to make sure we are not mocking the method we are testing,
        # so we rely on the internal keyring call.

        val = cfg.get_secret("SOME_KEY")
        assert val == "secret-value"
        mock_keyring_mod.get_password.assert_called_with("jules-cli", "SOME_KEY")

def test_config_get_secret_env(monkeypatch):
    with patch("jules_cli.utils.config.keyring") as mock_keyring_mod:
        mock_keyring_mod.get_password.return_value = None

        monkeypatch.setenv("SOME_KEY", "env-value")

        cfg = Config({}, "dummy_path")
        val = cfg.get_secret("SOME_KEY")
        assert val == "env-value"

def test_config_get_secret_config_file():
    with patch("jules_cli.utils.config.keyring") as mock_keyring_mod:
        mock_keyring_mod.get_password.return_value = None

        # Mock env to return None
        with patch.dict("os.environ", {}, clear=True):
            data = {"core": {"some_key": "config-value"}}
            cfg = Config(data, "dummy_path")

            # Map SOME_KEY to core.some_key logic needs to be implemented or
            # we just check if it falls back to checking the config dict directly
            # or we implement specific mapping logic.
            # For now, let's assume we pass a key that might exist in config or we just check fallback.
            # But wait, usually secrets like JULES_API_KEY are not in the main config dict for security,
            # or if they are, they are under a specific section.
            # Let's assume get_secret might look up in "core" if the key is "jules_api_key".

            # Let's simplify and say get_secret is generic.
            # If I ask for JULES_API_KEY, it might check os.environ["JULES_API_KEY"]
            # then keyring
            # then config.get("core", {}).get("jules_api_key")

            # For this test, let's assume we want to support fallback to config file (legacy)
            cfg.data = {"secrets": {"SOME_KEY": "config-value"}}
            val = cfg.get_secret("SOME_KEY")
            assert val == "config-value"
