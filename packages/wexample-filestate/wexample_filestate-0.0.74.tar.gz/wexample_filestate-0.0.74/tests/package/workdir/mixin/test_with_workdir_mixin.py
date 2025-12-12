from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.testing.abstract_workdir_mixin_test import (
    AbstractWorkdirMixinTest,
)
from wexample_filestate.workdir.mixin.with_workdir_mixin import WithWorkdirMixin

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class TestWithWorkdirMixin(AbstractWorkdirMixinTest):
    """Test WithWorkdirMixin functionality."""

    def test_workdir_mixin_instantiation(self, tmp_path) -> None:
        """Test that WithWorkdirMixin can be instantiated and used."""
        self._setup_with_tmp_path(tmp_path)

        # Create workdir manager with workdir mixin
        self._create_test_workdir_manager(tmp_path)

        # Test that the mixin provides workdir functionality
        # This is more about testing the mixin's properties and methods
        TestWorkdirClass = self._get_test_workdir_class()
        instance = TestWorkdirClass()

        # Test workdir properties exist
        assert hasattr(
            instance, "workdir"
        ), "WithWorkdirMixin should provide workdir property"
        assert hasattr(
            instance, "host_workdir"
        ), "WithWorkdirMixin should provide host_workdir property"

        # Test initial values
        assert instance.workdir is None, "workdir should initially be None"
        assert instance.host_workdir is None, "host_workdir should initially be None"

    def _apply_mixin_to_config(self, mixin_instance, config: DictConfig) -> DictConfig:
        """Apply the workdir mixin method to enhance the config."""
        # WithWorkdirMixin doesn't have a direct config method like the others
        # It's more about providing workdir management functionality
        # So we return the config as-is for basic testing
        return config

    def _assert_applied(self, tmp_path) -> None:
        """Assert applied state - no specific files expected."""
        # WithWorkdirMixin doesn't create specific files

    def _assert_not_applied(self, tmp_path) -> None:
        """Assert initial state - no specific files expected."""
        # WithWorkdirMixin doesn't create specific files

    def _get_apply_count(self) -> int:
        """Workdir mixin doesn't create operations directly."""
        return 0

    def _get_expected_files(self) -> list[str]:
        """Return list of files that should be created by the workdir mixin."""
        # WithWorkdirMixin doesn't create files directly, it manages workdirs
        return []

    def _get_mixin_config(self) -> DictConfig:
        """Return the base configuration for the workdir mixin test."""
        return {"children": []}

    def _get_test_workdir_class(self) -> type:
        """Return the test class that inherits from WithWorkdirMixin."""

        @base_class
        class WorkdirTest(WithWorkdirMixin, BaseClass):
            """Test class that inherits from WithWorkdirMixin."""

        return WorkdirTest
