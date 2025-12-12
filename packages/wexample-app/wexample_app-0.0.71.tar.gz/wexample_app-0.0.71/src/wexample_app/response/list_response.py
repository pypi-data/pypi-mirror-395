from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_app.response.abstract_response import AbstractResponse

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )

    from wexample_app.const.types import ResponsePrintable


@base_class
class ListResponse(AbstractResponse):
    """Response containing structured list data."""

    content: list[Any] = public_field(
        description="List containing structured response data"
    )

    def __attrs_post_init__(self) -> None:
        from wexample_app.exception.response_invalid_content_type_exception import (
            ResponseInvalidContentTypeException,
        )

        self._execute_super_attrs_post_init_if_exists()

        if not isinstance(self.content, list):
            raise ResponseInvalidContentTypeException(
                content=self.content, allowed_content_types=[list]
            )

    def get_printable(self) -> ResponsePrintable:
        return str(self.content)

    def _get_formatted_prompt_response(self) -> AbstractPromptResponse:
        """Get a list prompt response for structured display.

        Returns:
            ListPromptResponse for displaying the list items
        """
        from wexample_prompt.responses.data.list_prompt_response import (
            ListPromptResponse,
        )

        return ListPromptResponse.create_list(
            items=self.content,
        )

    def _get_formatted_yaml_content(self) -> str:
        """Get the list content formatted as YAML.

        Returns:
            YAML string representation of the list
        """
        import yaml

        return yaml.dump(self.content, default_flow_style=False)
