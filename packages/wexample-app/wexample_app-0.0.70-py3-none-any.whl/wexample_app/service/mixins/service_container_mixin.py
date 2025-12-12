from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.service.mixins.registry_container_mixin import (
    RegistryContainerMixin,
)

if TYPE_CHECKING:
    from wexample_helpers.service.registry import Registry

    from wexample_app.service.service_registry import ServiceRegistry


@base_class
class ServiceContainerMixin(RegistryContainerMixin):
    """Container for managing multiple service registries."""

    def get_service(self, registry_name: str, key: str) -> Any | None:
        """Retrieve a service from a specific registry by its key."""
        return self.get_item(registry_name, key)

    def get_service_registry(self, registry_name: str) -> ServiceRegistry:
        from wexample_app.service.service_registry import ServiceRegistry

        return cast(ServiceRegistry, self.get_registry(registry_name))

    def register_service(self, registry_name: str, key: str, service: Any) -> Registry:
        """Register a service in a specific registry."""
        return self.register_item(registry_name, key, service)

    def register_services(self, registry_name: str, services: list[Any]) -> Registry:
        """Register multiple services at once in a specific registry."""
        return self.register_items(registry_name, services)

    def _get_registry_class_type(self) -> type[ServiceRegistry]:
        from wexample_app.service.service_registry import ServiceRegistry

        return ServiceRegistry
