"""HTTP authentication middleware for PyP6Xer MCP Server."""

import os

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

API_KEY = os.getenv("API_KEY")


class APIKeyAuthMiddleware(BaseHTTPMiddleware):
    """Middleware to validate API key in Authorization header or query parameter."""

    EXEMPT_PATHS = {"/health"}

    async def dispatch(self, request, call_next):
        # Skip auth for exempt paths
        if request.url.path in self.EXEMPT_PATHS:
            return await call_next(request)

        token = self._extract_token(request)

        if not token:
            return JSONResponse(
                {
                    "error": "Missing API key. Use header 'Authorization: Bearer <key>' "
                    "or query param '?api_key=<key>'"
                },
                status_code=401,
            )

        if token != API_KEY:
            return JSONResponse({"error": "Invalid API key"}, status_code=401)

        return await call_next(request)

    def _extract_token(self, request) -> str | None:
        """Extract token from Authorization header or query parameter."""
        # Option 1: Check Authorization header (Bearer token)
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header[7:]

        # Option 2: Check query parameter (for Claude.ai connectors)
        return request.query_params.get("api_key")
