from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_app.common.abstract_kernel_child import AbstractKernelChild

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )

    from wexample_app.common.abstract_kernel import AbstractKernel
    from wexample_app.const.types import ResponsePrintable


@base_class
class AbstractResponse(AbstractKernelChild, BaseClass):
    content: Any = public_field(default=None, description="The response content")
    kernel: AbstractKernel = public_field(
        description="The kernel that produced the response"
    )

    def get_formatted(self, output_format: str) -> str:
        """Get the formatted response content according to the specified format.

        This method handles all output formats and always returns a string.
        Dispatches to specific format methods based on output_format.

        Args:
            output_format: The desired output format (str, json, yaml, etc.)

        Returns:
            The formatted response as a string
        """
        from wexample_app.const.output import (
            OUTPUT_FORMAT_JSON,
            OUTPUT_FORMAT_STR,
            OUTPUT_FORMAT_YAML,
        )

        if output_format == OUTPUT_FORMAT_JSON:
            return self._get_formatted_json_content()

        elif output_format == OUTPUT_FORMAT_YAML:
            return self._get_formatted_yaml_content()

        elif output_format == OUTPUT_FORMAT_STR:
            prompt_response = self._get_formatted_prompt_response()

            if prompt_response and self.kernel and self.kernel.io:
                # Print via kernel io and return empty string (io already printed)
                self.kernel.io.print_response(response=prompt_response)
                return ""

            # Fallback to simple string if no prompt response
            return self.get_wrapped_printable()

        else:
            # Unknown format, fallback to string representation
            return self.get_wrapped_printable()

    @abstract_method
    def get_printable(self) -> ResponsePrintable:
        pass

    def get_wrapped_printable(self) -> str:
        printable = self.get_printable()

        if printable is None:
            return ""

        return printable

    def _get_formatted_json_content(self) -> str:
        """Get the response content formatted as JSON.

        Default implementation returns the string representation.
        Subclasses can override for custom JSON serialization.

        Returns:
            JSON string representation
        """
        import json

        return json.dumps(self.content, indent=2)

    def _get_formatted_prompt_response(self) -> AbstractPromptResponse | None:
        """Get a prompt response for structured IO display.

        Default implementation returns None (no special prompt rendering).
        Subclasses can override to provide custom prompt responses.

        Returns:
            A prompt response for display, or None for default string output
        """
        return None

    def _get_formatted_yaml_content(self) -> str:
        """Get the response content formatted as YAML.

        Default implementation returns the string representation.
        Subclasses can override for custom YAML serialization.

        Returns:
            YAML string representation
        """
        import yaml

        return yaml.dump(str(self.get_printable()), default_flow_style=False)
