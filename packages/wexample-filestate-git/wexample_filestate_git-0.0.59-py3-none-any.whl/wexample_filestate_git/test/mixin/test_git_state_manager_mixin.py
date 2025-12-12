from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_config.options_provider.abstract_options_provider import (
        AbstractOptionsProvider,
    )


class TestGitFileStateManagerMixin:
    _env_patcher = None

    def _get_git_dir_path(self, item_name: str) -> Path:
        """Get the path to the .git directory for a given item."""
        from wexample_helpers.const.globals import DIR_GIT

        return (
            f"{self.state_manager.find_by_name_or_fail(item_name).get_path()}/{DIR_GIT}"
        )

    def _get_test_options_providers(
        self,
    ) -> list[type[AbstractOptionsProvider]] | None:
        from wexample_filestate.options_provider.default_options_provider import (
            DefaultOptionsProvider,
        )

        from wexample_filestate_git.options_provider.git_options_provider import (
            GitOptionsProvider,
        )

        return [DefaultOptionsProvider, GitOptionsProvider]

    def _mock_git_env(self) -> None:
        """Mock Git-related environment variables."""
        from unittest.mock import patch

        mock_env = {
            "GITHUB_API_TOKEN": "mock-token-123",
            "GITLAB_API_TOKEN": "mock-token-456",
            "GITHUB_DEFAULT_URL": "https://api.github.test",
            "GITLAB_DEFAULT_URL": "https://gitlab.test/api/v4",
        }

        self._env_patcher = patch.dict(os.environ, mock_env)
        self._env_patcher.start()

    def _remove_test_git_dir(self) -> None:
        from wexample_helpers.helpers.directory import directory_remove_tree_if_exists

        directory_remove_tree_if_exists(
            self._get_absolute_path_from_state_manager("test_git_dir/.git")
        )
