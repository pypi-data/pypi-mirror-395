from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.operation.abstract_operation import AbstractOperation

if TYPE_CHECKING:
    from wexample_filestate.enum.scopes import Scope


@base_class
class FileChangeModeOperation(AbstractOperation):
    recursive: bool = public_field(
        description="Apply mode to child list",
    )
    target_mode: bool = public_field(
        description="The permissions mode to apply",
    )
    _original_octal_mode: str | None = private_field(
        description="Cached mode to provide undo"
    )

    @classmethod
    def get_scopes(cls) -> [Scope]:
        from wexample_filestate.enum.scopes import Scope

        return [Scope.PERMISSIONS]

    def apply_operation(self) -> None:
        from wexample_helpers.helpers.file import (
            file_change_mode,
            file_change_mode_recursive,
        )

        self._original_octal_mode = self.target.get_source().get_octal_mode()

        if self.recursive:
            file_change_mode_recursive(
                self.target.get_source().get_path(), self.target_mode
            )
        else:
            file_change_mode(self.target.get_source().get_path(), self.target_mode)

    def undo(self) -> None:
        from wexample_helpers.helpers.file import (
            file_change_mode_recursive,
            file_mode_octal_to_num,
        )

        file_change_mode_recursive(
            self.target.get_source().get_path(),
            file_mode_octal_to_num(self._get_original_octal_mode()),
        )

    def _get_original_octal_mode(self) -> str:
        assert self._original_octal_mode is not None
        return self._original_octal_mode
