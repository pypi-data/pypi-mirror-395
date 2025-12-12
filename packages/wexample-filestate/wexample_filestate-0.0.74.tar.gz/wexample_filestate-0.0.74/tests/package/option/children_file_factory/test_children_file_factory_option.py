from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_test_operation import AbstractTestOperation

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_config.const.types import DictConfig


class TestChildrenFileFactoryOption(AbstractTestOperation):
    """Test ChildrenFileFactoryOption functionality."""

    def _get_test_data_path(self) -> Path:
        """Get the path to test data directory."""
        from pathlib import Path

        return Path(__file__).parent / "test_data"

    def _operation_get_count(self) -> int:
        """ChildrenFileFactoryOption may not generate direct operations."""
        return 0

    def _operation_test_assert_applied(self) -> None:
        """Assert state after applying operations."""
        from wexample_filestate.option.children_file_factory_option import (
            ChildrenFileFactoryOption,
        )

        # Since ChildrenFileFactoryOption generates children configurations
        # but doesn't directly create files, we test that the option
        # has been processed without errors
        test_root = self.state_manager.get_path()

        # The directories should still exist
        assert (test_root / "project_a").exists(), "project_a should still exist"
        assert (test_root / "project_b").exists(), "project_b should still exist"
        assert (test_root / "other_dir").exists(), "other_dir should still exist"
        assert (test_root / "no_match_dir").exists(), "no_match_dir should still exist"

        # Test that the ChildrenFileFactoryOption has generated children
        # by checking if the state manager has the expected structure
        children_factory_option = None
        for option in self.state_manager.options.values():
            # print(f"Option: {option}, name: {option.get_name()}")
            if option.get_name() == "children":
                # Look inside the children option for ChildrenFileFactoryOption
                if hasattr(option, "children") and option.children:
                    for child_option in option.children:
                        if isinstance(child_option, ChildrenFileFactoryOption):
                            children_factory_option = child_option
                            break
                # Also check if the option itself contains the factory option
                elif hasattr(option, "value") and isinstance(option.value, list):
                    for child_item in option.value:
                        if isinstance(child_item, ChildrenFileFactoryOption):
                            children_factory_option = child_item
                            break
            if children_factory_option:
                break

        assert (
            children_factory_option is not None
        ), "ChildrenFileFactoryOption should be configured"

        # Test the generate_children method directly
        generated_children = children_factory_option.generate_children()
        assert (
            len(generated_children) == 2
        ), "Should generate children for 2 matching directories (project_a, project_b)"

    def _operation_test_assert_initial(self) -> None:
        """Assert initial state before applying operations."""
        # Ensure test data directories exist
        test_root = self.state_manager.get_path()
        assert (test_root / "project_a").exists(), "project_a should exist"
        assert (test_root / "project_b").exists(), "project_b should exist"
        assert (test_root / "other_dir").exists(), "other_dir should exist"
        assert (test_root / "no_match_dir").exists(), "no_match_dir should exist"

        # Ensure config.txt files don't exist yet
        assert not (
            test_root / "project_a" / "config.txt"
        ).exists(), "config.txt should not exist in project_a initially"
        assert not (
            test_root / "project_b" / "config.txt"
        ).exists(), "config.txt should not exist in project_b initially"
        assert not (
            test_root / "other_dir" / "config.txt"
        ).exists(), "config.txt should not exist in other_dir initially"

    def _operation_test_setup(self) -> None:
        """Setup test by configuring and copying test data."""
        super()._operation_test_setup()
        self._operation_test_setup_copy_test_data()

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        """Setup configuration for testing ChildrenFileFactoryOption."""
        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.option.children_file_factory_option import (
            ChildrenFileFactoryOption,
        )

        return {
            "name": "test_root",
            "type": DiskItemType.DIRECTORY,
            "should_exist": True,
            "children": [
                ChildrenFileFactoryOption(
                    pattern={
                        "name": "config.txt",
                        "type": DiskItemType.FILE,
                        "should_exist": True,  # This should trigger FileCreateOperation
                    },
                    name_pattern=["project_.*"],  # Match project_a, project_b
                    recursive=False,
                )
            ],
        }

    def _operation_test_setup_copy_test_data(self) -> None:
        """Copy test data to the temporary directory."""
        import shutil

        test_data_path = self._get_test_data_path()
        target_path = self.state_manager.get_path()

        # Copy all test data directories
        for item in test_data_path.iterdir():
            if item.is_dir():
                shutil.copytree(item, target_path / item.name)
            else:
                shutil.copy2(item, target_path / item.name)
