from __future__ import annotations

from typing import Any

from wexample_config.config_value.config_value import ConfigValue
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class GitConfigValue(ConfigValue):
    main_branch: str | list[str] | None = public_field(
        default=None,
        description="Main branch name(s) to create",
    )
    raw: Any = public_field(
        default=None, description="Disabled raw value for this config."
    )
    remote: list[dict] | dict | None = public_field(
        default=None,
        description="Remote repositories configuration",
    )

    def to_option_raw_value(self) -> Any:
        from wexample_filestate_git.option._git.main_branch_option import (
            MainBranchOption,
        )
        from wexample_filestate_git.option._git.remote_option import RemoteOption

        return {
            MainBranchOption.get_name(): self.main_branch,
            RemoteOption.get_name(): self.remote,
        }
