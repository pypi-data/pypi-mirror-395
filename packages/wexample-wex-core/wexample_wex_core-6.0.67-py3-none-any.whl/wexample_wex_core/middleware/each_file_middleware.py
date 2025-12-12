from __future__ import annotations

import os
from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_wex_core.middleware.abstract_each_path_middleware import (
    AbstractEachPathMiddleware,
)

if TYPE_CHECKING:
    from wexample_app.command.option import Option
    from wexample_helpers.const.types import Kwargs

    from wexample_wex_core.common.command_method_wrapper import CommandMethodWrapper
    from wexample_wex_core.common.command_request import CommandRequest


@base_class
class EachFileMiddleware(AbstractEachPathMiddleware):
    def validate_options(
        self,
        command_wrapper: CommandMethodWrapper,
        request: CommandRequest,
        function_kwargs: Kwargs,
    ) -> bool:
        from wexample_wex_core.exception.path_is_not_file_command_option_exception import (
            PathIsNotFileCommandOptionException,
        )

        valid = super().validate_options(
            command_wrapper=command_wrapper,
            request=request,
            function_kwargs=function_kwargs,
        )

        # Do not search files in directory, so we check validity of curren given path.
        if valid and not self.expand_glob:
            file_path = self._get_option_file_path(function_kwargs=function_kwargs)
            if not os.path.isfile(file_path):
                option = self.get_option_by_name("file")
                raise PathIsNotFileCommandOptionException(
                    option_name=option.name, file_path=file_path
                )

            return True

        return valid

    def _get_middleware_options(self) -> list[Option]:
        """Get the default file option definition."""
        from wexample_app.command.option import Option

        return [
            Option(
                name="file",
                type=str,
                required=True,
                description="Path to local file",
            )
        ]

    def _should_process_item(self, request: CommandRequest, item_path: str) -> bool:
        return os.path.isfile(item_path)
