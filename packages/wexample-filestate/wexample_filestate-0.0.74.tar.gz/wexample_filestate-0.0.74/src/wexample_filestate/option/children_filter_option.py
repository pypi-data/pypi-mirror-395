from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.option.abstract_children_manipulator_option import (
    AbstractChildrenManipulationOption,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class ChildrenFilterOption(AbstractChildrenManipulationOption):
    # Optional callable used to decide whether to include an entry.
    # If provided, it takes precedence over name_pattern.
    filter: Callable[[Path], bool] | None = public_field(
        default=None,
        description="Use this callback to filter out the files to preserve.",
    )
    # When true, search recursively under the base path (all subdirectories)
    recursive: bool = public_field(
        default=False,
        description="Search recursively under the base path; apply filters/name_pattern to all descendants.",
    )

    def generate_children(self) -> list[TargetFileOrDirectoryType]:
        from wexample_filestate.const.disk import DiskItemType

        config = self.pattern
        children = []

        parent_item = self.get_parent_item()
        has_callable_filter = (
            callable(self.filter) if self.filter is not None else False
        )
        has_name_pattern = self.name_pattern is not None

        # Trigger generation if either a name_pattern is present or a callable filter is provided
        if has_name_pattern or has_callable_filter:
            base_path: Path = parent_item.get_path()
            if base_path.exists():
                # Use the instance field `filter` when provided
                entry_filter: Callable[[Path], bool] | None = (
                    self.filter if has_callable_filter else None
                )

                if self.recursive:
                    # Preserve hierarchy: build nested trees for subdirectories, and add base-level files
                    for entry in base_path.iterdir():
                        if entry.is_dir():
                            tree = self._build_dir_tree(entry, config, entry_filter)
                            if tree is not None:
                                children.append(
                                    self._create_child_from_config(
                                        path=entry,
                                        config=tree,
                                    )
                                )
                        elif entry.is_file() and self._include_entry(
                            entry, config, entry_filter
                        ):
                            file_cfg = dict(config)
                            file_cfg["name"] = entry.name
                            file_cfg.setdefault("type", DiskItemType.FILE)
                            children.append(
                                self._create_child_from_config(
                                    path=entry,
                                    config=file_cfg,
                                )
                            )
                else:
                    # Non-recursive: original behavior on the first level
                    for entry in base_path.iterdir():
                        entry_path: Path = entry
                        if self._include_entry(entry_path, config, entry_filter):
                            children.append(
                                self._create_child_from_config(
                                    path=entry_path,
                                    config=config,
                                )
                            )
        return children

    def _build_dir_tree(
        self,
        base_dir: Path,
        config: dict,
        entry_filter: Callable[[Path], bool] | None,
    ) -> dict | None:
        """Build a nested DictConfig preserving the directory structure; returns None if empty when filtering files only."""
        from wexample_filestate.const.disk import DiskItemType

        dir_config: dict = {
            "name": base_dir.name,
            "type": DiskItemType.DIRECTORY,
            "children": [],
            "should_exist": True,
        }

        # First, include matching files in this directory
        for entry in base_dir.iterdir():
            if entry.is_file() and self._include_entry(entry, config, entry_filter):
                file_cfg = dict(config)
                file_cfg["name"] = entry.name
                # Ensure type is FILE when matching files
                file_cfg.setdefault("type", DiskItemType.FILE)
                dir_config["children"].append(file_cfg)

        # Recurse into subdirectories
        for entry in base_dir.iterdir():
            if entry.is_dir():
                sub = self._build_dir_tree(entry, config, entry_filter)
                if sub is not None and (
                    sub.get("children") or config.get("type") == DiskItemType.DIRECTORY
                ):
                    # If filtering directories, also include dirs that match themselves
                    if config.get(
                        "type"
                    ) == DiskItemType.DIRECTORY and self._include_entry(
                        entry, config, entry_filter
                    ):
                        # Replace sub root with configured directory attributes
                        sub = {
                            "name": entry.name,
                            "type": DiskItemType.DIRECTORY,
                            "children": sub.get("children", []),
                            "should_exist": config.get("should_exist", True),
                        }
                    dir_config["children"].append(sub)

        # Prune empty directories when filtering files only
        if not dir_config["children"] and config.get("type") == DiskItemType.FILE:
            return None

        return dir_config

    def _include_entry(
        self,
        entry_path: Path,
        config: dict,
        entry_filter: Callable[[Path], bool] | None,
    ) -> bool:
        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.helpers.config_helper import (
            config_has_same_type_as_path,
        )

        requested_type = config.get("type")
        if requested_type == DiskItemType.DIRECTORY and not entry_path.is_dir():
            return False
        if requested_type == DiskItemType.FILE and not entry_path.is_file():
            return False

        # Inclusion decision: callback first, then name_pattern fallback
        include = False
        if entry_filter is not None:
            try:
                include = bool(entry_filter(entry_path))
            except Exception:
                include = False
        else:
            include = self._path_match_patterns(entry_path.name)

        if not include:
            return False

        # Validate type semantics (historical behavior)
        if "type" in config and not config_has_same_type_as_path(config, entry_path):
            return False
        return True
