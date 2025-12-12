from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_app.common.abstract_kernel_child import AbstractKernelChild
from wexample_helpers.decorator.base_class import base_class

from wexample_wex_core.workdir.workdir import Workdir

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig
    from wexample_filestate.item.item_target_directory import ItemTargetDirectory
    from wexample_prompt.common.io_manager import IoManager

    from wexample_wex_core.common.kernel import Kernel


@base_class
class KernelWorkdir(AbstractKernelChild, Workdir):
    # Class-scoped constant for the tmp shortcut
    SHORTCUT_REGISTRY: ClassVar[str] = "registry"

    @classmethod
    def create_from_kernel(
        cls, kernel: Kernel, io: IoManager, **kwargs
    ) -> ItemTargetDirectory:
        return super().create_from_path(
            path=kernel.entrypoint_path, kernel=kernel, io=io, **kwargs
        )

    def get_tmp(self) -> ItemTargetDirectory | None:
        from wexample_wex_core.const.globals import (
            CORE_DIR_NAME_TMP,
        )

        return self.find_by_name(item_name=CORE_DIR_NAME_TMP)

    def prepare_value(self, raw_value: DictConfig | None = None) -> DictConfig:
        from wexample_filestate.const.disk import DiskItemType

        from wexample_wex_core.const.globals import (
            CORE_DIR_NAME_TMP,
            CORE_FILE_NAME_REGISTRY,
        )
        from wexample_wex_core.path.kernel_registry_file import KernelRegistryFile

        config = super().prepare_value(raw_value=raw_value)

        raw_value["children"] = raw_value.get("children", [])
        raw_value["children"].append(
            {
                "shortcut": CORE_DIR_NAME_TMP,
                "name": CORE_DIR_NAME_TMP,
                "type": DiskItemType.DIRECTORY,
                "should_exist": True,
                "children": [
                    {
                        "name": "output",
                        "type": DiskItemType.DIRECTORY,
                        "should_exist": True,
                    },
                    {
                        "class": KernelRegistryFile,
                        "name": CORE_FILE_NAME_REGISTRY,
                        "shortcut": KernelWorkdir.SHORTCUT_REGISTRY,
                        "type": DiskItemType.FILE,
                        "should_exist": True,
                    },
                ],
            }
        )

        return config
