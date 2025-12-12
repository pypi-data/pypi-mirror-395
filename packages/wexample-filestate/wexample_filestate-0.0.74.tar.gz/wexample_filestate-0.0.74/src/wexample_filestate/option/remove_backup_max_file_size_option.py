from __future__ import annotations

from typing import Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption

REMOVE_BACKUP_MAX_FILE_SIZE_DEFAULT: int = 1000

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.option.mixin.option_mixin import OptionMixin


@base_class
class RemoveBackupMaxFileSizeOption(OptionMixin, AbstractConfigOption):
    value: int = REMOVE_BACKUP_MAX_FILE_SIZE_DEFAULT

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return int
