from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union
from collections.abc import Callable

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_value.config_value import ConfigValue
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_filestate.option.mixin.with_current_content_option_mixin import (
    WithCurrentContentOptionMixin,
)
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.enum.scopes import Scope
    from wexample_filestate.operation.abstract_operation import AbstractOperation


@base_class
class ContentOption(OptionMixin, WithCurrentContentOptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_config.config_value.config_value import ConfigValue

        return Union[str, ConfigValue, Callable]

    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        if not self.get_value().is_none():
            return self._create_write_operation_if_content_changed(
                target=target, target_content=self.get_value().get_str()
            )
        return None

    def get_description(self) -> str:
        return "Set file content to the specified value"

    def get_value(self) -> ConfigValue:
        """Get the name value, supporting both legacy string, nested dict, and callable formats."""
        value = super().get_value()

        # Check if we have a callable value stored
        if isinstance(value, str):
            return ConfigValue(raw=value)
        if value.is_callable():
            return ConfigValue(raw=str((value.get_callable())(self)))

        return value
