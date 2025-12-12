from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_state_manager_test import (
    AbstractStateManagerTest,
)

if TYPE_CHECKING:
    pass


class TestPrefixOption(AbstractStateManagerTest):
    """Test PrefixOption functionality."""

    def test_prefix_option_apply_correction_add_prefix(self, tmp_path) -> None:
        """Test PrefixOption apply_correction adds missing prefix."""
        from wexample_filestate.option.name.prefix_option import PrefixOption

        self._setup_with_tmp_path(tmp_path)

        # Test test_ prefix
        option = PrefixOption()
        option.set_value("test_")

        # Should add prefix to names that don't have it
        assert (
            option.apply_correction("file.txt") == "test_file.txt"
        ), "Should add test_ to file.txt"
        assert (
            option.apply_correction("document.md") == "test_document.md"
        ), "Should add test_ to document.md"
        assert (
            option.apply_correction("script.py") == "test_script.py"
        ), "Should add test_ to script.py"
        assert (
            option.apply_correction("") == "test_"
        ), "Should add test_ to empty string"

        # Should not modify names that already have the prefix
        assert (
            option.apply_correction("test_file.txt") == "test_file.txt"
        ), "Should not modify test_file.txt"
        assert (
            option.apply_correction("test_document.md") == "test_document.md"
        ), "Should not modify test_document.md"
        assert option.apply_correction("test_") == "test_", "Should not modify test_"

    def test_prefix_option_apply_correction_case_sensitive(self, tmp_path) -> None:
        """Test PrefixOption apply_correction is case-sensitive."""
        from wexample_filestate.option.name.prefix_option import PrefixOption

        self._setup_with_tmp_path(tmp_path)

        # Test TEMP_ prefix (uppercase)
        option = PrefixOption()
        option.set_value("TEMP_")

        # Should add prefix even if similar case exists
        assert (
            option.apply_correction("temp_file.txt") == "TEMP_temp_file.txt"
        ), "Should add TEMP_ even if temp_ exists"
        assert (
            option.apply_correction("Temp_file.txt") == "TEMP_Temp_file.txt"
        ), "Should add TEMP_ even if Temp_ exists"

        # Should not modify names that already have the exact prefix
        assert (
            option.apply_correction("TEMP_file.txt") == "TEMP_file.txt"
        ), "Should not modify TEMP_file.txt"

    def test_prefix_option_apply_correction_custom_prefix(self, tmp_path) -> None:
        """Test PrefixOption apply_correction with custom prefixes."""
        from wexample_filestate.option.name.prefix_option import PrefixOption

        self._setup_with_tmp_path(tmp_path)

        # Test draft- prefix
        option = PrefixOption()
        option.set_value("draft-")

        # Should add prefix to names that don't have it
        assert (
            option.apply_correction("document.txt") == "draft-document.txt"
        ), "Should add draft- to document.txt"
        assert (
            option.apply_correction("proposal.md") == "draft-proposal.md"
        ), "Should add draft- to proposal.md"
        assert (
            option.apply_correction("script.py") == "draft-script.py"
        ), "Should add draft- to script.py"

        # Should not modify names that already have the prefix
        assert (
            option.apply_correction("draft-document.txt") == "draft-document.txt"
        ), "Should not modify draft-document.txt"
        assert (
            option.apply_correction("draft-proposal.md") == "draft-proposal.md"
        ), "Should not modify draft-proposal.md"

    def test_prefix_option_apply_correction_empty_prefix(self, tmp_path) -> None:
        """Test PrefixOption apply_correction with empty prefix."""
        from wexample_filestate.option.name.prefix_option import PrefixOption

        self._setup_with_tmp_path(tmp_path)

        option = PrefixOption()
        option.set_value("")

        # Empty prefix should not modify any names (all strings already start with empty string)
        assert (
            option.apply_correction("file.txt") == "file.txt"
        ), "Should not modify file.txt"
        assert (
            option.apply_correction("any_name") == "any_name"
        ), "Should not modify any_name"
        assert option.apply_correction("") == "", "Should not modify empty string"

    def test_prefix_option_apply_correction_multiple_prefixes(self, tmp_path) -> None:
        """Test PrefixOption behavior with names that could have multiple prefixes."""
        from wexample_filestate.option.name.prefix_option import PrefixOption

        self._setup_with_tmp_path(tmp_path)

        # Test new_ prefix
        option = PrefixOption()
        option.set_value("new_")

        # Should add new_ even if other prefixes exist
        assert (
            option.apply_correction("old_file.txt") == "new_old_file.txt"
        ), "Should add new_ to old_file.txt"
        assert (
            option.apply_correction("temp_script.py") == "new_temp_script.py"
        ), "Should add new_ to temp_script.py"
        assert (
            option.apply_correction("draft_document.md") == "new_draft_document.md"
        ), "Should add new_ to draft_document.md"

        # Should not modify if already starts with new_
        assert (
            option.apply_correction("new_file.txt") == "new_file.txt"
        ), "Should not modify new_file.txt"

    def test_prefix_option_apply_correction_with_none_value(self, tmp_path) -> None:
        """Test PrefixOption apply_correction with None value."""
        from wexample_filestate.option.name.prefix_option import PrefixOption

        self._setup_with_tmp_path(tmp_path)

        option = PrefixOption()
        option.set_value(None)

        # Should return name unchanged when value is None
        assert (
            option.apply_correction("any_name.txt") == "any_name.txt"
        ), "Should return name unchanged when None"
        assert (
            option.apply_correction("") == ""
        ), "Should return empty string unchanged when None"

    def test_prefix_option_creation(self, tmp_path) -> None:
        """Test PrefixOption can be created."""
        from wexample_filestate.option.name.prefix_option import PrefixOption

        self._setup_with_tmp_path(tmp_path)

        option = PrefixOption()
        assert option is not None, "PrefixOption should be created"
        assert option.get_description() == "Enforce prefix requirement for file names"

    def test_prefix_option_numeric_prefix(self, tmp_path) -> None:
        """Test PrefixOption with numeric prefixes."""
        from wexample_filestate.option.name.prefix_option import PrefixOption

        self._setup_with_tmp_path(tmp_path)

        # Test numeric prefix
        option = PrefixOption()
        option.set_value("001_")

        # Should validate names with numeric prefix
        assert option.validate_name("001_file.txt") is True, "Should match 001_file.txt"
        assert (
            option.validate_name("001_document.md") is True
        ), "Should match 001_document.md"

        # Should not validate names without the exact numeric prefix
        assert (
            option.validate_name("1_file.txt") is False
        ), "Should not match 1_file.txt"
        assert (
            option.validate_name("01_file.txt") is False
        ), "Should not match 01_file.txt"

        # Should add the numeric prefix when correcting
        assert (
            option.apply_correction("file.txt") == "001_file.txt"
        ), "Should add 001_ to file.txt"

    def test_prefix_option_path_separator_prefix(self, tmp_path) -> None:
        """Test PrefixOption with path-like prefixes."""
        from wexample_filestate.option.name.prefix_option import PrefixOption

        self._setup_with_tmp_path(tmp_path)

        # Test path-like prefix
        option = PrefixOption()
        option.set_value("src/")

        # Should validate names with path-like prefix
        assert option.validate_name("src/main.py") is True, "Should match src/main.py"
        assert option.validate_name("src/utils.js") is True, "Should match src/utils.js"

        # Should not validate names without the path prefix
        assert option.validate_name("main.py") is False, "Should not match main.py"
        assert (
            option.validate_name("lib/main.py") is False
        ), "Should not match lib/main.py"

        # Should add the path prefix when correcting
        assert (
            option.apply_correction("main.py") == "src/main.py"
        ), "Should add src/ to main.py"

    def test_prefix_option_roundtrip_validation_correction(self, tmp_path) -> None:
        """Test that apply_correction produces names that validate successfully."""
        from wexample_filestate.option.name.prefix_option import PrefixOption

        self._setup_with_tmp_path(tmp_path)

        # Test v1_ prefix
        option = PrefixOption()
        option.set_value("v1_")

        test_names = [
            "file.txt",
            "document.md",
            "script.py",
            "data.json",
            "config.yml",
            "",
        ]

        for name in test_names:
            corrected_name = option.apply_correction(name)
            assert (
                option.validate_name(corrected_name) is True
            ), f"Corrected name '{corrected_name}' should validate successfully"

    def test_prefix_option_special_characters_in_prefix(self, tmp_path) -> None:
        """Test PrefixOption with special characters in prefix."""
        from wexample_filestate.option.name.prefix_option import PrefixOption

        self._setup_with_tmp_path(tmp_path)

        # Test prefix with special characters
        option = PrefixOption()
        option.set_value("v2.1-beta_")

        # Should validate names with the special prefix
        assert (
            option.validate_name("v2.1-beta_app.py") is True
        ), "Should match v2.1-beta_app.py"
        assert (
            option.validate_name("v2.1-beta_lib.js") is True
        ), "Should match v2.1-beta_lib.js"

        # Should not validate names without the exact prefix
        assert (
            option.validate_name("v2.1_app.py") is False
        ), "Should not match v2.1_app.py"
        assert (
            option.validate_name("v2.1-alpha_app.py") is False
        ), "Should not match v2.1-alpha_app.py"

        # Should add the special prefix when correcting
        assert (
            option.apply_correction("app.py") == "v2.1-beta_app.py"
        ), "Should add special prefix to app.py"
        assert (
            option.apply_correction("lib.js") == "v2.1-beta_lib.js"
        ), "Should add special prefix to lib.js"

    def test_prefix_option_unicode_prefix(self, tmp_path) -> None:
        """Test PrefixOption with Unicode characters in prefix."""
        from wexample_filestate.option.name.prefix_option import PrefixOption

        self._setup_with_tmp_path(tmp_path)

        # Test Unicode prefix
        option = PrefixOption()
        option.set_value("🚀_")

        # Should validate names with Unicode prefix
        assert option.validate_name("🚀_rocket.py") is True, "Should match 🚀_rocket.py"
        assert option.validate_name("🚀_launch.js") is True, "Should match 🚀_launch.js"

        # Should not validate names without the Unicode prefix
        assert option.validate_name("rocket.py") is False, "Should not match rocket.py"

        # Should add the Unicode prefix when correcting
        assert (
            option.apply_correction("rocket.py") == "🚀_rocket.py"
        ), "Should add 🚀_ to rocket.py"

    def test_prefix_option_validate_name_case_sensitive(self, tmp_path) -> None:
        """Test PrefixOption validation is case-sensitive."""
        from wexample_filestate.option.name.prefix_option import PrefixOption

        self._setup_with_tmp_path(tmp_path)

        # Test TEMP_ prefix (uppercase)
        option = PrefixOption()
        option.set_value("TEMP_")

        # Should match exact case
        assert (
            option.validate_name("TEMP_file.txt") is True
        ), "Should match TEMP_file.txt"
        assert (
            option.validate_name("TEMP_document.md") is True
        ), "Should match TEMP_document.md"

        # Should not match different case
        assert (
            option.validate_name("temp_file.txt") is False
        ), "Should not match temp_file.txt (lowercase)"
        assert (
            option.validate_name("Temp_file.txt") is False
        ), "Should not match Temp_file.txt (mixed case)"

    def test_prefix_option_validate_name_custom_prefix(self, tmp_path) -> None:
        """Test PrefixOption validation with custom prefixes."""
        from wexample_filestate.option.name.prefix_option import PrefixOption

        self._setup_with_tmp_path(tmp_path)

        # Test draft- prefix
        option = PrefixOption()
        option.set_value("draft-")

        # Should match names starting with draft-
        assert (
            option.validate_name("draft-document.txt") is True
        ), "Should match draft-document.txt"
        assert (
            option.validate_name("draft-proposal.md") is True
        ), "Should match draft-proposal.md"
        assert (
            option.validate_name("draft-script.py") is True
        ), "Should match draft-script.py"
        assert option.validate_name("draft-") is True, "Should match draft-"

        # Should not match names not starting with draft-
        assert (
            option.validate_name("document-draft.txt") is False
        ), "Should not match document-draft.txt"
        assert (
            option.validate_name("my-draft-file.md") is False
        ), "Should not match my-draft-file.md"
        assert (
            option.validate_name("draft") is False
        ), "Should not match draft (no hyphen)"

    def test_prefix_option_validate_name_empty_prefix(self, tmp_path) -> None:
        """Test PrefixOption validation with empty prefix."""
        from wexample_filestate.option.name.prefix_option import PrefixOption

        self._setup_with_tmp_path(tmp_path)

        option = PrefixOption()
        option.set_value("")

        # Empty prefix should match all names (all strings start with empty string)
        assert option.validate_name("") is True, "Should match empty string"
        assert option.validate_name("file.txt") is True, "Should match file.txt"
        assert option.validate_name("any_name") is True, "Should match any_name"

    def test_prefix_option_validate_name_file_prefix(self, tmp_path) -> None:
        """Test PrefixOption validation with file prefixes."""
        from wexample_filestate.option.name.prefix_option import PrefixOption

        self._setup_with_tmp_path(tmp_path)

        # Test test_ prefix
        option = PrefixOption()
        option.set_value("test_")

        # Should match names starting with test_
        assert (
            option.validate_name("test_file.txt") is True
        ), "Should match test_file.txt"
        assert (
            option.validate_name("test_script.py") is True
        ), "Should match test_script.py"
        assert (
            option.validate_name("test_document.md") is True
        ), "Should match test_document.md"
        assert option.validate_name("test_") is True, "Should match test_"

        # Should not match names not starting with test_
        assert (
            option.validate_name("file_test.txt") is False
        ), "Should not match file_test.txt"
        assert (
            option.validate_name("mytest_file.py") is False
        ), "Should not match mytest_file.py"
        assert (
            option.validate_name("TEST_file.txt") is False
        ), "Should not match TEST_file.txt (case sensitive)"
        assert (
            option.validate_name("test") is False
        ), "Should not match test (no underscore)"

    def test_prefix_option_validate_name_with_none_value(self, tmp_path) -> None:
        """Test PrefixOption validation with None value (should always return True)."""
        from wexample_filestate.option.name.prefix_option import PrefixOption

        self._setup_with_tmp_path(tmp_path)

        option = PrefixOption()
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
