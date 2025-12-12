from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.exception.undefined_exception import UndefinedException

if TYPE_CHECKING:
    from wexample_filestate.item.abstract_item_target import AbstractItemTarget


class ExistingShortcutException(UndefinedException):
    error_code: str = "FILE_STATE_EXISTING_SHORTCUT"

    def __init__(
        self,
        shortcut: str,
        new_item: AbstractItemTarget,
        existing_item: AbstractItemTarget,
        root_item: AbstractItemTarget,
        **kwargs,
    ) -> None:
        super().__init__(
            message=(
                f"Shortcut '{shortcut}' is already in use by "
                f"{existing_item.get_item_title()} '{existing_item.get_item_name()}' "
                f"and cannot be reassigned to {new_item.get_item_title()} "
                f"'{new_item.get_item_name()}' in root {root_item.get_item_title()} "
                f"'{root_item.get_item_name()}'."
            ),
            **kwargs,
        )
