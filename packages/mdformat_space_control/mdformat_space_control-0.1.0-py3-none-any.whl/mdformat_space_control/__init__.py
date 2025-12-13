"""An mdformat plugin for EditorConfig-based indentation and tight list formatting."""

__version__ = "0.1.0"

from .config import (
    get_current_file,
    get_indent_config,
    set_current_file,
)
from .plugin import RENDERERS, update_mdit

__all__ = [
    "RENDERERS",
    "update_mdit",
    "set_current_file",
    "get_current_file",
    "get_indent_config",
]
