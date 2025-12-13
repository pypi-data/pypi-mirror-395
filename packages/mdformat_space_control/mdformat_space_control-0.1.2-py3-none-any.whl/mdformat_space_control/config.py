"""EditorConfig integration for mdformat-space-control.

This module provides functions to track the current file being formatted
and retrieve indentation settings from .editorconfig files.
"""

from contextvars import ContextVar
from pathlib import Path

import editorconfig

# Thread-safe context variable to track the current file being formatted
_current_file: ContextVar[Path | None] = ContextVar("current_file", default=None)


def set_current_file(filepath: Path | str | None) -> None:
    """Set the current file being formatted (for editorconfig lookup).

    Args:
        filepath: Path to the file being formatted, or None to clear.
    """
    if filepath is None:
        _current_file.set(None)
    else:
        _current_file.set(Path(filepath).resolve())


def get_current_file() -> Path | None:
    """Get the current file being formatted.

    Returns:
        Path to the current file, or None if not set.
    """
    return _current_file.get()


def get_indent_config() -> tuple[str, int] | None:
    """Get indent configuration from .editorconfig for the current file.

    Looks up .editorconfig settings for the current file. If no file path
    is explicitly set (via set_current_file), falls back to using the
    current working directory for editorconfig lookup. This enables CLI
    usage when running mdformat from a project directory.

    If CWD-based lookup finds no settings and no explicit file was set,
    falls back to ~/.editorconfig as a final attempt. This handles cases
    where mdformat is called from applications (like Obsidian plugins)
    whose working directory is outside the user's HOME tree.

    Returns:
        Tuple of (indent_style, indent_size) where:
        - indent_style: "space" or "tab"
        - indent_size: number of columns per indent level
        Returns None if no indent config found.
    """
    filepath = _current_file.get()
    explicit_file_set = filepath is not None

    # Fallback to cwd for CLI usage - use a synthetic .md file path
    # to ensure markdown-specific editorconfig sections are matched
    if filepath is None:
        filepath = Path.cwd() / "_.md"

    try:
        props = editorconfig.get_properties(str(filepath))
    except editorconfig.EditorConfigError:
        props = {}

    indent_style = props.get("indent_style")
    indent_size = props.get("indent_size")

    # Fallback to ~/.editorconfig if no indent config found and no explicit file set
    # This handles CLI usage from apps whose CWD is outside the user's HOME tree
    if not indent_style and not indent_size and not explicit_file_set:
        home_editorconfig = Path.home() / ".editorconfig"
        if home_editorconfig.exists():
            try:
                # Use a synthetic .md file in HOME for the lookup
                home_props = editorconfig.get_properties(str(Path.home() / "_.md"))
                indent_style = home_props.get("indent_style")
                indent_size = home_props.get("indent_size")
            except editorconfig.EditorConfigError:
                pass

    # If still neither property is set, return None (passthrough)
    if not indent_style and not indent_size:
        return None

    # Default to "space" if only indent_size is set
    style = indent_style or "space"

    # Parse indent_size, default to 2 if not specified or invalid
    if indent_size and indent_size.isdigit():
        size = int(indent_size)
    elif indent_size == "tab":
        # Special case: indent_size = tab means use tab_width
        tab_width = props.get("tab_width")
        size = int(tab_width) if tab_width and tab_width.isdigit() else 4
    else:
        size = 2

    return (style, size)


def get_indent_str() -> str | None:
    """Get the indentation string based on .editorconfig settings.

    Returns:
        The string to use for one level of indentation:
        - Tab character if indent_style is "tab"
        - N spaces if indent_style is "space" (where N is indent_size)
        Returns None if no indent config found (use default).
    """
    config = get_indent_config()
    if config is None:
        return None

    style, size = config
    if style == "tab":
        return "\t"
    else:
        return " " * size
