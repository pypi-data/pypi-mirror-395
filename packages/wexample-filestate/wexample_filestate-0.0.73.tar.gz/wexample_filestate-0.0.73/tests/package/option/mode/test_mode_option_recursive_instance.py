from __future__ import annotations

from typing import TYPE_CHECKING

from tests.package.option.mode.test_mode_option_recursive import (
    TestItemChangeModeRecursiveOperation,
)

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class TestItemChangeModeOperationRecursiveInstance(
    TestItemChangeModeRecursiveOperation
):
    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.config_value.mode_config_value import ModeConfigValue
        from wexample_filestate.const.test import TEST_DIR_NAME_RECURSIVE
        from wexample_filestate.option.mode_option import ModeOption
        from wexample_filestate.option.name_option import NameOption

        return {
            "children": [
                {
                    NameOption.get_name(): TEST_DIR_NAME_RECURSIVE,
                    ModeOption.get_name(): ModeConfigValue(
                        permissions="755", recursive=True
                    ),
                },
            ]
        }
