from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from wexample_app.resolver.abstract_command_resolver import (
    AbstractCommandResolver as BaseAbstractCommandResolver,
)
from wexample_helpers.classes.abstract_method import abstract_method

if TYPE_CHECKING:
    from wexample_app.common.command_request import CommandRequest
    from wexample_helpers.const.types import Kwargs, StringsList, StructuredData

    from wexample_wex_core.common.command_method_wrapper import CommandMethodWrapper
    from wexample_wex_core.context.execution_context import ExecutionContext
    from wexample_wex_core.middleware.abstract_middleware import AbstractMiddleware


class AbstractCommandResolver(BaseAbstractCommandResolver, ABC):
    @classmethod
    def build_command_from_function(cls, command_wrapper: CommandMethodWrapper):
        parts = cls.build_command_parts_from_function_name(
            command_wrapper.function.__name__
        )

        return cls.build_command_from_parts(parts)

    @classmethod
    def build_command_from_parts(cls, parts: StringsList) -> str:
        """
        Returns the "default" format (addons style)
        """
        from wexample_helpers.helpers.string import string_to_kebab_case

        from wexample_wex_core.const.globals import (
            COMMAND_SEPARATOR_ADDON,
            COMMAND_SEPARATOR_GROUP,
        )

        # Convert each part to kebab-case
        kebab_parts = [string_to_kebab_case(part) for part in parts]

        return f"{kebab_parts[0]}{COMMAND_SEPARATOR_ADDON}{kebab_parts[1]}{COMMAND_SEPARATOR_GROUP}{kebab_parts[2]}"

    @classmethod
    def build_command_parts_from_function_name(cls, function_name: str) -> StringsList:
        """
        Returns the "default" format (addons style)
        """
        from wexample_wex_core.const.globals import COMMAND_SEPARATOR_FUNCTION_PARTS

        return function_name.split(COMMAND_SEPARATOR_FUNCTION_PARTS)[:3]

    def build_execution_context(
        self,
        middleware: AbstractMiddleware | None,
        command_wrapper: CommandMethodWrapper,
        request: CommandRequest,
        function_kwargs: Kwargs,
    ) -> ExecutionContext:
        from wexample_wex_core.context.execution_context import ExecutionContext

        return ExecutionContext(
            middleware=middleware,
            command_wrapper=command_wrapper,
            request=request,
            function_kwargs=function_kwargs,
        )

    @abstract_method
    def build_registry_data(self) -> StructuredData:
        pass
