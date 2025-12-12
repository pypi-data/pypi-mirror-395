from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_filestate.testing.abstract_content_file_test import (
    AbstractContentFileTest,
)

if TYPE_CHECKING:
    from wexample_filestate.item.file.env_file import EnvFile


class TestEnvFile(AbstractContentFileTest):
    """Test EnvFile functionality - smoke tests for .env file handling."""

    # ENV-specific tests that are not covered by the abstract class
    def test_env_file_dumps_formatting(self, tmp_path) -> None:
        """Test EnvFile produces properly formatted .env output."""
        self._setup_with_tmp_path(tmp_path)

        env_file = self._create_file(self._get_sample_filename(), tmp_path)

        # Test data
        test_data = {"APP_NAME": "test-app", "VERSION": "1.0.0", "DEBUG": "false"}

        # Serialize to .env format
        env_content = env_file.dumps(test_data)

        # Test output format
        assert isinstance(env_content, str), "Output should be string"
        assert "APP_NAME=test-app" in env_content, "Should contain APP_NAME"
        assert "VERSION=1.0.0" in env_content, "Should contain VERSION"
        assert "DEBUG=false" in env_content, "Should contain DEBUG"

    def _get_expected_extension(self) -> str:
        """Get the expected file extension."""
        return "env"

    def _get_extension_constants(self) -> dict[str, str]:
        """Get the extension constants as name->value mapping."""
        return {"EXTENSION_ENV": "env", "EXTENSION_DOT_ENV": ".env"}

    def _get_file_class(self) -> type[EnvFile]:
        """Get the EnvFile class."""
        from wexample_filestate.item.file.env_file import EnvFile

        return EnvFile

    def _get_file_type_name(self) -> str:
        """Get the file type name for messages."""
        return "EnvFile"

    def _get_sample_filename(self) -> str:
        """Get the sample test file name."""
        return "sample.env"

    def _validate_loaded_content(self, raw_content: str, loaded_content: Any) -> None:
        """Validate the loaded ENV content."""
        # EnvFile.loads() returns a dict of key-value pairs
        assert isinstance(loaded_content, dict), "Parsed content should be a dict"
        assert "DATABASE_URL" in loaded_content, "Should parse DATABASE_URL"
        assert "API_KEY" in loaded_content, "Should parse API_KEY"
        assert "DEBUG" in loaded_content, "Should parse DEBUG"
        assert "PORT" in loaded_content, "Should parse PORT"
        assert "SECRET_KEY" in loaded_content, "Should parse SECRET_KEY (even if empty)"

        # Test specific values
        assert loaded_content["DATABASE_URL"] == "postgresql://user:pass@localhost/db"
        assert loaded_content["API_KEY"] == "abc123"
        assert loaded_content["DEBUG"] == "true"
        assert loaded_content["PORT"] == "8000"
        assert loaded_content["SECRET_KEY"] == ""  # Empty value
