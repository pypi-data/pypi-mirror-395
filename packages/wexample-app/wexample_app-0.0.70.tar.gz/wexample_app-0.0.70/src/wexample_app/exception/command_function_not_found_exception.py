from __future__ import annotations

from wexample_app.exception.app_runtime_exception import AppRuntimeException
from wexample_app.exception.exception_data import CommandFunctionNotFoundData


class CommandFunctionNotFoundException(AppRuntimeException):
    """Exception raised when a command function cannot be found in the module."""

    error_code: str = "COMMAND_FUNCTION_NOT_FOUND"

    def __init__(
        self,
        function_name: str,
        module_path: str,
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        data: CommandFunctionNotFoundData = {
            "function_name": function_name,
            "module_path": module_path,
        }

        super().__init__(
            message=f"Command function '{function_name}' not found in module: {module_path}",
            data=data,
            cause=cause,
            previous=previous,
        )
