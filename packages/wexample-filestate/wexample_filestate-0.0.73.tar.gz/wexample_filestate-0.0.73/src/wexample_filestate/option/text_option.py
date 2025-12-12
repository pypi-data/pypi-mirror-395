from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_option.abstract_nested_config_option import (
    AbstractNestedConfigOption,
)
from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.option.mixin.option_mixin import OptionMixin

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.enum.scopes import Scope
    from wexample_filestate.operation.abstract_operation import AbstractOperation


@base_class
class TextOption(OptionMixin, AbstractNestedConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_helpers.const.types import StringKeysDict

        from wexample_filestate.config_value.text_config_value import TextConfigValue

        # Accept both list form ["trim", "end_new_line"] and dict form {"trim": true, "end_new_line": true}
        return Union[list[str], dict, StringKeysDict, TextConfigValue]

    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        """Create FileWriteOperation if text processing is needed."""
        return self._create_child_required_operation(target=target, scopes=scopes)

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.option.text.end_new_line_option import EndNewLineOption
        from wexample_filestate.option.text.sort_lines_option import SortLinesOption
        from wexample_filestate.option.text.trim_option import TrimOption
        from wexample_filestate.option.text.unique_lines_option import UniqueLinesOption

        return [
            TrimOption,
            EndNewLineOption,
            SortLinesOption,
            UniqueLinesOption,
        ]

    @abstract_method
    def get_description(self) -> str:
        return "Apply rules to text content"

    def set_value(self, raw_value: Any) -> None:
        # Convert list form to dict form for consistency
        if isinstance(raw_value, list):
            from wexample_filestate.option.text.end_new_line_option import (
                EndNewLineOption,
            )
            from wexample_filestate.option.text.sort_lines_option import SortLinesOption
            from wexample_filestate.option.text.trim_option import TrimOption
            from wexample_filestate.option.text.unique_lines_option import (
                UniqueLinesOption,
            )

            raw_value = {
                TrimOption.get_name(): "trim" in raw_value,
                EndNewLineOption.get_name(): "ensure_newline" in raw_value
                or "end_new_line" in raw_value,
                SortLinesOption.get_name(): "sort_lines" in raw_value,
                UniqueLinesOption.get_name(): "unique_lines" in raw_value,
            }

        super().set_value(raw_value=raw_value)
