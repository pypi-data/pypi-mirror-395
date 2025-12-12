from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.option.mixin.option_mixin import OptionMixin

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.enum.scopes import Scope
    from wexample_filestate.operation.abstract_operation import AbstractOperation


@base_class
class ShouldContainLinesOption(OptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return list[str]

    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        """Create FileWriteOperation if required lines are missing from file."""
        from wexample_helpers.helpers.string import string_append_missing_lines

        from wexample_filestate.operation.file_write_operation import FileWriteOperation

        # Get the required lines
        required_lines_value = self.get_value()
        if not required_lines_value or required_lines_value.is_none():
            return None

        required_lines = required_lines_value.get_list()
        if not required_lines:
            return None

        # Get current content
        current_content = self._read_current_content(target) or ""

        # Check if any lines are missing
        updated_content = string_append_missing_lines(
            lines=required_lines,
            content=current_content,
        )

        # If content changed, create operation
        if updated_content != current_content:
            return FileWriteOperation(
                option=self,
                target=target,
                content=updated_content,
                description="Add missing lines that should be present in the file",
            )

        return None

    def _read_current_content(self, target: TargetFileOrDirectoryType) -> str | None:
        """Read current file content, return empty string if file doesn't exist."""
        if not target.source or not target.source.get_path().exists():
            return ""
        return target.get_local_file().read() or ""
