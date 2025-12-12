from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.option.name.abstract_name_child_option import (
    AbstractNameChildOption,
)


@base_class
class PrefixOption(AbstractNameChildOption):
    def apply_correction(self, name: str) -> str:
        """Apply prefix correction to name."""
        if self.get_value().is_none():
            return name

        prefix = self.get_value().get_str()
        if not name.startswith(prefix):
            return prefix + name
        return name

    def get_description(self) -> str:
        return "Enforce prefix requirement for file names"

    def validate_name(self, name: str) -> bool:
        """Validate if name starts with the required prefix."""
        if self.get_value().is_none():
            return True

        prefix = self.get_value().get_str()
        return name.startswith(prefix)
