"""HTTP layer for PyP6Xer MCP Server.

Provides:
- APIKeyAuthMiddleware - Authentication middleware
- health_check - Health check endpoint
- upload_file - XER file upload endpoint
"""

from . import middleware, routes

__all__ = ["middleware", "routes"]
