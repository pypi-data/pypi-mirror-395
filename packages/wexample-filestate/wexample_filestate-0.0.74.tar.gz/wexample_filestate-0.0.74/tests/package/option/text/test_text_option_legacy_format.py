from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_test_operation import AbstractTestOperation

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class TestTextOptionLegacyFormat(AbstractTestOperation):
    initial_content: str = "Initial content"  # No leading spaces, only needs newline
    test_file_name: str = "test-text-legacy-list.txt"

    def _operation_test_assert_applied(self) -> None:
        from wexample_helpers.helpers.file import file_read

        target_file = self.state_manager.find_by_name_or_fail(self.test_file_name)
        content = file_read(target_file.get_path())

        # Check content ends with newline (legacy format support)
        assert (
            content == "Initial content\n"
        ), f"Content should end with newline, got: {repr(content)}"

    def _operation_test_assert_initial(self) -> None:
        from wexample_helpers.helpers.file import file_read

        target_file = self.state_manager.find_by_name_or_fail(self.test_file_name)
        content = file_read(target_file.get_path())

        assert (
            content == self.initial_content
        ), f"Initial content should be unchanged, got: {repr(content)}"

    def _operation_test_setup(self) -> None:
        from wexample_helpers.helpers.file import file_write

        super()._operation_test_setup()

        target_file = self.state_manager.find_by_name_or_fail(self.test_file_name)
        file_write(target_file.get_path(), self.initial_content)

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.const.disk import DiskItemType

        return {
            "children": [
                {
                    "name": self.test_file_name,
                    "type": DiskItemType.FILE,
                    "text": ["trim", "end_new_line"],
                },
            ]
        }
