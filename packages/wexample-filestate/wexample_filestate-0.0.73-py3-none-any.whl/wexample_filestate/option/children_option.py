from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union, cast

from wexample_config.config_option.children_config_option import ChildrenConfigOption
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.option.mixin.option_mixin import OptionMixin

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig
    from wexample_prompt.common.io_manager import IoManager

    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class ChildrenOption(OptionMixin, ChildrenConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.option.abstract_children_manipulator_option import (
            AbstractChildrenManipulationOption,
        )

        return list[Union[dict[str, Any], AbstractChildrenManipulationOption]]

    def build_item_tree(self) -> None:
        super().build_item_tree()
        children = self.create_children_items()

        # Continue item tree.
        for child in children:
            child.build_item_tree()

    def create_child_item(
        self, child_config: DictConfig, item_name: str | None = None
    ) -> TargetFileOrDirectoryType:
        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.exception.bad_configuration_class_type_exception import (
            BadConfigurationClassTypeException,
        )
        from wexample_filestate.helpers.config_helper import config_is_item_type
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.item.item_target_file import ItemTargetFile
        from wexample_filestate.option.class_option import (
            ClassOption,
        )
        from wexample_filestate.option.name_option import NameOption

        option_name = ClassOption.get_name()
        if option_name in child_config:
            class_definition = child_config.get(option_name)

            if not issubclass(class_definition, ItemTargetDirectory) and not issubclass(
                child_config.get(option_name), ItemTargetFile
            ):
                raise BadConfigurationClassTypeException(
                    class_definition=class_definition
                )

            child = class_definition.create_from_config(
                io=self.get_io(),
                # Name might be not mandatory when using custom class
                config=child_config,
                parent=self,
            )
        else:
            # Stricter resolution policy:
            # 1) If an explicit type is provided, use it.
            # 2) If explicit type is provided and the path exists, verify it matches the filesystem.
            # 3) Otherwise, attempt to infer from the real filesystem (if the target exists).
            # 4) If the target does not exist and no explicit type is provided, raise an error.
            is_file_type = config_is_item_type(child_config, DiskItemType.FILE)
            has_explicit_dir = config_is_item_type(child_config, DiskItemType.DIRECTORY)

            name = item_name or child_config.get(NameOption.get_name(), None)
            path = None
            if isinstance(name, str) and name:
                path = self.get_parent_item().get_path() / name

            # If explicit type is provided and we can resolve a path, verify when it exists
            if (
                (is_file_type or has_explicit_dir)
                and path is not None
                and path.exists()
            ):
                if is_file_type and not path.is_file():
                    raise ValueError(
                        f"ChildrenConfigOption: child '{path}' is configured as FILE but is a directory on disk."
                    )
                if has_explicit_dir and not path.is_dir():
                    raise ValueError(
                        f"ChildrenConfigOption: child '{path}' is configured as DIRECTORY but is a file on disk."
                    )

            # If no explicit type, try to infer from filesystem
            if not (is_file_type or has_explicit_dir):
                if not isinstance(name, str) or not name:
                    raise ValueError(
                        "ChildrenConfigOption: missing 'type' and 'name' to infer child item type."
                    )

                assert path is not None
                if path.exists():
                    if path.is_file():
                        is_file_type = True
                    elif path.is_dir():
                        is_file_type = False
                else:
                    raise ValueError(
                        "ChildrenConfigOption: missing 'type' in child_config and target does not exist to infer type."
                    )

            if is_file_type:
                child = ItemTargetFile(
                    io=self.get_io(),
                    parent=self,
                )
            else:
                child = ItemTargetDirectory(
                    io=self.get_io(),
                    parent=self,
                )

            child.configure(child_config)
        return child

    def create_children_items(self) -> list[TargetFileOrDirectoryType]:
        from wexample_filestate.option.abstract_children_manipulator_option import (
            AbstractChildrenManipulationOption,
        )

        children = []
        # Parent item should be a file or directory target.
        for child_config in self.get_value().get_list():
            if isinstance(child_config, AbstractChildrenManipulationOption):
                child = child_config
                # Parent has not been assigned before now.
                child.parent = self

                children.extend(child.generate_children())

            else:
                children.append(self.create_child_item(child_config=child_config))

        self.children = children
        return children

    def get_children(self) -> list[TargetFileOrDirectoryType]:
        from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType

        return cast(list[TargetFileOrDirectoryType], self.children)

    def get_io(self) -> IoManager:
        return self.get_parent_item().io

    def get_parent(self) -> TargetFileOrDirectoryType:
        assert self.parent is not None
        return self.parent

    def set_value(self, raw_value: Any) -> None:
        from wexample_config.config_option.abstract_config_option import (
            AbstractConfigOption,
        )

        # Ignore default children class set_value
        AbstractConfigOption.set_value(self, raw_value)
