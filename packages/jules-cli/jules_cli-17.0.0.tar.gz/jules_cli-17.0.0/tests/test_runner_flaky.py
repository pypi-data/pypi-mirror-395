import unittest
from unittest.mock import patch, MagicMock, call
from jules_cli.testing.runner import run_tests
import os

class TestRunnerFlaky(unittest.TestCase):
    @patch("jules_cli.testing.runner.run_cmd")
    @patch("jules_cli.testing.runner.json.load")
    @patch("jules_cli.testing.runner.open")
    @patch("jules_cli.testing.runner.os.remove")
    @patch("jules_cli.testing.runner.os.path.exists")
    def test_run_pytest_flaky_detection(self, mock_exists, mock_remove, mock_open, mock_json_load, mock_run_cmd):
        # Setup
        mock_exists.return_value = True

        # Scenario:
        # 1. First run fails with one failed test "test_example.py::test_flaky"
        # 2. Retry run passes for that test.

        # Mock run_cmd responses
        # First call: main run -> fails (1)
        # Second call: retry run -> passes (0)
        mock_run_cmd.side_effect = [
            (1, "Tests failed", ""),  # 1st run
            (0, "Tests passed", "")   # 2nd run (retry)
        ]

        # Mock json report content

        # Report 1: Failure
        report1 = {
            "summary": {"passed": 0, "failed": 1, "skipped": 0},
            "tests": [
                {"nodeid": "tests/test_example.py::test_flaky", "outcome": "failed"}
            ]
        }

        # Report 2: Success
        report2 = {
            "summary": {"passed": 1, "failed": 0, "skipped": 0},
            "tests": [
                {"nodeid": "tests/test_example.py::test_flaky", "outcome": "passed"}
            ]
        }

        mock_json_load.side_effect = [report1, report2]

        # Mock context manager for open
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        # ACT
        code, out, err = run_tests(runner="pytest", detect_flaky=True)

        # ASSERT
        # Should return 0 because flaky test passed eventually
        self.assertEqual(code, 0)
        self.assertIn("Flaky tests detected", out)
        self.assertIn("tests/test_example.py::test_flaky", out)

        # Verify run_cmd was called twice
        self.assertEqual(mock_run_cmd.call_count, 2)

        # Verify the second call targeted the specific test
        args, _ = mock_run_cmd.call_args_list[1]
        cmd = args[0]
        self.assertIn("pytest", cmd)
        self.assertIn("tests/test_example.py::test_flaky", cmd)

if __name__ == "__main__":
    unittest.main()
