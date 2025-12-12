from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class

from wexample_wex_core.middleware.abstract_each_path_middleware import (
    AbstractEachPathMiddleware,
)


@base_class
class EachPathMiddleware(AbstractEachPathMiddleware):
    """Middleware that iterates over each path (file or directory).

    Uses the default path option from AbstractEachPathMiddleware.
    """
