from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_option.abstract_nested_config_option import (
    AbstractNestedConfigOption,
)
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from types import UnionType

    from wexample_config.const.types import DictConfig, DictConfigValue
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.operation.abstract_operation import AbstractOperation


@base_class
class GitOption(OptionMixin, AbstractNestedConfigOption):
    @classmethod
    def get_scopes(cls) -> None | list[Scope]:
        from wexample_filestate.enum.scopes import Scope

        return [Scope.REMOTE]

    @classmethod
    def resolve_config(cls, config: DictConfig) -> DictConfig:
        from wexample_filestate.option.should_exist_option import (
            ShouldExistOption,
        )

        if GitOption.get_name() in config and cls.dict_value_should_have_git(
            config[GitOption.get_name()]
        ):
            config[ShouldExistOption.get_name()] = True
        return config

    @staticmethod
    def dict_value_should_have_git(value: DictConfigValue) -> bool:
        return (value is True) or isinstance(value, dict)

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_helpers.const.types import StringKeysDict

        from wexample_filestate_git.config_value.git_config_value import GitConfigValue

        return Union[dict, bool, StringKeysDict, GitConfigValue]

    @staticmethod
    def get_value_allowed_type() -> Any | type | UnionType:
        return dict | bool

    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        """Create GitInitOperation if Git is required but not initialized, or delegate to children."""
        from wexample_helpers_git.helpers.git import git_is_init

        # Check if Git is required
        if not self.should_have_git():
            return None

        # Check if target path exists (Git can only be initialized in existing directories)
        target_path = target.get_path()
        if not target_path.exists():
            return None

        # Check if Git is already initialized
        if not git_is_init(target_path):
            # Git needs to be initialized first
            from wexample_filestate_git.operation.git_init_operation import (
                GitInitOperation,
            )

            return GitInitOperation(
                option=self, target=target, description="Initialize Git repository"
            )

        # Git is already initialized, delegate to children for other operations
        return self._create_child_required_operation(target=target, scopes=scopes)

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate_git.option._git.main_branch_option import (
            MainBranchOption,
        )
        from wexample_filestate_git.option._git.remote_option import RemoteOption

        return [
            MainBranchOption,
            RemoteOption,
        ]

    def set_value(self, raw_value: Any) -> None:
        # Support True without config.
        if raw_value is True:
            raw_value = {}

        super().set_value(raw_value=raw_value)

    def should_have_git(self) -> bool:
        value = self.get_value()
        return (value.is_bool() and value.is_true()) or value.is_dict()
