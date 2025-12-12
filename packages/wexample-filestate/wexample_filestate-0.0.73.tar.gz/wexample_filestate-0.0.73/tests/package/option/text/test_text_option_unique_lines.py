from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_test_operation import AbstractTestOperation

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class TestTextOptionUniqueLines(AbstractTestOperation):
    """Test TextOption with unique_lines only."""

    expected_content: str = "apple\nbanana\ncherry\n"
    initial_content: str = "apple\nbanana\napple\ncherry\nbanana\n"
    test_file_name: str = "test-text-unique-lines.txt"

    def _operation_test_assert_applied(self) -> None:
        from wexample_helpers.helpers.file import file_read

        target_file = self.state_manager.find_by_name_or_fail(self.test_file_name)
        content = file_read(target_file.get_path())

        assert (
            content == self.expected_content
        ), f"Expected unique content, got: {repr(content)}"

    def _operation_test_assert_initial(self) -> None:
        from wexample_helpers.helpers.file import file_read

        target_file = self.state_manager.find_by_name_or_fail(self.test_file_name)
        content = file_read(target_file.get_path())

        assert (
            content == self.initial_content
        ), f"Expected initial content, got: {repr(content)}"

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.const.disk import DiskItemType

        return {
            "children": [
                {
                    "name": self.test_file_name,
                    "should_exist": True,
                    "type": DiskItemType.FILE,
                    "text": {
                        "unique_lines": True,
                    },
                }
            ]
        }
