from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_option.abstract_nested_config_option import (
    AbstractNestedConfigOption,
)
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    pass


@base_class
class RemoteItemOption(OptionMixin, AbstractNestedConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_helpers.const.types import StringKeysDict

        from wexample_filestate_git.config_value.remote_config_value import (
            RemoteConfigValue,
        )

        return Union[dict, StringKeysDict, RemoteConfigValue]

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.option.name_option import NameOption

        from wexample_filestate_git.option._git.create_remote_option import (
            CreateRemoteOption,
        )
        from wexample_filestate_git.option._git.type_option import TypeOption
        from wexample_filestate_git.option._git.url_option import UrlOption

        return [
            NameOption,
            CreateRemoteOption,
            TypeOption,
            UrlOption,
        ]
