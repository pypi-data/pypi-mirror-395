from __future__ import annotations

from wexample_helpers.exception.undefined_exception import UndefinedException


class CommandFunctionBuildFailedException(UndefinedException):
    """Exception raised when a command function could not be built correctly.

    This exception is thrown when the system tries to build a command function but
    the result is not of the expected type, indicating an issue with the command
    declaration or implementation.
    """

    error_code: str = "COMMAND_FUNCTION_BUILD_FAILED"

    def __init__(
        self,
        command_name: str,
        expected_type: str,
        actual_type: str,
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        # Store attributes as instance attributes
        self.command_name = command_name
        self.expected_type = expected_type
        self.actual_type = actual_type

        super().__init__(
            message=f"Failed to build command function for '{command_name}'. Expected type '{expected_type}' but got '{actual_type}'.",
            data={
                "command_name": command_name,
                "expected_type": expected_type,
                "actual_type": actual_type,
            },
            cause=cause,
            previous=previous,
        )
