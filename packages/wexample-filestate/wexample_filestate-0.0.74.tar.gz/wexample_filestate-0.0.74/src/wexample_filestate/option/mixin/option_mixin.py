from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.common.mixin.with_scope_mixin import WithScopeMixin
from wexample_filestate.config_option.mixin.item_config_option_mixin import (
    ItemTreeConfigOptionMixin,
)
from wexample_filestate.enum.scopes import Scope

if TYPE_CHECKING:
    from wexample_file.enum.local_path_type import LocalPathType

    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.operation.abstract_operation import AbstractOperation


@base_class
class OptionMixin(WithScopeMixin, ItemTreeConfigOptionMixin):
    @classmethod
    def get_class_name_suffix(cls) -> str | None:
        return "Option"

    def applicable_on_directory(self) -> bool:
        return True

    def applicable_on_empty_content_file(self) -> bool:
        return True

    def applicable_on_file(self) -> bool:
        return True

    def applicable_on_missing(self) -> bool:
        return True

    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        """Create and configure an operation instance if this option requires action.

        Returns:
            None if no operation is needed (option is satisfied or not applicable)
            AbstractOperation instance configured with necessary data if action is required

        The option is responsible for:
        - Determining if action is needed
        - Instantiating the appropriate operation class
        - Configuring the operation with necessary data
        - Passing any computed values (e.g., new content for FileWriteOperation)
        """
        return None

    def get_supported_item_types(self) -> list[LocalPathType]:
        from wexample_file.enum.local_path_type import LocalPathType

        return [
            LocalPathType.FILE,
            LocalPathType.DIRECTORY,
        ]

    def _create_child_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        """Create operation by iterating through all enabled sub-options."""
        for option_class in self.get_allowed_options():
            option = self.get_option(option_class)
            if option:
                operation = target.try_create_operation_from_option(
                    option=option, scopes=scopes
                )
                if operation:
                    # Return the first operation found
                    return operation

        return None
