from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class

from wexample_app.common.command_request import CommandRequest
from wexample_app.output.abstract_app_output_handler import (
    AbstractAppOutputHandler,
)


@base_class
class AppNoneOutputHandler(AbstractAppOutputHandler):
    """Don't return the output."""

    def get_target_name(self) -> str:
        from wexample_app.const.output import OUTPUT_TARGET_NONE

        return OUTPUT_TARGET_NONE

    def _write_output(self, request: CommandRequest, content: str) -> str | None:
        pass
