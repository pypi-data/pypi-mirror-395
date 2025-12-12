from __future__ import annotations

from typing import Any

from wexample_app.exception.app_runtime_exception import AppRuntimeException
from wexample_app.exception.exception_data import ResponseInvalidContentTypeData


class ResponseInvalidContentTypeException(AppRuntimeException):
    """Exception raised when a response contains invalid content that cannot be properly processed."""

    error_code: str = "RESPONSE_INVALID_CONTENT"

    def __init__(
        self,
        content: Any,
        allowed_content_types: list[type],
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        from wexample_helpers.helpers.string import string_truncate

        # Get the content type name
        content_type = type(content).__name__

        # Convert to string but limit length to avoid huge error messages
        content_str = string_truncate(str(content), 100)

        # Convert type objects to strings for the allowed values
        allowed_types = [t.__name__ for t in allowed_content_types]

        data: ResponseInvalidContentTypeData = {
            "content_type": content_type,
            "content_value": content_str,
            "allowed_types": allowed_types,
        }

        # Build a descriptive message
        allowed_str = ", ".join(allowed_types)
        message = (
            f"Invalid content type '{content_type}'. Expected one of: {allowed_str}"
        )

        super().__init__(
            message=message,
            data=data,
            cause=cause,
            previous=previous,
        )
