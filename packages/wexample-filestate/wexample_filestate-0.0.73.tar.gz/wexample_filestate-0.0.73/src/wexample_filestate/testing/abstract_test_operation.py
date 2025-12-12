from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method

from wexample_filestate.enum.scopes import Scope
from wexample_filestate.testing.abstract_state_manager_test import (
    AbstractStateManagerTest,
)

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig

    from wexample_filestate.result.file_state_dry_run_result import (
        FileStateDryRunResult,
    )


class AbstractTestOperation(AbstractStateManagerTest, ABC):
    def test_apply(self, tmp_path) -> None:
        self._setup_with_tmp_path(tmp_path)
        self._operation_test_setup()
        self._operation_test_assert_initial()
        self._operation_test_dry_run()
        self._operation_test_apply()
        self._operation_test_assert_applied()
        self._operation_test_rollback()
        self._operation_test_assert_rollback()

    def _dry_run_and_count_operations(self) -> FileStateDryRunResult:
        result = self.state_manager.dry_run(scopes=set(Scope))
        operations_count = len(result.operations)
        expected_count = self._operation_get_count()
        assert (
            operations_count == expected_count
        ), f"Expected {expected_count} operation(s) but found {operations_count}"
        return result

    def _operation_get_count(self) -> int:
        """Override this method if your test expects more than 1 operation."""
        return 1

    def _operation_test_apply(self) -> None:
        self.state_manager.apply()

    @abstract_method
    def _operation_test_assert_applied(self) -> None:
        pass

    def _operation_test_assert_initial(self) -> None:
        pass

    def _operation_test_assert_rollback(self) -> None:
        # Rerun initial checkup
        self._operation_test_assert_initial()

    def _operation_test_dry_run(self) -> None:
        expected_count = self._operation_get_count()
        if expected_count > 0:
            self._dry_run_and_count_operations()
        else:
            # For tests expecting 0 operations, just verify no operations are created
            result = self.state_manager.dry_run(scopes=set(Scope))
            operations_count = len(result.operations)
            assert (
                operations_count == 0
            ), f"Expected 0 operations but found {operations_count}"

    def _operation_test_rollback(self) -> None:
        self.state_manager.rollback()

    def _operation_test_setup(self) -> None:
        config = self._operation_test_setup_configuration()

        if config is not None:
            self.state_manager.configure(config=config)

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        return None
