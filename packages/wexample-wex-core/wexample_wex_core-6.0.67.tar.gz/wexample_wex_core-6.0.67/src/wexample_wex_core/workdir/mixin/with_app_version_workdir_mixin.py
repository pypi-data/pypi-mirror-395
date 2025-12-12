from __future__ import annotations

from typing import Any

from wexample_app.workdir.mixin.with_version_workdir_mixin import (
    WithVersionWorkdirMixin,
)
from wexample_helpers.decorator.base_class import base_class


@base_class
class WithAppVersionWorkdirMixin(WithVersionWorkdirMixin):
    def _get_version_default_content(self) -> Any:
        from wexample_wex_core.config_value.version_content_config_value import (
            VersionContentConfigValue,
        )

        return VersionContentConfigValue(
            raw=super()._get_version_default_content(), workdir=self
        )
