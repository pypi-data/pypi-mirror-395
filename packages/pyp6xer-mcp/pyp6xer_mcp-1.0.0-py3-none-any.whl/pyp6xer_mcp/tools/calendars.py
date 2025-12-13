"""Calendar management tools for PyP6Xer MCP Server."""

import json

from pyp6xer_mcp.server import mcp
from pyp6xer_mcp.models import CalendarInput, ResponseFormat
from pyp6xer_mcp.core import (
    xer_cache,
    safe_getattr,
    to_markdown_table,
)


@mcp.tool(
    name="pyp6xer_list_calendars",
    annotations={
        "title": "List Calendars",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def pyp6xer_list_calendars(params: CalendarInput) -> str:
    """List calendars in the XER file.

    Args:
        params: CalendarInput with cache_key and optional calendar_id for details.

    Returns:
        str: List of calendars or details of a specific calendar.
    """
    try:
        xer_data = xer_cache.get_raw(params.cache_key)
        calendars = xer_data.get("calendars", [])

        if not calendars:
            return "No calendars found in the XER file."

        calendar_data = []
        for c in calendars:
            cal_info = {
                "clndr_id": safe_getattr(c, "clndr_id"),
                "clndr_name": safe_getattr(c, "clndr_name"),
                "clndr_type": safe_getattr(c, "clndr_type"),
                "default_flag": safe_getattr(c, "default_flag"),
                "day_hr_cnt": safe_getattr(c, "day_hr_cnt"),
                "week_hr_cnt": safe_getattr(c, "week_hr_cnt"),
                "month_hr_cnt": safe_getattr(c, "month_hr_cnt"),
                "year_hr_cnt": safe_getattr(c, "year_hr_cnt"),
            }
            calendar_data.append(cal_info)

        # If specific calendar requested
        if params.calendar_id:
            cal = next(
                (c for c in calendar_data if str(c["clndr_id"]) == params.calendar_id), None
            )
            if not cal:
                return f"Calendar with ID '{params.calendar_id}' not found."

            if params.response_format == ResponseFormat.JSON:
                return json.dumps(cal, indent=2, default=str)

            lines = [
                f"## Calendar: {cal['clndr_name']}",
                f"- **ID**: {cal['clndr_id']}",
                f"- **Type**: {cal['clndr_type']}",
                f"- **Default**: {cal['default_flag']}",
                f"- **Hours/Day**: {cal['day_hr_cnt']}",
                f"- **Hours/Week**: {cal['week_hr_cnt']}",
                f"- **Hours/Month**: {cal['month_hr_cnt']}",
                f"- **Hours/Year**: {cal['year_hr_cnt']}",
            ]
            return "\n".join(lines)

        if params.response_format == ResponseFormat.JSON:
            return json.dumps({"calendars": calendar_data}, indent=2, default=str)

        # Markdown format
        lines = [f"## Calendars ({len(calendars)} total)\n"]

        # Group by type
        by_type = {}
        for c in calendar_data:
            ctype = c["clndr_type"] or "Unknown"
            if ctype not in by_type:
                by_type[ctype] = []
            by_type[ctype].append(c)

        for ctype, clist in by_type.items():
            lines.append(f"### {ctype} ({len(clist)})")
            headers = ["ID", "Name", "Hrs/Day", "Hrs/Week"]
            rows = [
                [c["clndr_id"], (c["clndr_name"] or "")[:30], c["day_hr_cnt"], c["week_hr_cnt"]]
                for c in clist
            ]
            lines.append(to_markdown_table(headers, rows))
            lines.append("")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"
