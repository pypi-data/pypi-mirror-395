from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from wexample_config.config_option.abstract_nested_config_option import (
    AbstractNestedConfigOption,
)
from wexample_event.common.dispatcher import EventDispatcherMixin
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_prompt.mixins.with_io_methods import WithIoMethods

from wexample_filestate.config_option.mixin.item_config_option_mixin import (
    ItemTreeConfigOptionMixin,
)
from wexample_filestate.item.mixins.item_mixin import ItemMixin
from wexample_filestate.option.mixin.option_mixin import OptionMixin

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_config.const.types import DictConfig
    from wexample_config.options_provider.abstract_options_provider import (
        AbstractOptionsProvider,
    )
    from wexample_helpers.const.types import PathOrString

    from wexample_filestate.const.state_items import SourceFileOrDirectory
    from wexample_filestate.const.types_state_items import (
        SourceFileOrDirectoryType,
        TargetFileOrDirectoryType,
    )
    from wexample_filestate.enum.scopes import Scope
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.result.abstract_result import AbstractResult
    from wexample_filestate.result.file_state_dry_run_result import (
        FileStateDryRunResult,
    )
    from wexample_filestate.result.file_state_result import FileStateResult


@base_class
class AbstractItemTarget(
    WithIoMethods,
    ItemMixin,
    ItemTreeConfigOptionMixin,
    AbstractNestedConfigOption,
    EventDispatcherMixin,
):
    last_result: AbstractResult | None = public_field(
        default=None, description="The last applied result of state operation"
    )
    operations_history: list[list[AbstractOperation]] = public_field(
        factory=list, description="Stack of operation batches for sequential rollbacks"
    )
    source: SourceFileOrDirectory | None = public_field(
        default=None, description="The original existing file or directory"
    )
    _enable_bubbling = True

    def __attrs_post_init__(self) -> None:
        super().__attrs_post_init__()
        self._init_listeners()

    @classmethod
    def create_from_config(cls, **kwargs) -> AbstractItemTarget:
        config = kwargs.get("config")
        kwargs.pop("config", None)
        instance = cls(**kwargs)
        instance.configure(config)

        return instance

    @classmethod
    def create_from_path(
        cls,
        path: PathOrString,
        config: DictConfig | None = None,
        configure: bool = True,
        **kwargs,
    ) -> AbstractItemTarget:
        from pathlib import Path

        path = Path(path)
        config = config or {}

        item_target = cls(
            base_path=path.parent, base_name=config.get("name", path.name), **kwargs
        )

        if configure:
            item_target.configure(config=config)

        return item_target

    def apply(
        self,
        interactive: bool = False,
        scopes: set[Scope] | None = None,
        filter_path: str | None = None,
        filter_operation: str | None = None,
        max: int = None,
    ) -> FileStateResult:
        from wexample_filestate.enum.scopes import Scope
        from wexample_filestate.result.file_state_result import FileStateResult

        result = FileStateResult(state_manager=self)

        try:
            if scopes is None:
                scopes = set(Scope)

            self.last_result = result
            self.build_operations(
                result=result,
                scopes=scopes,
                filter_path=filter_path,
                filter_operation=filter_operation,
                max=max,
            )

            if len(result.operations) > 0:
                result.apply_operations(interactive=interactive)

                # Push applied operations to history stack for sequential rollbacks
                applied_operations = [op for op in result.operations if op.applied]
                if applied_operations:
                    self.operations_history.append(applied_operations)
            else:
                self.log(
                    message=f"All configuration checks passed.",
                )
        except KeyboardInterrupt:
            self.log("Canceled by user")

        return result

    def build_operations(
        self: TargetFileOrDirectoryType,
        result: AbstractResult,
        scopes: set[Scope],
        filter_path: str | None = None,
        filter_operation: str | None = None,
        max: int = None,
    ) -> bool:
        from wexample_prompt.common.spinner_pool import SpinnerPool
        from wexample_prompt.enums.verbosity_level import VerbosityLevel

        if filter_path is not None and not self._path_matches(filter_path=filter_path):
            return False

        self.io.indentation_up()

        has_any_task: bool = False
        # Allow to set active to false
        if self.is_active():
            loading_log = self.log(
                message=f"{SpinnerPool.next()} @path{{{self.get_display_path()}}}",
            )

            has_task: bool = False
            has_any_task: bool = False

            operation = self._find_first_operation(scopes, filter_operation)
            if operation is not None:
                has_task = True
                self.io.task(f"[{operation.get_name()}] {operation.description}")
                result.operations.append(operation)

            if (
                not has_task
                and self.io.default_context_verbosity != VerbosityLevel.MAXIMUM
            ):
                self.io.erase_response(loading_log)

        self.io.indentation_down()
        return has_any_task

    def configure(self, config: DictConfig) -> None:
        self.set_value(raw_value=config)

        # Name is allways here, as an option and as an argument.
        config["name"] = config["name"] if config.get("name") else self.base_name

        if not self.base_name:
            self.base_name = str(config.get("name"))

        self.locate_source(self.get_path())

    def dry_run(
        self,
        scopes: set[Scope],
        filter_path: str | None = None,
        filter_operation: str | None = None,
        max: int = None,
    ) -> FileStateDryRunResult:
        from wexample_filestate.result.file_state_dry_run_result import (
            FileStateDryRunResult,
        )

        result = FileStateDryRunResult(state_manager=self)
        try:
            self.last_result = result
            self.build_operations(
                result=result,
                scopes=scopes,
                filter_path=filter_path,
                filter_operation=filter_operation,
                max=max,
            )
            result.apply_operations()
        except KeyboardInterrupt:
            self.log("Canceled by user")

        return result

    def dump(self) -> Any:
        output = super().dump()
        output["name"] = self.get_item_name()

        return output

    def find_closest(
        self, class_type: type[AbstractItemTarget]
    ) -> AbstractItemTarget | None:
        """Return the nearest parent item that is an instance of class_type.

        Traverses parents via self.get_parent_item_or_none() until a match is found
        or the root is reached.
        """
        current = self.get_parent_item_or_none()
        while current is not None:
            if isinstance(current, class_type):
                return current  # type: ignore[return-value]
            current = current.get_parent_item_or_none()
        return None

    def get_display_path(self) -> Path:
        return self.get_relative_path() or self.get_path()

    def get_env_parameter(self, key: str, default: str | None = None) -> str | None:
        """If no environment parameter defined by current item, ask its parent.
        The default behavior is to return default value but should be replaced by,
        for instance, .env loading in specific contexts"""
        parent_item = self.get_parent_item_or_none()
        if parent_item:
            return parent_item.get_env_parameter(
                key=key,
                default=default,
            )
        return default

    def get_item_name(self) -> str:
        # Mey be refactored soon.
        return self.base_name

    def get_options_providers(self) -> list[type[AbstractOptionsProvider]]:
        from wexample_filestate.options_provider.default_options_provider import (
            DefaultOptionsProvider,
        )

        providers = super().get_options_providers()
        if len(providers) > 0:
            return providers

        return [
            DefaultOptionsProvider,
        ]

    def get_path(self) -> Path:
        from pathlib import Path

        # Base path is specified, for instance for the tree root.
        if self.base_path is not None:
            base_path = Path(self.base_path)
        else:
            base_path = self.get_parent_item().get_path()

        return base_path / Path(self.get_item_name())

    def get_relative_path(self) -> Path | None:
        root = self.get_root()
        if root:
            return self.get_path().relative_to(root.get_path())
        return None

    def get_source(self) -> SourceFileOrDirectory:
        assert self.source is not None
        return self.source

    def is_active(self) -> bool:
        from wexample_filestate.option.active_option import (
            ActiveOption,
        )

        active_option = self.get_option(ActiveOption)
        return not active_option or ActiveOption.is_active(
            active_option.get_value().raw
        )

    def locate_source(self, path: Path) -> SourceFileOrDirectoryType:
        from wexample_filestate.item.item_source_directory import ItemSourceDirectory
        from wexample_filestate.item.item_source_file import ItemSourceFile

        if path.is_file():
            self.source = ItemSourceFile(
                path=path,
            )
        elif path.is_dir():
            self.source = ItemSourceDirectory(
                path=path,
            )

        return self.source

    def operation_dispatch_event(
        self,
        operation: AbstractOperation | type[AbstractOperation],
        suffix: str | None = None,
        payload: Mapping[str, Any] | None = None,
        **kwargs,
    ) -> None:
        if payload is None:
            payload = {}
        payload["operation"] = operation

        self.dispatch(
            event=operation.get_event_name(suffix=suffix), payload=payload, **kwargs
        )

    def render_display_path(self) -> str:
        from wexample_helpers.helpers.cli import cli_make_clickable_path

        return cli_make_clickable_path(
            path=self.get_path(),
            short_title=self.get_display_path(),
        )

    def rollback(self) -> FileStateResult:
        from wexample_filestate.result.file_state_result import FileStateResult

        result = FileStateResult(state_manager=self, rollback=True)

        # Pop the last batch of operations from history stack
        if self.operations_history:
            last_batch = self.operations_history.pop()
            result.operations.extend(last_batch)
            result.apply_operations()
        else:
            self.io.info(message="No operations to rollback")

        self.last_result = result
        return result

    def try_create_operation_from_option(
        self: TargetFileOrDirectoryType,
        option: OptionMixin,
        scopes: set[Scope],
        filter_operation: str | None = None,
    ) -> AbstractOperation | None:
        """Try to create an operation from an option.

        Returns None if no operation is needed or if the option doesn't support the new interface.
        """
        if not type(option).matches_scope_filter(scopes):
            return None

        if self.is_file() and not option.applicable_on_file():
            return None

        if self.is_directory() and not option.applicable_on_directory():
            return None

        if not self.get_path().exists() and not option.applicable_on_missing():
            return None

        if not option.applicable_on_empty_content_file():
            if not self.get_local_file().read().strip():
                return None

        # Create the required operation (returns None if satisfied/not applicable)
        operation = option.create_required_operation(target=self, scopes=scopes)
        if operation is None:
            return None

        # Apply filters
        if not self._operation_passes_filters(operation, scopes, filter_operation):
            return None

        return operation

    def _find_first_operation(
        self: TargetFileOrDirectoryType,
        scopes: set[Scope],
        filter_operation: str | None = None,
    ) -> AbstractOperation | None:
        """Find the first option that requires an operation and return it.

        Returns None if no operation is required.
        """
        for option in self.options.values():
            operation = self.try_create_operation_from_option(
                option, scopes, filter_operation
            )
            if operation is not None:
                return operation
        return None

    def _get_bubbling_parent(self):
        return self.get_parent_item_or_none()

    def _init_listeners(self) -> None:
        """Add event listeners"""

    def _operation_passes_filters(
        self,
        operation: AbstractOperation,
        scopes: set[Scope],
        filter_operation: str | None = None,
    ) -> bool:
        """Check if operation passes the provided filters."""
        if filter_operation is not None and not operation.__class__.matches_filter(
            filter_operation
        ):
            return False

        if not type(operation).matches_scope_filter(scopes):
            return False

        return True

    def _path_matches(self, filter_path: str) -> bool:
        import fnmatch

        if not filter_path.startswith("*"):
            filter_path = "*" + filter_path
        if not filter_path.endswith("*"):
            filter_path = filter_path + "*"

        return fnmatch.fnmatch(str(self.get_path()), filter_path)
