from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.item.item_target_directory import ItemTargetDirectory

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


@base_class
class FileStateManager(ItemTargetDirectory):
    def configure(self, config: DictConfig) -> None:
        super().configure(config=config)

        # As root
        self.build_item_tree()
