from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_filestate.config_value.content_config_value import ContentConfigValue
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_wex_core.workdir.workdir import Workdir


@base_class
class VersionContentConfigValue(ContentConfigValue):
    workdir: Workdir

    def get_str(self, type_check: bool = True) -> str:
        from wexample_helpers.helpers.string import string_ensure_end_with_new_line

        return string_ensure_end_with_new_line(
            self.workdir.get_config()
            .search(path="global.version", default=self.raw)
            .get_str()
        )

    def to_option_raw_value(self) -> Any:
        return self
