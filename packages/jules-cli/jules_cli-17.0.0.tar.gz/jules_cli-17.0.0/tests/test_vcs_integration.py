import pytest
from unittest.mock import patch, MagicMock
from jules_cli.git.vcs import git_get_remote_repo_info, gitlab_create_mr, bitbucket_create_pr
from jules_cli.utils.exceptions import GitError

def test_git_get_remote_repo_info_github():
    with patch("jules_cli.git.vcs.run_cmd") as mock_run:
        mock_run.return_value = (0, "https://github.com/owner/repo.git", "")
        owner, repo, platform = git_get_remote_repo_info()
        assert owner == "owner"
        assert repo == "repo"
        assert platform == "github"

def test_git_get_remote_repo_info_gitlab():
    with patch("jules_cli.git.vcs.run_cmd") as mock_run:
        mock_run.return_value = (0, "https://gitlab.com/owner/repo.git", "")
        owner, repo, platform = git_get_remote_repo_info()
        assert owner == "owner"
        assert repo == "repo"
        assert platform == "gitlab"

def test_git_get_remote_repo_info_bitbucket():
    with patch("jules_cli.git.vcs.run_cmd") as mock_run:
        mock_run.return_value = (0, "https://bitbucket.org/owner/repo.git", "")
        owner, repo, platform = git_get_remote_repo_info()
        assert owner == "owner"
        assert repo == "repo"
        assert platform == "bitbucket"

def test_gitlab_create_mr():
    with patch("jules_cli.git.vcs.requests.post") as mock_post, \
         patch("jules_cli.utils.config.config.get_secret", return_value="token"):

        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"web_url": "https://gitlab.com/owner/repo/-/merge_requests/1"}

        result = gitlab_create_mr("owner", "repo", "feature", "main", "Title", "Body")

        assert result["web_url"] == "https://gitlab.com/owner/repo/-/merge_requests/1"
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert kwargs["json"]["source_branch"] == "feature"
        assert kwargs["json"]["target_branch"] == "main"

def test_bitbucket_create_pr():
    with patch("jules_cli.git.vcs.requests.post") as mock_post, \
         patch("jules_cli.utils.config.config.get_secret", return_value="user:app_password"):

        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"links": {"html": {"href": "https://bitbucket.org/owner/repo/pull-requests/1"}}}

        result = bitbucket_create_pr("owner", "repo", "feature", "main", "Title", "Body")

        assert result["links"]["html"]["href"] == "https://bitbucket.org/owner/repo/pull-requests/1"
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert kwargs["json"]["source"]["branch"]["name"] == "feature"
        assert kwargs["json"]["destination"]["branch"]["name"] == "main"
