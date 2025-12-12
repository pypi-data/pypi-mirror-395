from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

from wexample_app.command.option import Option
from wexample_app.output.abstract_app_output_handler import AbstractAppOutputHandler

if TYPE_CHECKING:
    from wexample_filestate.utils.file_state_manager import FileStateManager

    from wexample_app.common.abstract_kernel import AbstractKernel
    from wexample_app.common.command_request import CommandRequest
    from wexample_app.const.types import CommandLineArgumentsList


@base_class
class CommandLineKernel(BaseClass):
    _call_workdir: FileStateManager = private_field(
        description="The directory path from where the call has been run"
    )
    _command_argv: list[str] = private_field(
        factory=list,
        description="User command line arguments with core options filtered out",
    )
    _core_argv: list[str] = private_field(
        factory=list, description="Core command arguments processed by the kernel"
    )
    _sys_argv: list[str] = private_field(
        factory=list, description="System command line arguments from sys.argv"
    )
    _sys_argv_end_index: int | None = private_field(
        default=None, description="End index for processing sys.argv slice"
    )
    _sys_argv_start_index: int = private_field(
        default=1, description="Start index for processing sys.argv slice"
    )

    @property
    def call_workdir(self) -> FileStateManager:
        # Getter is non-optional and always returns a conformant type
        return self._call_workdir

    def exec_argv(self: AbstractKernel) -> None:
        """
        Main entrypoint from command line calls.
        May not be called by an internal script.
        """
        try:
            command_requests = self._build_command_requests_from_arguments(
                self._command_argv[
                    self._sys_argv_start_index : self._sys_argv_end_index
                ]
            )
        except Exception as e:
            self.io.error(exception=e, fatal=True)

            return

        for command_request in command_requests:
            self.execute_kernel_command_and_print(command_request)

    def _build_command_requests_from_arguments(
        self: AbstractKernel, arguments: CommandLineArgumentsList
    ) -> list[CommandRequest]:
        # By default, allow one request per execution call.
        return self._build_single_command_request_from_arguments(arguments)

    def _build_single_command_request_from_arguments(
        self: AbstractKernel, arguments: CommandLineArgumentsList
    ):
        return [
            self._get_command_request_class()(
                kernel=self, name=arguments[0], arguments=arguments[1:]
            )
        ]

    def _get_core_args(self: AbstractKernel) -> list[Option]:
        return []

    def _get_default_output_handler_class(self) -> type[AbstractAppOutputHandler]:
        from wexample_app.output.app_stdout_output_handler import (
            AppStdoutOutputHandler,
        )

        return AppStdoutOutputHandler

    def _init_command_line_core_args(self: AbstractKernel) -> None:
        """Parse and handle core arguments, creating filtered _command_argv."""
        from wexample_app.helpers.argument import (
            argument_filter_core_options,
            argument_parse_options,
        )

        core_options = self._get_core_args()

        if not core_options:
            # No core options, user_argv is same as sys_argv
            self._command_argv = self._sys_argv.copy()
            return

        # Parse core arguments from sys_argv in non-strict mode
        # (ignores unknown options that belong to commands)
        parsed_core_args = argument_parse_options(
            arguments=self._sys_argv[1:],  # Skip program name
            options=core_options,
            allowed_option_names=[opt.name for opt in core_options],
            strict=False,
        )

        # Apply parsed values to kernel attributes
        for option in core_options:
            if option.name in parsed_core_args:
                value = parsed_core_args[option.name]

                # Normalize to list if always_list is True
                if option.always_list and not isinstance(value, list):
                    value = [value]

                setattr(self, f"_config_arg_{option.name}", value)

        # Create filtered user_argv without core options
        self._command_argv = [self._sys_argv[0]] + argument_filter_core_options(
            self._sys_argv[1:], core_options
        )

    def _init_command_line_kernel(self: AbstractKernel) -> None:
        import os
        import sys

        from wexample_filestate.utils.file_state_manager import FileStateManager

        self._sys_argv = sys.argv.copy()
        self._call_workdir = FileStateManager.create_from_path(
            path=os.getcwd(), config={}, io=self.io
        )

        self._init_command_line_core_args()
