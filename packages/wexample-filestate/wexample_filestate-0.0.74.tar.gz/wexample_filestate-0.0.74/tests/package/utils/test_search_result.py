from __future__ import annotations

import re
from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_state_manager_test import (
    AbstractStateManagerTest,
)

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_filestate.item.item_target_file import ItemTargetFile


class TestSearchResult(AbstractStateManagerTest):
    """Test SearchResult functionality with various search scenarios."""

    def test_create_for_all_matches_literal(self, tmp_path) -> None:
        """Test literal string search with multiple matches."""
        from wexample_filestate.utils.search_result import SearchResult

        self._setup_with_tmp_path(tmp_path)

        item = self._create_item_target_file("simple.txt", tmp_path)
        results = SearchResult.create_for_all_matches("hello", item)

        # Should find "hello" (lowercase) in "Multiple hello occurrences"
        assert (
            len(results) == 1
        ), "Case-sensitive literal search should find 1 'hello' match"
        assert results[0].line == 4, "Should find 'hello' on line 4"
        assert results[0].column == 10, "Should find 'hello' at column 10"

        # Test searching for "Hello" (uppercase)
        results = SearchResult.create_for_all_matches("Hello", item)
        assert len(results) == 2, "Should find 2 'Hello' matches"

        # Check first match details
        first_result = results[0]
        assert first_result.line == 1, "First 'Hello' should be on line 1"
        assert first_result.column == 1, "First 'Hello' should start at column 1"
        assert first_result.searched == "Hello", "Searched string should be preserved"
        assert first_result.item == item, "Item reference should be preserved"

        # Check second match
        second_result = results[1]
        assert second_result.line == 3, "Second 'Hello' should be on line 3"
        assert second_result.column == 1, "Second 'Hello' should start at column 1"

    def test_create_for_all_matches_regex(self, tmp_path) -> None:
        """Test regex search with case-insensitive flag."""
        from wexample_filestate.utils.search_result import SearchResult

        self._setup_with_tmp_path(tmp_path)

        item = self._create_item_target_file("multiline.txt", tmp_path)

        # Case-insensitive regex search for "pattern"
        results = SearchResult.create_for_all_matches(
            r"pattern", item, regex=True, flags=re.IGNORECASE
        )

        assert len(results) == 6, "Should find 6 'pattern' matches (case-insensitive)"

        # Check line positions
        expected_lines = [2, 3, 4, 8, 9, 10]  # Lines where "pattern" appears
        actual_lines = [result.line for result in results]
        assert (
            actual_lines == expected_lines
        ), f"Expected lines {expected_lines}, got {actual_lines}"

    def test_create_for_all_matches_word_boundary(self, tmp_path) -> None:
        """Test regex search with word boundaries."""
        from wexample_filestate.utils.search_result import SearchResult

        self._setup_with_tmp_path(tmp_path)

        item = self._create_item_target_file("code.py", tmp_path)

        # Search for "hello" as a whole word (case-insensitive)
        results = SearchResult.create_for_all_matches(
            r"\bhello\b", item, regex=True, flags=re.IGNORECASE
        )

        # Should find standalone "hello" words, not "hello_function" or "say_hello"
        assert len(results) >= 2, "Should find at least 2 standalone 'hello' words"

        # Verify some matches are not in function names
        content = item.read_text()
        for result in results:
            line_content = content.split("\n")[result.line - 1]
            # The match should be a standalone word, not part of identifier
            assert (
                "hello_function" not in line_content or "hello" in line_content.split()
            ), f"Match on line {result.line} should be standalone word"

    def test_create_one_if_match_found(self, tmp_path) -> None:
        """Test finding first match only."""
        from wexample_filestate.utils.search_result import SearchResult

        self._setup_with_tmp_path(tmp_path)

        item = self._create_item_target_file("simple.txt", tmp_path)
        result = SearchResult.create_one_if_match("Hello", item)

        assert result is not None, "Should find first 'Hello' match"
        assert result.line == 1, "First match should be on line 1"
        assert result.column == 1, "First match should start at column 1"
        assert result.searched == "Hello", "Searched string should be preserved"

    def test_create_one_if_match_not_found(self, tmp_path) -> None:
        """Test when no match is found."""
        from wexample_filestate.utils.search_result import SearchResult

        self._setup_with_tmp_path(tmp_path)

        item = self._create_item_target_file("simple.txt", tmp_path)
        result = SearchResult.create_one_if_match("nonexistent", item)

        assert result is None, "Should return None when no match found"

    def test_create_one_if_match_regex(self, tmp_path) -> None:
        """Test regex search for first match."""
        from wexample_filestate.utils.search_result import SearchResult

        self._setup_with_tmp_path(tmp_path)

        item = self._create_item_target_file("code.py", tmp_path)

        # Find first function definition
        result = SearchResult.create_one_if_match(r"def \w+", item, regex=True)

        assert result is not None, "Should find function definition"
        assert result.line == 1, "First function should be on line 1"
        assert (
            "def hello_function" in item.read_text().split("\n")[0]
        ), "Should match the function definition line"

    def test_deprecated_create_if_match(self, tmp_path) -> None:
        """Test backward compatibility method."""
        from wexample_filestate.utils.search_result import SearchResult

        self._setup_with_tmp_path(tmp_path)

        item = self._create_item_target_file("simple.txt", tmp_path)

        # Test deprecated method still works
        result = SearchResult.create_if_match("Hello", item)

        assert result is not None, "Deprecated method should still work"
        assert result.line == 1, "Should return same result as create_one_if_match"

        # Should be equivalent to create_one_if_match
        new_result = SearchResult.create_one_if_match("Hello", item)
        assert (
            result.line == new_result.line
        ), "Deprecated method should match new method"
        assert (
            result.column == new_result.column
        ), "Deprecated method should match new method"

    def test_empty_search_string(self, tmp_path) -> None:
        """Test behavior with empty search string."""
        from wexample_filestate.utils.search_result import SearchResult

        self._setup_with_tmp_path(tmp_path)

        item = self._create_item_target_file("simple.txt", tmp_path)

        # Empty string should return empty list for all matches
        results = SearchResult.create_for_all_matches("", item)
        assert results == [], "Empty search should return empty list"

        # Empty string should return None for single match
        result = SearchResult.create_one_if_match("", item)
        assert result is None, "Empty search should return None"

    def test_line_column_calculation(self, tmp_path) -> None:
        """Test accurate line and column calculation."""
        from wexample_filestate.utils.search_result import SearchResult

        self._setup_with_tmp_path(tmp_path)

        item = self._create_item_target_file("multiline.txt", tmp_path)

        # Search for "Pattern" at beginning of line
        results = SearchResult.create_for_all_matches("Pattern", item)

        # Find the match at "Pattern at the beginning"
        beginning_match = None
        for result in results:
            content_lines = item.read_text().split("\n")
            line_content = content_lines[result.line - 1]
            if line_content.startswith("Pattern"):
                beginning_match = result
                break

        assert beginning_match is not None, "Should find 'Pattern' at beginning of line"
        assert beginning_match.column == 1, "Pattern at beginning should be at column 1"

        # Find match in middle of line
        middle_match = None
        for result in results:
            content_lines = item.read_text().split("\n")
            line_content = content_lines[result.line - 1]
            if "with pattern in" in line_content.lower():
                middle_match = result
                break

        if middle_match:
            # Column should be > 1 for middle match
            assert middle_match.column > 1, "Pattern in middle should have column > 1"

    def _create_item_target_file(self, filename: str, tmp_path: Path) -> ItemTargetFile:
        """Create an ItemTargetFile from a test data file."""
        from wexample_prompt.common.io_manager import IoManager

        from wexample_filestate.item.item_target_file import ItemTargetFile

        # Copy test data file to tmp_path
        test_file = self._get_test_data_path() / filename
        target_file = tmp_path / filename
        target_file.write_text(test_file.read_text())

        # Create ItemTargetFile
        io = IoManager()
        return ItemTargetFile.create_from_path(path=str(target_file), io=io)

    def _get_test_data_path(self) -> Path:
        """Get the path to test data directory."""
        from pathlib import Path

        return Path(__file__).parent / "test_data"
