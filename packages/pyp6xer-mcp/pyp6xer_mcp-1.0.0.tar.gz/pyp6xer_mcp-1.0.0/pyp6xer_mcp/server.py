"""PyP6Xer MCP Server - Main server instance.

This module creates and configures the FastMCP server instance.
All tools, prompts, and resources are registered via imports.
"""

import os

from mcp.server.fastmcp import FastMCP

# Server configuration
SERVER_NAME = "pyp6xer_mcp"
SERVER_VERSION = "1.0.0"

INSTRUCTIONS = """PyP6Xer MCP Server - Primavera P6 XER File Analysis

IMPORTANT: This server can load XER files from URLs (http:// or https://).
If the user provides or mentions a URL to an XER file, use that URL directly
with pyp6xer_load_file. This is the recommended approach for cloud workflows.

Example: pyp6xer_load_file(file_path="https://example.com/project.xer")

For file uploads (when the user uploads an XER file to ChatGPT/Claude.ai):
- Read the file content and base64-encode it
- Use file_content parameter: pyp6xer_load_file(file_content="<base64_encoded_data>")

Workflow:
1. Load an XER file using pyp6xer_load_file (supports local paths, URLs, OR base64 content)
2. Use analysis tools: critical_path, schedule_quality, float_analysis, etc.
3. Export results with pyp6xer_export_csv if needed

The server caches loaded files - use the cache_key from load for subsequent operations."""

# Initialize server
mcp = FastMCP(
    SERVER_NAME,
    instructions=INSTRUCTIONS,
    host="0.0.0.0",
    port=int(os.getenv("PORT", "5000")),
    stateless_http=True,
)

# API Key for authentication (set via environment variable)
API_KEY = os.getenv("API_KEY")


def get_mcp() -> FastMCP:
    """Get the MCP server instance.

    Returns:
        The FastMCP server instance.
    """
    return mcp


# Import tools to register them with the server
# Tools are registered via @mcp.tool decorators in their respective modules
from pyp6xer_mcp.tools import (  # noqa: F401
    file_ops,
    projects,
    activities,
    analysis,
    resources,
    progress,
    calendars,
)

# Import prompts to register them
from pyp6xer_mcp.prompts import analysis as prompts_analysis  # noqa: F401

# Import resources for direct data access
from pyp6xer_mcp.resources import schedule as resources_schedule  # noqa: F401
