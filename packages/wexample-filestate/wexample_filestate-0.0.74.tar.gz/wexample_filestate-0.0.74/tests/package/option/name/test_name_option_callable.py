from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_test_operation import AbstractTestOperation

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class TestNameOptionCallable(AbstractTestOperation):
    """Test NameOption with callable/function value."""

    expected_name: str = "dynamic-name.txt"

    def _operation_test_assert_applied(self) -> None:
        # Verify the file exists with the dynamically generated name
        file_path = self._get_absolute_path_from_state_manager(self.expected_name)
        self._assert_file_exists(file_path=file_path, positive=True)

    def _operation_test_assert_initial(self) -> None:
        # Verify the file doesn't exist initially
        file_path = self._get_absolute_path_from_state_manager(self.expected_name)
        self._assert_file_exists(file_path=file_path, positive=False)

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.const.disk import DiskItemType

        def dynamic_name_generator(option) -> str:
            return self.expected_name

        return {
            "children": [
                {
                    "name": dynamic_name_generator,
                    "should_exist": True,
                    "type": DiskItemType.FILE,
                    "content": "test content with dynamic name",
                }
            ]
        }
