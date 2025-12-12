from __future__ import annotations


class AbstractGitRemoteTest:
    """Base class for Git remote service tests."""

    # Service specific attributes to be overridden by child classes
    ENV_TOKEN_NAME = None
    SERVICE_CLASS = None
    TEST_TOKEN = "test_token"

    @property
    def test_description(self) -> str:
        """Return the test repository description."""
        return "Test description"

    @property
    def test_namespace(self) -> str:
        """Return the test namespace."""
        return "test-namespace"

    @property
    def test_repo_name(self) -> str:
        """Return the test repository name."""
        return "test-repo"

    def _assert_check_repository_exists_request(self, mock_request) -> None:
        """Assert the request parameters for checking repository existence.
        To be implemented by child classes."""
        raise NotImplementedError()

    def _assert_create_repository_request(self, mock_request) -> None:
        """Assert the request parameters for creating a repository.
        To be implemented by child classes."""
        raise NotImplementedError()
