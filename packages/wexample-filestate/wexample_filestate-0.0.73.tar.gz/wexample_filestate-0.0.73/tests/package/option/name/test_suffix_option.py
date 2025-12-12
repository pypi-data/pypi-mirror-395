from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_state_manager_test import (
    AbstractStateManagerTest,
)

if TYPE_CHECKING:
    pass


class TestSuffixOption(AbstractStateManagerTest):
    """Test SuffixOption functionality."""

    def test_suffix_option_apply_correction_add_suffix(self, tmp_path) -> None:
        """Test SuffixOption apply_correction adds missing suffix."""
        from wexample_filestate.option.name.suffix_option import SuffixOption

        self._setup_with_tmp_path(tmp_path)

        # Test .txt suffix
        option = SuffixOption()
        option.set_value(".txt")

        # Should add suffix to names that don't have it
        assert option.apply_correction("file") == "file.txt", "Should add .txt to file"
        assert (
            option.apply_correction("document") == "document.txt"
        ), "Should add .txt to document"
        assert (
            option.apply_correction("test_file") == "test_file.txt"
        ), "Should add .txt to test_file"
        assert option.apply_correction("") == ".txt", "Should add .txt to empty string"

        # Should not modify names that already have the suffix
        assert (
            option.apply_correction("file.txt") == "file.txt"
        ), "Should not modify file.txt"
        assert (
            option.apply_correction("document.txt") == "document.txt"
        ), "Should not modify document.txt"
        assert option.apply_correction(".txt") == ".txt", "Should not modify .txt"

    def test_suffix_option_apply_correction_case_sensitive(self, tmp_path) -> None:
        """Test SuffixOption apply_correction is case-sensitive."""
        from wexample_filestate.option.name.suffix_option import SuffixOption

        self._setup_with_tmp_path(tmp_path)

        # Test .TXT suffix (uppercase)
        option = SuffixOption()
        option.set_value(".TXT")

        # Should add suffix even if similar case exists
        assert (
            option.apply_correction("file.txt") == "file.txt.TXT"
        ), "Should add .TXT even if .txt exists"
        assert (
            option.apply_correction("file.Txt") == "file.Txt.TXT"
        ), "Should add .TXT even if .Txt exists"

        # Should not modify names that already have the exact suffix
        assert (
            option.apply_correction("file.TXT") == "file.TXT"
        ), "Should not modify file.TXT"

    def test_suffix_option_apply_correction_custom_suffix(self, tmp_path) -> None:
        """Test SuffixOption apply_correction with custom suffixes."""
        from wexample_filestate.option.name.suffix_option import SuffixOption

        self._setup_with_tmp_path(tmp_path)

        # Test _backup suffix
        option = SuffixOption()
        option.set_value("_backup")

        # Should add suffix to names that don't have it
        assert (
            option.apply_correction("file") == "file_backup"
        ), "Should add _backup to file"
        assert (
            option.apply_correction("data") == "data_backup"
        ), "Should add _backup to data"
        assert (
            option.apply_correction("test_file") == "test_file_backup"
        ), "Should add _backup to test_file"

        # Should not modify names that already have the suffix
        assert (
            option.apply_correction("file_backup") == "file_backup"
        ), "Should not modify file_backup"
        assert (
            option.apply_correction("data_backup") == "data_backup"
        ), "Should not modify data_backup"

    def test_suffix_option_apply_correction_empty_suffix(self, tmp_path) -> None:
        """Test SuffixOption apply_correction with empty suffix."""
        from wexample_filestate.option.name.suffix_option import SuffixOption

        self._setup_with_tmp_path(tmp_path)

        option = SuffixOption()
        option.set_value("")

        # Empty suffix should not modify any names (all strings already end with empty string)
        assert (
            option.apply_correction("file.txt") == "file.txt"
        ), "Should not modify file.txt"
        assert (
            option.apply_correction("any_name") == "any_name"
        ), "Should not modify any_name"
        assert option.apply_correction("") == "", "Should not modify empty string"

    def test_suffix_option_apply_correction_multiple_suffixes(self, tmp_path) -> None:
        """Test SuffixOption behavior with names that could have multiple suffixes."""
        from wexample_filestate.option.name.suffix_option import SuffixOption

        self._setup_with_tmp_path(tmp_path)

        # Test .bak suffix
        option = SuffixOption()
        option.set_value(".bak")

        # Should add .bak even if other extensions exist
        assert (
            option.apply_correction("file.txt") == "file.txt.bak"
        ), "Should add .bak to file.txt"
        assert (
            option.apply_correction("script.py") == "script.py.bak"
        ), "Should add .bak to script.py"
        assert (
            option.apply_correction("data.json.old") == "data.json.old.bak"
        ), "Should add .bak to data.json.old"

        # Should not modify if already ends with .bak
        assert (
            option.apply_correction("file.txt.bak") == "file.txt.bak"
        ), "Should not modify file.txt.bak"

    def test_suffix_option_apply_correction_with_none_value(self, tmp_path) -> None:
        """Test SuffixOption apply_correction with None value."""
        from wexample_filestate.option.name.suffix_option import SuffixOption

        self._setup_with_tmp_path(tmp_path)

        option = SuffixOption()
        option.set_value(None)

        # Should return name unchanged when value is None
        assert (
            option.apply_correction("any_name.txt") == "any_name.txt"
        ), "Should return name unchanged when None"
        assert (
            option.apply_correction("") == ""
        ), "Should return empty string unchanged when None"

    def test_suffix_option_creation(self, tmp_path) -> None:
        """Test SuffixOption can be created."""
        from wexample_filestate.option.name.suffix_option import SuffixOption

        self._setup_with_tmp_path(tmp_path)

        option = SuffixOption()
        assert option is not None, "SuffixOption should be created"
        assert option.get_description() == "Enforce suffix requirement for file names"

    def test_suffix_option_roundtrip_validation_correction(self, tmp_path) -> None:
        """Test that apply_correction produces names that validate successfully."""
        from wexample_filestate.option.name.suffix_option import SuffixOption

        self._setup_with_tmp_path(tmp_path)

        # Test .log suffix
        option = SuffixOption()
        option.set_value(".log")

        test_names = ["file", "document", "test_file", "data.txt", "script.py", ""]

        for name in test_names:
            corrected_name = option.apply_correction(name)
            assert (
                option.validate_name(corrected_name) is True
            ), f"Corrected name '{corrected_name}' should validate successfully"

    def test_suffix_option_special_characters_in_suffix(self, tmp_path) -> None:
        """Test SuffixOption with special characters in suffix."""
        from wexample_filestate.option.name.suffix_option import SuffixOption

        self._setup_with_tmp_path(tmp_path)

        # Test suffix with special characters
        option = SuffixOption()
        option.set_value("_v1.0-final")

        # Should validate names with the special suffix
        assert (
            option.validate_name("app_v1.0-final") is True
        ), "Should match app_v1.0-final"
        assert (
            option.validate_name("lib_v1.0-final") is True
        ), "Should match lib_v1.0-final"

        # Should not validate names without the exact suffix
        assert option.validate_name("app_v1.0") is False, "Should not match app_v1.0"
        assert (
            option.validate_name("app_v1.0-beta") is False
        ), "Should not match app_v1.0-beta"

        # Should add the special suffix when correcting
        assert (
            option.apply_correction("app") == "app_v1.0-final"
        ), "Should add special suffix to app"
        assert (
            option.apply_correction("lib") == "lib_v1.0-final"
        ), "Should add special suffix to lib"

    def test_suffix_option_validate_name_case_sensitive(self, tmp_path) -> None:
        """Test SuffixOption validation is case-sensitive."""
        from wexample_filestate.option.name.suffix_option import SuffixOption

        self._setup_with_tmp_path(tmp_path)

        # Test .TXT suffix (uppercase)
        option = SuffixOption()
        option.set_value(".TXT")

        # Should match exact case
        assert option.validate_name("file.TXT") is True, "Should match file.TXT"
        assert option.validate_name("document.TXT") is True, "Should match document.TXT"

        # Should not match different case
        assert (
            option.validate_name("file.txt") is False
        ), "Should not match file.txt (lowercase)"
        assert (
            option.validate_name("file.Txt") is False
        ), "Should not match file.Txt (mixed case)"

    def test_suffix_option_validate_name_custom_suffix(self, tmp_path) -> None:
        """Test SuffixOption validation with custom suffixes."""
        from wexample_filestate.option.name.suffix_option import SuffixOption

        self._setup_with_tmp_path(tmp_path)

        # Test _backup suffix
        option = SuffixOption()
        option.set_value("_backup")

        # Should match names ending with _backup
        assert option.validate_name("file_backup") is True, "Should match file_backup"
        assert option.validate_name("data_backup") is True, "Should match data_backup"
        assert option.validate_name("test_backup") is True, "Should match test_backup"
        assert option.validate_name("_backup") is True, "Should match _backup"

        # Should not match names not ending with _backup
        assert (
            option.validate_name("backup_file") is False
        ), "Should not match backup_file"
        assert (
            option.validate_name("file_backup_old") is False
        ), "Should not match file_backup_old"
        assert (
            option.validate_name("backup") is False
        ), "Should not match backup (no underscore)"

    def test_suffix_option_validate_name_empty_suffix(self, tmp_path) -> None:
        """Test SuffixOption validation with empty suffix."""
        from wexample_filestate.option.name.suffix_option import SuffixOption

        self._setup_with_tmp_path(tmp_path)

        option = SuffixOption()
        option.set_value("")

        # Empty suffix should match all names (all strings end with empty string)
        assert option.validate_name("") is True, "Should match empty string"
        assert option.validate_name("file.txt") is True, "Should match file.txt"
        assert option.validate_name("any_name") is True, "Should match any_name"

    def test_suffix_option_validate_name_file_extension(self, tmp_path) -> None:
        """Test SuffixOption validation with file extension suffixes."""
        from wexample_filestate.option.name.suffix_option import SuffixOption

        self._setup_with_tmp_path(tmp_path)

        # Test .txt suffix
        option = SuffixOption()
        option.set_value(".txt")

        # Should match names ending with .txt
        assert option.validate_name("file.txt") is True, "Should match file.txt"
        assert (
            option.validate_name("test_file.txt") is True
        ), "Should match test_file.txt"
        assert option.validate_name("document.txt") is True, "Should match document.txt"
        assert option.validate_name(".txt") is True, "Should match .txt"

        # Should not match names not ending with .txt
        assert option.validate_name("file.py") is False, "Should not match file.py"
        assert (
            option.validate_name("file.txt.bak") is False
        ), "Should not match file.txt.bak"
        assert option.validate_name("txt") is False, "Should not match txt (no dot)"
        assert (
            option.validate_name("file") is False
        ), "Should not match file (no extension)"

    def test_suffix_option_validate_name_with_none_value(self, tmp_path) -> None:
        """Test SuffixOption validation with None value (should always return True)."""
        from wexample_filestate.option.name.suffix_option import SuffixOption

        self._setup_with_tmp_path(tmp_path)

        option = SuffixOption()
        option.set_value(None)

        # Should return True for any name when value is None
        assert (
            option.validate_name("test.txt") is True
        ), "Should validate any name when value is None"
        assert (
            option.validate_name("file123.py") is True
        ), "Should validate any name when value is None"
        assert (
            option.validate_name("invalid-name") is True
        ), "Should validate any name when value is None"
        assert (
            option.validate_name("") is True
        ), "Should validate empty string when value is None"
