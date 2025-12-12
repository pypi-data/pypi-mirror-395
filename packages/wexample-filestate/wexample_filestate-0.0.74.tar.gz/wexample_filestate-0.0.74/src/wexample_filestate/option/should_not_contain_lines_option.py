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
class ShouldNotContainLinesOption(OptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return list[str]

    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        from wexample_filestate.operation.file_write_operation import FileWriteOperation

        """Create FileWriteOperation if forbidden lines are present in file."""
        # Get the forbidden lines
        forbidden_lines_value = self.get_value()
        if not forbidden_lines_value or forbidden_lines_value.is_none():
            return None

        forbidden_lines = forbidden_lines_value.get_list()
        if not forbidden_lines:
            return None

        # Get current content
        current_content = self._read_current_content(target)
        if not current_content:
            return None  # No content to process

        # Check if any forbidden lines are present and remove them
        updated_content = self._remove_forbidden_lines(
            lines=forbidden_lines,
            content=current_content,
        )

        # If content changed, create operation
        if updated_content != current_content:
            return FileWriteOperation(
                option=self,
                target=target,
                content=updated_content,
                description="Remove lines that should not be present in the file",
            )

        return None

    def _read_current_content(self, target: TargetFileOrDirectoryType) -> str | None:
        """Read current file content, return None if file doesn't exist."""
        if not target.source or not target.source.get_path().exists():
            return None
        return target.get_local_file().read() or ""

    def _remove_forbidden_lines(self, lines: list[str], content: str) -> str:
        """Remove specified lines from content."""
        current_lines = content.splitlines()
        filtered_lines = [line for line in current_lines if line not in lines]
        return "\n".join(filtered_lines)
