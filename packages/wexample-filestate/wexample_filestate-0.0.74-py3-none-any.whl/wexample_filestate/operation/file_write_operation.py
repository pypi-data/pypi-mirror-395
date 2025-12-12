from __future__ import annotations

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.operation.abstract_existing_file_operation import (
    AbstractExistingFileOperation,
)


@base_class
class FileWriteOperation(AbstractExistingFileOperation):
    content: str = public_field(
        description="The content to write",
    )

    def apply_operation(self) -> None:
        self._target_file_write(content=self.content)
