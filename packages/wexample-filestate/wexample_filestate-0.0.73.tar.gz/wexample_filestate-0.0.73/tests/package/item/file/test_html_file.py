from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_filestate.testing.abstract_content_file_test import (
    AbstractContentFileTest,
)

if TYPE_CHECKING:
    from wexample_filestate.item.file.html_file import HtmlFile


class TestHtmlFile(AbstractContentFileTest):
    """Test HtmlFile functionality - smoke tests for HTML file handling."""

    def test_html_file_dumps_object_content(self, tmp_path) -> None:
        """Test HtmlFile dumps method with object input."""
        self._setup_with_tmp_path(tmp_path)

        html_file = self._create_file(self._get_sample_filename(), tmp_path)

        # Test with object that has __str__ method
        class MockHtmlObject:
            def __str__(self) -> str:
                return "<div>Generated HTML</div>"

        html_obj = MockHtmlObject()
        result = html_file.dumps(html_obj)

        assert result == "<div>Generated HTML</div>", "Should convert object to string"
        assert isinstance(result, str), "Result should be string"

    # HTML-specific tests that are not covered by the abstract class
    def test_html_file_dumps_string_content(self, tmp_path) -> None:
        """Test HtmlFile dumps method with string input."""
        self._setup_with_tmp_path(tmp_path)

        html_file = self._create_file(self._get_sample_filename(), tmp_path)

        # Test with string content (should pass through)
        html_string = "<html><body><h1>Test</h1></body></html>"
        result = html_file.dumps(html_string)

        assert result == html_string, "String content should pass through unchanged"
        assert isinstance(result, str), "Result should be string"

    def _get_expected_extension(self) -> str:
        """Get the expected file extension."""
        return "html"

    def _get_extension_constants(self) -> dict[str, str]:
        """Get the extension constants as name->value mapping."""
        return {"EXTENSION_HTML": "html", "EXTENSION_HTM": "htm"}

    def _get_file_class(self) -> type[HtmlFile]:
        """Get the HtmlFile class."""
        from wexample_filestate.item.file.html_file import HtmlFile

        return HtmlFile

    def _get_file_type_name(self) -> str:
        """Get the file type name for messages."""
        return "HtmlFile"

    def _get_sample_filename(self) -> str:
        """Get the sample test file name."""
        return "sample.html"

    def _validate_loaded_content(self, raw_content: str, loaded_content: Any) -> None:
        """Validate the loaded HTML content."""
        # HtmlFile.loads() just returns the raw string
        assert isinstance(loaded_content, str), "Parsed content should be a string"
        assert (
            loaded_content == raw_content
        ), "Loads should return the original content unchanged"

        # Test that HTML content is preserved
        assert "<!DOCTYPE html>" in loaded_content, "Should preserve DOCTYPE"
        assert "<html" in loaded_content, "Should preserve HTML tag"
        assert "<head>" in loaded_content, "Should preserve head section"
        assert "<body>" in loaded_content, "Should preserve body section"
        assert "Welcome to Test Project" in loaded_content, "Should preserve content"
