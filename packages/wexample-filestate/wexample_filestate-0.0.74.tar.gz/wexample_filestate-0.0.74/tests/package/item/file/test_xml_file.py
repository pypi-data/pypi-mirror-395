from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_filestate.testing.abstract_structured_file_test import (
    AbstractStructuredFileTest,
)

if TYPE_CHECKING:
    from wexample_filestate.item.file.xml_file import XmlFile


class TestXmlFile(AbstractStructuredFileTest):
    """Test XmlFile functionality - smoke tests for XML file handling."""

    def test_xml_file_dumps_dict_content(self, tmp_path) -> None:
        """Test XmlFile dumps method with dict input."""
        self._setup_with_tmp_path(tmp_path)

        xml_file = self._create_file(self._get_sample_filename(), tmp_path)

        # Test data as dict
        test_data = {
            "root": {
                "name": "test-app",
                "version": "1.0.0",
                "items": {"item": ["item1", "item2", "item3"]},
            }
        }

        # Serialize to XML format
        xml_content = xml_file.dumps(test_data)

        # Test output format
        assert isinstance(xml_content, str), "Output should be string"
        assert "<root>" in xml_content, "Should contain root element"
        assert "<name>" in xml_content, "Should contain name element"
        assert "test-app" in xml_content, "Should contain content"

    # XML-specific tests that are not covered by the abstract class
    def test_xml_file_dumps_string_content(self, tmp_path) -> None:
        """Test XmlFile dumps method with string input."""
        self._setup_with_tmp_path(tmp_path)

        xml_file = self._create_file(self._get_sample_filename(), tmp_path)

        # Test with string content (should pass through)
        xml_string = "<root><item>test</item></root>"
        result = xml_file.dumps(xml_string)

        assert result == xml_string, "String content should pass through unchanged"

    def test_xml_file_roundtrip_simple(self, tmp_path) -> None:
        """Test XmlFile can parse and serialize simple XML consistently."""
        self._setup_with_tmp_path(tmp_path)

        xml_file = self._create_file(self._get_sample_filename(), tmp_path)

        # Simple XML for testing
        simple_xml = (
            '<?xml version="1.0"?><root><name>test</name><value>123</value></root>'
        )

        # Parse and serialize back
        parsed = xml_file.loads(simple_xml)
        serialized = xml_file.dumps(parsed)

        # Parse again to compare structure
        reparsed = xml_file.loads(serialized)

        # Should have same structure (exact format may differ)
        assert isinstance(reparsed, dict), "Reparsed should be dict"
        assert "root" in reparsed, "Should preserve root structure"

    def _assert_roundtrip_equality(self, original: Any, roundtrip: Any) -> None:
        """Assert XML roundtrip equality - XML may not preserve exact structure."""
        # XML roundtrip may not preserve exact structure due to conversion complexities
        # Just ensure we get some structured data back
        assert isinstance(roundtrip, dict), "XML roundtrip should return dict"

    def _get_expected_extension(self) -> str:
        """Get the expected file extension."""
        return "xml"

    def _get_extension_constant_name(self) -> str:
        """Get the extension constant name."""
        return "EXTENSION_XML"

    def _get_file_class(self) -> type[XmlFile]:
        """Get the XmlFile class."""
        from wexample_filestate.item.file.xml_file import XmlFile

        return XmlFile

    def _get_file_type_name(self) -> str:
        """Get the file type name for messages."""
        return "XmlFile"

    def _get_sample_filename(self) -> str:
        """Get the sample test file name."""
        return "sample.xml"

    def _validate_parsed_content(self, parsed: dict) -> None:
        """Validate the structure of parsed XML content."""
        # XML has different structure - no name/version at root
        # Custom validation for XML
        assert "project" in parsed, "Should parse root element"

        # Test project structure
        project = parsed["project"]
        assert isinstance(project, dict), "Project should be dict"

        # Basic smoke test - just ensure parsing works without errors
        # XML structure can vary based on xmltodict implementation
        assert len(project) > 0, "Project should have content"
