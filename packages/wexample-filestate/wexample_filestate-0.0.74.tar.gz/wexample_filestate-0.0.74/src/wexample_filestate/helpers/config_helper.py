from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig
    from wexample_helpers.const.types import FileStringOrPath

    from wexample_filestate.const.disk import DiskItemType


def config_has_same_type_as_path(config: DictConfig, path: FileStringOrPath) -> bool:
    from wexample_helpers.helpers.file import file_resolve_path

    from wexample_filestate.const.disk import DiskItemType

    resolved_path = file_resolve_path(path)

    if resolved_path.is_file() and config_is_item_type(config, DiskItemType.FILE):
        return True

    if resolved_path.is_dir() and config_is_item_type(config, DiskItemType.DIRECTORY):
        return True

    return False


def config_is_item_type(config: DictConfig, type_enum: DiskItemType) -> bool:
    return config.get("type") is not None and (
        config["type"] == type_enum or config["type"] == type_enum.value
    )
