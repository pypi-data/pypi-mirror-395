from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.mixin.with_path_mixin import WithPathMixin

if TYPE_CHECKING:
    from wexample_helpers.const.types import FileStringOrPath


@base_class
class ItemMixin(WithPathMixin):
    base_name: FileStringOrPath | None = public_field(
        description="The name of the item (filename, basename)", default=None
    )
    base_path: FileStringOrPath | None = public_field(
        description="The parent path of the item", default=None
    )

    @abstract_method
    def get_item_title(self) -> str:
        pass

    def get_octal_mode(self: ItemMixin) -> str:
        from wexample_helpers.helpers.file import file_path_get_octal_mode

        return file_path_get_octal_mode(self.get_path())

    @abstract_method
    def is_directory(self) -> bool:
        pass

    @abstract_method
    def is_file(self) -> bool:
        pass
