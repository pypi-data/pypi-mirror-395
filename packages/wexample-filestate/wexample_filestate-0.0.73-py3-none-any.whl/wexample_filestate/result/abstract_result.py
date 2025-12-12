from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.mixin.printable_mixin import PrintableMixin
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.item.abstract_item_target import AbstractItemTarget
from wexample_filestate.operation.abstract_operation import AbstractOperation

if TYPE_CHECKING:
    from wexample_filestate.item.abstract_item_target import AbstractItemTarget
    from wexample_filestate.operation.abstract_operation import AbstractOperation


@base_class
class AbstractResult(PrintableMixin, BaseClass):
    operations: list[AbstractOperation] = public_field(
        factory=list,
        description="List of operations performed in this result",
    )
    rollback: bool = public_field(
        default=False,
        description="Indicates whether a rollback should be performed",
    )
    state_manager: AbstractItemTarget = public_field(
        description="Item target state manager associated with this result",
    )

    def apply_operations(self, interactive: bool = False) -> None:
        self._executed_operations = []

        # Define order of operations based on rollback mode
        operations = reversed(self.operations) if self.rollback else self.operations

        # Apply each operation directly (no dependencies needed)
        for operation in operations:
            if operation in self._executed_operations:
                continue

            if self.rollback:
                operation.undo()
                operation.applied = False
                self._executed_operations.append(operation)
            else:
                self.state_manager.subtitle(
                    f"OPERATION: {operation.get_snake_short_class_name().upper()}"
                )
                applied = self._apply_single_operation(
                    operation=operation, interactive=interactive
                )

                if applied:
                    operation.applied = True
                    self._executed_operations.append(operation)

                    self.state_manager.task(
                        message=f"{operation.target.get_item_title()}: {operation.target.render_display_path()}\n"
                        f"    → {operation.description}\n"
                    )
                else:
                    self.state_manager.log(
                        message=f"{operation.target.get_item_title()}: {operation.target.render_display_path()}\n"
                        f"    → {operation.description}\n"
                        f"    ⋮ Operation aborted"
                    )

    @abstract_method
    def _apply_single_operation(
        self, operation: AbstractOperation, interactive: bool = False
    ) -> bool:
        pass
