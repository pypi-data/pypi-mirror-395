from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, TypeVar

from wexample_filestate.item.file.structured_content_file import StructuredContentFile
from wexample_filestate.testing.abstract_state_manager_test import (
    AbstractStateManagerTest,
)

if TYPE_CHECKING:
    from pathlib import Path

# Type variable for the specific file type (HtmlFile, EnvFile, etc.)
FileType = TypeVar("FileType", bound=StructuredContentFile)


class AbstractContentFileTest(AbstractStateManagerTest, ABC):
    """Abstract base class for testing content file types (HTML, ENV, etc.).

    This class provides common functionality for testing files that contain
    text content with specific parsing/processing requirements.
    """

    def test_file_creation(self, tmp_path) -> None:
        """Test file can be created and basic properties work."""
        self._setup_with_tmp_path(tmp_path)

        file_instance = self._create_file(self._get_sample_filename(), tmp_path)

        # Test basic properties
        file_type_name = self._get_file_type_name()
        assert (
            file_instance is not None
        ), f"{file_type_name} should be created successfully"

        expected_ext = self._get_expected_extension()
        assert (
            file_instance._expected_file_name_extension() == expected_ext
        ), f"Extension should be '{expected_ext}'"

        # Test extension constants
        constants = self._get_extension_constants()
        for constant_name, expected_value in constants.items():
            assert hasattr(
                file_instance, constant_name
            ), f"Should have {constant_name} constant"
            constant_value = getattr(file_instance, constant_name)
            assert (
                constant_value == expected_value
            ), f"{constant_name} should be '{expected_value}'"

    def test_file_loads(self, tmp_path) -> None:
        """Test file loads method returns expected content."""
        self._setup_with_tmp_path(tmp_path)

        file_instance = self._create_file(self._get_sample_filename(), tmp_path)

        # Read raw content and parsed content
        raw_content = file_instance.read_text()
        loaded_content = file_instance.loads(raw_content)

        # Validate loaded content
        self._validate_loaded_content(raw_content, loaded_content)

    def _create_file(self, filename: str, tmp_path: Path) -> FileType:
        """Create a file instance from a test data file."""
        from wexample_prompt.common.io_manager import IoManager

        # Copy test data file to tmp_path
        test_file = self._get_test_data_path() / filename
        target_file = tmp_path / filename
        target_file.write_text(test_file.read_text())

        # Create file instance
        io = IoManager()
        file_class = self._get_file_class()
        return file_class.create_from_path(path=str(target_file), io=io)

    @abstractmethod
    def _get_expected_extension(self) -> str:
        """Get the expected file extension (e.g., 'html', 'env')."""

    @abstractmethod
    def _get_extension_constants(self) -> dict[str, str]:
        """Get the extension constants as name->value mapping.

        Example: {'EXTENSION_HTML': 'html', 'EXTENSION_HTM': 'htm'}
        """

    @abstractmethod
    def _get_file_class(self) -> type[FileType]:
        """Get the file class to test (e.g., HtmlFile, EnvFile)."""

    @abstractmethod
    def _get_file_type_name(self) -> str:
        """Get the file type name for messages (e.g., 'HtmlFile', 'EnvFile')."""

    @abstractmethod
    def _get_sample_filename(self) -> str:
        """Get the sample test file name (e.g., 'sample.html')."""

    def _get_test_data_path(self) -> Path:
        """Get the path to test data directory."""
        from pathlib import Path

        # Navigate from src/wexample_filestate/testing/ to tests/package/item/test_data/
        return (
            Path(__file__).parent.parent.parent.parent
            / "tests"
            / "package"
            / "item"
            / "file"
            / "test_data"
        )

    @abstractmethod
    def _validate_loaded_content(self, raw_content: str, loaded_content: Any) -> None:
        """Validate the loaded content from the file.

        This method should contain file-type-specific validations.
        """
