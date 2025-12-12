from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_state_manager_test import (
    AbstractStateManagerTest,
)

if TYPE_CHECKING:
    from pathlib import Path


class TestChildrenFileFactoryOptionUnit(AbstractStateManagerTest):
    """Unit tests for ChildrenFileFactoryOption functionality."""

    def test_children_file_factory_option_creation(self, tmp_path) -> None:
        """Test ChildrenFileFactoryOption can be created."""
        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.option.children_file_factory_option import (
            ChildrenFileFactoryOption,
        )

        self._setup_with_tmp_path(tmp_path)

        option = ChildrenFileFactoryOption(
            pattern={
                "name": "test.txt",
                "type": DiskItemType.FILE,
                "should_exist": True,
            },
            name_pattern=["project_.*"],
            recursive=False,
        )

        assert option is not None, "ChildrenFileFactoryOption should be created"
        assert option.recursive is False, "recursive should be False"
        assert option.pattern["name"] == "test.txt", "pattern name should be set"

    def test_children_file_factory_option_pattern_matching(self, tmp_path) -> None:
        """Test ChildrenFileFactoryOption pattern matching logic."""
        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.option.children_file_factory_option import (
            ChildrenFileFactoryOption,
        )

        self._setup_with_tmp_path(tmp_path)

        # Create the option with specific pattern
        option = ChildrenFileFactoryOption(
            pattern={
                "name": "test.txt",
                "type": DiskItemType.FILE,
            },
            name_pattern=["project_.*"],
            recursive=False,
        )

        # Test pattern matching directly
        # Debug: let's see what the actual pattern matching does
        import re

        pattern_str = "project_.*"
        pattern = re.compile(pattern_str)

        # Test the regex directly first
        assert pattern.match("project_a") is not None, "Regex should match project_a"
        assert pattern.match("project_b") is not None, "Regex should match project_b"
        assert pattern.match("other_dir") is None, "Regex should not match other_dir"

        # Now test the option's method
        assert (
            option._path_match_patterns("project_a") is True
        ), "Should match project_a"
        assert (
            option._path_match_patterns("project_b") is True
        ), "Should match project_b"
        assert (
            option._path_match_patterns("other_dir") is False
        ), "Should not match other_dir"

    def test_children_file_factory_option_pattern_matching_no_pattern(
        self, tmp_path
    ) -> None:
        """Test _path_match_patterns with no pattern (should match all)."""
        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.option.children_file_factory_option import (
            ChildrenFileFactoryOption,
        )

        self._setup_with_tmp_path(tmp_path)

        # Create the option without name pattern
        option = ChildrenFileFactoryOption(
            pattern={
                "name": "test.txt",
                "type": DiskItemType.FILE,
                # No name_pattern
            },
            recursive=False,
        )

        # Test pattern matching - should match all when no pattern
        assert (
            option._path_match_patterns("project_a") is True
        ), "Should match project_a when no pattern"
        assert (
            option._path_match_patterns("other_dir") is True
        ), "Should match other_dir when no pattern"
        assert (
            option._path_match_patterns("anything") is True
        ), "Should match anything when no pattern"

    def test_children_file_factory_option_recursive_property(self, tmp_path) -> None:
        """Test ChildrenFileFactoryOption recursive property."""
        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.option.children_file_factory_option import (
            ChildrenFileFactoryOption,
        )

        self._setup_with_tmp_path(tmp_path)

        # Test recursive=True
        option_recursive = ChildrenFileFactoryOption(
            pattern={
                "name": "test.txt",
                "type": DiskItemType.FILE,
            },
            recursive=True,
        )

        assert option_recursive.recursive is True, "recursive should be True"

        # Test recursive=False (default)
        option_non_recursive = ChildrenFileFactoryOption(
            pattern={
                "name": "test.txt",
                "type": DiskItemType.FILE,
            },
            recursive=False,
        )

        assert option_non_recursive.recursive is False, "recursive should be False"

    def _get_test_data_path(self) -> Path:
        """Get the path to test data directory."""
        from pathlib import Path

        return Path(__file__).parent / "test_data"

    def _setup_test_data(self, tmp_path: Path) -> None:
        """Setup test data directories."""
        import shutil

        test_data_path = self._get_test_data_path()

        # Copy all test data directories
        for item in test_data_path.iterdir():
            if item.is_dir():
                shutil.copytree(item, tmp_path / item.name)
            else:
                shutil.copy2(item, tmp_path / item.name)
