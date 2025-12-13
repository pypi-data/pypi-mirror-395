"""PyP6Xer MCP Server - Primavera P6 XER File Analysis.

A Model Context Protocol (MCP) server for parsing, analyzing, and manipulating
Primavera P6 XER (eXchange ERport) files.

This package provides:
- 22 MCP tools for schedule analysis, resource management, and progress tracking
- 5 prompts for common analysis workflows
- 3 resources for direct data access
- Pydantic models for input validation
- Core utilities for XER file caching and formatting

Usage:
    from pyp6xer_mcp import mcp
    mcp.run()
"""

__version__ = "1.0.0"

# Import from the modular server
from .server import mcp

# Import models for backward compatibility
from .models import ResponseFormat, ExportType, LoadXerInput

# Import core utilities for backward compatibility
from .core import xer_cache, safe_getattr, format_activity, to_markdown_table
from .core.helpers import get_project

# Backward compatibility aliases (old names with underscore prefix)
_xer_cache = xer_cache._cache  # Raw dict for legacy code
_safe_getattr = safe_getattr
_format_activity = format_activity
_to_markdown_table = to_markdown_table
_get_project = get_project


def _get_xer(cache_key: str):
    """Backward compatibility wrapper for getting XER data."""
    return xer_cache.get_raw(cache_key)


__all__ = [
    "__version__",
    "mcp",
    # Models
    "ResponseFormat",
    "ExportType",
    "LoadXerInput",
    # Core
    "xer_cache",
    "safe_getattr",
    "format_activity",
    "to_markdown_table",
    "get_project",
    # Backward compat aliases
    "_xer_cache",
    "_safe_getattr",
    "_format_activity",
    "_to_markdown_table",
    "_get_xer",
    "_get_project",
]
