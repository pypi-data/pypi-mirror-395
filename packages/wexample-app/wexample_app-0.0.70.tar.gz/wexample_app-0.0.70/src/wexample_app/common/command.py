from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_app.common.abstract_kernel_child import AbstractKernelChild

if TYPE_CHECKING:
    from collections.abc import Callable

    from wexample_app.common.abstract_kernel import AbstractKernel
    from wexample_app.common.command_request import CommandRequest
    from wexample_app.response.abstract_response import AbstractResponse


@base_class
class Command(AbstractKernelChild):
    function: Callable[..., Any] = public_field(
        default=None, description="The function to execute"
    )
    kernel: AbstractKernel = public_field(default=None, description="The app kernel")

    def execute_request(self, request: CommandRequest) -> Any:
        # Basic way to execute command.
        return self.function(kernel=self.kernel, arguments=request.arguments)

    def execute_request_and_normalize(
        self, request: CommandRequest
    ) -> AbstractResponse:
        from wexample_app.helpers.response import response_normalize

        return response_normalize(
            kernel=self.kernel, response=self.execute_request(request=request)
        )
