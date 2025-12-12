from __future__ import annotations

import pytest

from wexample_filestate_git.remote.github_remote import GithubRemote
from wexample_filestate_git.testing.abstract_git_remote_test import (
    AbstractGitRemoteTest,
)


class TestGithubRemote(AbstractGitRemoteTest):
    """Test cases for GitHub remote operations."""

    ENV_TOKEN_NAME = "GITHUB_API_TOKEN"
    SERVICE_CLASS = GithubRemote

    @pytest.fixture
    def remote(self) -> GithubRemote:
        pass

        from wexample_prompt.common.io_manager import IoManager

        io_manager = IoManager()
        remote = GithubRemote(io=io_manager, api_token="test_token")
        return remote

    def test_check_repository_exists(self, remote) -> None:
        from unittest.mock import patch

        with patch(
            "wexample_api.common.abstract_gateway.AbstractGateway.make_request"
        ) as mock_request:
            mock_request.return_value.status_code = 200

            exists = remote.check_repository_exists("test-repo", "test-namespace")

            mock_request.assert_called_once()
            self._assert_check_repository_exists_request(mock_request)
            assert exists is True

    def test_create_repository(self, remote) -> None:
        from unittest.mock import patch

        with patch(
            "wexample_api.common.abstract_gateway.AbstractGateway.make_request"
        ) as mock_request:
            mock_request.return_value.json.return_value = {"id": 1}

            result = remote.create_repository(
                name="test-repo",
                namespace="test-namespace",
                description="Test description",
                private=True,
            )

            mock_request.assert_called_once()
            self._assert_create_repository_request(mock_request)
            assert result == {"id": 1}

    def test_parse_repository_url_https(self, remote) -> None:
        url = "https://github.com/test-namespace/test-repo.git"
        info = remote.parse_repository_url(url)
        assert info == {"name": "test-repo", "namespace": "test-namespace"}

    def test_parse_repository_url_ssh(self, remote) -> None:
        url = "git@github.com:test-namespace/test-repo.git"
        info = remote.parse_repository_url(url)
        assert info == {"name": "test-repo", "namespace": "test-namespace"}

    def _assert_check_repository_exists_request(self, mock_request) -> None:
        """Assert the request parameters for checking repository existence."""
        assert (
            mock_request.call_args[1]["endpoint"]
            == f"repos/{self.test_namespace}/{self.test_repo_name}"
        )

    def _assert_create_repository_request(self, mock_request) -> None:
        """Assert the request parameters for creating a repository."""
        assert (
            mock_request.call_args[1]["endpoint"] == f"orgs/{self.test_namespace}/repos"
        )
        assert mock_request.call_args[1]["data"]["name"] == self.test_repo_name
