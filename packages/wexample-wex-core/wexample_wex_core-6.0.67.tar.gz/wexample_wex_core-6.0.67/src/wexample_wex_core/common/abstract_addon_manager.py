from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from wexample_app.common.abstract_kernel_child import AbstractKernelChild
from wexample_filestate.workdir.mixin.with_workdir_mixin import WithWorkdirMixin
from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import (
    HasSnakeShortClassNameClassMixin,
)
from wexample_helpers.classes.mixin.has_two_steps_init import HasTwoStepInit
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_wex_core.middleware.abstract_middleware import AbstractMiddleware


@base_class
class AbstractAddonManager(
    AbstractKernelChild,
    HasTwoStepInit,
    HasSnakeShortClassNameClassMixin,
    WithWorkdirMixin,
):
    def __attrs_post_init__(self) -> None:
        import inspect
        import os.path

        # Get the path of the actual addon manager class file
        manager_file = inspect.getfile(self.__class__)

        self._init_workdir(
            entrypoint_path=os.path.dirname(manager_file),
            io=self.kernel.io,
        )

    @classmethod
    def get_class_name_suffix(cls) -> str | None:
        return "AddonManager"

    @abstract_method
    @classmethod
    def get_package_module(cls) -> Any:
        pass

    @classmethod
    def get_package_source_path(cls) -> Path:
        from wexample_helpers.helpers.module import module_get_path

        return module_get_path(cls.get_package_module())

    def get_middlewares_classes(self) -> list[type[AbstractMiddleware]]:
        return []
