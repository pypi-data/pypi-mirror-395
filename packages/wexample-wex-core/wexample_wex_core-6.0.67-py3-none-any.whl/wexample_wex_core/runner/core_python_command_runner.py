from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_app.runner.python_command_runner import PythonCommandRunner

if TYPE_CHECKING:
    from wexample_app.common.command import Command

    from wexample_wex_core.common.command_request import CommandRequest


class CorePythonCommandRunner(PythonCommandRunner):
    def build_runnable_command(self, request: CommandRequest) -> Command | None:
        from wexample_wex_core.command.extended_command import ExtendedCommand
        from wexample_wex_core.common.command_method_wrapper import CommandMethodWrapper
        from wexample_wex_core.exception.command_function_build_failed_exception import (
            CommandFunctionBuildFailedException,
        )

        command_wrapper = self._build_command_function(request=request)
        if not isinstance(command_wrapper, CommandMethodWrapper):
            actual_type = type(command_wrapper).__name__
            raise CommandFunctionBuildFailedException(
                command_name=request.name,
                expected_type=CommandMethodWrapper.__name__,
                actual_type=actual_type,
            )

        return ExtendedCommand(kernel=self.kernel, command_wrapper=command_wrapper)
