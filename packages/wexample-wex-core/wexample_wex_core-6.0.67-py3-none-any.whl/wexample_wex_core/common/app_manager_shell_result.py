from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from wexample_app.const.globals import APP_PATH_APP_MANAGER
from wexample_app.const.path import APP_DIR_PATH_RELATIVE_OUTPUT
from wexample_config.config_value.config_value import ConfigValue
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.classes.shell_result import ShellResult
from wexample_helpers.helpers.file import file_remove_if_exists
from wexample_helpers.helpers.json import json_load_if_valid


@dataclass
class AppManagerShellResult(ShellResult):
    output_json: None | str = private_field(
        default=None,
        description="The parsed output json",
    )
    request_id: str = private_field(
        description="The request id that produced the response",
    )

    def __post_init__(self) -> None:
        path = (
            self.cwd
            / APP_PATH_APP_MANAGER
            / APP_DIR_PATH_RELATIVE_OUTPUT
            / self.request_id
        )

        # Store output for later usage.
        self.output_json = json_load_if_valid(path=path)

        # We avoid storing requests output.
        file_remove_if_exists(path)

    @classmethod
    def from_shell_result(
        cls, result: ShellResult, request_id: str
    ) -> AppManagerShellResult:
        """Convert ShellResult to AppManagerShellResult."""
        return cls(
            args=result.args,
            cwd=result.cwd,
            duration=result.duration,
            end_time=result.end_time,
            returncode=result.returncode,
            start_time=result.start_time,
            stderr=result.stderr,
            stdout=result.stdout,
            request_id=request_id,
        )

    def get_output(self) -> Any:
        return self.output_json

    def get_output_value(self) -> ConfigValue:
        return ConfigValue(raw=self.output_json)
