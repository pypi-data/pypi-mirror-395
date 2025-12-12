from __future__ import annotations

from wexample_wex_core.exception.abstract_command_option_exception import (
    AbstractCommandOptionException,
)


class PathNotFoundCommandOptionException(AbstractCommandOptionException):
    """Exception raised when a file specified in a command option is not found."""

    error_code: str = "FILE_NOT_FOUND_COMMAND_OPTION"

    def __init__(
        self,
        option_name: str,
        file_path: str,
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        super().__init__(
            option_name=option_name,
            message=f"File or directory not found, specified in option '{option_name}': '{file_path}'",
            data={file_path: file_path},
            cause=cause,
            previous=previous,
        )
