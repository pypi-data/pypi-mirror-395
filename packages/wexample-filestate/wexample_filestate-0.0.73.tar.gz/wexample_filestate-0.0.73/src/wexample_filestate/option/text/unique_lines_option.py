from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.option.text.abstract_text_child_option import (
    AbstractTextChildOption,
)

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.enum.scopes import Scope
    from wexample_filestate.operation.abstract_operation import AbstractOperation


@base_class
class UniqueLinesOption(AbstractTextChildOption):
    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        from wexample_filestate.operation.file_write_operation import FileWriteOperation

        if self.get_value().is_true():
            current_content = self._read_current_content(target)
            if current_content is not None:
                unique_content = self._unique_lines_content(current_content)

                if unique_content != current_content:
                    return FileWriteOperation(
                        option=self,
                        target=target,
                        content=unique_content,
                        description=self.get_description(),
                    )

        return None

    def get_description(self) -> str:
        return "Remove duplicate lines from file content"

    def _unique_lines_content(self, content: str) -> str:
        """Ensure each line of the file content is unique (remove duplicates preserving order)."""
        # Preserve a trailing newline if it exists
        had_trailing_newline = content.endswith("\n")
        lines = content.splitlines()
        seen: set[str] = set()
        unique_lines: list[str] = []
        for line in lines:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)
        out = "\n".join(unique_lines)
        if had_trailing_newline:
            out += "\n"
        return out
