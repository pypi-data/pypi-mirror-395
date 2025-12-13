# tests/test_conflict_resolver.py
import unittest
from unittest.mock import patch, MagicMock
from jules_cli.patch.apply import apply_patch_text, extract_rejected_hunks
from jules_cli.utils.exceptions import PatchError

class TestConflictResolver(unittest.TestCase):

    def test_extract_rejected_hunks(self):
        patch_output = """
        Hunk #1 FAILED at 1.
         - old line
         + new line
        Hunk #2 FAILED at 10.
         - another old line
         + another new line
        """
        rejected_hunks = extract_rejected_hunks(patch_output)
        self.assertEqual(rejected_hunks, "- old line\n+ new line\n- another old line\n+ another new line")

    @patch('jules_cli.patch.apply.run_cmd')
    def test_successful_patch_application(self, mock_run_cmd):
        # Mock successful patch application
        mock_run_cmd.return_value = (0, "Success", "")

        apply_patch_text("dummy_patch_text")

        # Verify that run_cmd was called once
        mock_run_cmd.assert_called_once()

    @patch('jules_cli.patch.resolver.anthropic.Anthropic')
    @patch('jules_cli.patch.apply.run_cmd')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('os.remove')
    @patch('os.path.exists')
    def test_failed_patch_application_with_successful_ai_resolution(self, mock_exists, mock_remove, mock_open, mock_run_cmd, mock_anthropic):
        # Mock failed patch application followed by successful AI resolution
        # We need to simulate the patch output containing the filename being patched
        # patch usually prints "patching file X" to stdout, and Hunk failures to stdout or stderr.
        # Let's put the filename in stdout (out) and the hunks in stderr (err) or both in out/err depending on implementation.
        # My implementation searches `out` for "patching file".

        stdout_output = "patching file target_file.py\n"
        stderr_output = "Hunk #1 FAILED at 1.\n - old line\n + new line"

        mock_run_cmd.side_effect = [(1, stdout_output, stderr_output), (0, "Success", "")]
        mock_anthropic.return_value.messages.create.return_value.content = [MagicMock(text="resolved_patch_text")]

        # Mock file reading for the target file
        file_mock = MagicMock()
        file_mock.read.return_value = "original file content"

        # Configure open mock to return file_mock when opening target_file.py
        # We need side_effect to handle different files
        def open_side_effect(filename, mode='r', encoding=None):
            if filename == "target_file.py":
                return file_mock
            return MagicMock() # Return a dummy mock for other files (like tmp_patch.diff)

        mock_open.side_effect = open_side_effect
        # We also need __enter__ return value for the context manager
        file_mock.__enter__.return_value = file_mock

        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test_key'}):
            apply_patch_text("dummy_patch_text")

        # Verify that run_cmd was called twice and the AI service was called once with the rejected hunk AND file content
        self.assertEqual(mock_run_cmd.call_count, 2)

        # Check if the prompt includes the file content
        call_args = mock_anthropic.return_value.messages.create.call_args
        content_sent = call_args[1]['messages'][0]['content']

        self.assertIn("original file content", content_sent)
        self.assertIn("- old line\n+ new line", content_sent)

    @patch('jules_cli.patch.apply.logger')
    @patch('jules_cli.patch.resolver.anthropic.Anthropic')
    @patch('jules_cli.patch.apply.run_cmd')
    def test_failed_patch_application_with_failed_ai_resolution(self, mock_run_cmd, mock_anthropic, mock_logger):
        # Mock failed patch application followed by failed AI resolution
        mock_run_cmd.return_value = (1, "Error", "Hunk #1 FAILED at 1.\n - old line\n + new line")
        mock_anthropic.return_value.messages.create.side_effect = Exception("AI error")

        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test_key'}):
            with self.assertRaises(PatchError) as context:
                apply_patch_text("dummy_patch_text")

        self.assertEqual(str(context.exception), "patch failed and AI could not resolve it")

        # Verify that the fallback strategies were logged
        mock_logger.info.assert_any_call("Fallback strategies:")
        mock_logger.info.assert_any_call("1. Manually resolve the conflicts in the rejected patch file.")
        mock_logger.info.assert_any_call("2. Apply the patch with a different tool, such as `git apply`.")
        mock_logger.info.assert_any_call("3. Discard the patch and start over.")

    @patch('jules_cli.patch.resolver.anthropic.Anthropic')
    @patch('jules_cli.patch.apply.run_cmd')
    def test_failed_patch_application_and_reapplication(self, mock_run_cmd, mock_anthropic):
        # Mock failed patch application, successful AI resolution, but failed re-application
        mock_run_cmd.side_effect = [(1, "Error", "Hunk #1 FAILED at 1.\n - old line\n + new line"), (1, "Error", "Re-application failed")]
        mock_anthropic.return_value.messages.create.return_value.content = [MagicMock(text="resolved_patch_text")]

        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test_key'}):
            with self.assertRaises(PatchError) as context:
                apply_patch_text("dummy_patch_text")

        self.assertEqual(str(context.exception), "patch failed after AI resolution")

        # Verify that run_cmd was called twice and the AI service was called once with the rejected hunk
        self.assertEqual(mock_run_cmd.call_count, 2)
        mock_anthropic.return_value.messages.create.assert_called_once_with(
            model="claude-2.1",
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": "The following patch failed to apply. Please resolve the conflicts and return a conflict-free patch.\n\n- old line\n+ new line",
                }
            ],
        )

if __name__ == '__main__':
    unittest.main()
