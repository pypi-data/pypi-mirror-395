from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_config.const.types import DictConfig

from wexample_filestate.testing.abstract_test_operation import AbstractTestOperation

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class TestFileCreateReadmeOperation(AbstractTestOperation):
    missing_file_name: str = "simple-readme.md"

    def _operation_test_assert_applied(self) -> None:
        target_file = self.state_manager.find_by_name_or_fail(self.missing_file_name)
        assert (
            target_file.get_path().exists()
        ), "The target file should have been created"

    def _operation_test_assert_initial(self) -> None:
        target_file = self.state_manager.find_by_name_or_fail(self.missing_file_name)
        assert not target_file.get_path().exists(), "The file should not exist"

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.config_value.readme_content_config_value import (
            ReadmeContentConfigValue,
        )
        from wexample_filestate.const.disk import DiskItemType

        return {
            "children": [
                {
                    "name": self.missing_file_name,
                    "should_exist": True,
                    "type": DiskItemType.FILE,
                    "default_content": ReadmeContentConfigValue(
                        templates=["## Introduction", "## License"], parameters={}
                    ),
                }
            ]
        }
