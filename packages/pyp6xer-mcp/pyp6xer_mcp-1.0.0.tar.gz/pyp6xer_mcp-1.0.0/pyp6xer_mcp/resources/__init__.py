"""MCP Resources for PyP6Xer MCP Server.

Resources provide direct access to schedule data:
- schedule://projects - List loaded projects
- schedule://{cache_key}/summary - Schedule summary
- schedule://{cache_key}/critical - Critical activities
"""

from . import schedule

__all__ = ["schedule"]
