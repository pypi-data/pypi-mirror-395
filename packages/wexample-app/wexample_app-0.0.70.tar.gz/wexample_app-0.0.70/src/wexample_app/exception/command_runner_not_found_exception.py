from __future__ import annotations

from wexample_app.exception.app_runtime_exception import AppRuntimeException
from wexample_app.exception.exception_data import CommandRunnerNotFoundData


class CommandRunnerNotFoundException(AppRuntimeException):
    """Exception raised when no suitable runner is found for a command.

    This exception is thrown when the system cannot find an appropriate runner
    to execute a command, which means the command cannot be executed.
    """

    error_code: str = "COMMAND_RUNNER_NOT_FOUND"

    def __init__(
        self,
        command_name: str,
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        data: CommandRunnerNotFoundData = {"command_name": command_name}

        super().__init__(
            message=f'No runner found supporting execution of command "{command_name}"',
            data=data,
            cause=cause,
            previous=previous,
        )
