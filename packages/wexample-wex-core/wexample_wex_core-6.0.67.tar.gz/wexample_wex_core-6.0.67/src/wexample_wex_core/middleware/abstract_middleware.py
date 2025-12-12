from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.mixin.has_class_dependencies import HasClassDependencies
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import (
    HasSnakeShortClassNameClassMixin,
)
from wexample_helpers.classes.mixin.has_two_steps_init import HasTwoStepInit
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_app.command.option import Option
    from wexample_helpers.const.types import Kwargs

    from wexample_wex_core.common.command_method_wrapper import CommandMethodWrapper
    from wexample_wex_core.common.command_request import CommandRequest
    from wexample_wex_core.context.execution_context import ExecutionContext


@base_class
class AbstractMiddleware(
    HasSnakeShortClassNameClassMixin,
    HasTwoStepInit,
    HasClassDependencies,
    BaseClass,
):
    max_iterations: int | None = public_field(
        default=None,
        description="Maximum number of iterations allowed for this middleware",
    )
    normalized_options: list[Option] = public_field(
        factory=list,
        description="List of normalized option objects for middleware configuration",
    )
    options: list[Option] = public_field(
        factory=list,
        description="Option objects provided to the middleware",
    )
    parallel: None | bool | str = public_field(
        default=False,
        description="Whether the middleware should run in parallel (bool, str, or None)",
    )
    show_progress: None | bool | str = public_field(
        default=False,
        description="Whether to display a progress indicator during execution",
    )
    stop_on_failure: None | bool | str = public_field(
        default=False,
        description="Whether to stop execution immediately if a failure occurs",
    )

    def __attrs_post_init__(self) -> None:
        self.normalized_options = self._init_options()

    @classmethod
    def get_class_name_suffix(cls) -> str | None:
        return "Middleware"

    def append_options(
        self, request: CommandRequest, command_wrapper: CommandMethodWrapper
    ) -> None:
        from wexample_app.command.option import Option

        from wexample_wex_core.const.middleware import MIDDLEWARE_OPTION_VALUE_OPTIONAL

        if self.parallel:
            self.stop_on_failure = False
            request.kernel.io.log(
                'Option "stop_on_failure" will be ignored due to parallelization'
            )

        if self.parallel == MIDDLEWARE_OPTION_VALUE_OPTIONAL:
            command_wrapper.set_option(
                Option(
                    name="parallel",
                    short_name="pll",
                    type=bool,
                    description="Execute async when possible",
                    default=False,
                    is_flag=True,
                )
            )

        if self.show_progress == MIDDLEWARE_OPTION_VALUE_OPTIONAL:
            command_wrapper.set_option(
                Option(
                    name="progress",
                    short_name="prgs",
                    type=bool,
                    description="Display progress bar",
                    default=False,
                    is_flag=True,
                )
            )

        if self.stop_on_failure == MIDDLEWARE_OPTION_VALUE_OPTIONAL:
            command_wrapper.set_option(
                Option(
                    name="stop-on-failure",
                    short_name="sof",
                    type=bool,
                    description="Stop at first failure response if not async",
                    default=False,
                    is_flag=True,
                )
            )

    def build_execution_contexts(
        self,
        command_wrapper: CommandMethodWrapper,
        request: CommandRequest,
        function_kwargs: Kwargs,
    ) -> list[ExecutionContext]:
        from wexample_wex_core.context.execution_context import ExecutionContext

        self.validate_options(
            command_wrapper=command_wrapper,
            request=request,
            function_kwargs=function_kwargs,
        )

        return [
            ExecutionContext(
                middleware=self,
                command_wrapper=command_wrapper,
                request=request,
                function_kwargs=function_kwargs,
            )
        ]

    def get_option_by_name(self, name: str) -> Option | None:
        """Get an option by its name from the normalized options."""
        for option in self.normalized_options:
            if option.name == name:
                return option
        return None

    def validate_options(
        self,
        command_wrapper: CommandMethodWrapper,
        request: CommandRequest,
        function_kwargs: Kwargs,
    ) -> bool:
        return True

    def _get_middleware_options(self) -> list[Option]:
        return []

    def _init_options(self) -> list[Option]:
        """Get middleware options."""
        return self._get_middleware_options()
