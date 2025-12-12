from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.decorator.base_class import base_class

from wexample_app.common.abstract_kernel_child import AbstractKernelChild

if TYPE_CHECKING:
    from wexample_app.common.command_request import CommandRequest
    from wexample_app.response.abstract_response import AbstractResponse


@base_class
class AbstractAppOutputHandler(AbstractKernelChild):
    """Base class for app output handlers.

    Output handlers are responsible for processing and displaying AbstractResponse objects.
    Different implementations can write to stdout, files, buffers, or other destinations.
    """

    @abstract_method
    def get_target_name(self) -> str:
        """Get the name of this output target.

        Returns:
            The target name (e.g., 'stdout', 'file')
        """
        self._raise_not_implemented_error()

    def print(self, request: CommandRequest, response: AbstractResponse) -> str | None:
        """Print or process the response.

        Args:
            request: The command request containing output format
            response: The AbstractResponse to print or process

        Returns:
            The printed/processed string, or None if nothing was output
        """
        from wexample_app.response.null_response import NullResponse

        # Skip null responses
        if isinstance(response, NullResponse):
            return None

        # Get the output format from request
        output_format = request.output_format

        # Get formatted output (response handles io.print internally if needed)
        formatted = response.get_formatted(output_format=output_format)

        # Delegate to subclass for actual output
        if formatted:
            return self._write_output(request=request, content=formatted)

        return None

    @abstract_method
    def _write_output(self, request: CommandRequest, content: str) -> str | None:
        """Write the formatted content to the output destination.

        Args:
            request: The command request (for dynamic path building or context)
            content: The formatted content to write

        Returns:
            The written string, or None if nothing was written
        """
        self._raise_not_implemented_error()
