from __future__ import annotations

from typing import TYPE_CHECKING

from tests.package.option.mode.test_mode_option import TestItemChangeModeOperation

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig

    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class TestItemChangeModeRecursiveOperation(TestItemChangeModeOperation):
    def _get_expected_mode(self) -> str:
        from wexample_filestate.option.mode_option import ModeOption

        return (
            self._get_target()
            .get_option_value(ModeOption)
            .get_dict()
            .get("permissions")
        )

    def _get_target(self) -> TargetFileOrDirectoryType | None:
        from wexample_filestate.const.test import TEST_DIR_NAME_RECURSIVE

        return self.state_manager.find_by_name(TEST_DIR_NAME_RECURSIVE)

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.const.test import TEST_DIR_NAME_RECURSIVE
        from wexample_filestate.option.mode.permissions_option import PermissionsOption
        from wexample_filestate.option.mode.recursive_option import RecursiveOption
        from wexample_filestate.option.mode_option import ModeOption
        from wexample_filestate.option.name_option import NameOption

        return {
            "children": [
                {
                    NameOption.get_name(): TEST_DIR_NAME_RECURSIVE,
                    ModeOption.get_name(): {
                        PermissionsOption.get_name(): "755",
                        RecursiveOption.get_name(): True,
                    },
                },
            ]
        }
