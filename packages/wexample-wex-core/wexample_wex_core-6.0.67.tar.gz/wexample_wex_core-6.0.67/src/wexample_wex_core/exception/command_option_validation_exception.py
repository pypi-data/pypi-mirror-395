from __future__ import annotations

from typing import Any

from wexample_wex_core.exception.abstract_command_option_exception import (
    AbstractCommandOptionException,
)


class CommandOptionValidationException(AbstractCommandOptionException):
    def __init__(self, option_name: str, value: Any, error_message: str) -> None:
        super().__init__(
            message=f'Option "{option_name}" validation failed: {error_message}',
            option_name=option_name,
        )
        self.value = value
        self.error_message = error_message
