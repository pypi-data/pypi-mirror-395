from __future__ import annotations

from pathlib import Path

from wexample_app.output.app_file_output_handler import AppFileOutputHandler
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_wex_core.common.command_request import CommandRequest


@base_class
class RequestFileOutputHandler(AppFileOutputHandler):
    """Extended file output handler for core kernel with predefined output path."""

    file_path: Path = public_field(default=None, description="Path to the output file")

    def _get_file_path(self, request: CommandRequest) -> Path:
        return (
            request.kernel.workdir.get_tmp().get_path() / "output" / request.request_id
        )
