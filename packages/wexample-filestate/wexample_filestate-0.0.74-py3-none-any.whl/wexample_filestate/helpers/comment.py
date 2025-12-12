"""Helper functions for filestate inline markers used in TOML comments."""

from __future__ import annotations


def comment_indicates_protected(comment: str | None) -> bool:
    """Return True if the given inline comment marks the item as protected.

    A comment is considered protective if it contains the base tag and any known action.
    Matching is case-insensitive.
    """
    from wexample_filestate.const.filestate_markers import (
        FILESTATE_ACTIONS,
        FILESTATE_TAG,
    )

    if not comment:
        return False
    c = str(comment).strip().lower()
    if FILESTATE_TAG not in c:
        return False
    return any(action in c for action in FILESTATE_ACTIONS)
