from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_structured_file_test import (
    AbstractStructuredFileTest,
)

if TYPE_CHECKING:
    from wexample_filestate.item.file.yaml_file import YamlFile


class TestYamlFile(AbstractStructuredFileTest):
    """Test YamlFile functionality - smoke tests for YAML file handling."""

    # YAML-specific tests that are not covered by the abstract class
    def test_yaml_file_formatting(self, tmp_path) -> None:
        """Test YamlFile produces properly formatted YAML output."""
        self._setup_with_tmp_path(tmp_path)

        yaml_file = self._create_file(self._get_sample_filename(), tmp_path)

        # Test data
        test_data = {
            "name": "test-app",
            "config": {"debug": True},
            "items": ["item1", "item2"],
        }

        # Serialize to YAML format
        yaml_content = yaml_file.dumps(test_data)

        # Test YAML formatting characteristics
        assert "name: test-app" in yaml_content, "Should contain key-value pairs"
        assert "- item1" in yaml_content, "Should format lists with dashes"

    def _get_expected_extension(self) -> str:
        """Get the expected file extension."""
        return "yml"

    def _get_extension_constant_name(self) -> str:
        """Get the extension constant name."""
        return "EXTENSION_YML"

    def _get_file_class(self) -> type[YamlFile]:
        """Get the YamlFile class."""
        from wexample_filestate.item.file.yaml_file import YamlFile

        return YamlFile

    def _get_file_type_name(self) -> str:
        """Get the file type name for messages."""
        return "YamlFile"

    def _get_sample_filename(self) -> str:
        """Get the sample test file name."""
        return "sample.yaml"

    def _validate_parsed_content(self, parsed: dict) -> None:
        """Validate the structure of parsed YAML content."""
        # Call parent validation
        super()._validate_parsed_content(parsed)

        # YAML-specific validations
        assert "dependencies" in parsed, "Should parse dependencies field"
        assert "scripts" in parsed, "Should parse scripts field"

        # Test specific values
        assert parsed["name"] == "test-project"
        assert parsed["version"] == "1.0.0"
        assert parsed["author"] == "Test Author"
        assert parsed["license"] == "MIT"

        # Test nested structures (YAML dependencies are a list, not dict like JSON)
        assert isinstance(parsed["dependencies"], list), "Dependencies should be list"
        assert len(parsed["dependencies"]) == 2, "Should have 2 dependencies"

        assert isinstance(parsed["scripts"], dict), "Scripts should be dict"
        assert "start" in parsed["scripts"]
        assert "test" in parsed["scripts"]

        assert isinstance(parsed["config"], dict), "Config should be dict"
        assert (
            parsed["config"]["debug"] is True
        ), "Boolean values should be parsed correctly"
        assert (
            parsed["config"]["port"] == 8000
        ), "Integer values should be parsed correctly"
