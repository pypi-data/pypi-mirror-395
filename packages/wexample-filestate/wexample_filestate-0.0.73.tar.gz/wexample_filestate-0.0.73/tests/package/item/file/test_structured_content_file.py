from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.item.file.structured_content_file import StructuredContentFile
from wexample_filestate.testing.abstract_state_manager_test import (
    AbstractStateManagerTest,
)

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_helpers.const.types import StructuredData


class TestStructuredContentFile(AbstractStateManagerTest):
    """Test StructuredContentFile base class functionality."""

    def test_structured_content_file_abstract_methods(self, tmp_path) -> None:
        """Test that concrete implementation provides required abstract methods."""
        self._setup_with_tmp_path(tmp_path)

        structured_file = self._create_concrete_structured_file("sample.json", tmp_path)

        # Test that abstract methods are implemented
        assert hasattr(structured_file, "dumps"), "Should have dumps method"
        assert hasattr(structured_file, "loads"), "Should have loads method"
        assert hasattr(
            structured_file, "_expected_file_name_extension"
        ), "Should have _expected_file_name_extension method"

        # Test that methods are callable
        assert callable(structured_file.dumps), "dumps should be callable"
        assert callable(structured_file.loads), "loads should be callable"
        assert callable(
            structured_file._expected_file_name_extension
        ), "_expected_file_name_extension should be callable"

    def test_structured_content_file_creation(self, tmp_path) -> None:
        """Test StructuredContentFile can be instantiated with concrete implementation."""
        self._setup_with_tmp_path(tmp_path)

        structured_file = self._create_concrete_structured_file("sample.json", tmp_path)

        # Test basic properties
        assert (
            structured_file is not None
        ), "StructuredContentFile should be created successfully"
        assert (
            structured_file._expected_file_name_extension() == "test"
        ), "Extension should be 'test'"

        # Test that it's a StructuredContentFile
        assert isinstance(
            structured_file, StructuredContentFile
        ), "Should be instance of StructuredContentFile"

    def test_structured_content_file_dumps_method(self, tmp_path) -> None:
        """Test StructuredContentFile dumps method works."""
        self._setup_with_tmp_path(tmp_path)

        structured_file = self._create_concrete_structured_file("sample.json", tmp_path)

        # Test dumps with various inputs
        result = structured_file.dumps({"key": "value"})
        assert isinstance(result, str), "dumps should return string"

        result = structured_file.dumps(None)
        assert result == "", "dumps should handle None input"

        result = structured_file.dumps("test content")
        assert "test content" in result, "dumps should handle string input"

    def test_structured_content_file_error_handling(self, tmp_path) -> None:
        """Test StructuredContentFile error handling."""
        self._setup_with_tmp_path(tmp_path)

        # Create a structured file that can raise errors
        class ErrorStructuredFile(StructuredContentFile):
            def dumps(self, content: StructuredData | None) -> str:
                if content == "error":
                    raise ValueError("Test error")
                return str(content or "")

            def loads(self, text: str, strict: bool = False) -> StructuredData:
                if text == "error":
                    if strict:
                        raise ValueError("Test error")
                    return {}
                return {"content": text}

            def _expected_file_name_extension(self) -> str:
                return "test"

        from wexample_prompt.common.io_manager import IoManager

        # Create test file
        test_file = tmp_path / "error_test.txt"
        test_file.write_text("test content")

        io = IoManager()
        error_file = ErrorStructuredFile.create_from_path(path=str(test_file), io=io)

        # Test error handling in loads (non-strict)
        result = error_file.loads("error", strict=False)
        assert result == {}, "Should return empty dict on error in non-strict mode"

        # Test error handling in loads (strict)
        try:
            error_file.loads("error", strict=True)
            assert False, "Should raise exception in strict mode"
        except ValueError:
            pass  # Expected

    def test_structured_content_file_inheritance(self, tmp_path) -> None:
        """Test that StructuredContentFile properly inherits from parent classes."""
        self._setup_with_tmp_path(tmp_path)

        structured_file = self._create_concrete_structured_file("sample.json", tmp_path)

        # Test that it has file-related methods from parent classes
        assert hasattr(structured_file, "read_text"), "Should inherit read_text method"
        assert hasattr(structured_file, "get_path"), "Should inherit get_path method"

        # Test that file operations work
        content = structured_file.read_text()
        assert isinstance(content, str), "read_text should return string"

        path = structured_file.get_path()
        assert path is not None, "get_path should return path"

    def test_structured_content_file_loads_method(self, tmp_path) -> None:
        """Test StructuredContentFile loads method works."""
        self._setup_with_tmp_path(tmp_path)

        structured_file = self._create_concrete_structured_file("sample.json", tmp_path)

        # Test loads with text input
        result = structured_file.loads("test content")
        assert isinstance(result, dict), "loads should return structured data"
        assert "content" in result, "loads should parse content"
        assert result["content"] == "test content", "loads should preserve content"

        # Test loads with empty input
        result = structured_file.loads("")
        assert result == {}, "loads should handle empty input"

    def test_structured_content_file_roundtrip(self, tmp_path) -> None:
        """Test StructuredContentFile roundtrip functionality."""
        self._setup_with_tmp_path(tmp_path)

        structured_file = self._create_concrete_structured_file("sample.json", tmp_path)

        # Test roundtrip with simple data
        original_data = "test content for roundtrip"

        # Serialize and parse back
        serialized = structured_file.dumps(original_data)
        parsed = structured_file.loads(serialized)

        # Should preserve the essence of the data (exact format may vary)
        assert isinstance(parsed, dict), "Parsed data should be structured"
        assert "content" in parsed, "Should contain content key"

    def _create_concrete_structured_file(
        self, filename: str, tmp_path: Path
    ) -> StructuredContentFile:
        """Create a concrete StructuredContentFile implementation for testing."""
        from wexample_prompt.common.io_manager import IoManager

        # Create a concrete implementation for testing
        class TestStructuredFile(StructuredContentFile):
            def dumps(self, content: StructuredData | None) -> str:
                if content is None:
                    return ""
                return str(content)

            def loads(self, text: str, strict: bool = False) -> StructuredData:
                if not text.strip():
                    return {}
                try:
                    # Simple test implementation - just return the text as-is
                    return {"content": text}
                except Exception as e:
                    if strict:
                        raise e
                    return {}

            def _expected_file_name_extension(self) -> str:
                return "test"

        # Copy test data file to tmp_path
        test_file = self._get_test_data_path() / filename
        target_file = tmp_path / filename
        target_file.write_text(test_file.read_text())

        # Create TestStructuredFile
        io = IoManager()
        return TestStructuredFile.create_from_path(path=str(target_file), io=io)

    def _get_test_data_path(self) -> Path:
        """Get the path to test data directory."""
        from pathlib import Path

        return Path(__file__).parent / "test_data"
