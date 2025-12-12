from __future__ import annotations

from pathlib import Path

from wexample_app.const.path import APP_DIR_NAME_TMP

# filestate: python-constant-sort
CORE_DIR_NAME_KNOWLEDGE: Path = Path("knowledge")
CORE_DIR_NAME_TMP: Path = APP_DIR_NAME_TMP
CORE_FILE_NAME_REGISTRY: Path = Path("registry.yml")

# filestate: python-constant-sort
COMMAND_SEPARATOR_ADDON: str = "::"
COMMAND_SEPARATOR_FUNCTION_PARTS: str = "__"
COMMAND_SEPARATOR_GROUP: str = "/"

# Command types
# filestate: python-constant-sort
COMMAND_TYPE_ADDON: str = "addon"
COMMAND_TYPE_SERVICE: str = "service"

# Command patterns
# filestate: python-constant-sort
COMMAND_PATTERN_ADDON: str = r"^(?:([\w_-]+)::)?([\w_-]+)/([\w_-]+)$"
COMMAND_PATTERN_SERVICE: str = r"^@([\w_-]+)::([\w_-]+)/([\w_-]+)$"

COMMAND_PATTERNS: list[str] = [
    # filestate: python-iterable-sort
    COMMAND_PATTERN_ADDON,
    COMMAND_PATTERN_SERVICE,
]
