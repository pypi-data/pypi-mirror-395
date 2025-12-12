from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.operation.abstract_operation import AbstractOperation

if TYPE_CHECKING:
    from wexample_helpers.const.types import PathOrString

    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class AbstractFileManipulationOperation(AbstractOperation):
    _original_file_content: str = private_field(
        description="Cached original file content for undo"
    )
    _original_file_mode: int = private_field(
        description="Cached original file mode for undo"
    )
    _original_path: PathOrString = private_field(
        description="Cached original file path for undo"
    )

    def _backup_file_content(
        self, target: TargetFileOrDirectoryType, file_path: PathOrString
    ) -> bool:
        import os

        from wexample_helpers.helpers.file import file_read

        from wexample_filestate.option.remove_backup_max_file_size_option import (
            REMOVE_BACKUP_MAX_FILE_SIZE_DEFAULT,
            RemoveBackupMaxFileSizeOption,
        )

        size = os.path.getsize(file_path)

        # Save content if not too large.
        if size < int(
            target.get_option_value(
                RemoveBackupMaxFileSizeOption,
                default=REMOVE_BACKUP_MAX_FILE_SIZE_DEFAULT,
            ).get_int()
        ):
            self._original_file_content = file_read(file_path)

            return True
        return False

    def _backup_target_file(self) -> None:
        self._original_path = self.target.get_path()
        self._original_file_mode = self.target.get_path().stat().st_mode

        self._backup_file_content(
            target=self.target,
            file_path=self._original_path,
        )

    def _restore_target_file(self) -> None:
        import os

        from wexample_helpers.helpers.file import file_write

        if self.target.is_file():
            file_write(self._original_path, self._original_file_content)
            os.chmod(self._original_path, self._original_file_mode)
        elif self.target.is_directory():
            os.mkdir(self._original_path)

    def _target_file_write(self, content: str) -> None:
        self._backup_target_file()
        self.target.get_local_file().write(content=content)
