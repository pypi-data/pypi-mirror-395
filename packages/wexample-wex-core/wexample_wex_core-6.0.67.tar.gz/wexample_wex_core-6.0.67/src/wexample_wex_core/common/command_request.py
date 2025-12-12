from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_app.common.command_request import CommandRequest as BaseCommandRequest
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    pass


@base_class
class CommandRequest(BaseCommandRequest):
    request_id: str = public_field(description="A unique id from the initial execution")

    def get_addon_manager(self):
        return self.resolver.get_request_addon_manager(self)
