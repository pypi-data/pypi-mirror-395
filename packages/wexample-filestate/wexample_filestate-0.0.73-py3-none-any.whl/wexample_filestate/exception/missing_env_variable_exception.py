from __future__ import annotations

from wexample_filestate.exception.abstract_file_state_exception import (
    AbstractFileStateException,
)


class MissingEnvVariableException(AbstractFileStateException):
    """Exception raised when a required environment variable is missing."""

    error_code: str = "FILE_STATE_MISSING_ENV_VARIABLE"

    def __init__(self, message: str, env_key: str = None, **kwargs) -> None:
        super().__init__(message, **kwargs)
        self.env_key = env_key
