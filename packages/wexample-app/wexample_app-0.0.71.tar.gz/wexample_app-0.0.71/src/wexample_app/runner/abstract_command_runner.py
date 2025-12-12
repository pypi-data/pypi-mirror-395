from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.mixin.printable_mixin import PrintableMixin
from wexample_helpers.decorator.base_class import base_class

from wexample_app.common.abstract_kernel_child import AbstractKernelChild
from wexample_app.common.service.service_mixin import ServiceMixin

if TYPE_CHECKING:
    from wexample_helpers.const.types import AnyCallable

    from wexample_app.common.command import Command
    from wexample_app.common.command_request import CommandRequest


@base_class
class AbstractCommandRunner(
    AbstractKernelChild, ServiceMixin, PrintableMixin, BaseClass
):
    @classmethod
    def get_class_name_suffix(cls) -> str | None:
        return "CommandRunner"

    def build_runnable_command(self, request: CommandRequest) -> Command | None:
        from wexample_app.common.command import Command

        function = self._build_command_function_or_fail(request=request)

        return Command(kernel=self.kernel, function=function)

    def will_run(self, request: CommandRequest) -> bool:
        return False

    @abstract_method
    def _build_command_function(self, request: CommandRequest) -> AnyCallable:
        pass

    def _build_command_function_or_fail(self, request: CommandRequest) -> AnyCallable:
        from wexample_app.exception.command_function_not_found_exception import (
            CommandFunctionNotFoundException,
        )

        function = self._build_command_function(request=request)

        if not function:
            path = self.build_command_path(request)
            function_name = request.resolver.build_command_function_name(request)
            raise CommandFunctionNotFoundException(
                function_name=function_name, module_path=path
            )

        return function
