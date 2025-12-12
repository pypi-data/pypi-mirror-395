from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_app.response.abstract_response import AbstractResponse

if TYPE_CHECKING:
    from wexample_app.const.types import ResponsePrintable


@base_class
class FailureResponse(AbstractResponse):
    exception: Any | None = public_field(
        description="The message to display", default=None
    )
    message: str = public_field(
        description="The original exception instance", default=None
    )

    def get_printable(self) -> ResponsePrintable:
        # Build a string representation from exception and/or message
        if self.exception and self.message:
            return f"{self.message}: {str(self.exception)}"
        elif self.exception:
            return str(self.exception)
        elif self.message:
            return self.message
        else:
            return "Unknown failure"
