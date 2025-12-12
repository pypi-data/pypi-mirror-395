from __future__ import annotations

from typing import TYPE_CHECKING, cast

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class ItemTreeConfigOptionMixin(BaseClass):
    """
    Give properties to every option that can be a part of the file system configuration tree,
    like any file or directory descriptor, and also children option a children factories.
    """

    def build_item_tree(self) -> None:
        pass

    def get_parent_item(self) -> TargetFileOrDirectoryType:
        from wexample_filestate.const.state_items import TargetFileOrDirectory
        from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType

        # In all case, when asking for parent item,
        # every config option should be an item tree item.
        assert isinstance(self.parent, ItemTreeConfigOptionMixin)

        if isinstance(self.parent, TargetFileOrDirectory):
            return cast(TargetFileOrDirectoryType, self.parent)

        # give a try to parent.
        return cast(TargetFileOrDirectoryType, self.parent).get_parent_item()

    def get_parent_item_or_none(self) -> TargetFileOrDirectoryType | None:
        if self.parent:
            return self.get_parent_item()
        return None
