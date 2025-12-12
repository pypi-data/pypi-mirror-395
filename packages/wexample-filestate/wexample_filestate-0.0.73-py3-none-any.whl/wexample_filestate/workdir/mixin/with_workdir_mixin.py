from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig
    from wexample_prompt.common.io_manager import IoManager

    from wexample_filestate.utils.file_state_manager import FileStateManager


@base_class
class WithWorkdirMixin(BaseClass):
    _host_workdir: FileStateManager | None = private_field(
        default=None,
        description="Internal file state manager for the host workdir",
    )
    _workdir: FileStateManager | None = private_field(
        default=None,
        description="Internal file state manager for the current working directory",
    )

    def __init__(self, *args, **kwargs) -> None:
        # Forward all arguments to parent class
        super().__init__(*args, **kwargs)

    @property
    def host_workdir(self) -> FileStateManager | None:
        return self._host_workdir

    @host_workdir.setter
    def host_workdir(self, value: FileStateManager | None) -> None:
        self._host_workdir = value

    @property
    def workdir(self) -> FileStateManager | None:
        return self._workdir

    @workdir.setter
    def workdir(self, value: FileStateManager | None) -> None:
        self._workdir = value

    def _create_workdir_state_manager(
        self,
        entrypoint_path: str,
        io: IoManager,
        config: DictConfig | None = None,
    ) -> FileStateManager:
        return self._get_workdir_state_manager_class().create_from_path(
            path=entrypoint_path, config=config or {}, io=io
        )

    def _get_workdir_state_manager_class(
        self,
    ) -> type[FileStateManager]:
        from wexample_filestate.utils.file_state_manager import FileStateManager

        return FileStateManager

    def _init_workdir(
        self,
        entrypoint_path: str,
        io: IoManager,
        config: DictConfig | None = None,
    ) -> None:
        import os

        from wexample_filestate.enum.scopes import Scope
        from wexample_filestate.utils.file_state_manager import FileStateManager

        self.workdir = self._create_workdir_state_manager(
            entrypoint_path=entrypoint_path,
            io=io,
            config=config,
        )

        # Hide core config logs
        original_verbosity = io.default_response_verbosity
        io.default_response_verbosity = VerbosityLevel.MAXIMUM

        # Ensure files state, but not content at this point.
        self.workdir.apply(
            scopes={
                Scope.LOCATION,
                Scope.NAME,
                Scope.OWNERSHIP,
                Scope.PERMISSIONS,
                Scope.TIMESTAMPS,
            },
        )

        io.default_response_verbosity = original_verbosity

        # The calling workdir may be in a virtual env host system.
        self.host_workdir = FileStateManager.create_from_path(path=os.getcwd(), io=io)

    def _rebuild_workdir_content(self) -> None:
        from wexample_filestate.enum.scopes import Scope

        self.workdir.apply(
            scopes={
                Scope.CONTENT,
            }
        )
