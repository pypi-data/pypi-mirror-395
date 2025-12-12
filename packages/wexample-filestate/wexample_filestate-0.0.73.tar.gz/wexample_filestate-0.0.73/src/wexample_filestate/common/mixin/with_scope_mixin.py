from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_filestate.enum.scopes import Scope


class WithScopeMixin:
    @classmethod
    def get_scopes(cls) -> None | list[Scope]:
        return None

    @classmethod
    def matches_scope_filter(cls, scopes: Iterable[Scope]) -> bool:
        """
        Return True when the provided scope filter should allow instances of this class.

        If the class does not declare any scopes, it is considered compatible with any filter.
        """
        declared_scopes = cls.get_scopes()

        if declared_scopes is None:
            return True

        declared_set = set(declared_scopes)
        filter_set = set(scopes)

        return len(declared_set.intersection(filter_set)) > 0
