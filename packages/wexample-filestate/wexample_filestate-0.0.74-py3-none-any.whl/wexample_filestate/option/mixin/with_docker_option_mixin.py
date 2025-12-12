from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.helpers.docker import (
    docker_build_image,
    docker_build_name_from_path,
    docker_container_exists,
    docker_container_is_running,
    docker_exec,
    docker_image_exists,
    docker_run_container,
    docker_start_container,
)
from wexample_helpers.helpers.path import path_rebase
from wexample_helpers.helpers.shell import shell_run

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class WithDockerOptionMixin:
    # Run a dry run version sharing the stdio to help seeing error from container.
    _debug: bool = False
    # Set to True to force rebuild of Docker image and container
    _docker_rebuild: bool = False

    def _ensure_docker_container(self, target: TargetFileOrDirectoryType) -> None:
        from wexample_helpers.helpers.docker import (
            docker_remove_container,
            docker_remove_image,
            docker_stop_container,
        )

        container_name = self._get_container_name(target)
        app_root = str(target.get_root().get_path())
        image_name = self._get_docker_image_name()

        # Force rebuild if requested - must be done BEFORE ensuring image
        if self._docker_rebuild:
            # 1. Stop and remove container first
            if docker_container_exists(container_name):
                if docker_container_is_running(container_name):
                    docker_stop_container(container_name)
                docker_remove_container(container_name)

            # 2. Then remove image
            if docker_image_exists(image_name):
                docker_remove_image(image_name)

        # Now ensure image exists (will rebuild if removed)
        self._ensure_docker_image()

        # Finally ensure container exists and is running
        if docker_container_exists(container_name):
            if not docker_container_is_running(container_name):
                docker_start_container(container_name)
        else:
            import os

            # Get current user UID/GID to avoid creating root-owned files
            user = f"{os.getuid()}:{os.getgid()}"
            docker_run_container(
                container_name,
                image_name,
                volumes={app_root: "/var/www/html"},
                user=user,
            )

    def _ensure_docker_image(self) -> None:
        image_name = self._get_docker_image_name()

        if not docker_image_exists(image_name):
            docker_build_image(image_name, self._get_dockerfile_path())

    def _execute_in_docker(
        self, target: TargetFileOrDirectoryType, command: list[str]
    ) -> str:
        import os

        self._ensure_docker_container(target)
        container_name = self._get_container_name(target)
        # Get current user UID/GID to avoid creating root-owned files
        user = f"{os.getuid()}:{os.getgid()}"

        if self._debug:
            shell_run(
                cmd=["docker", "exec", "--user", user, container_name] + command,
                inherit_stdio=True,
            )

        return docker_exec(container_name, command, user=user)

    def _get_container_file_path(self, target):
        app_root = target.get_root().get_path()
        file_path = target.get_path()

        return path_rebase(
            root_src=app_root,
            path_src=file_path,
            root_dest="/var/www/html",
        )

    def _get_container_name(self, target):
        return docker_build_name_from_path(
            root_path=target.get_root().get_path(),
            image_name=self._get_docker_image_name(),
        )

    @abstract_method
    def _get_docker_image_name(self) -> str:
        """Return the Docker image name to use."""

    @abstract_method
    def _get_dockerfile_path(self) -> Path:
        """Return the path to the Dockerfile."""
