from __future__ import annotations

from wexample_app.exception.app_runtime_exception import AppRuntimeException
from wexample_app.exception.exception_data import CommandModuleLoadErrorData


class CommandModuleLoadErrorException(AppRuntimeException):
    """Exception raised when a Python module cannot be loaded from a command file."""

    error_code: str = "COMMAND_MODULE_LOAD_ERROR"

    def __init__(
        self,
        file_path: str,
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        data: CommandModuleLoadErrorData = {"file_path": file_path}

        super().__init__(
            message=f"Failed to load Python module from file: {file_path}",
            data=data,
            cause=cause,
            previous=previous,
        )
