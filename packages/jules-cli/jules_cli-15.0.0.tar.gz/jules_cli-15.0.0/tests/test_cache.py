# tests/test_cache.py
import unittest
import os
import json
from pathlib import Path
from jules_cli.cache import load_from_cache, save_to_cache, clear_cache, get_cache_file
from jules_cli.commands.apply import cmd_apply
from jules_cli.state import _state
from unittest.mock import patch

class TestCache(unittest.TestCase):

    def setUp(self):
        self.cache_key = "test_data"
        self.cache_file = get_cache_file(self.cache_key)
        self.test_data = {"key": "value"}
        self.patch_data = {"type": "patch", "patch": "dummy_patch"}
        _state.clear()

    def tearDown(self):
        clear_cache(self.cache_key)
        clear_cache(f"patch_{_state.get('session_id')}")

    def test_save_and_load_from_cache(self):
        # S-a-v-e data to cache
        save_to_cache(self.cache_key, self.test_data)

        # V-e-r-i-f-y that the cache file was created
        self.assertTrue(self.cache_file.exists())

        # L-o-a-d data from cache
        loaded_data = load_from_cache(self.cache_key)

        # V-e-r-i-f-y that the loaded data matches the original data
        self.assertEqual(loaded_data, self.test_data)

    def test_load_from_nonexistent_cache(self):
        # A-t-t-e-m-p-t to load data from a nonexistent cache
        loaded_data = load_from_cache("nonexistent_key")

        # V-e-r-i-f-y that the loaded data is None
        self.assertIsNone(loaded_data)

    def test_clear_cache(self):
        # S-a-v-e data to cache
        save_to_cache(self.cache_key, self.test_data)

        # V-e-r-i-f-y that the cache file was created
        self.assertTrue(self.cache_file.exists())

        # C-l-e-a-r the cache
        clear_cache(self.cache_key)

        # V-e-r-i-f-y that the cache file was deleted
        self.assertFalse(self.cache_file.exists())

    @patch('jules_cli.cache.logger')
    def test_load_from_cache_invalid_json(self, mock_logger):
        # Create a cache file with invalid JSON
        with open(self.cache_file, "w", encoding="utf-8") as f:
            f.write("invalid json")

        # Attempt to load data from the cache
        loaded_data = load_from_cache(self.cache_key)

        # Verify that the loaded data is None and a warning was logged
        self.assertIsNone(loaded_data)
        mock_logger.warning.assert_called_once()
        self.assertIn("Failed to load from cache", mock_logger.warning.call_args[0][0])

    @patch('jules_cli.cache.logger')
    @patch('builtins.open', side_effect=IOError("Test IOError"))
    def test_load_from_cache_io_error(self, mock_open, mock_logger):
        # Create a dummy cache file to ensure open is called
        self.cache_file.touch()

        # Attempt to load data from the cache
        loaded_data = load_from_cache(self.cache_key)

        # Verify that the loaded data is None and a warning was logged
        self.assertIsNone(loaded_data)
        mock_logger.warning.assert_called_once()
        self.assertIn("Failed to load from cache", mock_logger.warning.call_args[0][0])
        self.assertIn("Test IOError", mock_logger.warning.call_args[0][0])

    @patch('jules_cli.cache.logger')
    @patch('builtins.open', side_effect=IOError("Test IOError"))
    def test_save_to_cache_io_error(self, mock_open, mock_logger):
        # Attempt to save data to the cache
        save_to_cache(self.cache_key, self.test_data)

        # Verify that an error was logged
        mock_logger.error.assert_called_once()
        self.assertIn("Failed to save to cache", mock_logger.error.call_args[0][0])
        self.assertIn("Test IOError", mock_logger.error.call_args[0][0])

    @patch('jules_cli.cache.logger')
    @patch('os.remove', side_effect=OSError("Test OSError"))
    def test_clear_cache_os_error(self, mock_os_remove, mock_logger):
        # Create a dummy cache file to ensure os.remove is called
        self.cache_file.touch()

        # Attempt to clear the cache
        clear_cache(self.cache_key)

        # Verify that an error was logged
        mock_logger.error.assert_called_once()
        self.assertIn("Failed to clear cache", mock_logger.error.call_args[0][0])
        self.assertIn("Test OSError", mock_logger.error.call_args[0][0])


    @patch('jules_cli.commands.apply.apply_patch_text')
    def test_patch_caching(self, mock_apply_patch_text):
        # S-e-t up the state for the apply command
        _state["last_result"] = self.patch_data
        _state["session_id"] = "test_session"

        # R-u-n the apply command
        cmd_apply()

        # V-e-r-i-f-y that the patch was cached
        cached_patch = load_from_cache(f"patch_{_state['session_id']}")
        self.assertEqual(cached_patch, {"patch": self.patch_data["patch"]})

if __name__ == '__main__':
    unittest.main()
