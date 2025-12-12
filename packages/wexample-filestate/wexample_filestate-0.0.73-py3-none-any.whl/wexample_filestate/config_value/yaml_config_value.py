from __future__ import annotations

from typing import Any

from wexample_config.config_value.config_value import ConfigValue
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class YamlConfigValue(ConfigValue):
    raw: Any = public_field(
        default=None, description="Disabled raw value for this config."
    )
    sort_recursive: bool | None = public_field(
        default=None,
        description="Ask to sort recursively every keys of the yaml content",
    )

    def to_option_raw_value(self) -> Any:
        from wexample_filestate.option.yaml.sort_recursive_option import (
            SortRecursiveOption,
        )

        return {
            SortRecursiveOption.get_name(): self.sort_recursive,
        }
