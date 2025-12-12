from __future__ import annotations

from enum import Enum, auto


class Scope(Enum):
    CONTENT = auto()
    LOCATION = auto()
    NAME = auto()
    OWNERSHIP = auto()
    PERMISSIONS = auto()
    REMOTE = auto()
    TIMESTAMPS = auto()
