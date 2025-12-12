from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.config_option.mixin.item_config_option_mixin import (
    ItemTreeConfigOptionMixin,
)

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.operation.file_write_operation import FileWriteOperation


@base_class
class WithCurrentContentOptionMixin(ItemTreeConfigOptionMixin):
    def _create_write_operation_if_content_changed(
        self,
        target: TargetFileOrDirectoryType,
        target_content: str,
        description: str | None = None,
    ) -> None | FileWriteOperation:
        """Create FileWriteOperation if content is different."""
        from wexample_filestate.operation.file_write_operation import FileWriteOperation

        # If the target file does not exist, we don't create it,
        # it should be created by other dedicated options.
        if not target.get_path().exists():
            return None

        if target_content is not None:
            # Apply any class-level content transformations
            target_content = target.preview_write(content=target_content)
            # Get current content
            current_content = self._read_current_content(target) or ""

            # If content is different, create operation
            if target_content != current_content:
                return FileWriteOperation(
                    option=self,
                    target=target,
                    content=target_content,
                    description=description or self.get_description(),
                )

        return None

    def _read_current_content(self, target: TargetFileOrDirectoryType) -> str | None:
        """Read current file content, return None if file doesn't exist."""
        if not target.source or not target.source.get_path().exists():
            return None
        return target.get_local_file().read()
