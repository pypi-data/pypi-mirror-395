from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, ClassVar

from wexample_filestate.item.file.xml_file import XmlFile

if TYPE_CHECKING:
    from wexample_helpers.const.types import StructuredData


class ImlFile(XmlFile):
    """
    IntelliJ IDEA/PyCharm .iml helper with a minimal, editor-agnostic module skeleton pre-populated.
    """

    EXTENSION_IML: ClassVar[str] = "iml"
    MODULE_ROOT_COMPONENT_NAME: ClassVar[str] = "NewModuleRootManager"
    MODULE_ROOT_COMPONENT_INHERIT_COMPILER_OUTPUT: ClassVar[str] = "true"
    MODULE_DIR_URL: ClassVar[str] = "file://$MODULE_DIR$"

    @classmethod
    def get_extension(cls) -> str:
        return cls.EXTENSION_IML

    def dumps(self, content: StructuredData | None) -> str:
        from xmltodict import unparse

        if not isinstance(content, dict):
            return super().dumps(content)

        normalized = self._ensure_minimal_structure(content)
        xml_body = unparse(
            normalized,
            pretty=True,
            short_empty_elements=True,
            full_document=False,
        )

        # xmltodict does not emit a declaration when full_document=False; prepend one ourselves.
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_body

    def loads(self, text: str, strict: bool = False) -> StructuredData:
        parsed = super().loads(text, strict=strict)
        if not isinstance(parsed, dict):
            parsed = {}
        return self._ensure_minimal_structure(parsed)

    def _coerce_list_of_dicts(self, value: Any) -> list[dict[str, Any]]:
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        if isinstance(value, dict):
            return [value]
        return []

    def _default_exclude_folders(self) -> Iterable[dict[str, Any]]:
        return ()

    def _default_module_attributes(self) -> dict[str, str]:
        return {"@version": "4"}

    def _default_order_entries(self) -> Iterable[dict[str, Any]]:
        return ()

    def _default_source_folders(self) -> Iterable[dict[str, Any]]:
        return ()

    def _ensure_component_defaults(self, component: dict[str, Any]) -> None:
        component.setdefault(
            "@inherit-compiler-output",
            self.MODULE_ROOT_COMPONENT_INHERIT_COMPILER_OUTPUT,
        )
        component.setdefault("exclude-output", None)

        content = component.get("content")
        if isinstance(content, list):
            content_dicts = [c for c in content if isinstance(c, dict)]
            content = content_dicts[0] if content_dicts else {}
        elif not isinstance(content, dict):
            content = {}

        content.setdefault("@url", self.MODULE_DIR_URL)

        source_folders = self._merge_with_defaults(
            content.get("sourceFolder"),
            self._default_source_folders(),
            key="@url",
        )
        if source_folders:
            content["sourceFolder"] = source_folders

        exclude_folders = self._merge_with_defaults(
            content.get("excludeFolder"),
            self._default_exclude_folders(),
            key="@url",
        )
        if exclude_folders:
            content["excludeFolder"] = exclude_folders

        component["content"] = content
        order_entries = self._merge_order_entries(component.get("orderEntry"))
        if order_entries:
            component["orderEntry"] = order_entries

    def _ensure_component_list(self, module: dict[str, Any]) -> list[dict[str, Any]]:
        component = module.get("component")
        if isinstance(component, list):
            components = [c for c in component if isinstance(c, dict)]
        elif isinstance(component, dict):
            components = [component]
        else:
            components = []
        return components

    def _ensure_minimal_structure(self, data: StructuredData | None) -> StructuredData:
        from copy import deepcopy

        draft: dict[str, Any] = deepcopy(data) if isinstance(data, dict) else {}

        module = self._ensure_module_section(draft)
        components = self._ensure_component_list(module)
        root_component = self._ensure_root_component(components)
        self._ensure_component_defaults(root_component)

        module["component"] = components
        draft["module"] = module
        return draft

    def _ensure_module_section(self, container: dict[str, Any]) -> dict[str, Any]:
        module = container.get("module")
        if not isinstance(module, dict):
            module = {}
        defaults = self._default_module_attributes()
        for key, value in defaults.items():
            module.setdefault(key, value)
        return module

    def _ensure_root_component(
        self, components: list[dict[str, Any]]
    ) -> dict[str, Any]:
        for component in components:
            if component.get("@name") == self.MODULE_ROOT_COMPONENT_NAME:
                return component
        component = {"@name": self.MODULE_ROOT_COMPONENT_NAME}
        components.append(component)
        return component

    def _expected_file_name_extension(self) -> str:
        return self.EXTENSION_IML

    def _merge_order_entries(self, current: Any) -> list[dict[str, Any]]:
        entries = self._coerce_list_of_dicts(current)
        merged: list[dict[str, Any]] = []
        seen_types: set[str | None] = set()

        def append_entry(entry: dict[str, Any]) -> None:
            from copy import deepcopy

            entry_type = entry.get("@type")
            if entry_type in seen_types:
                return
            merged.append(deepcopy(entry))
            seen_types.add(entry_type)

        # Preserve existing order first.
        for entry in entries:
            append_entry(entry)

        # Ensure required defaults are present.
        for default in self._default_order_entries():
            append_entry(default)

        return merged

    def _merge_with_defaults(
        self,
        current: Any,
        defaults: Iterable[dict[str, Any]],
        *,
        key: str,
    ) -> list[dict[str, Any]]:
        from copy import deepcopy

        items = self._coerce_list_of_dicts(current)
        seen = {item.get(key) for item in items}
        for default in defaults:
            value = default.get(key)
            if value not in seen:
                items.append(deepcopy(default))
                seen.add(value)
        return items
