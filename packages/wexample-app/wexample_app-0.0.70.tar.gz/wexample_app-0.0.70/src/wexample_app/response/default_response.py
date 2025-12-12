from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_app.response.abstract_response import AbstractResponse

if TYPE_CHECKING:
    from wexample_app.const.types import ResponsePrintable


@base_class
class DefaultResponse(AbstractResponse):
    content: Any = public_field(description="Scalar content of the response")

    def __attrs_post_init__(self) -> None:
        from wexample_helpers.const.types import Scalar
        from wexample_helpers.helpers.args import args_is_basic_value

        from wexample_app.exception.response_invalid_content_type_exception import (
            ResponseInvalidContentTypeException,
        )

        self._execute_super_attrs_post_init_if_exists()

        if not args_is_basic_value(self.content):
            raise ResponseInvalidContentTypeException(
                content=self.content, allowed_content_types=Scalar
            )

    def get_printable(self) -> ResponsePrintable:
        # For now consider every output as a string
        return str(self.content)
