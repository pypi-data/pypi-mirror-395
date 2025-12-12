from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_app.common.abstract_kernel_child import AbstractKernelChild
from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.mixin.printable_mixin import PrintableMixin
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class
from wexample_prompt.mixins.with_io_manager import WithIoManager

if TYPE_CHECKING:
    from wexample_app.common.mixins.command_runner_kernel import CommandRunnerKernel
    from wexample_helpers.const.types import AnyCallable, Kwargs
    from wexample_prompt.common.progress.progress_handle import ProgressHandle

    from wexample_wex_core.common.command_method_wrapper import CommandMethodWrapper
    from wexample_wex_core.common.command_request import CommandRequest
    from wexample_wex_core.middleware.abstract_middleware import AbstractMiddleware


@base_class
class ExecutionContext(
    AbstractKernelChild,
    WithIoManager,
    PrintableMixin,
    BaseClass,
):
    command_wrapper: CommandMethodWrapper = public_field(
        description="Wrapper around the command method being executed",
    )
    function: AnyCallable | None = public_field(
        default=None,
        description="Optional custom function to execute instead of command_wrapper.function",
    )
    function_kwargs: Kwargs = public_field(
        factory=dict,
        description="Keyword arguments passed to the command function",
    )
    kernel: CommandRunnerKernel = public_field(
        description="The kernel is extracted from request", default=None
    )
    middleware: AbstractMiddleware | None = public_field(
        description="Optional middleware applied in this execution context",
    )
    request: CommandRequest = public_field(
        description="The command request associated with this execution",
    )
    _current_progress: ProgressHandle | None = private_field(
        default=None,
        description="Internal progress handle used to track execution progress",
    )

    def __attrs_post_init__(self) -> None:
        self.function_kwargs["context"] = self
        self.kernel = self.request.kernel
        self.io = self.kernel.io

    def create_progress_range(self, **kwargs) -> ProgressHandle:
        self._current_progress = self.get_or_create_progress().create_range_handle(
            **kwargs
        )
        return self._current_progress

    def finish_progress(self, **kwargs) -> ProgressHandle:
        self._current_progress.finish()

        self._current_progress = self._current_progress.parent
        self._current_progress.update(**kwargs)
        return self._current_progress

    def get_or_create_progress(self, **kwargs) -> ProgressHandle:
        if self._current_progress is None:
            self._current_progress = self.io.progress(
                **kwargs, context=self.io.create_context()
            ).get_handle()
        return self._current_progress
