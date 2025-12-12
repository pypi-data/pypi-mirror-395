from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate_git.operation.abstract_git_operation import AbstractGitOperation

if TYPE_CHECKING:
    pass


@base_class
class GitInitOperation(AbstractGitOperation):
    _has_initialized_git: bool = False

    def apply_operation(self) -> None:
        from git import Repo

        path = self.target.get_path()
        self._has_initialized_git = True

        repo = Repo.init(path)
        repo.init()

    def undo(self) -> None:
        import shutil

        from wexample_helpers.const.globals import DIR_GIT

        if self._has_initialized_git:
            shutil.rmtree(f"{self.target.get_path()}/{DIR_GIT}")
