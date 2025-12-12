from __future__ import annotations

from wexample_helpers.exception.mixin.not_allowed_item_mixin import (
    NotAllowedItemMixin,
)

from wexample_app.exception.app_runtime_exception import AppRuntimeException


class CommandUnexpectedArgumentException(AppRuntimeException, NotAllowedItemMixin):
    """Exception raised when an unexpected argument is provided to a command."""

    error_code: str = "COMMAND_UNEXPECTED_ARGUMENT"

    def __init__(
        self,
        argument: str,
        allowed_arguments: list[str],
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        # Use mixin methods to generate message and data
        message = self.format_not_allowed_item_message(
            item_type="argument",
            item_value=argument,
            allowed_values=allowed_arguments,
        )

        data = self.get_not_allowed_item_data(
            item_type="argument",
            item_value=argument,
            allowed_values=allowed_arguments,
        )

        super().__init__(
            message=message,
            data=data,
            cause=cause,
            previous=previous,
        )
