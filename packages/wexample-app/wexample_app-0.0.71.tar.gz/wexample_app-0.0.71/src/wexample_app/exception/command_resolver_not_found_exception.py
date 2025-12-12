from __future__ import annotations

from wexample_app.exception.app_runtime_exception import AppRuntimeException
from wexample_app.exception.exception_data import CommandResolverNotFoundData


class CommandResolverNotFoundException(AppRuntimeException):
    """Exception raised when no resolver is found for a specific command type."""

    error_code: str = "COMMAND_RESOLVER_NOT_FOUND"

    def __init__(
        self,
        command_type: str,
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        data: CommandResolverNotFoundData = {"command_type": command_type}

        super().__init__(
            message=f"No resolver found for command type: {command_type}",
            data=data,
            cause=cause,
            previous=previous,
        )
