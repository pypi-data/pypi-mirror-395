from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_option.abstract_nested_config_option import (
    AbstractNestedConfigOption,
)
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.option.mixin.option_mixin import OptionMixin

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.enum.scopes import Scope
    from wexample_filestate.operation.abstract_operation import AbstractOperation


@base_class
class NameOption(OptionMixin, AbstractNestedConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from pathlib import Path

        from wexample_filestate.config_value.name_config_value import NameConfigValue

        return Union[str, Path, dict, NameConfigValue, Callable]

    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        """Create operation via OnBadFormatOption if name format validation fails."""
        from wexample_filestate.option.name.on_bad_format_option import (
            OnBadFormatOption,
        )

        # Check if OnBadFormatOption is configured
        on_bad_format_option = self.get_option(OnBadFormatOption)
        if on_bad_format_option:
            return on_bad_format_option.create_required_operation(
                target=target, scopes=scopes
            )

        return None

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.option.name.case_format_option import CaseFormatOption
        from wexample_filestate.option.name.on_bad_format_option import (
            OnBadFormatOption,
        )
        from wexample_filestate.option.name.prefix_option import PrefixOption
        from wexample_filestate.option.name.regex_option import RegexOption
        from wexample_filestate.option.name.suffix_option import SuffixOption
        from wexample_filestate.option.name.value_option import ValueOption

        return [
            ValueOption,
            CaseFormatOption,
            RegexOption,
            PrefixOption,
            SuffixOption,
            OnBadFormatOption,
        ]

    def get_name_value(self) -> str | None:
        """Get the name value, supporting both legacy string, nested dict, and callable formats."""
        from wexample_filestate.option.name.value_option import ValueOption

        value = self.get_value()
        # Check if we have a callable value stored
        if callable(value):
            try:
                # Execute the callable with self as parameter
                result = self._callable_value(self)
                return str(result) if result is not None else None
            except Exception:
                # If callable fails, fall back to None
                return None

        value_option = self.get_option_value(ValueOption, default=None)
        if value_option and not value_option.is_none():
            return value_option.get_str()

        return None

    def set_value(self, raw_value: Any) -> None:
        from pathlib import Path

        from wexample_filestate.option.name.value_option import ValueOption

        if isinstance(raw_value, Path):
            raw_value = str(raw_value)

        # Store callable directly without conversion
        if callable(raw_value):
            # Create a placeholder dict to satisfy the nested config structure
            raw_value = {ValueOption.get_name(): raw_value}
        # Convert string form to dict form for consistency
        elif isinstance(raw_value, str):
            raw_value = {ValueOption.get_name(): raw_value}

        super().set_value(raw_value=raw_value)

    def validate_name(self, name: str) -> bool:
        """Validate if a name matches all format rules using child options."""
        from wexample_filestate.option.name.case_format_option import CaseFormatOption
        from wexample_filestate.option.name.prefix_option import PrefixOption
        from wexample_filestate.option.name.regex_option import RegexOption
        from wexample_filestate.option.name.suffix_option import SuffixOption

        # Check each format rule using child options
        for option_class in [CaseFormatOption, RegexOption, PrefixOption, SuffixOption]:
            option = self.get_option(option_class)
            if option and not option.validate_name(name):
                return False

        return True
