from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.operation.abstract_file_manipulation_operation import (
    AbstractFileManipulationOperation,
)

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.enum.scopes import Scope


@base_class
class AbstractExistingFileOperation(AbstractFileManipulationOperation):
    """Base class for operations that require the target to be an existing file on disk.

    This class only abstracts the existence check (no extension or name check).
    Subclasses remain responsible for option typing/semantics and any extra filters.
    """

    _changed_source: str | None = private_field(
        default=None,
        description="Internal storage for a modified source string, if any",
    )
    _source_need_change: bool | None = private_field(
        default=None,
        description="Flag indicating whether the source requires modification",
    )

    @classmethod
    def get_scopes(cls) -> [Scope]:
        from wexample_filestate.enum.scopes import Scope

        return [Scope.CONTENT]

    @classmethod
    @abstract_method
    def preview_source_change(cls, target: TargetFileOrDirectoryType) -> str | None:
        pass

    @classmethod
    def _read_current_non_empty_src(
        cls, target: TargetFileOrDirectoryType
    ) -> str | None:
        src = cls._read_current_src(target)
        return src if src is not None and src.strip() != "" else None

    @classmethod
    def _read_current_str_or_fail(cls, target: TargetFileOrDirectoryType) -> str:
        src = cls._read_current_src(target)
        assert isinstance(src, str)
        return src

    @staticmethod
    def _is_existing_file(target: TargetFileOrDirectoryType) -> bool:
        if not target.source or not target.is_file():
            return False
        return target.get_local_file().path.exists()

    @staticmethod
    def _read_current_src(target: TargetFileOrDirectoryType) -> str | None:
        """Read current file content if it exists; return None if it does not exist."""
        return target.get_local_file().read()

    def apply_operation(self) -> None:
        if self._changed_source is not None:
            self._target_file_write(content=self._changed_source)

    def undo(self) -> None:
        self._restore_target_file()
