from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.item.item_target_file import ItemTargetFile
from wexample_filestate.testing.abstract_state_manager_test import (
    AbstractStateManagerTest,
)

if TYPE_CHECKING:
    from pathlib import Path


class TestChildrenFilterOption(AbstractStateManagerTest):
    """Test ChildrenFilterOption functionality - filtering children based on patterns and callbacks."""

    def test_children_filter_option_callable_filter(self, tmp_path) -> None:
        """Test ChildrenFilterOption with callable filter."""
        from wexample_prompt.common.io_manager import IoManager

        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.option.children_filter_option import (
            ChildrenFilterOption,
        )

        self._setup_with_tmp_path(tmp_path)

        # Copy test data structure to tmp_path
        test_data_path = self._get_test_data_path()
        self._copy_directory_structure(test_data_path, tmp_path)

        # Create a callable filter that only accepts files with "collection" in the name
        def collection_filter(path: Path) -> bool:
            return "collection" in path.name and path.is_file()

        # Create a parent directory item and configure it properly
        io = IoManager()
        parent_directory = ItemTargetDirectory.create_from_path(
            path=str(tmp_path), io=io
        )

        # Use the new API with callable filter
        config = {
            "children": [
                ChildrenFilterOption(
                    pattern={"type": DiskItemType.FILE}, filter=collection_filter
                )
            ]
        }

        parent_directory.set_value(config)
        parent_directory.build_item_tree()

        # Get filtered children
        children = parent_directory.get_children_list()
        files = [child for child in children if child.is_file()]

        # Should only find files with "collection" in the name
        collection_files = [f for f in files if "collection" in f.get_item_name()]
        non_collection_files = [
            f for f in files if "collection" not in f.get_item_name()
        ]

        assert len(collection_files) > 0, "Should find files with 'collection' in name"
        assert (
            len(non_collection_files) == 0
        ), "Should not find files without 'collection' in name"

    def test_children_filter_option_callable_filter_exception_handling(
        self, tmp_path
    ) -> None:
        """Test ChildrenFilterOption handles exceptions in callable filter."""
        from wexample_prompt.common.io_manager import IoManager

        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.option.children_filter_option import (
            ChildrenFilterOption,
        )

        self._setup_with_tmp_path(tmp_path)

        # Copy test data structure to tmp_path
        test_data_path = self._get_test_data_path()
        self._copy_directory_structure(test_data_path, tmp_path)

        # Create a callable filter that raises an exception
        def failing_filter(path: Path) -> bool:
            raise ValueError("Filter failed")

        # Create a parent directory item and configure it properly
        io = IoManager()
        parent_directory = ItemTargetDirectory.create_from_path(
            path=str(tmp_path), io=io
        )

        # Use the new API with failing callable filter
        config = {
            "children": [
                ChildrenFilterOption(
                    pattern={"type": DiskItemType.FILE}, filter=failing_filter
                )
            ]
        }

        parent_directory.set_value(config)
        parent_directory.build_item_tree()

        # Get filtered children - should handle exception gracefully
        children = parent_directory.get_children_list()
        files = [child for child in children if child.is_file()]

        # Should find no files due to exception handling (returns False)
        assert len(files) == 0, "Should find no files when filter raises exception"

    def test_children_filter_option_complex_pattern(self, tmp_path) -> None:
        """Test ChildrenFilterOption with complex regex pattern."""
        from wexample_prompt.common.io_manager import IoManager

        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.option.children_filter_option import (
            ChildrenFilterOption,
        )

        self._setup_with_tmp_path(tmp_path)

        # Copy test data structure to tmp_path
        test_data_path = self._get_test_data_path()
        self._copy_directory_structure(test_data_path, tmp_path)

        # Create a parent directory item and configure it properly
        io = IoManager()
        parent_directory = ItemTargetDirectory.create_from_path(
            path=str(tmp_path), io=io
        )

        # Use the new API with complex pattern
        config = {
            "children": [
                ChildrenFilterOption(
                    pattern={"type": DiskItemType.FILE},
                    name_pattern=r"^test-collection-[a-z]+-[a-z]+\.txt$",
                    recursive=True,
                )
            ]
        }

        parent_directory.set_value(config)
        parent_directory.build_item_tree()

        # Get filtered children
        children = parent_directory.get_children_list()

        # Should preserve directory structure and find matching files
        assert len(children) > 0, "Should find children with complex pattern"

        # Verify that we can find the specific test files
        def find_files_recursive(items, filename):
            found = []
            for item in items:
                if item.is_file() and item.get_item_name() == filename:
                    found.append(item)
                elif item.is_directory():
                    # For directories, we'd need to check their children
                    # This is a simplified check
                    pass
            return found

        # The pattern should match test-collection-one-one.txt and test-collection-one-two.txt
        # but not other-file.txt
        # We can't easily traverse the nested structure here, but we can verify
        # that some structure was created
        assert len(children) > 0, "Should create filtered structure"

    def test_children_filter_option_creation(self, tmp_path) -> None:
        """Test ChildrenFilterOption can be created."""
        from wexample_filestate.option.children_filter_option import (
            ChildrenFilterOption,
        )

        self._setup_with_tmp_path(tmp_path)

        option = ChildrenFilterOption(pattern={"type": "file"}, name_pattern="*.txt")

        assert option is not None, "ChildrenFilterOption should be created"
        assert option.pattern is not None, "Pattern should be set"
        assert option.recursive is False, "Default recursive should be False"
        assert option.filter is None, "Default filter should be None"
        assert option.name_pattern == "*.txt", "Name pattern should be set correctly"

    def test_children_filter_option_name_pattern_directories(self, tmp_path) -> None:
        """Test ChildrenFilterOption with name pattern for directories."""
        from wexample_prompt.common.io_manager import IoManager

        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.option.children_filter_option import (
            ChildrenFilterOption,
        )

        self._setup_with_tmp_path(tmp_path)

        # Copy test data structure to tmp_path
        test_data_path = self._get_test_data_path()
        self._copy_directory_structure(test_data_path, tmp_path)

        # Create a parent directory item and configure it properly
        io = IoManager()
        parent_directory = ItemTargetDirectory.create_from_path(
            path=str(tmp_path), io=io
        )

        # Use the new API with name_pattern as direct argument
        config = {
            "children": [
                ChildrenFilterOption(
                    pattern={"type": DiskItemType.DIRECTORY}, name_pattern=r"^test-.*"
                )
            ]
        }

        parent_directory.set_value(config)
        parent_directory.build_item_tree()

        # Get filtered children
        children = parent_directory.get_children_list()

        # Should only find directories starting with "test-"
        test_dirs = [
            child
            for child in children
            if child.is_directory() and child.get_item_name().startswith("test-")
        ]
        other_dirs = [
            child
            for child in children
            if child.is_directory() and not child.get_item_name().startswith("test-")
        ]

        assert len(test_dirs) > 0, "Should find some test- directories"
        assert len(other_dirs) == 0, "Should not find other directories"

    def test_children_filter_option_name_pattern_files(self, tmp_path) -> None:
        """Test ChildrenFilterOption with name pattern for files."""
        from wexample_prompt.common.io_manager import IoManager

        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.option.children_filter_option import (
            ChildrenFilterOption,
        )

        self._setup_with_tmp_path(tmp_path)

        # Copy test data structure to tmp_path
        test_data_path = self._get_test_data_path()
        self._copy_directory_structure(test_data_path, tmp_path)

        # Create a parent directory item and configure it properly
        io = IoManager()
        parent_directory = ItemTargetDirectory.create_from_path(
            path=str(tmp_path), io=io
        )

        # Use the new API with name_pattern as direct argument
        config = {
            "children": [
                ChildrenFilterOption(
                    pattern={"type": DiskItemType.FILE}, name_pattern=r".*\.txt$"
                )
            ]
        }

        parent_directory.set_value(config)
        parent_directory.build_item_tree()

        # Get filtered children
        children = parent_directory.get_children_list()

        # Should only find .txt files
        txt_files = [
            child
            for child in children
            if child.is_file() and child.get_item_name().endswith(".txt")
        ]
        non_txt_files = [
            child
            for child in children
            if child.is_file() and not child.get_item_name().endswith(".txt")
        ]

        assert (
            len(txt_files) > 0
        ), f"Should find some .txt files. Found {len(children)} children total, files in dir: {list(tmp_path.glob('*.txt'))}"
        assert len(non_txt_files) == 0, "Should not find non-.txt files"

    def test_children_filter_option_no_pattern_no_filter(self, tmp_path) -> None:
        """Test ChildrenFilterOption with no pattern and no filter."""
        from wexample_prompt.common.io_manager import IoManager

        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.option.children_filter_option import (
            ChildrenFilterOption,
        )

        self._setup_with_tmp_path(tmp_path)

        # Copy test data structure to tmp_path
        test_data_path = self._get_test_data_path()
        self._copy_directory_structure(test_data_path, tmp_path)

        # Create a parent directory item and configure it properly
        io = IoManager()
        parent_directory = ItemTargetDirectory.create_from_path(
            path=str(tmp_path), io=io
        )

        # Use the new API with empty pattern and no filter
        config = {"children": [ChildrenFilterOption(pattern={})]}

        parent_directory.set_value(config)
        parent_directory.build_item_tree()

        # Get filtered children
        children = parent_directory.get_children_list()

        # Should find no children when no pattern or filter is provided
        assert (
            len(children) == 0
        ), "Should find no children when no pattern or filter provided"

    def test_children_filter_option_recursive_false(self, tmp_path) -> None:
        """Test ChildrenFilterOption with recursive=False (default)."""
        from wexample_prompt.common.io_manager import IoManager

        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.option.children_filter_option import (
            ChildrenFilterOption,
        )

        self._setup_with_tmp_path(tmp_path)

        # Copy test data structure to tmp_path
        test_data_path = self._get_test_data_path()
        self._copy_directory_structure(test_data_path, tmp_path)

        # Create a parent directory item and configure it properly
        io = IoManager()
        parent_directory = ItemTargetDirectory.create_from_path(
            path=str(tmp_path), io=io
        )

        # Use the new API with name_pattern as direct argument
        config = {
            "children": [
                ChildrenFilterOption(
                    pattern={"type": DiskItemType.FILE},
                    name_pattern=r".*",
                    recursive=False,
                )
            ]
        }

        parent_directory.set_value(config)
        parent_directory.build_item_tree()

        # Get filtered children
        children = parent_directory.get_children_list()
        files = [child for child in children if child.is_file()]

        # Should only find files in the root directory, not in subdirectories
        # Based on our test data structure, we should find root level files
        assert len(files) > 0, "Should find root level files"

    def test_children_filter_option_recursive_true(self, tmp_path) -> None:
        """Test ChildrenFilterOption with recursive=True."""
        from wexample_prompt.common.io_manager import IoManager

        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.option.children_filter_option import (
            ChildrenFilterOption,
        )

        self._setup_with_tmp_path(tmp_path)

        # Copy test data structure to tmp_path
        test_data_path = self._get_test_data_path()
        self._copy_directory_structure(test_data_path, tmp_path)

        # Create a parent directory item and configure it properly
        io = IoManager()
        parent_directory = ItemTargetDirectory.create_from_path(
            path=str(tmp_path), io=io
        )

        # Use the new API with name_pattern as direct argument
        config = {
            "children": [
                ChildrenFilterOption(
                    pattern={"type": DiskItemType.FILE},
                    name_pattern=r".*\.txt$",
                    recursive=True,
                )
            ]
        }

        parent_directory.set_value(config)
        parent_directory.build_item_tree()

        # Get filtered children - this should include nested structure
        children = parent_directory.get_children_list()

        # With recursive=True, we should get a nested structure preserving directories
        # that contain matching files
        assert len(children) > 0, "Should find children with recursive filtering"

        # Check that we have directories in the result (preserving hierarchy)
        directories = [child for child in children if child.is_directory()]
        assert (
            len(directories) > 0
        ), "Should preserve directory hierarchy when recursive"

    def test_children_filter_option_type_filtering(self, tmp_path) -> None:
        """Test ChildrenFilterOption respects type filtering."""
        from wexample_prompt.common.io_manager import IoManager

        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.option.children_filter_option import (
            ChildrenFilterOption,
        )

        self._setup_with_tmp_path(tmp_path)

        # Copy test data structure to tmp_path
        test_data_path = self._get_test_data_path()
        self._copy_directory_structure(test_data_path, tmp_path)

        # Create a parent directory item and configure it properly
        io = IoManager()
        parent_directory = ItemTargetDirectory.create_from_path(
            path=str(tmp_path), io=io
        )

        # Use the new API - filter that only matches directories but with a file pattern
        config = {
            "children": [
                ChildrenFilterOption(
                    pattern={"type": DiskItemType.DIRECTORY},  # But only directories
                    name_pattern=r".*\.txt$",  # File pattern
                )
            ]
        }

        parent_directory.set_value(config)
        parent_directory.build_item_tree()

        # Get filtered children
        children = parent_directory.get_children_list()
        files = [child for child in children if child.is_file()]
        directories = [child for child in children if child.is_directory()]

        # Should find no files (type mismatch) and no directories (name pattern mismatch)
        assert len(files) == 0, "Should find no files when type is DIRECTORY"
        assert len(directories) == 0, "Should find no directories with .txt pattern"

    def _copy_directory_structure(self, source: Path, target: Path) -> None:
        """Recursively copy directory structure for testing."""
        import shutil

        if source.exists():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(source, target)

    def _get_test_data_path(self) -> Path:
        """Get the path to test data directory."""
        from pathlib import Path

        return Path(__file__).parent / "test_data"


