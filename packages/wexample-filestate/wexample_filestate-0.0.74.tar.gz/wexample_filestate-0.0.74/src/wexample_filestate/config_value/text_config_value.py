from __future__ import annotations

from typing import Any

from wexample_config.config_value.config_value import ConfigValue
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class TextConfigValue(ConfigValue):
    end_new_line: bool | None = public_field(
        default=None,
        description="Ensure file content ends with a newline character",
    )
    raw: Any = public_field(
        default=None, description="Disabled raw value for this config."
    )
    trim: bool | None = public_field(
        default=None,
        description="Ask to trim leading and trailing whitespace from file content",
    )

    def to_option_raw_value(self) -> Any:
        from wexample_filestate.option.text.end_new_line_option import EndNewLineOption
        from wexample_filestate.option.text.trim_option import TrimOption

        return {
            TrimOption.get_name(): self.trim,
            EndNewLineOption.get_name(): self.end_new_line,
        }
