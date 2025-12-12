from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_filestate.option.mixin.with_current_content_option_mixin import (
    WithCurrentContentOptionMixin,
)
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.enum.scopes import Scope


@base_class
class ClassOption(OptionMixin, WithCurrentContentOptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.item.item_target_file import ItemTargetFile

        return type[ItemTargetDirectory] | type[ItemTargetFile]

    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        from wexample_filestate.item.mixins.item_file_mixin import ItemFileMixin

        if isinstance(target, ItemFileMixin):
            return self._create_write_operation_if_content_changed(
                target=target,
                target_content=target.preview_write(),
                description=f"Rewrite content according to {target.__class__.__name__} rules",
            )

        return None

    def get_description(self) -> str:
        return "Define a class as a file or directory configuration manager"
