from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.result.abstract_result import AbstractResult

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation


class FileStateResult(AbstractResult):
    _executed_operations: list = []

    def _apply_single_operation(
        self, operation: AbstractOperation, interactive: bool = False
    ) -> bool:
        from wexample_helpers.helpers.classes import classes_get_definition_path
        from wexample_prompt.responses.interactive.confirm_prompt_response import (
            ConfirmPromptResponse,
        )

        if interactive:
            from wexample_helpers.helpers.cli import cli_make_clickable_path

            if self.state_manager.io.confirm(
                question=f"Do you want to apply this change:\n"
                f"    {operation.target.get_item_title()}: {operation.target.render_display_path()}\n"
                f"    Option: {cli_make_clickable_path(classes_get_definition_path(operation.option), operation.option.get_name())}\n"
                f"  → {operation.description}\n",
                choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
                default="yes",
            ).is_ok():
                operation.target.operation_dispatch_event(
                    operation=operation,
                    suffix="pre",
                )
                operation.apply_operation()
                operation.target.operation_dispatch_event(
                    operation=operation,
                    suffix="post",
                )
                return True

            return False

        # Non interactive.
        operation.apply_operation()
        return True

    def _find_dependency(self, dependency_class) -> AbstractOperation | None:
        for operation in self.operations:
            if isinstance(operation, dependency_class):
                return operation
        return None
