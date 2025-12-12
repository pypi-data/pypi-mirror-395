from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_test_operation import AbstractTestOperation

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class TestFileCreateFromClassOperation(AbstractTestOperation):
    missing_file_name: str = "simple-readme.md"

    def _operation_get_count(self) -> int:
        return 2  # Creates directory + file

    def _operation_test_assert_applied(self) -> None:
        target_file = self.state_manager.find_by_name_or_fail("test_class_handler")
        assert (
            target_file.get_path().exists()
        ), "The target file should have been created"

    def _operation_test_assert_initial(self) -> None:
        target_file = self.state_manager.find_by_name_or_fail("test_class_handler")
        assert not target_file.get_path().exists(), "The file should not exist"

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_config.const.types import DictConfig

        from wexample_filestate.utils.file_state_manager import FileStateManager

        class TestClassForTestFileCreateFromClassOperation(FileStateManager):
            def prepare_value(self, config: DictConfig | None = None) -> DictConfig:
                from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT

                config.update(
                    {
                        "children": [
                            {
                                "name": TEST_FILE_NAME_SIMPLE_TEXT,
                                "should_exist": True,
                                # Use string instead of enum to test support
                                "type": "file",
                                "default_content": "TEST_CUSTOM_CLASS",
                            }
                        ]
                    }
                )

                return config

        return {
            "children": [
                {
                    "name": "test_class_handler",
                    "should_exist": True,
                    # Use string instead of enum to test support
                    "type": "dir",
                    "class": TestClassForTestFileCreateFromClassOperation,
                }
            ]
        }
