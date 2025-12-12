from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate_git.operation.abstract_git_operation import AbstractGitOperation

if TYPE_CHECKING:
    pass


@base_class
class GitCreateBranchOperation(AbstractGitOperation):
    def __init__(self, option, target, branch_name: str, description: str) -> None:
        super().__init__(option=option, target=target, description=description)
        self.branch_name = branch_name

    def apply_operation(self) -> None:
        """Create the desired branch locally if it does not exist.

        Notes:
        - This operation is local-only (no remote push, no deletion/rename of other branches).
        - The branch is created at current HEAD.
        """
        repo = self._get_target_git_repo()
        if not repo:
            return

        if any(h.name == self.branch_name for h in getattr(repo, "heads", [])):
            return  # Already exists

        # Create new branch at current HEAD
        repo.create_head(self.branch_name)

    def undo(self) -> None:
        # No destructive undo: we do not auto-delete newly created branches
        pass
