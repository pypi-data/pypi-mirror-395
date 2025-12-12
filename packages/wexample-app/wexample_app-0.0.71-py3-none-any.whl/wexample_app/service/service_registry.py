from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.service.registry import Registry

from wexample_app.common.service.service_mixin import ServiceMixin
from wexample_app.service.mixins.service_container_mixin import ServiceContainerMixin

if TYPE_CHECKING:
    from wexample_app.service.mixins.service_container_mixin import (
        ServiceContainerMixin,
    )


@base_class
class ServiceRegistry(Registry[type[ServiceMixin]]):
    """Registry for managing services of type ServiceMixin."""

    container: ServiceContainerMixin = public_field(description="The service container")
    _service_instances: dict[str, ServiceMixin] = private_field(
        description="The service container", factory=dict
    )

    def all_classes(self) -> list[type[ServiceMixin]]:
        """Return all registered service classes."""
        return list(self._items.values())

    def all_instances(self) -> dict[str, ServiceMixin]:
        """Return all instantiated services."""
        return self._service_instances.copy()

    def get(self, key: str | type[ServiceMixin], **kwargs) -> ServiceMixin | None:
        """
        Retrieve a service by its key. Instantiates the service if it doesn't exist.
        Additional kwargs are passed to the service constructor.
        """
        # If key is a class, use its name
        if isinstance(key, type):
            key = key.get_snake_short_class_name()

        # Return existing instance if already instantiated
        if key in self._service_instances:
            return self._service_instances[key]

        # Get service class and create new instance if exists
        service_class = self._items.get(key)
        if service_class:
            # Create instance with kernel
            instance = service_class(**kwargs).setup()
            self._service_instances[key] = instance
            return instance

        self._raise_error_if_expected(key, None)

        return None

    def get_all(self) -> dict[str, ServiceMixin]:
        """Get all instantiated services."""
        return self._service_instances

    def get_class(self, key: str) -> type[ServiceMixin] | None:
        """Get the service class without instantiating it."""
        return self._items.get(key)

    def instantiate_all(self, **kwargs) -> dict[str, ServiceMixin]:
        """
        Instantiate all registered services with the given kwargs.
        Returns a dictionary of service instances keyed by their names.
        """
        for key, service_class in self._items.items():
            if key not in self._service_instances:
                self.get(key, **kwargs)
        return self.all_instances()

    def register(self, key: str, service_class: type[ServiceMixin]) -> None:
        """Register a service class in the registry."""
        self._items[key] = service_class
