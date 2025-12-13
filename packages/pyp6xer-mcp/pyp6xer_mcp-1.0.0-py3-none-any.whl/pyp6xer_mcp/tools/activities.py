"""Activity management tools for PyP6Xer MCP Server.

This module provides tools for listing, searching, viewing, and updating activities.
"""

import json
from typing import Any

from pyp6xer_mcp.server import mcp
from pyp6xer_mcp.models import (
    ActivityDetailInput,
    ListActivitiesInput,
    ResponseFormat,
    SearchActivitiesInput,
    UpdateActivityInput,
)
from pyp6xer_mcp.core import (
    xer_cache,
    format_activity,
    safe_getattr,
    to_markdown_table,
    get_project_from_dict,
)


def _get_xer(cache_key: str) -> dict[str, Any]:
    """Get cached XER data as dictionary (backward compatible)."""
    return xer_cache.get_raw(cache_key)


def _get_project(xer_data: dict[str, Any], project_id: str | None = None) -> Any:
    """Get a project from the cached XER data, optionally by ID or name."""
    return get_project_from_dict(xer_data, project_id)


@mcp.tool(
    name="pyp6xer_list_activities",
    annotations={
        "title": "List Activities",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def pyp6xer_list_activities(params: ListActivitiesInput) -> str:
    """List activities/tasks with optional filtering.

    Args:
        params: ListActivitiesInput with filters for project, status, WBS, pagination.

    Returns:
        str: List of activities matching the criteria.
    """
    try:
        xer_data = _get_xer(params.cache_key)

        # Get activities
        if params.project_id:
            project = _get_project(xer_data, params.project_id)
            activities = list(project.activities)
        else:
            activities = xer_data.get("activities", [])

        # Apply filters
        if params.status_filter and params.status_filter != 'all':
            activities = [a for a in activities if safe_getattr(a, 'status_code') == params.status_filter]

        if params.wbs_id:
            activities = [a for a in activities if str(safe_getattr(a, 'wbs_id')) == params.wbs_id]

        total_count = len(activities)

        # Apply pagination
        activities = activities[params.offset:params.offset + params.limit]

        activity_data = [format_activity(a) for a in activities]

        if params.response_format == ResponseFormat.JSON:
            return json.dumps({
                "total": total_count,
                "offset": params.offset,
                "limit": params.limit,
                "count": len(activity_data),
                "has_more": total_count > params.offset + len(activity_data),
                "activities": activity_data
            }, indent=2, default=str)

        # Markdown format
        lines = [f"## Activities ({len(activity_data)} of {total_count})\n"]

        headers = ["Code", "Name", "Duration", "Status", "Float (hrs)", "% Complete"]
        rows = []
        for a in activity_data:
            rows.append([
                a["task_code"],
                (a["task_name"] or "")[:40],
                a["duration"] or "-",
                (a["status_code"] or "")[-10:],
                a["total_float_hr_cnt"] or "-",
                f"{a['phys_complete_pct']}%" if a['phys_complete_pct'] is not None else "-"
            ])

        lines.append(to_markdown_table(headers, rows))

        if total_count > params.offset + len(activity_data):
            lines.append(f"\n*Showing {params.offset + 1}-{params.offset + len(activity_data)} of {total_count}. Use offset parameter to see more.*")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


@mcp.tool(
    name="pyp6xer_get_activity",
    annotations={
        "title": "Get Activity Details",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def pyp6xer_get_activity(params: ActivityDetailInput) -> str:
    """Get detailed information about a specific activity.

    Args:
        params: ActivityDetailInput with cache_key and activity_code.

    Returns:
        str: Detailed activity information including dates, float, predecessors, successors.
    """
    try:
        xer_data = _get_xer(params.cache_key)
        activities = xer_data.get("activities", [])

        # Find the activity
        activity = None
        for a in activities:
            if safe_getattr(a, 'task_code') == params.activity_code:
                activity = a
                break

        if not activity:
            return f"Error: Activity with code '{params.activity_code}' not found."

        data = format_activity(activity, detailed=True)

        # Get predecessors and successors
        predecessors = []
        if hasattr(activity, 'predecessors'):
            for pred in activity.predecessors:
                predecessors.append({
                    "pred_task_code": safe_getattr(pred, 'pred_task_code', safe_getattr(pred, 'task_id')),
                    "pred_type": safe_getattr(pred, 'pred_type'),
                    "lag_hr_cnt": safe_getattr(pred, 'lag_hr_cnt')
                })

        successors = []
        if hasattr(activity, 'successors'):
            for succ in activity.successors:
                successors.append({
                    "succ_task_code": safe_getattr(succ, 'task_code', safe_getattr(succ, 'task_id')),
                    "pred_type": safe_getattr(succ, 'pred_type'),
                    "lag_hr_cnt": safe_getattr(succ, 'lag_hr_cnt')
                })

        data["predecessors"] = predecessors
        data["successors"] = successors

        # Get resource assignments
        resources = []
        if hasattr(activity, 'resources'):
            for res in activity.resources:
                resources.append({
                    "rsrc_id": safe_getattr(res, 'rsrc_id'),
                    "target_qty": safe_getattr(res, 'target_qty'),
                    "target_cost": safe_getattr(res, 'target_cost'),
                    "act_reg_qty": safe_getattr(res, 'act_reg_qty'),
                    "remain_qty": safe_getattr(res, 'remain_qty')
                })
        data["resource_assignments"] = resources

        if params.response_format == ResponseFormat.JSON:
            return json.dumps(data, indent=2, default=str)

        # Markdown format
        lines = [f"## Activity: {data['task_code']}\n"]
        lines.append(f"**{data['task_name']}**\n")

        lines.append("### Basic Information")
        lines.append(f"- **Status**: {data['status_code']}")
        lines.append(f"- **Type**: {data['task_type']}")
        lines.append(f"- **Duration**: {data['duration']} days")
        lines.append(f"- **% Complete**: {data['phys_complete_pct']}%")

        lines.append("\n### Float")
        lines.append(f"- **Total Float**: {data['total_float_hr_cnt']} hours")
        lines.append(f"- **Free Float**: {data['free_float_hr_cnt']} hours")

        lines.append("\n### Dates")
        lines.append(f"- **Target Start**: {data['target_start_date']}")
        lines.append(f"- **Target End**: {data['target_end_date']}")
        lines.append(f"- **Early Start**: {data['early_start_date']}")
        lines.append(f"- **Early End**: {data['early_end_date']}")
        lines.append(f"- **Late Start**: {data['late_start_date']}")
        lines.append(f"- **Late End**: {data['late_end_date']}")
        if data['act_start_date']:
            lines.append(f"- **Actual Start**: {data['act_start_date']}")
        if data['act_end_date']:
            lines.append(f"- **Actual End**: {data['act_end_date']}")

        if predecessors:
            lines.append(f"\n### Predecessors ({len(predecessors)})")
            for p in predecessors:
                lines.append(f"- {p['pred_task_code']} ({p['pred_type']}, lag: {p['lag_hr_cnt']}h)")

        if successors:
            lines.append(f"\n### Successors ({len(successors)})")
            for s in successors:
                lines.append(f"- {s['succ_task_code']} ({s['pred_type']}, lag: {s['lag_hr_cnt']}h)")

        if resources:
            lines.append(f"\n### Resource Assignments ({len(resources)})")
            for r in resources:
                lines.append(f"- Resource {r['rsrc_id']}: target={r['target_qty']}, actual={r['act_reg_qty']}, remaining={r['remain_qty']}")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


@mcp.tool(
    name="pyp6xer_search_activities",
    annotations={
        "title": "Search Activities",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def pyp6xer_search_activities(params: SearchActivitiesInput) -> str:
    """Search for activities by code or name.

    Args:
        params: SearchActivitiesInput with search_term and optional filters.

    Returns:
        str: Activities matching the search criteria.
    """
    try:
        xer_data = _get_xer(params.cache_key)

        if params.project_id:
            project = _get_project(xer_data, params.project_id)
            activities = list(project.activities)
        else:
            activities = xer_data.get("activities", [])

        search_lower = params.search_term.lower()
        matches = []

        for a in activities:
            task_code = safe_getattr(a, 'task_code') or ""
            task_name = safe_getattr(a, 'task_name') or ""

            if search_lower in task_code.lower() or search_lower in task_name.lower():
                matches.append(a)

        matches = matches[:params.limit]
        activity_data = [format_activity(a) for a in matches]

        if params.response_format == ResponseFormat.JSON:
            return json.dumps({
                "search_term": params.search_term,
                "matches": len(activity_data),
                "activities": activity_data
            }, indent=2, default=str)

        # Markdown format
        lines = [
            f"## Search Results for '{params.search_term}'",
            f"Found **{len(activity_data)}** matching activities\n"
        ]

        if activity_data:
            headers = ["Code", "Name", "Duration", "Status", "% Complete"]
            rows = [[
                a["task_code"],
                (a["task_name"] or "")[:40],
                a["duration"] or "-",
                (a["status_code"] or "")[-10:],
                f"{a['phys_complete_pct']}%" if a['phys_complete_pct'] is not None else "-"
            ] for a in activity_data]
            lines.append(to_markdown_table(headers, rows))
        else:
            lines.append("*No activities found matching the search criteria.*")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


@mcp.tool(
    name="pyp6xer_update_activity",
    annotations={
        "title": "Update Activity",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def pyp6xer_update_activity(params: UpdateActivityInput) -> str:
    """Update an activity's properties (e.g., physical completion, status).

    Args:
        params: UpdateActivityInput with activity_code and properties to update.

    Returns:
        str: Confirmation of the update.
    """
    try:
        xer_data = _get_xer(params.cache_key)
        activities = xer_data.get("activities", [])

        # Find the activity
        activity = None
        for a in activities:
            if safe_getattr(a, 'task_code') == params.activity_code:
                activity = a
                break

        if not activity:
            return f"Error: Activity with code '{params.activity_code}' not found."

        updates = []

        if params.phys_complete_pct is not None:
            old_val = safe_getattr(activity, 'phys_complete_pct')
            activity.phys_complete_pct = params.phys_complete_pct
            updates.append(f"phys_complete_pct: {old_val} → {params.phys_complete_pct}")

        if params.status_code is not None:
            if params.status_code not in ["TK_Complete", "TK_Active", "TK_NotStarted"]:
                return f"Error: Invalid status_code. Must be one of: TK_Complete, TK_Active, TK_NotStarted"
            old_val = safe_getattr(activity, 'status_code')
            activity.status_code = params.status_code
            updates.append(f"status_code: {old_val} → {params.status_code}")

        if not updates:
            return "No updates specified. Provide phys_complete_pct or status_code to update."

        return f"Successfully updated activity '{params.activity_code}':\n" + "\n".join(f"- {u}" for u in updates)

    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"
