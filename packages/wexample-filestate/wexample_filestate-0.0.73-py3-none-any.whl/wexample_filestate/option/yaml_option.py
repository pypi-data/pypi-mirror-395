from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_option.abstract_nested_config_option import (
    AbstractNestedConfigOption,
)
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.option.mixin.option_mixin import OptionMixin

if TYPE_CHECKING:
    from wexample_file.enum.local_path_type import LocalPathType

    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.enum.scopes import Scope
    from wexample_filestate.operation.abstract_operation import AbstractOperation


@base_class
class YamlOption(OptionMixin, AbstractNestedConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.config_value.yaml_config_value import YamlConfigValue

        return Union[dict, YamlConfigValue]

    def applicable_on_directory(self) -> bool:
        return False

    def applicable_on_missing(self) -> bool:
        return False

    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        """Create operation using child options."""
        return self._create_child_required_operation(target=target, scopes=scopes)

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.option.yaml.sort_recursive_option import (
            SortRecursiveOption,
        )

        return [
            SortRecursiveOption,
        ]

    def get_supported_item_types(self) -> list[LocalPathType]:
        from wexample_file.enum.local_path_type import LocalPathType

        return [
            LocalPathType.FILE,
        ]
