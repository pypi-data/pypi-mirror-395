from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.exception.undefined_exception import UndefinedException

if TYPE_CHECKING:
    from wexample_filestate.item.abstract_item_target import AbstractItemTarget


class UndefinedShortcutException(UndefinedException):
    error_code: str = "FILE_STATE_UNDEFINED_SHORTCUT"

    def __init__(self, shortcut: str, root_item: AbstractItemTarget, **kwargs) -> None:
        super().__init__(
            message=(
                f"Shortcut '{shortcut}' is not defined in root "
                f"{root_item.get_item_title()} '{root_item.get_item_name()}'."
            ),
            **kwargs,
        )
