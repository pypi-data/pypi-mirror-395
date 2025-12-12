from __future__ import annotations

from wexample_config.const.types import DictConfig

from wexample_filestate.testing.abstract_test_operation import AbstractTestOperation


class TestShouldExistOptionCreate(AbstractTestOperation):
    missing_dir_name: str = "simple-directory-missing"
    missing_file_name: str = "simple-text-missing.txt"

    def _operation_get_count(self) -> int:
        return 2  # Creates directory + file

    def _operation_test_assert_applied(self) -> None:
        target_dir = self.state_manager.find_by_name_or_fail(self.missing_dir_name)
        target_file = self.state_manager.find_by_name_or_fail(self.missing_file_name)

        assert (
            target_dir.get_path().exists()
        ), "The target directory should have been created"
        assert (
            target_file.get_path().exists()
        ), "The target file should have been created"

    def _operation_test_assert_initial(self) -> None:
        target_dir = self.state_manager.find_by_name_or_fail(self.missing_dir_name)
        target_file = self.state_manager.find_by_name_or_fail(self.missing_file_name)

        assert not target_dir.get_path().exists(), "The directory should not exist"
        assert not target_file.get_path().exists(), "The file should not exist"

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.const.disk import DiskItemType

        return {
            "children": [
                {
                    "name": self.missing_dir_name,
                    "should_exist": True,
                    "type": DiskItemType.DIRECTORY,
                },
                {
                    "name": self.missing_file_name,
                    "should_exist": True,
                    "type": DiskItemType.FILE,
                    "default_content": "This is a test",
                },
            ]
        }
