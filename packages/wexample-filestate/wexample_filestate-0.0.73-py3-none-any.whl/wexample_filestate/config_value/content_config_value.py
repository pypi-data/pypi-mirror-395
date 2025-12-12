from __future__ import annotations

from typing import Any

from wexample_config.config_value.config_value import ConfigValue
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class ContentConfigValue(ConfigValue):
    raw: Any = public_field(
        default=None, description="Disabled raw value for this config."
    )
    text: str | None = public_field(
        default=None,
        description="The text content to write to the file",
    )

    def build_content(self) -> str | None:
        return self.text

    def to_option_raw_value(self) -> Any:
        return self.text

    def _create_default_raw(self, raw: Any) -> str:
        return ""
