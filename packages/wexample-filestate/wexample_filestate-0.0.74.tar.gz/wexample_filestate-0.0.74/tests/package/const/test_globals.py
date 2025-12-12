from __future__ import annotations

import re

from wexample_filestate.testing.abstract_state_manager_test import (
    AbstractStateManagerTest,
)


class TestGlobals(AbstractStateManagerTest):
    """Test global constants and patterns."""

    def test_name_pattern_any_item(self, tmp_path) -> None:
        """Test NAME_PATTERN_ANY_ITEM pattern."""
        from wexample_filestate.const.globals import NAME_PATTERN_ANY_ITEM

        self._setup_with_tmp_path(tmp_path)

        pattern = re.compile(NAME_PATTERN_ANY_ITEM)

        # Should match normal files and directories
        assert pattern.match("file.txt"), "Should match normal file"
        assert pattern.match("directory"), "Should match normal directory"
        assert pattern.match("test-file"), "Should match file with dash"
        assert pattern.match("test_file"), "Should match file with underscore"
        assert pattern.match("123"), "Should match numeric name"

        # Should NOT match . and ..
        assert not pattern.match("."), "Should not match current directory"
        assert not pattern.match(".."), "Should not match parent directory"

        # Should match hidden files (starting with dot but not . or ..)
        assert pattern.match(".hidden"), "Should match hidden files"
        assert pattern.match(".gitignore"), "Should match .gitignore"

    def test_name_pattern_no_leading_dot(self, tmp_path) -> None:
        """Test NAME_PATTERN_NO_LEADING_DOT pattern."""
        from wexample_filestate.const.globals import NAME_PATTERN_NO_LEADING_DOT

        self._setup_with_tmp_path(tmp_path)

        pattern = re.compile(NAME_PATTERN_NO_LEADING_DOT)

        # Should match normal files and directories
        assert pattern.match("file.txt"), "Should match normal file"
        assert pattern.match("directory"), "Should match normal directory"
        assert pattern.match("test-file"), "Should match file with dash"
        assert pattern.match("test_file"), "Should match file with underscore"
        assert pattern.match("123"), "Should match numeric name"

        # Should NOT match anything starting with dot
        assert not pattern.match("."), "Should not match current directory"
        assert not pattern.match(".."), "Should not match parent directory"
        assert not pattern.match(".hidden"), "Should not match hidden files"
        assert not pattern.match(".gitignore"), "Should not match .gitignore"

    def test_patterns_with_real_files(self, tmp_path) -> None:
        """Test patterns with real file system entries."""
        from wexample_filestate.const.globals import (
            NAME_PATTERN_ANY_ITEM,
            NAME_PATTERN_NO_LEADING_DOT,
        )

        self._setup_with_tmp_path(tmp_path)

        # Create test files and directories
        (tmp_path / "normal_file.txt").touch()
        (tmp_path / "normal_dir").mkdir()
        (tmp_path / ".hidden_file").touch()
        (tmp_path / ".hidden_dir").mkdir()

        any_pattern = re.compile(NAME_PATTERN_ANY_ITEM)
        no_dot_pattern = re.compile(NAME_PATTERN_NO_LEADING_DOT)

        for item in tmp_path.iterdir():
            item_name = item.name

            if item_name.startswith("."):
                # Hidden items
                assert any_pattern.match(
                    item_name
                ), f"ANY_ITEM should match {item_name}"
                assert not no_dot_pattern.match(
                    item_name
                ), f"NO_LEADING_DOT should not match {item_name}"
            else:
                # Normal items
                assert any_pattern.match(
                    item_name
                ), f"ANY_ITEM should match {item_name}"
                assert no_dot_pattern.match(
                    item_name
                ), f"NO_LEADING_DOT should match {item_name}"
