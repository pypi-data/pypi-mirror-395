from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_test_operation import AbstractTestOperation

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class TestNameFormatOptionCaseFormat(AbstractTestOperation):
    """Test NameFormatOption with case format validation."""

    test_name: str = "TestFile.txt"

    def _operation_test_assert_applied(self) -> None:
        # Verify the file exists
        file_path = self._get_absolute_path_from_state_manager(self.test_name)
        self._assert_file_exists(file_path=file_path, positive=True)

    def _operation_test_assert_initial(self) -> None:
        # Verify the file doesn't exist initially
        file_path = self._get_absolute_path_from_state_manager(self.test_name)
        self._assert_file_exists(file_path=file_path, positive=False)

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.const.disk import DiskItemType

        return {
            "children": [
                {
                    "name": {"value": self.test_name, "case_format": "lowercase"},
                    "should_exist": True,
                    "type": DiskItemType.FILE,
                    "content": "test content",
                }
            ]
        }


class TestNameFormatOptionRegex(AbstractTestOperation):
    """Test NameFormatOption with regex validation."""

    test_name: str = "valid123.txt"

    def _operation_test_assert_applied(self) -> None:
        # Verify the file exists
        file_path = self._get_absolute_path_from_state_manager(self.test_name)
        self._assert_file_exists(file_path=file_path, positive=True)

    def _operation_test_assert_initial(self) -> None:
        # Verify the file doesn't exist initially
        file_path = self._get_absolute_path_from_state_manager(self.test_name)
        self._assert_file_exists(file_path=file_path, positive=False)

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.const.disk import DiskItemType

        return {
            "children": [
                {
                    "name": {"value": self.test_name, "regex": r"^[a-z]+\d+\.txt$"},
                    "should_exist": True,
                    "type": DiskItemType.FILE,
                    "content": "test content",
                }
            ]
        }


class TestNameFormatOptionPrefixSuffix(AbstractTestOperation):
    """Test NameFormatOption with prefix and suffix validation."""

    test_name: str = "prefix_test_suffix.txt"

    def _operation_test_assert_applied(self) -> None:
        # Verify the file exists
        file_path = self._get_absolute_path_from_state_manager(self.test_name)
        self._assert_file_exists(file_path=file_path, positive=True)

    def _operation_test_assert_initial(self) -> None:
        # Verify the file doesn't exist initially
        file_path = self._get_absolute_path_from_state_manager(self.test_name)
        self._assert_file_exists(file_path=file_path, positive=False)

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.const.disk import DiskItemType

        return {
            "children": [
                {
                    "name": {
                        "value": self.test_name,
                        "prefix": "prefix_",
                        "suffix": "_suffix.txt",
                    },
                    "should_exist": True,
                    "type": DiskItemType.FILE,
                    "content": "test content",
                }
            ]
        }
