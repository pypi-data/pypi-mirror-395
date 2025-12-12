from __future__ import annotations

from wexample_helpers.exception.undefined_exception import UndefinedException


class AbstractFileStateException(UndefinedException):
    """Base exception class for all filestate-related exceptions."""

    error_code: str = "FILE_STATE_ERROR"
