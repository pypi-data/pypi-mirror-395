from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.operation.abstract_operation import AbstractOperation

if TYPE_CHECKING:
    from git import Repo
    from wexample_config.config_option.abstract_config_option import (
        AbstractConfigOption,
    )
    from wexample_filestate.enum.scopes import Scope


class AbstractGitOperation(AbstractOperation):
    @classmethod
    def get_scopes(cls) -> [Scope]:
        from wexample_filestate.enum.scopes import Scope

        return [Scope.REMOTE]

    # Shared Git helpers
    def _get_target_git_repo(self) -> Repo:
        """Return the GitPython Repo for the target path."""
        from git import Repo

        return Repo(self.target.get_path())

    # Evaluate an 'active' flag consistently across operations.
    # Accepts raw values (bool, int, str, etc.) and treats missing as inactive.
    def _is_active_flag(self, raw_value) -> bool:
        from wexample_filestate.option.active_option import (
            ActiveOption,
        )

        if raw_value is None:
            return True
        return ActiveOption.is_active(raw_value)

    def _is_active_git_option(self, option: AbstractConfigOption) -> bool:
        from wexample_filestate.option.active_option import (
            ActiveOption,
        )

        from wexample_filestate_git.option.git_option import (
            GitOption,
        )

        if isinstance(option, GitOption):
            value = self.target.get_option_value(GitOption)
            if value:
                if value.has_key_in_dict(ActiveOption.get_name()):
                    active_option = value.get_dict().get(ActiveOption.get_name())
                    return ActiveOption.is_active(active_option)
                return True
        return False
