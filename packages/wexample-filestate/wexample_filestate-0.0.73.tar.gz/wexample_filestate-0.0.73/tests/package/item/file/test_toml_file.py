from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_structured_file_test import (
    AbstractStructuredFileTest,
)

if TYPE_CHECKING:
    from wexample_filestate.item.file.toml_file import TomlFile


class TestTomlFile(AbstractStructuredFileTest):
    """Test TomlFile functionality - smoke tests for TOML file handling."""

    # TOML-specific tests that are not covered by the abstract class
    def test_toml_file_formatting(self, tmp_path) -> None:
        """Test TomlFile produces properly formatted TOML output."""
        self._setup_with_tmp_path(tmp_path)

        toml_file = self._create_file(self._get_sample_filename(), tmp_path)

        # Test data
        test_data = {
            "app": {"name": "test-app"},
            "database": {"host": "localhost", "port": 5432},
        }

        # Serialize to TOML format
        toml_content = toml_file.dumps(test_data)

        # Test TOML formatting characteristics
        assert "[app]" in toml_content, "Should contain section headers"
        assert "[database]" in toml_content, "Should contain section headers"
        assert "name = " in toml_content, "Should contain key-value assignments"

    def _get_expected_extension(self) -> str:
        """Get the expected file extension."""
        return "toml"

    def _get_extension_constant_name(self) -> str:
        """Get the extension constant name."""
        return "EXTENSION_TOML"

    def _get_file_class(self) -> type[TomlFile]:
        """Get the TomlFile class."""
        from wexample_filestate.item.file.toml_file import TomlFile

        return TomlFile

    def _get_file_type_name(self) -> str:
        """Get the file type name for messages."""
        return "TomlFile"

    def _get_sample_filename(self) -> str:
        """Get the sample test file name."""
        return "sample.toml"

    def _validate_parsed_content(self, parsed: dict) -> None:
        """Validate the structure of parsed TOML content."""
        # Call parent validation (which expects name and version at root)
        # But TOML has them in project section, so we need custom validation
        assert "project" in parsed, "Should parse project section"

        # Test project section
        project = parsed["project"]
        assert project["name"] == "test-project"
        assert project["version"] == "1.0.0"
        assert project["author"] == "Test Author"
        assert project["license"] == "MIT"

        # Test other sections
        assert "dependencies" in parsed, "Should parse dependencies section"
        assert "scripts" in parsed, "Should parse scripts section"
        assert "config" in parsed, "Should parse config section"

        # Test dependencies section
        deps = parsed["dependencies"]
        assert "express" in deps
        assert "lodash" in deps

        # Test config section with data types
        config = parsed["config"]
        assert config["debug"] is True, "Boolean values should be parsed correctly"
        assert config["port"] == 8000, "Integer values should be parsed correctly"
