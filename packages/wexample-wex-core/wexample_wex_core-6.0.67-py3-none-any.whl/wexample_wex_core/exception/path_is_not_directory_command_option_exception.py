from __future__ import annotations

from wexample_wex_core.exception.abstract_command_option_exception import (
    AbstractCommandOptionException,
)


class PathIsNotDirectoryCommandOptionException(AbstractCommandOptionException):
    """Exception raised when a path specified in a command option exists but is not a directory."""

    error_code: str = "PATH_IS_NOT_DIRECTORY_COMMAND_OPTION"

    def __init__(
        self,
        option_name: str,
        directory_path: str,
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        super().__init__(
            option_name=option_name,
            message=f"Path exists but is not a directory, specified in option '{option_name}': '{directory_path}'",
            data={"directory_path": directory_path},
            cause=cause,
            previous=previous,
        )
