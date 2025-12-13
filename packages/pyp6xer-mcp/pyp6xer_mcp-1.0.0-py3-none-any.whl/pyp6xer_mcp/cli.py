"""CLI entry point for PyP6Xer MCP Server.

Usage:
    python -m pyp6xer_mcp.cli [stdio|sse|streamable-http]
    pyp6xer-mcp [stdio|sse|streamable-http]
"""

import sys


def main():
    """Main entry point for PyP6Xer MCP Server."""
    from pyp6xer_mcp.server import mcp, API_KEY

    # Default to stdio for backward compatibility
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"

    if transport not in ("stdio", "sse", "streamable-http"):
        print(f"Unknown transport: {transport}")
        print("Usage: pyp6xer-mcp [stdio|sse|streamable-http]")
        sys.exit(1)

    if transport == "streamable-http":
        _run_http_server(mcp, API_KEY)
    else:
        mcp.run(transport=transport)


def _run_http_server(mcp, api_key: str | None):
    """Run HTTP server with optional authentication."""
    import uvicorn
    from starlette.applications import Starlette
    from starlette.middleware import Middleware
    from starlette.middleware.cors import CORSMiddleware
    from starlette.routing import Mount, Route

    from pyp6xer_mcp.http.routes import health_check, upload_file
    from pyp6xer_mcp.http.middleware import APIKeyAuthMiddleware

    fastmcp_app = mcp.streamable_http_app()

    # Enable CORS for demo web UI
    middlewares = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]

    if api_key:
        middlewares.append(Middleware(APIKeyAuthMiddleware))
        print(f"Starting PyP6Xer MCP Server with API key authentication on port {mcp.settings.port}")
    else:
        print(f"Warning: Running without API key authentication (API_KEY not set)")
        print(f"Starting PyP6Xer MCP Server on port {mcp.settings.port}")

    app = Starlette(
        debug=False,
        routes=[
            Route("/health", health_check),
            Route("/upload", upload_file, methods=["POST"]),
            Mount("/", app=fastmcp_app),
        ],
        middleware=middlewares,
        lifespan=lambda app: mcp.session_manager.run(),
    )

    uvicorn.run(app, host="0.0.0.0", port=mcp.settings.port)


if __name__ == "__main__":
    main()
