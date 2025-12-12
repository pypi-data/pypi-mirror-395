from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_state_manager_test import (
    AbstractStateManagerTest,
)

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_filestate.item.item_target_directory import ItemTargetDirectory


class TestItemTargetDirectory(AbstractStateManagerTest):
    """Test ItemTargetDirectory functionality - directory navigation and traversal."""

    def test_directory_creation(self, tmp_path) -> None:
        """Test ItemTargetDirectory can be created and basic properties work."""
        self._setup_with_tmp_path(tmp_path)

        directory = self._create_directory_item(tmp_path)

        # Test basic properties
        assert directory is not None, "Directory should be created successfully"
        assert directory.is_directory(), "Should be identified as directory"
        assert not directory.is_file(), "Should not be identified as file"
        assert directory.get_path() == tmp_path, "Path should match"

    def test_find_by_path(self, tmp_path) -> None:
        """Test find_by_path() method."""
        self._setup_with_tmp_path(tmp_path)

        directory = self._create_directory_item(tmp_path)

        # Test finding existing files
        file1_path = "file1.txt"
        found_file1 = directory.find_by_path(file1_path)
        assert found_file1 is not None, "Should find file1.txt"
        assert found_file1.get_path().name == file1_path, "Path should match"
        assert found_file1.is_file(), "Should be a file"

        # Test finding existing directory
        subdir1_path = "subdir1"
        found_subdir1 = directory.find_by_path(subdir1_path)
        assert found_subdir1 is not None, "Should find subdir1"
        assert found_subdir1.get_path().name == subdir1_path, "Path should match"
        assert found_subdir1.is_directory(), "Should be a directory"

        # Test finding non-existent path
        non_existent_path = "non_existent.txt"
        found_none = directory.find_by_path(non_existent_path)
        assert found_none is None, "Should not find non-existent file"

    def test_find_by_path_recursive(self, tmp_path) -> None:
        """Test find_by_path(... recursive=True) method."""
        self._setup_with_tmp_path(tmp_path)

        directory = self._create_directory_item(tmp_path)

        # Test finding nested files
        nested_file_path = "subdir1/nested_file1.txt"
        found_nested = directory.find_by_path(nested_file_path, recursive=True)
        assert found_nested is not None, "Should find nested file recursively"
        assert found_nested.get_path().name == "nested_file1.txt", "Path should match"

        # Test finding very deep files
        very_deep_path = "subdir2/subsubdir/very_deep_file.json"
        found_deep = directory.find_by_path(very_deep_path, recursive=True)
        assert found_deep is not None, "Should find very deep file recursively"
        assert found_deep.get_path().name == "very_deep_file.json", "Path should match"

        # Test finding files in root (should still work)
        root_file_path = "file2.json"
        found_root = directory.find_by_path(root_file_path, recursive=True)
        assert found_root is not None, "Should find root file recursively"

        # Test finding non-existent path
        non_existent_path = "subdir1/non_existent.txt"
        found_none = directory.find_by_path(non_existent_path, recursive=True)
        assert found_none is None, "Should not find non-existent file recursively"

    def test_for_each_child_file_recursive(self, tmp_path) -> None:
        """Test for_each_child_file_recursive() method."""
        from wexample_filestate.item.item_target_file import ItemTargetFile

        self._setup_with_tmp_path(tmp_path)

        directory = self._create_directory_item(tmp_path)

        # Collect all files using the convenience method
        files_found = []

        def collect_files(item) -> None:
            files_found.append(item)

        directory.for_each_child_file_recursive(collect_files)

        # Should find all files recursively
        assert len(files_found) >= 5, "Should find at least 5 files recursively"

        # All items should be files
        for item in files_found:
            assert item.is_file(), "All items should be files"
            assert isinstance(
                item, ItemTargetFile
            ), "All items should be ItemTargetFile"

        # Check file extensions variety
        extensions = [item.get_path().suffix for item in files_found]
        assert ".txt" in extensions, "Should find .txt files"
        assert ".json" in extensions, "Should find .json files"
        assert ".yaml" in extensions, "Should find .yaml files"

    def test_for_each_child_of_type(self, tmp_path) -> None:
        """Test for_each_child_of_type() method."""
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.item.item_target_file import ItemTargetFile

        self._setup_with_tmp_path(tmp_path)

        directory = self._create_directory_item(tmp_path)

        # Collect files only
        files_found = []

        def collect_files(item) -> None:
            files_found.append(item)

        directory.for_each_child_of_type(ItemTargetFile, collect_files)

        # Should find files in root directory only (not recursive)
        assert len(files_found) >= 2, "Should find at least 2 files in root"

        # All collected items should be files
        for item in files_found:
            assert item.is_file(), "All items should be files"
            assert isinstance(
                item, ItemTargetFile
            ), "All items should be ItemTargetFile"

        # Collect directories only
        dirs_found = []

        def collect_dirs(item) -> None:
            dirs_found.append(item)

        directory.for_each_child_of_type(ItemTargetDirectory, collect_dirs)

        # Should find directories in root directory only
        assert len(dirs_found) >= 2, "Should find at least 2 directories in root"

        # All collected items should be directories
        for item in dirs_found:
            assert item.is_directory(), "All items should be directories"
            assert isinstance(
                item, ItemTargetDirectory
            ), "All items should be ItemTargetDirectory"

    def test_for_each_child_of_type_recursive(self, tmp_path) -> None:
        """Test for_each_child_of_type_recursive() method."""
        from wexample_filestate.item.item_target_file import ItemTargetFile

        self._setup_with_tmp_path(tmp_path)

        directory = self._create_directory_item(tmp_path)

        # Collect all files recursively
        all_files = []

        def collect_all_files(item) -> None:
            all_files.append(item)

        directory.for_each_child_of_type_recursive(ItemTargetFile, collect_all_files)

        # Should find files in all directories recursively
        assert len(all_files) >= 5, "Should find at least 5 files recursively"

        # Check that we found files from different levels
        file_names = [item.get_item_name() for item in all_files]
        assert "file1.txt" in file_names, "Should find root level file"
        assert "nested_file1.txt" in file_names, "Should find nested file"
        assert "very_deep_file.json" in file_names, "Should find very deep file"

        # All collected items should be files
        for item in all_files:
            assert item.is_file(), "All items should be files"
            assert isinstance(
                item, ItemTargetFile
            ), "All items should be ItemTargetFile"

    def test_for_each_child_recursive(self, tmp_path) -> None:
        """Test for_each_child_recursive() method."""
        self._setup_with_tmp_path(tmp_path)

        directory = self._create_directory_item(tmp_path)

        # Collect all items (files and directories) recursively
        all_items = []

        def collect_all_items(item) -> None:
            all_items.append(item)

        directory.for_each_child_recursive(collect_all_items)

        # Should find both files and directories
        assert len(all_items) >= 8, "Should find at least 8 items recursively"

        # Should have both files and directories
        files = [item for item in all_items if item.is_file()]
        directories = [item for item in all_items if item.is_directory()]

        assert len(files) >= 5, "Should find at least 5 files"
        assert len(directories) >= 3, "Should find at least 3 directories"

        # Check that we traverse the full tree
        item_paths = [str(item.get_path()) for item in all_items]
        assert any("subdir1" in path for path in item_paths), "Should traverse subdir1"
        assert any("subdir2" in path for path in item_paths), "Should traverse subdir2"
        assert any(
            "subsubdir" in path for path in item_paths
        ), "Should traverse subsubdir"

    def test_get_children_list(self, tmp_path) -> None:
        """Test get_children_list() method."""
        self._setup_with_tmp_path(tmp_path)

        directory = self._create_directory_item(tmp_path)

        # Get children
        children = directory.get_children_list()

        # Should have children (files and subdirectories)
        assert len(children) > 0, "Should have children"

        # Check that we have the expected files and directories
        child_names = [child.get_item_name() for child in children]
        assert "file1.txt" in child_names, "Should find file1.txt"
        assert "file2.json" in child_names, "Should find file2.json"
        assert "subdir1" in child_names, "Should find subdir1"
        assert "subdir2" in child_names, "Should find subdir2"

        # Check types
        files = [child for child in children if child.is_file()]
        directories = [child for child in children if child.is_directory()]

        assert len(files) >= 2, "Should have at least 2 files"
        assert len(directories) >= 2, "Should have at least 2 subdirectories"

    def _configure_subdirectories_recursively(
        self, directory: ItemTargetDirectory
    ) -> None:
        """Recursively configure subdirectories to have their children."""
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.option.children_option import ChildrenOption

        for child in directory.get_children_list():
            if child.is_directory() and isinstance(child, ItemTargetDirectory):
                child_path = child.get_path()
                children_configs = []

                # Scan subdirectory and create child configurations
                for item_path in child_path.iterdir():
                    if item_path.is_file():
                        children_configs.append(
                            {
                                "name": item_path.name,
                                "type": "file",
                                "should_exist": True,
                            }
                        )
                    elif item_path.is_dir():
                        children_configs.append(
                            {
                                "name": item_path.name,
                                "type": "directory",
                                "should_exist": True,
                            }
                        )

                # Set children configuration for subdirectory
                if children_configs:
                    child.set_value({ChildrenOption.get_name(): children_configs})
                    child.build_item_tree()

                    # Recurse into subdirectories
                    self._configure_subdirectories_recursively(child)

    def _copy_directory_structure(self, source: Path, target: Path) -> None:
        """Recursively copy directory structure for testing."""
        import shutil

        if source.exists():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(source, target)

    def _create_directory_item(self, tmp_path: Path) -> ItemTargetDirectory:
        """Create an ItemTargetDirectory from test data."""
        from wexample_prompt.common.io_manager import IoManager

        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.option.children_option import ChildrenOption

        # Copy test data structure to tmp_path
        test_data_path = self._get_test_data_path()
        self._copy_directory_structure(test_data_path, tmp_path)

        # Create ItemTargetDirectory
        io = IoManager()
        directory = ItemTargetDirectory.create_from_path(path=str(tmp_path), io=io)

        # Manually create children for testing
        children_configs = []

        # Scan directory and create child configurations
        for item_path in tmp_path.iterdir():
            if item_path.is_file():
                children_configs.append(
                    {"name": item_path.name, "type": "file", "should_exist": True}
                )
            elif item_path.is_dir():
                children_configs.append(
                    {"name": item_path.name, "type": "directory", "should_exist": True}
                )

        # Set children configuration
        if children_configs:
            directory.set_value({ChildrenOption.get_name(): children_configs})

        # Build item tree first
        directory.build_item_tree()

        # Then configure subdirectories recursively
        self._configure_subdirectories_recursively(directory)

        return directory

    def _get_test_data_path(self) -> Path:
        """Get the path to test data directory."""
        from pathlib import Path

        return Path(__file__).parent / "test_data" / "directory_test"
