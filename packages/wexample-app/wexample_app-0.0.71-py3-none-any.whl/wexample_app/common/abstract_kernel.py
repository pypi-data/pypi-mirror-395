from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_filestate.workdir.mixin.with_workdir_mixin import WithWorkdirMixin
from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.mixin.printable_mixin import PrintableMixin
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.mixin.with_entrypoint_path_mixin import WithEntrypointPathMixin
from wexample_helpers_yaml.classes.mixin.has_yaml_env_keys_file import (
    HasYamlEnvKeysFile,
)
from wexample_prompt.mixins.with_io_methods import WithIoMethods

from wexample_app.service.mixins.service_container_mixin import ServiceContainerMixin

if TYPE_CHECKING:
    from wexample_app.common.command_request import CommandRequest
    from wexample_app.output.abstract_app_output_handler import (
        AbstractAppOutputHandler,
    )
    from wexample_app.response.abstract_response import AbstractResponse


@base_class
class AbstractKernel(
    ServiceContainerMixin,
    HasYamlEnvKeysFile,
    WithWorkdirMixin,
    WithIoMethods,
    PrintableMixin,
    WithEntrypointPathMixin,
):
    root_request: Any | None = public_field(
        default=None,
        description="The initial request that may have launched sub requests",
    )

    def create_output_handlers(self) -> [AbstractAppOutputHandler]:
        """Initialize the output handlers with default stdout handler."""
        from wexample_app.output.app_stdout_output_handler import (
            AppStdoutOutputHandler,
        )

        return [AppStdoutOutputHandler(kernel=self)]

    def execute_kernel_command(self, request: CommandRequest) -> AbstractResponse:
        # Save unique root request
        self.root_request = self.root_request if self.root_request else request

        return request.execute()

    def execute_kernel_command_and_print(self, request: CommandRequest) -> None:
        """Execute a command and print its response using all active output handlers.

        Args:
            request: The command request to execute
        """
        response = self.execute_kernel_command(request=request)

        for output_handler in self.create_output_handlers():
            output_handler.print(request=request, response=response)

    def get_expected_env_keys(self) -> list[str]:
        from wexample_app.const.globals import ENV_VAR_NAME_APP_ENV

        return [ENV_VAR_NAME_APP_ENV]

    def setup(self) -> AbstractKernel:
        from pathlib import Path

        from wexample_helpers.const.globals import FILE_NAME_ENV, FILE_NAME_ENV_YAML

        # Use entrypoint as env root if not defied.
        self.env_files_directory = self.env_files_directory or str(
            Path(self.entrypoint_path).parent
        )

        env_dir_path = self._get_env_files_directory()
        self._init_io_manager()
        self._init_env_file(env_dir_path / FILE_NAME_ENV)
        self._init_env_file_yaml(env_dir_path / FILE_NAME_ENV_YAML)
        self._init_workdir(entrypoint_path=self.entrypoint_path, io=self.io)

        return self

    def _get_available_output_handlers(
        self,
    ) -> dict[str, type[AbstractAppOutputHandler]]:
        """Get the registry of available output handlers.

        Returns:
            Dictionary mapping handler names to handler classes
        """
        from wexample_app.const.output import OUTPUT_TARGET_STDOUT
        from wexample_app.output.app_stdout_output_handler import (
            AppStdoutOutputHandler,
        )

        return {OUTPUT_TARGET_STDOUT: AppStdoutOutputHandler}

    def _get_command_request_class(self) -> type[CommandRequest]:
        from wexample_app.common.command_request import CommandRequest

        return CommandRequest
