from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.result.abstract_result import AbstractResult

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation


class FileStateDryRunResult(AbstractResult):
    def _apply_single_operation(
        self, operation: AbstractOperation, interactive: bool = False
    ) -> bool:
        return True
