from __future__ import annotations

from wexample_api.common.abstract_gateway import AbstractGateway
from wexample_helpers.classes.abstract_method import abstract_method


class AbstractRemote(AbstractGateway):
    """
    Abstract base class for Git repository hosting services (GitHub, GitLab, etc.).
    Provides a common interface for interacting with remote repositories.
    """

    @classmethod
    @abstract_method
    def build_remote_api_url_from_repo(cls, remote_url: str) -> str | None:
        """Derive the REST API base URL from a git remote URL.

        Implementations should support both SSH and HTTPS remotes and custom domains.
        Return None to use the class default base_url.
        """

    @classmethod
    @abstract_method
    def detect_remote_type(cls, remote_url: str) -> bool:
        """
        Detect if a remote URL corresponds to this service.

        Args:
            remote_url: Git remote URL to check

        Returns:
            bool: True if the URL matches this service's pattern
        """

    @classmethod
    def get_class_name_suffix(cls) -> str | None:
        return "Remote"

    @abstract_method
    def check_repository_exists(self, name: str, namespace: str) -> bool:
        """
        Check if a repository exists on the remote service.

        Args:
            name: Repository name
            namespace: Repository namespace/organization (mandatory)

        Returns:
            bool: True if the repository exists
        """

    @abstract_method
    def create_repository(
        self, name: str, namespace: str, description: str = "", private: bool = False
    ) -> dict:
        """
        Create a new repository on the remote service.

        Args:
            name: Repository name
            namespace: Repository namespace/organization (mandatory)
            description: Repository description
            private: Whether the repository should be private

        Returns:
            Dict: Repository information from the API
        """

    @abstract_method
    def create_repository_if_not_exists(
        self, remote_url: str, description: str = "", private: bool = False
    ) -> dict:
        """
        Create a repository from a complete remote URL if it doesn't exist.

        Args:
            remote_url: Complete remote repository URL
            description: Optional repository description
            private: Whether the repository should be private

        Returns:
            Dict: Repository information from the API if created, empty dict if already exists
        """

    @abstract_method
    def parse_repository_url(self, remote_url: str) -> dict[str, str]:
        """
        Parse a repository URL to extract repository information.

        Args:
            remote_url: Git remote URL to parse

        Returns:
            Dict with keys:
                - name: Repository name (without .git)
                - namespace: Repository namespace/organization (optional)
        """
