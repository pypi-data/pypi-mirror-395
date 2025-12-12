from __future__ import annotations

from wexample_app.exception.app_runtime_exception import AppRuntimeException
from wexample_app.exception.exception_data import CommandRunnerMissingData


class CommandRunnerMissingException(AppRuntimeException):
    """Exception raised when no runner is available for a command."""

    error_code: str = "COMMAND_RUNNER_MISSING"

    def __init__(
        self,
        command_name: str,
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        data: CommandRunnerMissingData = {"command_name": command_name}

        super().__init__(
            message=f"No runner available for command: {command_name}",
            data=data,
            cause=cause,
            previous=previous,
        )
