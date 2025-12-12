from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_state_manager_test import (
    AbstractStateManagerTest,
)

if TYPE_CHECKING:
    pass


class TestRegexOption(AbstractStateManagerTest):
    """Test RegexOption functionality."""

    def test_regex_option_anchored_vs_unanchored_patterns(self, tmp_path) -> None:
        """Test difference between anchored and unanchored regex patterns."""
        from wexample_filestate.option.name.regex_option import RegexOption

        self._setup_with_tmp_path(tmp_path)

        # Unanchored pattern (matches anywhere in string)
        option_unanchored = RegexOption()
        option_unanchored.set_value("test")

        assert option_unanchored.validate_name("test") is True, "Should match 'test'"
        assert (
            option_unanchored.validate_name("test_file") is True
        ), "Should match 'test_file' (starts with test)"
        # re.match() only matches from the beginning, so these will fail
        assert (
            option_unanchored.validate_name("my_test") is False
        ), "Should not match 'my_test' (re.match only matches from start)"
        assert (
            option_unanchored.validate_name("my_test_file") is False
        ), "Should not match 'my_test_file' (re.match only matches from start)"

        # Anchored pattern (matches from beginning)
        option_anchored = RegexOption()
        option_anchored.set_value("^test")

        assert option_anchored.validate_name("test") is True, "Should match 'test'"
        assert (
            option_anchored.validate_name("test_file") is True
        ), "Should match 'test_file' (starts with test)"
        assert (
            option_anchored.validate_name("my_test") is False
        ), "Should not match 'my_test' (doesn't start with test)"
        assert (
            option_anchored.validate_name("my_test_file") is False
        ), "Should not match 'my_test_file' (doesn't start with test)"

    def test_regex_option_apply_correction_no_change(self, tmp_path) -> None:
        """Test RegexOption apply_correction returns name unchanged."""
        from wexample_filestate.option.name.regex_option import RegexOption

        self._setup_with_tmp_path(tmp_path)

        option = RegexOption()
        option.set_value(r"test_.*")

        # apply_correction should return the name unchanged (no automatic correction for regex)
        assert (
            option.apply_correction("invalid_name.txt") == "invalid_name.txt"
        ), "Should return name unchanged"
        assert (
            option.apply_correction("test_file.txt") == "test_file.txt"
        ), "Should return name unchanged"
        assert option.apply_correction("") == "", "Should return empty string unchanged"

    def test_regex_option_apply_correction_with_none_value(self, tmp_path) -> None:
        """Test RegexOption apply_correction with None value."""
        from wexample_filestate.option.name.regex_option import RegexOption

        self._setup_with_tmp_path(tmp_path)

        option = RegexOption()
        option.set_value(None)

        # Should return name unchanged when value is None
        assert (
            option.apply_correction("any_name.txt") == "any_name.txt"
        ), "Should return name unchanged when None"

    def test_regex_option_creation(self, tmp_path) -> None:
        """Test RegexOption can be created."""
        from wexample_filestate.option.name.regex_option import RegexOption

        self._setup_with_tmp_path(tmp_path)

        option = RegexOption()
        assert option is not None, "RegexOption should be created"
        assert (
            option.get_description() == "Enforce regex pattern matching for file names"
        )

    def test_regex_option_dot_star_pattern(self, tmp_path) -> None:
        """Test RegexOption with .* pattern (matches everything)."""
        from wexample_filestate.option.name.regex_option import RegexOption

        self._setup_with_tmp_path(tmp_path)

        option = RegexOption()
        option.set_value(".*")

        # .* pattern should match everything
        assert option.validate_name("") is True, "Should match empty string"
        assert option.validate_name("test.txt") is True, "Should match test.txt"
        assert (
            option.validate_name("file with spaces.doc") is True
        ), "Should match file with spaces"
        assert (
            option.validate_name("special!@#$%^&*()chars.txt") is True
        ), "Should match special characters"

    def test_regex_option_empty_pattern(self, tmp_path) -> None:
        """Test RegexOption with empty pattern."""
        from wexample_filestate.option.name.regex_option import RegexOption

        self._setup_with_tmp_path(tmp_path)

        option = RegexOption()
        option.set_value("")

        # Empty pattern matches everything (re.match("", string) always succeeds)
        assert (
            option.validate_name("") is True
        ), "Should match empty string with empty pattern"
        assert (
            option.validate_name("test.txt") is True
        ), "Should match any string with empty pattern"

    def test_regex_option_invalid_regex_pattern(self, tmp_path) -> None:
        """Test RegexOption behavior with invalid regex patterns."""
        from wexample_filestate.option.name.regex_option import RegexOption

        self._setup_with_tmp_path(tmp_path)

        import re

        option = RegexOption()
        option.set_value("[invalid_regex")  # Missing closing bracket

        # Should raise an exception when trying to validate with invalid regex
        try:
            option.validate_name("test.txt")
            assert False, "Should have raised an exception for invalid regex"
        except re.error:
            pass  # Expected behavior

    def test_regex_option_validate_name_case_insensitive_pattern(
        self, tmp_path
    ) -> None:
        """Test RegexOption validation with case-insensitive patterns."""
        from wexample_filestate.option.name.regex_option import RegexOption

        self._setup_with_tmp_path(tmp_path)

        # Test case-insensitive pattern using (?i) flag
        option = RegexOption()
        option.set_value(r"(?i)^readme\..*")

        # Should match regardless of case
        assert option.validate_name("README.md") is True, "Should match README.md"
        assert option.validate_name("readme.txt") is True, "Should match readme.txt"
        assert option.validate_name("Readme.rst") is True, "Should match Readme.rst"
        assert option.validate_name("ReadMe.md") is True, "Should match ReadMe.md"

        # Should not match files not starting with readme
        assert (
            option.validate_name("INSTALL.md") is False
        ), "Should not match INSTALL.md"
        assert (
            option.validate_name("my_readme.txt") is False
        ), "Should not match my_readme.txt"

    def test_regex_option_validate_name_complex_pattern(self, tmp_path) -> None:
        """Test RegexOption validation with complex regex patterns."""
        from wexample_filestate.option.name.regex_option import RegexOption

        self._setup_with_tmp_path(tmp_path)

        # Test pattern for specific naming convention: word_word_number.ext
        option = RegexOption()
        option.set_value(r"^[a-z]+_[a-z]+_\d+\.[a-z]+$")

        # Should match the pattern
        assert (
            option.validate_name("test_file_123.txt") is True
        ), "Should match test_file_123.txt"
        assert (
            option.validate_name("my_script_001.py") is True
        ), "Should match my_script_001.py"
        assert (
            option.validate_name("data_model_42.json") is True
        ), "Should match data_model_42.json"

        # Should not match the pattern
        assert (
            option.validate_name("TestFile123.txt") is False
        ), "Should not match TestFile123.txt (uppercase)"
        assert (
            option.validate_name("test_file.txt") is False
        ), "Should not match test_file.txt (no number)"
        assert (
            option.validate_name("test_file_abc.txt") is False
        ), "Should not match test_file_abc.txt (letters instead of number)"
        assert (
            option.validate_name("test_file_123") is False
        ), "Should not match test_file_123 (no extension)"

    def test_regex_option_validate_name_file_extension_pattern(self, tmp_path) -> None:
        """Test RegexOption validation with file extension patterns."""
        from wexample_filestate.option.name.regex_option import RegexOption

        self._setup_with_tmp_path(tmp_path)

        # Test pattern for Python files
        option = RegexOption()
        option.set_value(r".*\.py$")

        # Should match Python files
        assert option.validate_name("script.py") is True, "Should match script.py"
        assert option.validate_name("test_file.py") is True, "Should match test_file.py"
        assert option.validate_name("module.py") is True, "Should match module.py"

        # Should not match non-Python files
        assert (
            option.validate_name("script.txt") is False
        ), "Should not match script.txt"
        assert option.validate_name("file.pyc") is False, "Should not match file.pyc"
        assert (
            option.validate_name("python") is False
        ), "Should not match python (no extension)"

    def test_regex_option_validate_name_simple_pattern(self, tmp_path) -> None:
        """Test RegexOption validation with simple regex patterns."""
        from wexample_filestate.option.name.regex_option import RegexOption

        self._setup_with_tmp_path(tmp_path)

        # Test pattern for files starting with "test_"
        option = RegexOption()
        option.set_value("test_.*")

        # Should match names starting with "test_"
        assert (
            option.validate_name("test_file.txt") is True
        ), "Should match test_file.txt"
        assert option.validate_name("test_123.py") is True, "Should match test_123.py"
        assert option.validate_name("test_") is True, "Should match test_"

        # Should not match names not starting with "test_"
        assert (
            option.validate_name("file_test.txt") is False
        ), "Should not match file_test.txt"
        assert (
            option.validate_name("mytest_file.py") is False
        ), "Should not match mytest_file.py"
        assert (
            option.validate_name("TEST_file.txt") is False
        ), "Should not match TEST_file.txt (case sensitive)"

    def test_regex_option_validate_name_with_none_value(self, tmp_path) -> None:
        """Test RegexOption validation with None value (should always return True)."""
        from wexample_filestate.option.name.regex_option import RegexOption

        self._setup_with_tmp_path(tmp_path)

        option = RegexOption()
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
