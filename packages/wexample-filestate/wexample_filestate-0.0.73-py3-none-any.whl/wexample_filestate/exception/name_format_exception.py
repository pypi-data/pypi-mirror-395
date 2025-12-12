from __future__ import annotations

from wexample_filestate.exception.abstract_file_state_exception import (
    AbstractFileStateException,
)


class NameFormatException(AbstractFileStateException):
    """Exception raised when a file name does not match the required format rules."""

    error_code: str = "FILE_STATE_NAME_FORMAT_ERROR"

    def __init__(self, message: str, file_name: str = None, **kwargs) -> None:
        super().__init__(message, **kwargs)
        self.file_name = file_name
