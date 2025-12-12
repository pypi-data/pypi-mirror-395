from __future__ import annotations

import os
from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.operation.abstract_file_manipulation_operation import (
    AbstractFileManipulationOperation,
)

if TYPE_CHECKING:
    from wexample_filestate.enum.scopes import Scope


@base_class
class FileRenameOperation(AbstractFileManipulationOperation):
    new_name: str = public_field(
        description="The new name",
        default=False,
    )

    @classmethod
    def get_scopes(cls) -> [Scope]:
        from wexample_filestate.enum.scopes import Scope

        return [Scope.LOCATION]

    def apply_operation(self) -> None:
        self._backup_target_file()

        old_path = self._original_path
        new_path = old_path.parent / self.new_name

        os.rename(old_path, new_path)

    def undo(self) -> None:
        # Rename back from new name to original name
        old_path = self._original_path
        new_path = old_path.parent / self.new_name

        # Rename back to original name
        os.rename(new_path, old_path)
