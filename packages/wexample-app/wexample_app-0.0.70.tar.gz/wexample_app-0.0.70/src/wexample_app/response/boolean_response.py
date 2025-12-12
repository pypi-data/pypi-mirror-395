from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_app.response.abstract_response import AbstractResponse

if TYPE_CHECKING:
    from wexample_app.const.types import ResponsePrintable


@base_class
class BooleanResponse(AbstractResponse):
    content: bool = public_field(description="Boolean value of the response")

    def get_printable(self) -> ResponsePrintable:
        from wexample_helpers.helpers.string import string_render_boolean

        return string_render_boolean(self.content)
