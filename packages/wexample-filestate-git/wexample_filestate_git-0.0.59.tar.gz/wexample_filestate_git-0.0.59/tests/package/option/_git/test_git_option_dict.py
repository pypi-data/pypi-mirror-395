from __future__ import annotations

from wexample_filestate_git.testing.abstract_git_option_test import (
    AbstractGitOptionTest,
)


class TestGitOptionDict(AbstractGitOptionTest):
    """Test GitOption with dict value on existing directory."""

    git_config: dict = {}  # Empty dict
    test_dir_name: str = "test_git_dir"
