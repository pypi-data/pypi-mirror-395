from __future__ import annotations

from wexample_wex_core.exception.abstract_command_option_exception import (
    AbstractCommandOptionException,
)


class PathIsNotFileCommandOptionException(AbstractCommandOptionException):
    """Exception raised when a path specified in a command option exists but is not a file."""

    error_code: str = "PATH_IS_NOT_FILE_COMMAND_OPTION"

    def __init__(
        self,
        option_name: str,
        file_path: str,
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        super().__init__(
            option_name=option_name,
            message=f"Path exists but is not a file, specified in option '{option_name}': '{file_path}'",
            data={"file_path": file_path},
            cause=cause,
            previous=previous,
        )
