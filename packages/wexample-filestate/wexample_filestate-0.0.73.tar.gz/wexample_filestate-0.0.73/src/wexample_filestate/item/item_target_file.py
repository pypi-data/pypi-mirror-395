from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_config.const.types import DictConfig
from wexample_helpers.classes.field import public_field

from wexample_filestate.item.abstract_item_target import AbstractItemTarget
from wexample_filestate.item.mixins.item_file_mixin import ItemFileMixin

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class ItemTargetFile(ItemFileMixin, AbstractItemTarget):
    config: DictConfig | None = public_field(
        default=None,
        description="Filesystem path to the content file",
    )
