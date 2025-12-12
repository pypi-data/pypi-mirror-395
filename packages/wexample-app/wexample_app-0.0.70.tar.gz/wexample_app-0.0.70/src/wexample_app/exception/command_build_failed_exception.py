from __future__ import annotations

from wexample_app.exception.app_runtime_exception import AppRuntimeException
from wexample_app.exception.exception_data import CommandBuildFailedData


class CommandBuildFailedException(AppRuntimeException):
    """Exception raised when a command cannot be built by its resolver."""

    error_code: str = "COMMAND_BUILD_FAILED"

    def __init__(
        self,
        command_name: str,
        resolver_name: str,
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        data: CommandBuildFailedData = {
            "command_name": command_name,
            "resolver_name": resolver_name,
        }

        super().__init__(
            message=f"Failed to build command '{command_name}' with resolver: {resolver_name}",
            data=data,
            cause=cause,
            previous=previous,
        )
