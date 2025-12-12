from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from wexample_wex_core.resolver.abstract_command_resolver import AbstractCommandResolver

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_app.common.command_request import CommandRequest


class ServiceCommandResolver(AbstractCommandResolver):
    @classmethod
    def get_pattern(cls) -> str:
        from wexample_wex_core.const.globals import COMMAND_PATTERN_SERVICE

        return COMMAND_PATTERN_SERVICE

    @classmethod
    def get_type(cls) -> str:
        from wexample_wex_core.const.globals import COMMAND_TYPE_SERVICE

        return COMMAND_TYPE_SERVICE

    def build_command_function_name(self, request: CommandRequest) -> str | None:
        import re

        return re.sub(r"[^a-zA-Z0-9_]", "", request.name.replace("/", "__"))

    def build_command_path(
        self, request: CommandRequest, extension: str
    ) -> Path | None:
        base = self.kernel.workdir.get_path()
        return base / "cli" / f"{request.name}.{extension}"

    def build_registry_data(self, test: bool = False):
        registry = {}

        return registry
