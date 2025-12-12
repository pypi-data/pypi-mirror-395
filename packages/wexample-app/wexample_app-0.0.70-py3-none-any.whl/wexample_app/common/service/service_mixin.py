from __future__ import annotations

from wexample_helpers.classes.mixin.has_class_dependencies import HasClassDependencies
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import (
    HasSnakeShortClassNameClassMixin,
)
from wexample_helpers.classes.mixin.has_two_steps_init import HasTwoStepInit
from wexample_helpers.decorator.base_class import base_class
from wexample_prompt.mixins.with_io_methods import WithIoMethods


@base_class
class ServiceMixin(
    WithIoMethods,
    HasSnakeShortClassNameClassMixin,
    HasTwoStepInit,
    HasClassDependencies,
):
    @classmethod
    def get_class_name_suffix(cls) -> str | None:
        return "Service"
