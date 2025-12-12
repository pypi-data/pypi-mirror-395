from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from wexample_wex_core.const.registries import RegistryResolverData
from wexample_wex_core.resolver.abstract_command_resolver import AbstractCommandResolver

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_wex_core.common.abstract_addon_manager import AbstractAddonManager
    from wexample_wex_core.common.command_request import CommandRequest
    from wexample_wex_core.const.registries import RegistryResolverData


class AddonCommandResolver(AbstractCommandResolver):
    @classmethod
    def get_pattern(cls) -> str:
        from wexample_wex_core.const.globals import COMMAND_PATTERN_ADDON

        return COMMAND_PATTERN_ADDON

    @classmethod
    def get_type(cls) -> str:
        from wexample_wex_core.const.globals import COMMAND_TYPE_ADDON

        return COMMAND_TYPE_ADDON

    def build_command_function_name(self, request: CommandRequest) -> str | None:
        from wexample_helpers.helpers.string import string_to_snake_case

        from wexample_wex_core.const.globals import COMMAND_SEPARATOR_FUNCTION_PARTS

        return COMMAND_SEPARATOR_FUNCTION_PARTS.join(
            string_to_snake_case(part)
            for part in self.get_function_name_parts(request.match.groups())
        )

    def build_command_path(
        self, request: CommandRequest, extension: str
    ) -> Path | None:
        from wexample_helpers.helpers.string import string_to_snake_case

        match = request.match

        # Extract addon, group and command from match
        group = string_to_snake_case(match.group(2))
        command = string_to_snake_case(match.group(3))

        addon_manager = self.get_request_addon_manager(request)

        return (
            addon_manager.workdir.get_path()
            / "commands"
            / group
            / f"{command}.{extension}"
        )

    def build_registry_data(self, test: bool = False) -> RegistryResolverData:
        from wexample_wex_core.common.abstract_addon_manager import AbstractAddonManager

        registry: RegistryResolverData = {}

        for addon in self.kernel.get_addons().values():
            assert isinstance(addon, AbstractAddonManager)
            registry[addon.get_snake_short_class_name()] = {}

        return registry

    def get_request_addon_manager(
        self, request: CommandRequest
    ) -> AbstractAddonManager:
        from wexample_helpers.helpers.string import string_to_snake_case

        from wexample_wex_core.exception.addon_not_registered_exception import (
            AddonNotRegisteredException,
        )

        match = request.match
        addon_name = string_to_snake_case(match.group(1))
        addon_registry = self.kernel.get_registry("addon")

        if not addon_registry.has(addon_name):
            # Get list of available addons for better error reporting
            available_addons = list(addon_registry.get_all().keys())
            raise AddonNotRegisteredException(
                addon_name=addon_name, available_addons=available_addons
            )

        return addon_registry.get(addon_name)
