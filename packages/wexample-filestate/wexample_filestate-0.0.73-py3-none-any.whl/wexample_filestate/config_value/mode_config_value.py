from __future__ import annotations

from typing import Any

from wexample_config.config_value.config_value import ConfigValue
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class ModeConfigValue(ConfigValue):
    permissions: str | int = public_field(
        description="The expected file permission",
    )
    raw: Any = public_field(
        default=None, description="Disabled raw value for this config."
    )
    recursive: bool | None = public_field(
        default=None,
        description="Apply to sub items if origin is a directory",
    )

    def to_option_raw_value(self) -> Any:
        from wexample_filestate.option.mode.permissions_option import PermissionsOption
        from wexample_filestate.option.mode.recursive_option import RecursiveOption

        return {
            PermissionsOption.get_name(): self.permissions,
            RecursiveOption.get_name(): self.recursive,
        }
