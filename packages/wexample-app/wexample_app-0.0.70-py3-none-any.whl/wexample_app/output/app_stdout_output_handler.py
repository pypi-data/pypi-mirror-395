from __future__ import annotations

import sys

from wexample_helpers.decorator.base_class import base_class

from wexample_app.common.command_request import CommandRequest
from wexample_app.output.abstract_app_output_handler import (
    AbstractAppOutputHandler,
)


@base_class
class AppStdoutOutputHandler(AbstractAppOutputHandler):
    """Output handler for app responses that writes to stdout.

    This handler is specifically designed for AbstractResponse objects from the app package.
    It detects the response type and uses appropriate rendering:
    - DictResponse: renders via io.properties() for structured display
    - Other responses: uses get_wrapped_printable() for simple string output
    """

    def get_target_name(self) -> str:
        """Get the target name for this handler.

        Returns:
            'stdout'
        """
        from wexample_app.const.output import OUTPUT_TARGET_STDOUT

        return OUTPUT_TARGET_STDOUT

    def _write_output(self, request: CommandRequest, content: str) -> str | None:
        """Write the formatted content to stdout.

        Args:
            request: The command request (unused for stdout)
            content: The formatted content to write

        Returns:
            The written string
        """
        sys.stdout.write(content + "\n")
        sys.stdout.flush()
        return content
