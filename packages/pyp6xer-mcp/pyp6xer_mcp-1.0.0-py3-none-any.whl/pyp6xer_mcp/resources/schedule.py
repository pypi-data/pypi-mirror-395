"""MCP Resources for schedule data access.

Exposes schedule data as MCP Resources for direct access without tool calls.
"""

import json

from pyp6xer_mcp.server import mcp
from pyp6xer_mcp.core import xer_cache, safe_getattr


@mcp.resource("schedule://projects")
def list_loaded_projects() -> str:
    """Get all loaded projects across cached XER files."""
    result = []
    for key in xer_cache.keys():
        data = xer_cache.get_raw(key)
        for proj in data.get("projects", []):
            result.append(
                {
                    "cache_key": key,
                    "proj_id": safe_getattr(proj, "proj_id"),
                    "proj_short_name": safe_getattr(proj, "proj_short_name"),
                }
            )
    return json.dumps(result, indent=2)


@mcp.resource("schedule://{cache_key}/summary")
def get_schedule_summary(cache_key: str) -> str:
    """Get summary of a specific loaded schedule."""
    try:
        data = xer_cache.get_raw(cache_key)
        return json.dumps(
            {
                "projects": len(data.get("projects", [])),
                "activities": len(data.get("activities", [])),
                "resources": len(data.get("resources", [])),
                "calendars": len(data.get("calendars", [])),
            }
        )
    except ValueError as e:
        return json.dumps({"error": str(e)})


@mcp.resource("schedule://{cache_key}/critical")
def get_critical_activities(cache_key: str) -> str:
    """Get critical activities (float <= 0) for a schedule."""
    try:
        data = xer_cache.get_raw(cache_key)
        activities = data.get("activities", [])
        critical = [
            {
                "code": safe_getattr(a, "task_code", ""),
                "name": safe_getattr(a, "task_name", ""),
                "float_hrs": safe_getattr(a, "total_float_hr_cnt"),
            }
            for a in activities
            if safe_getattr(a, "total_float_hr_cnt") is not None
            and safe_getattr(a, "total_float_hr_cnt") <= 0
        ]
        return json.dumps(critical[:50])  # Limit to 50
    except ValueError as e:
        return json.dumps({"error": str(e)})
