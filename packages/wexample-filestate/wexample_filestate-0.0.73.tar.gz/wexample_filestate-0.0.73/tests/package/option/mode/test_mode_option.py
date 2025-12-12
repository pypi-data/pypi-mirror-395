from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_test_operation import AbstractTestOperation

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig

    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class TestItemChangeModeOperation(AbstractTestOperation):
    def _get_expected_mode(self) -> str:
        from wexample_filestate.option.mode.permissions_option import PermissionsOption
        from wexample_filestate.option.mode_option import ModeOption

        return (
            self._get_target()
            .get_option_value(ModeOption)
            .get_dict()
            .get(PermissionsOption.get_name())
        )

    def _get_target(self) -> TargetFileOrDirectoryType | None:
        from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT

        return self.state_manager.find_by_name(TEST_FILE_NAME_SIMPLE_TEXT)

    def _operation_test_assert_applied(self) -> None:
        assert self._get_target().get_octal_mode() == self._get_expected_mode()

    def _operation_test_assert_initial(self) -> None:
        assert self.state_manager.get_path().is_dir() is True
        assert self._get_target().source.get_octal_mode() != self._get_expected_mode()

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT

        return {
            "children": [
                {"name": TEST_FILE_NAME_SIMPLE_TEXT, "mode": "644"},
            ]
        }
