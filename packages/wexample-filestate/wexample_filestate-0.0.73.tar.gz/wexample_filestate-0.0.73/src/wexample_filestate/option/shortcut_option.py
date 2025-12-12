from __future__ import annotations

from typing import Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.option.mixin.option_mixin import OptionMixin


@base_class
class ShortcutOption(OptionMixin, AbstractConfigOption):
    def __attrs_post_init__(self) -> None:
        from wexample_filestate.item.abstract_item_target import AbstractItemTarget

        super().__attrs_post_init__()

        # The parent should always be a path item.
        assert isinstance(self.parent, AbstractItemTarget)

        # If no parent, root might be a file as it returns itself.
        root = self.parent.get_root()

        # Register shortcuts only in root directories.
        if root and root != self.parent and root.is_directory():
            root.set_shortcut(self.get_value().get_str(), self.parent)

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from pathlib import PosixPath

        return str | PosixPath

    def prepare_value(self, raw_value: Any) -> Any:
        # Enforce str
        return super().prepare_value(raw_value=str(raw_value))
