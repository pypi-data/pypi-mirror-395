from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.option.mixin.option_mixin import OptionMixin

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.enum.scopes import Scope
    from wexample_filestate.operation.abstract_operation import AbstractOperation


@base_class
class OnBadFormatOption(OptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return str

    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        """Create operation based on the action when format validation fails."""
        # Get parent NameOption that contains the format rules
        parent_option = self.get_parent()
        if not parent_option:
            return None

        # Get the current name
        current_name = target.get_item_name()

        # Validate name using parent NameOption
        if parent_option.validate_name(current_name):
            return None  # Name is valid, no action needed

        # Name is invalid, take action based on configuration
        action = self.get_value().get_str()

        if action == "delete":
            from wexample_filestate.operation.file_remove_operation import (
                FileRemoveOperation,
            )

            return FileRemoveOperation(
                option=self,
                target=target,
                description=f"Delete file with invalid name format: {current_name}",
            )
        elif action == "rename":
            # Generate new name based on format rules
            new_name = self._generate_corrected_name(current_name)
            if new_name and new_name != current_name:
                from wexample_filestate.operation.file_rename_operation import (
                    FileRenameOperation,
                )

                return FileRenameOperation(
                    option=self,
                    target=target,
                    new_name=new_name,
                    description=f"Rename file from '{current_name}' to '{new_name}' to match format rules",
                )
            return None
        elif action == "error":
            from wexample_filestate.exception.name_format_exception import (
                NameFormatException,
            )

            raise NameFormatException(
                f"File name '{current_name}' does not match required format"
            )
        # "ignore" action returns None (no operation)

        return None

    def get_description(self) -> str:
        return "Action to take when name format validation fails (delete, rename, ignore, error)"

    def _generate_corrected_name(self, current_name: str) -> str | None:
        """Generate a corrected name based on format rules using child options."""
        import os

        from wexample_filestate.option.name.case_format_option import CaseFormatOption
        from wexample_filestate.option.name.prefix_option import PrefixOption
        from wexample_filestate.option.name.suffix_option import SuffixOption

        # Get parent NameOption that contains the format rules
        parent_option = self.get_parent()
        if not parent_option:
            return None

        # Split name and extension
        name_part, ext = os.path.splitext(current_name)
        corrected_name = name_part

        # Apply corrections in order: case format, prefix, suffix
        # Each child option handles its own correction logic
        for option_class in [CaseFormatOption, PrefixOption, SuffixOption]:
            option = parent_option.get_option(option_class)
            if option:
                corrected_name = option.apply_correction(corrected_name)

        # Note: RegexOption doesn't provide automatic correction
        # Reconstruct full name with extension
        return corrected_name + ext
