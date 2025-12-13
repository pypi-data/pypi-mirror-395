"""Context helpers for PyP6Xer MCP Server.

NOTE: MCP's FastMCP doesn't currently support @mcp.context() decorators.
This module provides helper functions for getting XER file context.
"""

from .xer_context import get_xer_files_context

__all__ = ["get_xer_files_context"]
