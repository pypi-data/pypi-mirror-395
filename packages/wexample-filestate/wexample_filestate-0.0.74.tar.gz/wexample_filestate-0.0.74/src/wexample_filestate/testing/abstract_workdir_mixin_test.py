from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method

from wexample_filestate.testing.abstract_state_manager_test import (
    AbstractStateManagerTest,
)

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig

    from wexample_filestate.utils.file_state_manager import FileStateManager


class AbstractWorkdirMixinTest(AbstractStateManagerTest):
    """Base class for testing workdir mixins."""

    def test_mixin_apply_and_rollback(self, tmp_path) -> None:
        """Test that mixin creates files on apply and removes them on rollback."""
        self._setup_with_tmp_path(tmp_path)

        # Create workdir manager with mixin
        manager = self._create_test_workdir_manager(tmp_path)

        # Initially files should not exist
        self._assert_not_applied(tmp_path)

        # Apply multiple times if needed (Single Operation Per Pass principle)
        apply_count = self._get_apply_count()
        for i in range(apply_count):
            manager.apply()

        self._assert_applied(tmp_path)

        # Rollback same number of times to fully undo
        for i in range(apply_count):
            manager.rollback()

        self._assert_not_applied(tmp_path)

    @abstract_method
    def _apply_mixin_to_config(self, mixin_instance, config: DictConfig) -> DictConfig:
        """Apply the mixin method to enhance the config."""

    @abstract_method
    def _assert_applied(self, tmp_path: Path) -> None:
        pass

    @abstract_method
    def _assert_not_applied(self, tmp_path: Path) -> None:
        pass

    def _create_test_workdir_manager(self, tmp_path: Path) -> FileStateManager:
        """Create a test workdir manager that uses the mixin."""
        from wexample_prompt.common.io_manager import IoManager

        from wexample_filestate.utils.file_state_manager import FileStateManager

        # Create the test class that inherits from the mixin
        TestWorkdirClass = self._get_test_workdir_class()

        # Create an instance with the mixin
        test_instance = TestWorkdirClass()

        # Create FileStateManager
        io = IoManager()
        manager = FileStateManager.create_from_path(
            path=str(tmp_path), config={}, io=io
        )

        # Configure with mixin-specific config
        config = self._get_mixin_config()
        enhanced_config = self._apply_mixin_to_config(test_instance, config)
        manager.configure(config=enhanced_config)

        return manager

    def _get_apply_count(self) -> int:
        """Return number of apply() calls needed for complete setup. Override if needed."""
        return 1

    @abstract_method
    def _get_expected_files(self) -> list[str]:
        """Return list of files that should be created by the mixin."""

    @abstract_method
    def _get_mixin_config(self) -> DictConfig:
        """Return the base configuration for the mixin test."""

    @abstract_method
    def _get_test_workdir_class(self) -> type:
        """Return the test class that inherits from the mixin being tested."""

    def _setup_with_tmp_path(self, tmp_path) -> None:
        """Setup test with temporary path."""
        super()._setup_with_tmp_path(tmp_path)
