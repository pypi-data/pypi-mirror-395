from __future__ import annotations

from typing import TYPE_CHECKING

from tests.package.option.mode.test_mode_option import TestItemChangeModeOperation

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class TestItemChangeModeOperationDict(TestItemChangeModeOperation):
    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT
        from wexample_filestate.option.mode.permissions_option import PermissionsOption
        from wexample_filestate.option.mode.recursive_option import RecursiveOption
        from wexample_filestate.option.mode_option import ModeOption
        from wexample_filestate.option.name_option import NameOption

        return {
            "children": [
                {
                    NameOption.get_name(): TEST_FILE_NAME_SIMPLE_TEXT,
                    ModeOption.get_name(): {
                        PermissionsOption.get_name(): "755",
                        RecursiveOption.get_name(): True,
                    },
                },
            ]
        }
