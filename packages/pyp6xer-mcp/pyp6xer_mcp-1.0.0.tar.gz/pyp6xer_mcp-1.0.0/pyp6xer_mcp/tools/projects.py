"""Project management tools for PyP6Xer MCP Server.

This module contains tools for:
- Listing projects in loaded XER files
"""

import json

from pyp6xer_mcp.core import format_project, xer_cache
from pyp6xer_mcp.models import ResponseFormat, XerCacheKeyInput
from pyp6xer_mcp.server import mcp


@mcp.tool(
    name="pyp6xer_list_projects",
    annotations={
        "title": "List Projects",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def pyp6xer_list_projects(params: XerCacheKeyInput) -> str:
    """List all projects in the loaded XER file.

    Args:
        params: XerCacheKeyInput with cache_key and response_format.

    Returns:
        str: List of projects with their basic information.
    """
    try:
        xer_data = xer_cache.get_raw(params.cache_key)
        projects = xer_data.get("projects", [])

        if not projects:
            return "No projects found in the XER file."

        project_data = [format_project(p) for p in projects]

        if params.response_format == ResponseFormat.JSON:
            return json.dumps({"projects": project_data}, indent=2, default=str)

        # Markdown format
        lines = [f"## Projects ({len(projects)} total)\n"]
        for p in project_data:
            lines.append(f"### {p['proj_short_name']}")
            lines.append(f"- **ID**: {p['proj_id']}")
            lines.append(f"- **Activities**: {p['activity_count']}")
            lines.append(f"- **WBS Elements**: {p['wbs_count']}")
            if p["plan_start_date"]:
                lines.append(f"- **Plan Start**: {p['plan_start_date']}")
            if p["plan_end_date"]:
                lines.append(f"- **Plan End**: {p['plan_end_date']}")
            lines.append("")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"
