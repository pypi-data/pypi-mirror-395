from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption

from wexample_filestate.option.mixin.option_mixin import OptionMixin

if TYPE_CHECKING:
    pass


class AbstractNameChildOption(OptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return str

    def apply_correction(self, name: str) -> str:
        """Apply correction to make the name comply with this format rule."""
        raise NotImplementedError("Subclasses must implement apply_correction")

    def validate_name(self, name: str) -> bool:
        """Validate if a name matches this format rule."""
        raise NotImplementedError("Subclasses must implement validate_name")
