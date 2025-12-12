from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_wex_core.common.abstract_addon_manager import AbstractAddonManager

if TYPE_CHECKING:
    from wexample_wex_core.middleware.abstract_middleware import AbstractMiddleware


class DefaultAddonManager(AbstractAddonManager):
    def get_middlewares_classes(self) -> list[type[AbstractMiddleware]]:
        from wexample_wex_core.middleware.each_directory_middleware import (
            EachDirectoryMiddleware,
        )
        from wexample_wex_core.middleware.each_file_middleware import EachFileMiddleware
        from wexample_wex_core.middleware.each_path_middleware import EachPathMiddleware

        return [
            EachDirectoryMiddleware,
            EachFileMiddleware,
            EachPathMiddleware,
        ]
