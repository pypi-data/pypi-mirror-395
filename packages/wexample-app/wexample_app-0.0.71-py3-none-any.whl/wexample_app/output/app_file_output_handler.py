from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_app.common.command_request import CommandRequest
from wexample_app.output.abstract_app_output_handler import (
    AbstractAppOutputHandler,
)

if TYPE_CHECKING:
    from pathlib import Path


@base_class
class AppFileOutputHandler(AbstractAppOutputHandler):
    """Output handler for app responses that writes to a file.

    This handler writes the response content to a specified file path.
    """

    file_path: Path = public_field(description="Path to the output file")

    def get_target_name(self) -> str:
        """Get the target name for this handler.

        Returns:
            'file'
        """
        from wexample_app.const.output import OUTPUT_TARGET_FILE

        return OUTPUT_TARGET_FILE

    def _get_file_path(self, request: CommandRequest) -> Path:
        """Get the file path for output.

        Can be overridden by subclasses to compute path dynamically.

        Args:
            request: The command request

        Returns:
            The file path to write to
        """
        return self.file_path

    def _write_output(self, request: CommandRequest, content: str) -> str | None:
        """Write the formatted content to a file.

        Args:
            request: The command request (for dynamic path building)
            content: The formatted content to write

        Returns:
            The written string
        """
        from wexample_helpers.helpers.cli import cli_make_clickable_path
        from wexample_prompt.enums.verbosity_level import VerbosityLevel

        file_path = self._get_file_path(request)
        file_path.write_text(content, encoding="utf-8")
        self.kernel.io.log(
            message=f"Output saved to: {cli_make_clickable_path(file_path)}",
            verbosity=VerbosityLevel.MAXIMUM,
        )
        return content
