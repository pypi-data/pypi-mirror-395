from __future__ import annotations

from wexample_config.const.types import DictConfig

from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
from wexample_filestate.testing.abstract_test_operation import AbstractTestOperation


class TestYamlSortRecursiveOperation(AbstractTestOperation):
    def _get_target(self) -> TargetFileOrDirectoryType | None:
        return self.state_manager.find_by_name("unsorted.yml")

    def _operation_test_assert_applied(self) -> None:
        assert self._read_test_file().startswith("a_key")

    def _operation_test_assert_initial(self) -> None:
        assert self._read_test_file().startswith("x_key")

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.option.name_option import NameOption
        from wexample_filestate.option.yaml.sort_recursive_option import (
            SortRecursiveOption,
        )
        from wexample_filestate.option.yaml_option import YamlOption

        return {
            "children": [
                {
                    NameOption.get_name(): "unsorted.yml",
                    YamlOption.get_name(): {SortRecursiveOption.get_name(): True},
                },
            ]
        }

    def _read_test_file(self) -> str:
        target = self.state_manager.find_by_name("unsorted.yml")
        return target.get_local_file().read()
