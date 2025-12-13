# tests/test_plugins.py
import unittest
from unittest.mock import patch, MagicMock
import typer
from typer.testing import CliRunner
from jules_cli.cli import app, load_plugins
from importlib import metadata

runner = CliRunner()

class TestPlugins(unittest.TestCase):

    @patch('jules_cli.cli.init_db')
    @patch('jules_cli.cli.check_env')
    def test_plugin_loading(self, mock_check_env, mock_init_db):
        # C-r-e-a-t-e a dummy plugin
        dummy_app = typer.Typer(name="dummy")
        @dummy_app.command()
        def hello():
            print("Hello from dummy plugin!")

        # M-o-c-k importlib.metadata.entry_points to return the dummy plugin
        mock_entry_point = MagicMock(spec=metadata.EntryPoint)
        mock_entry_point.name = "dummy"
        mock_entry_point.load.return_value = dummy_app

        with patch("importlib.metadata.entry_points", return_value=[mock_entry_point]):
            load_plugins()

        # I-n-v-o-k-e the dummy command and verify the output
        result = runner.invoke(app, ["dummy", "hello"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Hello from dummy plugin!", result.stdout)

if __name__ == "__main__":
    unittest.main()
