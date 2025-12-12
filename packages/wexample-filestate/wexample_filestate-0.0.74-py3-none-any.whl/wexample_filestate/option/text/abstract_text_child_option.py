from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption

from wexample_filestate.option.mixin.option_mixin import OptionMixin

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class AbstractTextChildOption(OptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return bool

    def _read_current_content(self, target: TargetFileOrDirectoryType) -> str | None:
        """Read current file content, return None if file doesn't exist."""
        if not target.source or not target.source.get_path().exists():
            return None
        return target.get_local_file().read()
