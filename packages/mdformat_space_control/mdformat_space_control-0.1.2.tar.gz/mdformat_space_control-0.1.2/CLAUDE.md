# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

mdformat-space-control is an mdformat plugin that provides unified control over Markdown spacing:
- **EditorConfig support**: Configure list indentation via `.editorconfig` files
- **Tight list formatting**: Automatically removes unnecessary blank lines between list items
- **Frontmatter spacing**: Normalizes spacing after YAML frontmatter (works with mdformat-frontmatter)

This plugin merges functionality from mdformat-editorconfig and mdformat-tight-lists into a single plugin, solving the issue where mdformat only applies one set of list renderers when multiple plugins are installed.

## Build and Test Commands

```bash
uv sync --extra test     # Install dependencies including test deps
uv run pytest            # Run all tests
uv run pytest -v         # Run tests verbosely
uv run pytest --cov=mdformat_space_control  # Run with coverage
uv run pytest tests/test_editorconfig.py    # Run specific test file
```

## Architecture

```
mdformat_space_control/
├── __init__.py    # Public API exports, version
├── config.py      # EditorConfig lookup, file context tracking
└── plugin.py      # List renderers (RENDERERS dict)
```

**Key components:**

- **`config.py`**: Uses `contextvars` for thread-safe file path tracking. Falls back to `Path.cwd() / "_.md"` for CLI usage when no explicit file context is set.
- **`plugin.py`**: Provides renderers and postprocessors:
  - `_render_list_item`: Per-item tight/loose formatting based on paragraph count
  - `_render_bullet_list`: Configurable indent + content-based tight/loose
  - `_render_ordered_list`: Configurable indent + content-based tight/loose
  - `_postprocess_root`: Normalizes frontmatter spacing (works with mdformat-frontmatter)

## Plugin Extension Points

mdformat plugins expose:
1. **`RENDERERS`**: Dict mapping node types to render functions
2. **`POSTPROCESSORS`**: Dict mapping node types to postprocess functions
3. **`update_mdit(mdit)`**: Hook to modify the markdown-it parser (no-op here)

Entry point in `pyproject.toml`:
```toml
[project.entry-points."mdformat.parser_extension"]
space_control = "mdformat_space_control"
```

## Test Structure

- **`tests/fixtures.md`**: Markdown-it fixture format for tight-list tests
- **`tests/test_fixtures.py`**: Parametrized fixture tests
- **`tests/test_editorconfig.py`**: EditorConfig-specific tests using temp directories
- **`tests/test_frontmatter.py`**: Frontmatter spacing tests (requires mdformat-frontmatter)

## Key Dependencies

- **mdformat** (>=0.7.0): The Markdown formatter being extended
- **editorconfig** (>=0.12.0): EditorConfig file parsing

## Release Process

1. Update version in `__init__.py`
2. Commit changes
3. Tag with `git tag vX.Y.Z`
4. Push tag to trigger PyPI publish: `git push origin vX.Y.Z`
