from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_helpers.const.types import AnyCallable

    from wexample_wex_core.common.command_method_wrapper import CommandMethodWrapper


def command(type: str, description: str | None = None):
    def decorator(function: AnyCallable) -> CommandMethodWrapper:
        from wexample_wex_core.common.command_method_wrapper import CommandMethodWrapper

        return CommandMethodWrapper(
            type=type, function=function, description=description
        )

    return decorator
