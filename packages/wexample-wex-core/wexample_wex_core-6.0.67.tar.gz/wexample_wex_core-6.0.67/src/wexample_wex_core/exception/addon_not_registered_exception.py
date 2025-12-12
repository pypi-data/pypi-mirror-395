from __future__ import annotations

from wexample_helpers.exception.not_allowed_item_exception import (
    NotAllowedItemException,
)


class AddonNotRegisteredException(NotAllowedItemException):
    """Exception raised when trying to access an addon that is not registered.

    This exception extends NotAllowedItemException to provide a standardized way
    of handling cases where an addon name is not in the list of registered addons.
    """

    error_code: str = "ADDON_NOT_REGISTERED"

    def __init__(
        self,
        addon_name: str,
        available_addons: list[str] | None = None,
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        # Call parent constructor with appropriate parameters
        super().__init__(
            item_type="addon",
            item_value=addon_name,
            allowed_values=available_addons or [],
            cause=cause,
            previous=previous,
        )
