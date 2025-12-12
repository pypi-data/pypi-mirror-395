from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_filestate.enum.scopes import Scope
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.operation.abstract_operation import AbstractOperation


@base_class
class MainBranchOption(OptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return Union[str, list]

    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        """Create GitCreateBranchOperation if branch needs to be created."""
        # Get desired branch name
        branch_name = self._get_desired_branch_name()
        if not branch_name:
            return None

        # Check if Git repo exists
        repo = self._get_target_git_repo(target)
        if not repo:
            return None

        # Check if branch already exists
        if any(h.name == branch_name for h in getattr(repo, "heads", [])):
            return None

        # Create operation with branch name parameter
        from wexample_filestate_git.operation.git_create_branch_operation import (
            GitCreateBranchOperation,
        )

        return GitCreateBranchOperation(
            option=self,
            target=target,
            branch_name=branch_name,
            description=f"Create Git branch '{branch_name}'",
        )

    def _get_desired_branch_name(self) -> str:
        """Resolve desired branch name from config.

        Accepts either a list (first item) or a single string value.
        Defaults to "main" if the option exists but is empty/invalid.
        """
        from wexample_helpers_git.const.common import GIT_BRANCH_MAIN

        v = self.get_value()

        # Prefer list form
        if v.is_list():
            items = v.get_list()
            if items:
                first = items[0]
                if isinstance(first, str):
                    return first
                # If not plain string, try to coerce via build_value
                return self._build_str_value(first)

        # Fallback: single string value
        if v.is_str():
            return v.get_str()

        if isinstance(v.raw, str):
            return v.raw

        # If the option exists but has no usable value, default to "main"
        return GIT_BRANCH_MAIN

    def _get_target_git_repo(self, target):
        """Get Git repository for the target."""
        try:
            from git import Repo
            from wexample_helpers.const.globals import DIR_GIT

            git_dir = target.get_path() / DIR_GIT
            if git_dir.exists():
                return Repo(str(target.get_path()))
        except Exception:
            pass
        return None
