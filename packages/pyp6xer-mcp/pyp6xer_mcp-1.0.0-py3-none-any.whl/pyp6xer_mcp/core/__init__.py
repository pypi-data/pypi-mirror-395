"""Core utilities for PyP6Xer MCP Server.

This package contains:
- cache: XerCache class for managing loaded XER files
- formatters: Functions for formatting XER objects as dictionaries/markdown
- helpers: Utility functions for working with cached data
"""

from .cache import CachedXer, XerCache, xer_cache
from .formatters import (
    format_activity,
    format_project,
    format_resource,
    safe_getattr,
    to_markdown_table,
)
from .helpers import get_project, get_project_from_dict

__all__ = [
    # Cache
    "CachedXer",
    "XerCache",
    "xer_cache",
    # Formatters
    "safe_getattr",
    "format_activity",
    "format_resource",
    "format_project",
    "to_markdown_table",
    # Helpers
    "get_project",
    "get_project_from_dict",
]
