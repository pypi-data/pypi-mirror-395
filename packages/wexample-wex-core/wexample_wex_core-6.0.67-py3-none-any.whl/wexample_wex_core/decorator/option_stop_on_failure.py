from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_helpers.const.types import AnyCallable

    from wexample_wex_core.common.command_method_wrapper import CommandMethodWrapper

OPTION_NAME_STOP_ON_FAILURE: str = "stop_on_failure"


def option_stop_on_failure() -> AnyCallable:
    def decorator(command_wrapper: CommandMethodWrapper) -> CommandMethodWrapper:
        from wexample_app.command.option import Option

        command_wrapper.set_option(
            Option(
                name=OPTION_NAME_STOP_ON_FAILURE,
                type=bool,
                description="Stop execution when exception occurs",
                required=False,
                default=False,
                is_flag=True,
            )
        )

        return command_wrapper

    return decorator
