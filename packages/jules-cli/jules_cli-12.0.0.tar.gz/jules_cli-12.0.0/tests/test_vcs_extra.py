# tests/test_vcs_extra.py

from unittest.mock import patch
from jules_cli.git import vcs
from jules_cli.utils.exceptions import GitError

@patch('jules_cli.git.vcs.run_cmd', return_value=(1, "", "error"))
def test_git_create_branch_and_commit_add_error(mock_run_cmd):
    with patch('time.time', return_value=12345):
        try:
            vcs.git_create_branch_and_commit("new-branch")
        except GitError as e:
            assert "Failed to create branch" in str(e)

@patch('jules_cli.git.vcs.run_cmd', side_effect=[(0, "", ""), (1, "", "error")])
def test_git_create_branch_and_commit_commit_error(mock_run_cmd):
    with patch('time.time', return_value=12345):
        try:
            vcs.git_create_branch_and_commit("new-branch")
        except GitError as e:
            assert "Failed to add files" in str(e)

@patch('jules_cli.git.vcs.run_cmd', side_effect=[(0, "", ""), (0, "", ""), (1, "", "error")])
def test_git_create_branch_and_commit_final_error(mock_run_cmd):
    with patch('time.time', return_value=12345):
        try:
            vcs.git_create_branch_and_commit("new-branch")
        except GitError as e:
            assert "Failed to commit changes" in str(e)

@patch('os.getenv', side_effect=lambda key: None if key == "GITHUB_TOKEN" else os.environ.get(key))
def test_github_create_pr_no_token(mock_getenv):
    try:
        vcs.github_create_pr("owner", "repo", "head")
    except GitError as e:
        assert "GITHUB_TOKEN not set" in str(e)
