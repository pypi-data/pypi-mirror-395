from __future__ import annotations

from typing import Any, Union

from wexample_helpers.testing.abstract_test_helpers import AbstractTestHelpers


class TestFileStateManager(AbstractTestHelpers):
    def test_types(self) -> None:
        from wexample_helpers.helpers.polyfill import polyfill_register_global

        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.option.children_filter_option import (
            ChildrenFilterOption,
        )
        from wexample_filestate.result.abstract_result import AbstractResult
        from wexample_filestate.utils.file_state_manager import FileStateManager

        polyfill_register_global(AbstractResult)

        class TestClass(FileStateManager):
            pass

        self._test_type_validate_or_fail(
            success_cases=[
                (TestClass, type[ItemTargetDirectory]),
                (
                    [ChildrenFilterOption(pattern={})],
                    list[ChildrenFilterOption],
                ),
                (
                    [ChildrenFilterOption(pattern={})],
                    list[Union[dict[str, Any], ChildrenFilterOption]],
                ),
            ]
        )
