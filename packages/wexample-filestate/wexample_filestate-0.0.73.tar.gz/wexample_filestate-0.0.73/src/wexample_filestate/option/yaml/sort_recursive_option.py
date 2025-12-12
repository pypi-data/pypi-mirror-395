from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.option.yaml.abstract_yaml_child_option import (
    AbstractYamlChildOption,
)

if TYPE_CHECKING:
    from wexample_filestate.enum.scopes import Scope


@base_class
class SortRecursiveOption(AbstractYamlChildOption):
    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        from wexample_filestate.operation.file_write_operation import FileWriteOperation

        if self.get_value().is_true():
            # Check if file needs sorting
            if self._is_yaml_sorted(target):
                return None

            # Read and sort the YAML content
            data = self._read_yaml_data(target)
            sorted_data = self._sort_recursive(data)
            sorted_content = self._dump_yaml_content(sorted_data)

            return FileWriteOperation(
                option=self,
                target=target,
                content=sorted_content,
                description=self.get_description(),
            )

        return None

    def get_description(self) -> str:
        return "Sort YAML file content recursively by keys"

    def _is_yaml_sorted(self, target: TargetFileOrDirectoryType) -> bool:
        """Check if YAML file is already recursively sorted."""
        data = self._read_yaml_data(target)
        sorted_data = self._sort_recursive(data)

        current_dump = self._dump_yaml_content(data)
        sorted_dump = self._dump_yaml_content(sorted_data)

        return current_dump == sorted_dump

    def _sort_recursive(self, obj):
        """Recursively sort dictionary keys and process lists."""
        if isinstance(obj, dict):
            return {k: self._sort_recursive(obj[k]) for k in sorted(obj.keys())}
        if isinstance(obj, list):
            return [self._sort_recursive(v) for v in obj]
        return obj
