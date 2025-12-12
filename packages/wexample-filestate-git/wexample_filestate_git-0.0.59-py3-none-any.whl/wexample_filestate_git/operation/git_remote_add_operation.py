from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate_git.operation.abstract_git_operation import AbstractGitOperation

if TYPE_CHECKING:
    from git import Repo


@base_class
class GitRemoteAddOperation(AbstractGitOperation):
    _created_remote: dict[str, bool]

    def __init__(
        self, option, target, remotes: list[dict], description="Add Git remotes"
    ) -> None:
        super().__init__(option=option, target=target, description=description)
        self.remotes = remotes  # List of {"name": str, "url": str}
        self._created_remote = {}

    def apply_operation(self) -> None:
        """Add configured remotes to the Git repository."""
        from wexample_helpers_git.helpers.git import git_remote_create_once

        repo = self._get_target_git_repo()
        if not repo:
            return

        for remote in self.remotes:
            remote_name = remote["name"]
            remote_url = remote["url"]

            self._created_remote[remote_name] = (
                git_remote_create_once(repo, remote_name, remote_url) is not None
            )

    def undo(self) -> None:
        """Remove remotes that were created by this operation."""
        if not self._created_remote:
            return

        repo = self._get_target_git_repo()
        if not repo:
            return

        for remote_name, was_created in self._created_remote.items():
            if was_created:
                try:
                    repo.delete_remote(remote=repo.remote(name=remote_name))
                except Exception:
                    # Remote might already be deleted or not exist
                    pass

    def _get_target_git_repo(self) -> Repo:
        from git import Repo

        return Repo(self.target.get_path())

    def _remotes_description(self) -> str:
        """Generate description for this remote add operation."""
        parts: list[str] = []
        for remote in self.remotes:
            name = remote.get("name")
            url = remote.get("url")
            if name and url:
                parts.append(f"{name} -> {url}")
            elif name:
                parts.append(str(name))
            elif url:
                parts.append(str(url))
        return ", ".join(parts)
