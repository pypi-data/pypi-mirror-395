from __future__ import annotations

from wexample_filestate_git.testing.abstract_git_option_test import (
    AbstractGitOptionTest,
)


class TestGitOptionBoolTrue(AbstractGitOptionTest):
    """Test GitOption with boolean True value."""

    git_config: bool = True
    test_dir_name: str = "test-git-repo"
    # Directory already exists
