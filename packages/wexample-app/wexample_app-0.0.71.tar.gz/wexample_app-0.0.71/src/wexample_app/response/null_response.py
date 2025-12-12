from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_app.response.abstract_response import AbstractResponse

if TYPE_CHECKING:
    from wexample_app.const.types import ResponsePrintable


class NullResponse(AbstractResponse):
    def get_printable(self) -> ResponsePrintable:
        return None
