from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_wex_core.const.globals import COMMAND_TYPE_ADDON
from wexample_wex_core.decorator.command import command

if TYPE_CHECKING:
    from wexample_wex_core.context.execution_context import ExecutionContext


@command(type=COMMAND_TYPE_ADDON)
def git__reset__permissions(
    context: ExecutionContext,
) -> str:
    from wexample_helpers.helpers.shell import shell_run

    # Reset file permissions to match HEAD without changing content
    shell_run(
        "git diff --summary | grep 'mode change' | awk '{print $NF}' | xargs -r git checkout-index --force --",
        cwd=context.kernel._call_workdir.get_path(),
        shell=True,
        inherit_stdio=True,
    )
