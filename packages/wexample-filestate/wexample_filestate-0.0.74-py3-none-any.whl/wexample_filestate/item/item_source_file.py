from __future__ import annotations

from wexample_filestate.item.abstract_item_source import AbstractItemSource
from wexample_filestate.item.mixins.item_file_mixin import ItemFileMixin


class ItemSourceFile(ItemFileMixin, AbstractItemSource):
    pass
