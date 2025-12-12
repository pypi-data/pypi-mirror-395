from __future__ import annotations

from wexample_filestate_git.testing.abstract_git_option_test import (
    AbstractGitOptionTest,
)


class TestGitOptionExistingDirectory(AbstractGitOptionTest):
    """Test GitOption on existing directory."""

    git_config: bool = True
    test_dir_name: str = "test_git_dir"
