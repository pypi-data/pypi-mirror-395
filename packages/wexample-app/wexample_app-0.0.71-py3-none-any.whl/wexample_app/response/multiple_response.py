from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_app.response.abstract_response import AbstractResponse

if TYPE_CHECKING:
    from wexample_app.const.types import ResponsePrintable


@base_class
class MultipleResponse(AbstractResponse):
    responses: list[Any] = public_field(factory=list, description="List of responses")

    def __attrs_post_init__(self) -> None:
        from wexample_app.exception.response_invalid_content_type_exception import (
            ResponseInvalidContentTypeException,
        )

        super()._execute_super_attrs_post_init_if_exists()

        if not isinstance(self.responses, list):
            raise ResponseInvalidContentTypeException(
                content=self.responses, allowed_content_types=[list]
            )

    def append(self, response: AbstractResponse) -> None:
        from wexample_app.exception.response_invalid_content_type_exception import (
            ResponseInvalidContentTypeException,
        )

        if not isinstance(response, AbstractResponse):
            raise ResponseInvalidContentTypeException(
                content=response, allowed_content_types=[AbstractResponse]
            )

        self.responses.append(response)

    def get_printable(self) -> ResponsePrintable:
        # For now consider every output as a string
        return str(self.responses)
