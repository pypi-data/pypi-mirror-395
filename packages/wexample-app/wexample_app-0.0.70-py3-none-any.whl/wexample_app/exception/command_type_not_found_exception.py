from __future__ import annotations

from wexample_app.exception.app_runtime_exception import AppRuntimeException
from wexample_app.exception.exception_data import CommandTypeNotFoundData


class CommandTypeNotFoundException(AppRuntimeException):
    """Exception raised when the system cannot determine the type of a command."""

    error_code: str = "COMMAND_TYPE_NOT_FOUND"

    def __init__(
        self,
        command_name: str,
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        data: CommandTypeNotFoundData = {"command_name": command_name}

        super().__init__(
            message=f"Unable to determine command type for: {command_name}",
            data=data,
            cause=cause,
            previous=previous,
        )
