from __future__ import annotations

from wexample_app.exception.app_runtime_exception import AppRuntimeException
from wexample_app.exception.exception_data import CommandFunctionNameMissingData


class CommandFunctionNameMissingException(AppRuntimeException):
    """Exception raised when a command function name cannot be determined."""

    error_code: str = "COMMAND_FUNCTION_NAME_MISSING"

    def __init__(
        self,
        command_name: str,
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        data: CommandFunctionNameMissingData = {"command_name": command_name}

        super().__init__(
            message=f"Command function name could not be determined for: {command_name}",
            data=data,
            cause=cause,
            previous=previous,
        )
