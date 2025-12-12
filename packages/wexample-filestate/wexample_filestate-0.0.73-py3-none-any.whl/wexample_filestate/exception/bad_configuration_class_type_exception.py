from __future__ import annotations

from typing import Any

from wexample_helpers.exception.undefined_exception import UndefinedException


class BadConfigurationClassTypeException(UndefinedException):
    def __init__(self, class_definition: Any, **kwargs) -> None:
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.item.item_target_file import ItemTargetFile

        # If not given a type at all, report the actual type/value
        if not isinstance(class_definition, type):
            provided_type = type(class_definition).__name__
            super().__init__(
                message=(
                    f"Invalid value for 'class' option: type '{provided_type}'. "
                    f"Expected a class (subclass of '{ItemTargetDirectory.__name__}' or "
                    f"'{ItemTargetFile.__name__}'), got {class_definition!r}."
                ),
                **kwargs,
            )
            return

        super().__init__(
            message=(
                f"Invalid class for 'class' option: '{class_definition.__module__}.{class_definition.__name__}'. "
                f"Expected a subclass of '{ItemTargetDirectory.__name__}' or "
                f"'{ItemTargetFile.__name__}'."
            ),
            **kwargs,
        )
