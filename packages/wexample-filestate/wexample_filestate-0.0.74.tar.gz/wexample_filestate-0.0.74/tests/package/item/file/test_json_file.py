from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from wexample_filestate.testing.abstract_structured_file_test import (
    AbstractStructuredFileTest,
)

if TYPE_CHECKING:
    from wexample_filestate.item.file.json_file import JsonFile


class TestJsonFile(AbstractStructuredFileTest):
    """Test JsonFile functionality - smoke tests for JSON file handling."""

    def test_json_file_dumps_none_content(self, tmp_path) -> None:
        """Test JsonFile dumps method with None input."""
        self._setup_with_tmp_path(tmp_path)

        json_file = self._create_file("sample.json", tmp_path)

        # Test with None content
        result = json_file.dumps(None)
        assert result == "{}", "Should return empty JSON object for None input"

        # Should be valid JSON
        parsed = json.loads(result)
        assert parsed == {}, "Should parse to empty dict"

    # JSON-specific tests that are not covered by the abstract class
    def test_json_file_formatting(self, tmp_path) -> None:
        """Test JsonFile produces properly formatted output."""
        self._setup_with_tmp_path(tmp_path)

        json_file = self._create_file(self._get_sample_filename(), tmp_path)

        # Test data
        test_data = {"name": "test", "config": {"debug": True}}

        # Serialize to JSON format
        json_content = json_file.dumps(test_data)

        # Test formatting (should be indented)
        assert "  " in json_content, "Should be indented (pretty printed)"
        assert json_content.count("\n") > 1, "Should be multi-line formatted"

    def test_json_file_loads_error_handling(self, tmp_path) -> None:
        """Test JsonFile error handling in loads method."""
        self._setup_with_tmp_path(tmp_path)

        json_file = self._create_file("sample.json", tmp_path)

        # Test with invalid JSON (non-strict mode)
        result = json_file.loads("{ invalid json }", strict=False)
        assert result == {}, "Should return empty dict on error in non-strict mode"

        # Test with empty content
        result = json_file.loads("", strict=False)
        assert result == {}, "Should handle empty content"

        # Test strict mode raises exception
        try:
            json_file.loads("{ invalid json }", strict=True)
            assert False, "Should raise exception in strict mode"
        except Exception:
            pass  # Expected

    def test_json_file_unicode_handling(self, tmp_path) -> None:
        """Test JsonFile handles Unicode characters correctly."""
        self._setup_with_tmp_path(tmp_path)

        json_file = self._create_file("sample.json", tmp_path)

        # Test data with Unicode
        test_data = {
            "name": "tést-àpp",
            "description": "Ünïcödé tëst 🚀",
            "emoji": "🎉✨🔥",
        }

        # Serialize and parse back
        serialized = json_file.dumps(test_data)
        reparsed = json_file.loads(serialized)

        # Should preserve Unicode characters
        assert reparsed == test_data, "Unicode characters should be preserved"
        assert "tést-àpp" in serialized, "Unicode should be in output"
        assert "🚀" in serialized, "Emoji should be in output"

    def _assert_roundtrip_equality(self, original: Any, roundtrip: Any) -> None:
        """Assert JSON roundtrip equality."""
        # For JSON, we expect exact equality
        assert original == roundtrip, "JSON roundtrip should preserve data exactly"

    def _get_expected_extension(self) -> str:
        """Get the expected file extension."""
        return "json"

    def _get_extension_constant_name(self) -> str:
        """Get the extension constant name."""
        return "EXTENSION_JSON"

    def _get_file_class(self) -> type[JsonFile]:
        """Get the JsonFile class."""
        from wexample_filestate.item.file.json_file import JsonFile

        return JsonFile

    def _get_file_type_name(self) -> str:
        """Get the file type name for messages."""
        return "JsonFile"

    def _get_sample_filename(self) -> str:
        """Get the sample test file name."""
        return "sample.json"

    def _validate_parsed_content(self, parsed: dict) -> None:
        """Validate the structure of parsed JSON content."""
        # Call parent validation
        super()._validate_parsed_content(parsed)

        # JSON-specific validations
        assert "dependencies" in parsed, "Should parse dependencies field"
        assert "scripts" in parsed, "Should parse scripts field"

        # Test specific values
        assert parsed["name"] == "test-project"
        assert parsed["version"] == "1.0.0"
        assert parsed["author"] == "Test Author"
        assert parsed["license"] == "MIT"

        # Test nested objects
        assert isinstance(parsed["dependencies"], dict), "Dependencies should be dict"
        assert "express" in parsed["dependencies"]
        assert "lodash" in parsed["dependencies"]

        assert isinstance(parsed["scripts"], dict), "Scripts should be dict"
        assert "start" in parsed["scripts"]
        assert "test" in parsed["scripts"]
