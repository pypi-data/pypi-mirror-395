from __future__ import annotations

from wexample_filestate_git.testing.abstract_main_branch_test import (
    AbstractMainBranchTest,
)


class TestMainBranchOptionDefault(AbstractMainBranchTest):
    """Test MainBranchOption with default 'main' branch."""

    expected_branch_name: str = "main"
    main_branch_config: list = []  # Empty list should default to "main"
    test_dir_name: str = "test-git-branch-default"
