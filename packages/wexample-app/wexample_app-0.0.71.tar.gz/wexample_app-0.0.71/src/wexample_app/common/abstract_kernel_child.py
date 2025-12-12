from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_app.common.abstract_kernel import AbstractKernel


@base_class
class AbstractKernelChild(BaseClass):
    kernel: AbstractKernel = public_field(description="Reference to the main kernel")
