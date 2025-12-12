from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

from wexample_app.common.abstract_kernel_child import AbstractKernelChild
from wexample_app.const.output import OUTPUT_FORMAT_STR, OUTPUT_TARGET_STDOUT

if TYPE_CHECKING:
    from wexample_helpers.const.types import StringsMatch

    from wexample_app.common.mixins.command_runner_kernel import CommandRunnerKernel
    from wexample_app.resolver.abstract_command_resolver import AbstractCommandResolver
    from wexample_app.response.abstract_response import AbstractResponse
    from wexample_app.runner.abstract_command_runner import AbstractCommandRunner


@base_class
class CommandRequest(AbstractKernelChild):
    arguments: list[str | int] = public_field(
        factory=list,
        description="List of command arguments passed to the request",
    )
    kernel: CommandRunnerKernel = public_field(
        description="Reference to the main command runner kernel"
    )
    name: str = public_field(
        description="Name of the command to execute",
    )
    output_format: str | None = public_field(
        default=None,
        description="The output format (str, json, yaml, etc.)",
    )
    output_target: list[str] | None = public_field(
        default=None,
        description="The list of output targets (stdout, file, etc.)",
    )
    path: str | None = public_field(
        default=None,
        description="Optional path context for the command",
    )
    type: str | None = public_field(
        default=None,
        description="Optional type classification of the command",
    )
    _match: StringsMatch | None = private_field(
        default=None,
        description="Internal string matching result used during command resolution",
    )
    _resolver: AbstractCommandResolver | None = private_field(
        default=None,
        description="Command resolver instance responsible for analyzing the request",
    )
    _runner: AbstractCommandRunner | None = private_field(
        default=None,
        description="Command runner instance responsible for executing the request",
    )

    def __attrs_post_init__(self) -> None:
        from wexample_app.exception.command_runner_not_found_exception import (
            CommandRunnerNotFoundException,
        )
        from wexample_app.exception.command_type_not_found_exception import (
            CommandTypeNotFoundException,
        )

        self.type = self._guess_type()
        if self.type is None:
            raise CommandTypeNotFoundException(self.name)

        self.resolver = self._get_resolver()
        self.runner = self._guess_runner()
        if not self.runner:
            raise CommandRunnerNotFoundException(command_name=self.name)

        self.path = self.runner.build_command_path(request=self)

        if self.output_target is None:
            self.output_target = [OUTPUT_TARGET_STDOUT]

        if self.output_format is None:
            self.output_format = OUTPUT_FORMAT_STR

    @property
    def match(self) -> StringsMatch:
        return self._match

    @match.setter
    def match(self, value: StringsMatch) -> None:
        self._match = value

    @property
    def resolver(self) -> AbstractCommandResolver:
        return self._resolver

    @resolver.setter
    def resolver(self, value: AbstractCommandResolver) -> None:
        self._resolver = value

    @property
    def runner(self) -> AbstractCommandRunner:
        return self._runner

    @runner.setter
    def runner(self, value: AbstractCommandRunner) -> None:
        self._runner = value

    def execute(self) -> AbstractResponse:
        from wexample_app.exception.app_runtime_exception import AppRuntimeException
        from wexample_app.exception.command_build_failed_exception import (
            CommandBuildFailedException,
        )
        from wexample_app.exception.command_runner_missing_exception import (
            CommandRunnerMissingException,
        )
        from wexample_app.response.null_response import NullResponse

        if self.runner is None:
            raise CommandRunnerMissingException(command_name=self.name)

        try:
            command = self.resolver.build_command(request=self)
            if command is None:
                raise CommandBuildFailedException(
                    command_name=self.name,
                    resolver_name=self.resolver.__class__.__name__,
                )

            return command.execute_request_and_normalize(self)
        except AppRuntimeException as e:
            e.format_error_with_kernel(kernel=self.kernel)

        return NullResponse(kernel=self.kernel)

    def _get_resolver(self) -> AbstractCommandResolver:
        from wexample_app.exception.command_resolver_not_found_exception import (
            CommandResolverNotFoundException,
        )

        resolver = self.kernel.get_resolver(self.type)
        if resolver is None:
            raise CommandResolverNotFoundException(self.type)
        return resolver

    def _guess_runner(self) -> AbstractCommandRunner | None:
        for runner in self.kernel.get_runners().values():
            if runner.will_run(self):
                return runner
        return None

    def _guess_type(self) -> str | None:
        for resolver in self.kernel.get_resolvers().values():
            match = resolver.supports(request=self)
            if match is not None:
                self.match = match
                return resolver.get_type()
        return None
