from __future__ import annotations

from typing import TYPE_CHECKING, cast

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_app.resolver.abstract_command_resolver import AbstractCommandResolver
    from wexample_app.runner.abstract_command_runner import AbstractCommandRunner
    from wexample_app.service.mixins.service_container_mixin import (
        ServiceContainerMixin,
    )


@base_class
class CommandRunnerKernel(BaseClass):
    def get_resolver(
        self: ServiceContainerMixin, type: str
    ) -> AbstractCommandResolver | None:
        from wexample_app.const.registries import REGISTRY_KERNEL_COMMAND_RESOLVER
        from wexample_app.resolver.abstract_command_resolver import (
            AbstractCommandResolver,
        )

        return cast(
            AbstractCommandResolver,
            self.get_service_registry(REGISTRY_KERNEL_COMMAND_RESOLVER).get(key=type),
        )

    def get_resolvers(
        self: ServiceContainerMixin,
    ) -> dict[str, AbstractCommandResolver]:
        from wexample_app.const.registries import REGISTRY_KERNEL_COMMAND_RESOLVER
        from wexample_app.resolver.abstract_command_resolver import (
            AbstractCommandResolver,
        )

        return cast(
            dict[str, AbstractCommandResolver],
            self.get_service_registry(REGISTRY_KERNEL_COMMAND_RESOLVER).all_instances(),
        )

    def get_runner(
        self: ServiceContainerMixin, type: str
    ) -> AbstractCommandRunner | None:
        from wexample_app.const.registries import REGISTRY_KERNEL_COMMAND_RUNNERS
        from wexample_app.runner.abstract_command_runner import AbstractCommandRunner

        return cast(
            AbstractCommandRunner,
            self.get_service_registry(REGISTRY_KERNEL_COMMAND_RUNNERS).get(key=type),
        )

    def get_runners(self: ServiceContainerMixin) -> dict[str, AbstractCommandRunner]:
        from wexample_app.const.registries import REGISTRY_KERNEL_COMMAND_RUNNERS
        from wexample_app.runner.abstract_command_runner import AbstractCommandRunner

        return cast(
            dict[str, AbstractCommandRunner],
            self.get_service_registry(REGISTRY_KERNEL_COMMAND_RUNNERS).all_instances(),
        )

    def _get_command_resolvers(self) -> list[type[AbstractCommandResolver]]:
        return []

    def _get_command_runners(self) -> list[type[AbstractCommandRunner]]:
        from wexample_app.runner.python_command_runner import PythonCommandRunner

        return [
            # Default runner.
            PythonCommandRunner
        ]

    def _init_resolvers(
        self: CommandRunnerKernel | ServiceContainerMixin,
    ) -> None:
        from wexample_app.const.registries import REGISTRY_KERNEL_COMMAND_RESOLVER
        from wexample_app.service.service_registry import ServiceRegistry

        cast(
            ServiceRegistry,
            self.register_services(
                REGISTRY_KERNEL_COMMAND_RESOLVER, self._get_command_resolvers()
            ),
        ).instantiate_all(kernel=self)

    def _init_runners(self: [CommandRunnerKernel, ServiceContainerMixin]) -> None:
        from wexample_app.const.registries import REGISTRY_KERNEL_COMMAND_RUNNERS
        from wexample_app.service.service_registry import ServiceRegistry

        cast(
            ServiceRegistry,
            self.register_services(
                REGISTRY_KERNEL_COMMAND_RUNNERS, self._get_command_runners()
            ),
        ).instantiate_all(kernel=self)
