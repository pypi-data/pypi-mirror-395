from __future__ import annotations

import re

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from .abstract_remote import AbstractRemote


@base_class
class GithubRemote(AbstractRemote):
    api_token: str = public_field(description="GitHub API token")
    base_url: str = public_field(
        default="https://api.github.com", description="GitHub API base URL"
    )

    def __attrs_post_init__(self) -> None:
        self.default_headers.update(
            {
                "Authorization": f"token {self.api_token}",
                "Accept": "application/vnd.github.v3+json",
            }
        )

    @classmethod
    def build_remote_api_url_from_repo(cls, remote_url: str) -> str | None:
        """Build API base URL from a GitHub remote URL.

        Supports:
        - https://github.com/owner/repo(.git)
        - git@github.com:owner/repo(.git)
        - GHES custom domains: https://github.example.com/... or git@github.example.com:...
        Returns the appropriate https://<host>/api/v3 for custom domains,
        or https://api.github.com for github.com.
        """
        m = re.search(r"^(?:https://|git@)([^/:]+)", remote_url)
        if not m:
            return None
        host = m.group(1)
        if host == "github.com":
            return "https://api.github.com"
        # GitHub Enterprise Server
        return f"https://{host}/api/v3"

    @classmethod
    def detect_remote_type(cls, remote_url: str) -> bool:
        return bool(re.search(r"github\.com[:/]", remote_url))

    @classmethod
    def is_github_repo(cls, remote_url: str) -> bool:
        """Return True if the URL is a GitHub remote (SSH or HTTPS)."""
        return bool(re.search(r"github\.com[:/]", remote_url))

    @classmethod
    def resolve_url_from_repo_url(cls, remote_url: str) -> str | None:
        """
        Normalize any GitHub remote URL into a clean HTTPS repository URL:
        - git@github.com:owner/repo.git → https://github.com/owner/repo
        - https://github.com/owner/repo.git → https://github.com/owner/repo
        """
        if not cls.is_github_repo(remote_url):
            return None

        # Extract user & repo
        m = re.search(r"github\.com[:/](.+?)(?:\.git)?$", remote_url)
        if not m:
            return None

        path = m.group(1)
        return f"https://github.com/{path}"

    def check_repository_exists(self, name: str, namespace: str) -> bool:
        """
        Check if a repository exists in the specified namespace.

        Args:
            name: Repository name
            namespace: Organization or user name (mandatory)
        """
        endpoint = f"repos/{namespace}/{name}"
        response = self.make_request(
            endpoint=endpoint,
            call_origin=__file__,
            expected_status_codes=[200, 404],
            fatal_if_unexpected=True,
        )
        return response.status_code == 200

    def create_repository(
        self, name: str, namespace: str, description: str = "", private: bool = False
    ) -> dict:
        """
        Create a new repository in the specified namespace.

        Args:
            name: Repository name
            namespace: Organization or user name (mandatory)
            description: Optional repository description
            private: Whether the repository should be private
        """
        from wexample_api.enums.http import HttpMethod

        endpoint = f"orgs/{namespace}/repos"

        response = self.make_request(
            method=HttpMethod.POST,
            endpoint=endpoint,
            data={
                "name": name,
                "description": description,
                "private": private,
                "auto_init": True,
            },
            call_origin=__file__,
            expected_status_codes=[201],  # Only 201 Created is acceptable
            fatal_if_unexpected=True,  # Any other status code should raise an error
        )
        return response.json()

    def create_repository_if_not_exists(
        self, remote_url: str, description: str = "", private: bool = False
    ) -> dict:
        """
        Create a repository from a complete remote URL if it doesn't exist.

        Args:
            remote_url: Complete GitHub repository URL
            description: Optional repository description
            private: Whether the repository should be private
        """
        repo_info = self.parse_repository_url(remote_url)

        if not self.check_repository_exists(repo_info["name"], repo_info["namespace"]):
            return self.create_repository(
                name=repo_info["name"],
                namespace=repo_info["namespace"],
                description=description,
                private=private,
            )
        return {}

    def parse_repository_url(self, remote_url: str) -> dict[str, str]:
        """
        Parse a GitHub repository URL to extract repository information.
        Supports both HTTPS and SSH URLs:
        - https://github.com/owner/repo.git
        - git@github.com:owner/repo.git
        """
        # Remove protocol and domain
        path = re.sub(r"^(https://github\.com/|git@github\.com:)", "", remote_url)
        # Remove .git suffix if present
        path = path.replace(".git", "")

        parts = path.split("/")
        if len(parts) >= 2:
            return {"name": parts[-1], "namespace": parts[-2]}
        return {"name": parts[0], "namespace": ""}
