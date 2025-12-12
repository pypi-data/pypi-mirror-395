from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.option.abstract_children_manipulator_option import (
    AbstractChildrenManipulationOption,
)

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_config.const.types import DictConfig

    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class ChildrenFileFactoryOption(AbstractChildrenManipulationOption):
    pattern: DictConfig = public_field(
        description="Pattern is a template used to create generated child configs (e.g., name/type for files to add under each matched directory)",
    )
    recursive: bool = public_field(
        default=False,
        description="Whether to recurse into subdirectories when generating children from the base path.",
    )

    def generate_children(self) -> list[TargetFileOrDirectoryType]:
        from pathlib import Path

        children = []
        path = self.get_parent_item().get_path()

        if path.exists():
            directories = self._get_directories_filtered(base_path=path)

            for directory in directories:
                directory_path = Path(directory)

                dir_config = self._generate_children_recursive(
                    path=directory_path,
                )

                children.append(
                    self._create_child_from_config(
                        path=directory_path,
                        config=dir_config,
                    )
                )

        return children

    def _generate_children_recursive(
        self,
        path: Path,
    ) -> DictConfig:
        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.option.children_option import ChildrenOption
        from wexample_filestate.option.name_option import NameOption
        from wexample_filestate.option.should_exist_option import ShouldExistOption
        from wexample_filestate.option.type_option import TypeOption

        dir_config = {
            NameOption.get_name(): path.name,
            TypeOption.get_name(): DiskItemType.DIRECTORY,
            ChildrenOption.get_name(): [],
            ShouldExistOption.get_name(): True,
        }

        if self._path_match_patterns(path.name):
            dir_config[ChildrenOption.get_name()].append(
                {
                    NameOption.get_name(): self.pattern[NameOption.get_name()],
                    TypeOption.get_name(): self.pattern[TypeOption.get_name()],
                    ShouldExistOption.get_name(): True,
                }
            )

        if self.recursive:
            # Iterate safely over child entries using Path API
            for entry in path.iterdir():
                if entry.is_dir() and self._path_match_patterns(entry.name):
                    dir_config[ChildrenOption.get_name()].append(
                        self._generate_children_recursive(
                            path=entry,
                        )
                    )
        return dir_config
