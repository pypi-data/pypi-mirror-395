from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_wex_core.const.globals import COMMAND_TYPE_ADDON
from wexample_wex_core.decorator.command import command

if TYPE_CHECKING:
    from wexample_wex_core.context.execution_context import ExecutionContext


@command(type=COMMAND_TYPE_ADDON)
def default__info__show(context: ExecutionContext) -> None:
    import platform

    registry = context.kernel.get_configuration_registry()

    context.io.properties(
        title="General",
        properties={
            "Location": context.kernel.workdir.get_path(),
            "Environment": registry.env,
            "Arguments": context.kernel._sys_argv,
            "Python version": platform.python_version(),
        },
    )