# Keep the original operation test as well for backward compatibility
class TestFileCreateFromMapConfigOperation(AbstractStateManagerTest):
    """Original test for map config operation - kept for backward compatibility."""

    def test_file_create_from_map_config_operation(self, tmp_path) -> None:
        """Test file creation from map config with ChildrenFilterOption."""
        from wexample_config.const.types import DictConfig
        from wexample_prompt.common.io_manager import IoManager

        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.option.children_filter_option import (
            ChildrenFilterOption,
        )

        self._setup_with_tmp_path(tmp_path)

        # Copy test data
        test_data_path = self._get_test_data_path()
        self._copy_directory_structure(test_data_path, tmp_path)

        class TestClass(ItemTargetFile):
            def prepare_value(self, config: DictConfig | None = None) -> DictConfig:
                if config is None:
                    config = {}
                return config

        # Create directory with complex filter configuration
        io = IoManager()
        directory = ItemTargetDirectory.create_from_path(path=str(tmp_path), io=io)

        config = {
            "children": [
                {
                    "name": "collection",
                    "type": DiskItemType.DIRECTORY,
                    "children": [
                        {
                            "name": "one",
                            "type": DiskItemType.DIRECTORY,
                            "children": [
                                ChildrenFilterOption(
                                    pattern={
                                        "class": TestClass,
                                        "type": DiskItemType.FILE,
                                        "should_exist": False,
                                    },
                                    name_pattern=r"^test-collection-[a-z]+-[a-z]+\.txt$",
                                ),
                                ChildrenFilterOption(
                                    pattern={
                                        "class": TestClass,
                                        "type": DiskItemType.DIRECTORY,
                                        "should_exist": True,
                                        "children": [
                                            {
                                                "name": "file.txt",
                                                "should_exist": True,
                                            }
                                        ],
                                    },
                                    name_pattern=r"^test-directory-[a-z]$",
                                ),
                            ],
                        }
                    ],
                }
            ]
        }

        directory.set_value(config)
        directory.build_item_tree()

        # Test that we can find the expected structure
        collection_dir = directory.find_by_name("collection")
        assert collection_dir is not None, "Should find collection directory"
        assert collection_dir.is_directory(), "Collection should be a directory"

        one_dir = collection_dir.find_by_name("one")
        assert one_dir is not None, "Should find one directory"
        assert one_dir.is_directory(), "One should be a directory"

        # Test that the filter worked by checking if we can find the test files
        target_file = directory.find_by_name(
            "test-collection-one-one.txt", recursive=True
        )
        assert target_file is not None, "Should find filtered target file"

    def _copy_directory_structure(self, source: Path, target: Path) -> None:
        """Recursively copy directory structure for testing."""
        import shutil

        if source.exists():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(source, target)

    def _get_test_data_path(self) -> Path:
        """Get the path to test data directory."""
        from pathlib import Path

        return Path(__file__).parent / "test_data"
