from __future__ import annotations

import os
from abc import ABC
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_config.options_provider.abstract_options_provider import (
        AbstractOptionsProvider,
    )
    from wexample_helpers.const.types import PathOrString

    from wexample_filestate.utils.file_state_manager import FileStateManager


class AbstractStateManagerTest(ABC):
    state_manager: FileStateManager

    def setup_method(self) -> None:
        # State manager will be initialized in _setup_with_tmp_path
        pass

    def _assert_dir_exists(self, dir_path: PathOrString, positive: bool = True) -> None:
        assert (os.path.isdir(dir_path)) == positive

    def _assert_file_content_equals(
        self, file_path: str, expected_value: str, positive: bool = True
    ) -> None:
        from wexample_helpers.helpers.file import file_read

        assert (file_read(file_path) == expected_value) == positive

    def _assert_file_exists(
        self, file_path: PathOrString, positive: bool = True
    ) -> None:
        assert (os.path.exists(file_path)) == positive

    def _assert_state_manager_target_directory_exists(
        self, item_name: str, positive: bool = True
    ) -> None:
        target = self.state_manager.find_by_name_or_fail(item_name)

        # Target should always exist
        assert target is not None
        self._assert_dir_exists(target.get_path(), positive=positive)

    def _get_absolute_path_from_state_manager(self, relative: str) -> Path:
        return self.state_manager.get_path() / relative

    def _get_package_root_path(self) -> str:
        return f"{os.path.abspath(os.curdir)}{os.sep}"

    def _get_test_manager_class(self):
        from wexample_filestate.utils.file_state_manager import FileStateManager

        return FileStateManager

    def _get_test_options_providers(
        self,
    ) -> list[type[AbstractOptionsProvider]] | None:
        return None

    def _get_test_state_manager_path(
        self, package_root_path: str | None = None
    ) -> Path:
        from pathlib import Path

        return (
            Path(package_root_path or self._get_package_root_path())
            / "tests"
            / "resources"
        )

    def _setup_with_tmp_path(self, tmp_path) -> None:
        import shutil

        from wexample_prompt.common.io_manager import IoManager

        from wexample_filestate.utils.file_state_manager import FileStateManager

        # Copy test data from resources to tmp_path
        resources_path = self._get_test_state_manager_path()
        if resources_path.exists():
            for item in resources_path.iterdir():
                if item.is_file():
                    shutil.copy2(item, tmp_path)
                elif item.is_dir():
                    shutil.copytree(item, tmp_path / item.name)

        self.state_manager = cast(
            FileStateManager,
            self._get_test_manager_class().create_from_path(
                io=IoManager(),
                path=tmp_path,
                options_providers=self._get_test_options_providers(),
            ),
        )
