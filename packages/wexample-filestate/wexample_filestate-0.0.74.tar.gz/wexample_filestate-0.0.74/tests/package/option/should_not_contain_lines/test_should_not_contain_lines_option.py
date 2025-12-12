from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_test_operation import AbstractTestOperation

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class TestShouldNotContainLinesOption(AbstractTestOperation):
    forbidden_lines: list = ["Forbidden line 1", "Forbidden line 2"]
    initial_content: str = (
        "Initial line 1\nForbidden line 1\nInitial line 2\nForbidden line 2\nInitial line 3"
    )
    test_file_name: str = "test-should-not-contain-lines.txt"

    def _operation_test_assert_applied(self) -> None:
        from wexample_helpers.helpers.file import file_read

        target_file = self.state_manager.find_by_name_or_fail(self.test_file_name)
        content = file_read(target_file.get_path())
        lines = content.splitlines()

        # Check initial content is preserved (non-forbidden lines)
        assert "Initial line 1" in lines, "Original content should be preserved"
        assert "Initial line 2" in lines, "Original content should be preserved"
        assert "Initial line 3" in lines, "Original content should be preserved"

        # Check forbidden lines were removed
        for forbidden_line in self.forbidden_lines:
            assert (
                forbidden_line not in lines
            ), f"Forbidden line '{forbidden_line}' should have been removed"

    def _operation_test_assert_initial(self) -> None:
        from wexample_helpers.helpers.file import file_read

        target_file = self.state_manager.find_by_name_or_fail(self.test_file_name)
        content = file_read(target_file.get_path())

        # Check initial content is correct
        assert content == self.initial_content, "Initial content should be unchanged"

        # Check forbidden lines are present initially
        for line in self.forbidden_lines:
            assert (
                line in content.splitlines()
            ), f"Forbidden line '{line}' should be present initially"

    def _operation_test_setup(self) -> None:
        from wexample_helpers.helpers.file import file_write

        super()._operation_test_setup()

        # Create file with initial content including forbidden lines
        target_file = self.state_manager.find_by_name_or_fail(self.test_file_name)
        file_write(target_file.get_path(), self.initial_content)

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.const.disk import DiskItemType

        return {
            "children": [
                {
                    "name": self.test_file_name,
                    "type": DiskItemType.FILE,
                    "should_not_contain_lines": self.forbidden_lines,
                },
            ]
        }
