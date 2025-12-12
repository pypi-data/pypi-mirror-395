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
class DictResponse(AbstractResponse):
    """Response containing structured dictionary data."""

    content: dict[str, Any] = public_field(
        description="Dictionary containing structured response data"
    )

    def __attrs_post_init__(self) -> None:
        from wexample_app.exception.response_invalid_content_type_exception import (
            ResponseInvalidContentTypeException,
        )

        self._execute_super_attrs_post_init_if_exists()

        if not isinstance(self.content, dict):
            raise ResponseInvalidContentTypeException(
                content=self.content, allowed_content_types=[dict]
            )

    def get_printable(self) -> ResponsePrintable:
        return str(self.content)

    def _get_formatted_prompt_response(self) -> AbstractPromptResponse:
        """Get a properties prompt response for structured display.

        Returns:
            PropertiesPromptResponse for displaying the dictionary as properties
        """
        from wexample_prompt.responses.data.properties_prompt_response import (
            PropertiesPromptResponse,
        )

        return PropertiesPromptResponse.create_properties(
            properties=self.content,
        )

    def _get_formatted_yaml_content(self) -> str:
        """Get the dict content formatted as YAML.

        Returns:
            YAML string representation of the dictionary
        """
        import yaml

        return yaml.dump(self.content, default_flow_style=False)
