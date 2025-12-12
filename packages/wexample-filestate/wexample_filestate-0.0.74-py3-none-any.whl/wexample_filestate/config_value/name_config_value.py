from __future__ import annotations

from typing import Any

from wexample_config.config_value.config_value import ConfigValue
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class NameConfigValue(ConfigValue):
    case_format: str | None = public_field(
        default=None,
        description="Case format: uppercase, lowercase, camelCase, snake_case, kebab-case",
    )
    prefix: str | None = public_field(
        default=None,
        description="Required prefix for the name",
    )
    raw: Any = public_field(
        default=None, description="Disabled raw value for this config."
    )
    regex: str | None = public_field(
        default=None,
        description="Regular expression pattern the name must match",
    )
    suffix: str | None = public_field(
        default=None,
        description="Required suffix for the name",
    )
    value: str = public_field(
        description="The name value",
    )

    def to_option_raw_value(self) -> Any:
        from wexample_filestate.option.name.case_format_option import CaseFormatOption
        from wexample_filestate.option.name.prefix_option import PrefixOption
        from wexample_filestate.option.name.regex_option import RegexOption
        from wexample_filestate.option.name.suffix_option import SuffixOption
        from wexample_filestate.option.name.value_option import ValueOption

        return {
            ValueOption.get_name(): self.value,
            CaseFormatOption.get_name(): self.case_format,
            RegexOption.get_name(): self.regex,
            PrefixOption.get_name(): self.prefix,
            SuffixOption.get_name(): self.suffix,
        }
