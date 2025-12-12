from __future__ import annotations

from typing import Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.decorator.base_class import base_class


@base_class
class UrlOption(OptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from collections.abc import Callable

        from wexample_filestate.item.abstract_item_target import AbstractItemTarget

        return Union[str, Callable[[AbstractItemTarget], str]]

    def get_url(self, target: TargetFileOrDirectoryType) -> str:
        """Not name get_str because I'm not sure of convention"""
        value = self.get_value()

        if value.is_callable():
            return str(value.get_callable()(target=target))

        return value.get_str()
