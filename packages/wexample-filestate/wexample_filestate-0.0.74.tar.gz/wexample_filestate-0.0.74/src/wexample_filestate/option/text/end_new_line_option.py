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
class EndNewLineOption(AbstractTextChildOption):
    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        from wexample_filestate.operation.file_write_operation import FileWriteOperation

        if self.get_value().is_true():
            # Check end_new_line second
            current_content = self._read_current_content(target)
            if current_content and not current_content.endswith("\n"):
                updated_content = current_content + "\n"
                return FileWriteOperation(
                    option=self,
                    target=target,
                    content=updated_content,
                    description=self.get_description(),
                )

        return None

    def get_description(self) -> str:
        return "Ensure file ends with a newline character"
