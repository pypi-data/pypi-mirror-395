"""Formatting utilities for PyP6Xer MCP Server.

This module provides functions for formatting XER objects (activities,
resources, projects) as dictionaries and converting data to markdown tables.
"""

from typing import Any, Dict, List


def safe_getattr(obj: Any, attr: str, default: Any = None) -> Any:
    """Safely get an attribute from an object.

    Args:
        obj: Object to get the attribute from.
        attr: Attribute name.
        default: Default value if attribute doesn't exist or errors.

    Returns:
        The attribute value or default.
    """
    try:
        return getattr(obj, attr, default)
    except Exception:
        return default


def format_activity(activity: Any, detailed: bool = False) -> Dict[str, Any]:
    """Format an activity as a dictionary.

    Args:
        activity: Activity object from xerparser.
        detailed: If True, include all available fields.

    Returns:
        Dictionary with activity data.
    """
    result = {
        "task_code": safe_getattr(activity, "task_code", "N/A"),
        "task_name": safe_getattr(activity, "task_name", "N/A"),
        "duration": safe_getattr(activity, "duration"),
        "status_code": safe_getattr(activity, "status_code"),
        "task_type": safe_getattr(activity, "task_type"),
        "phys_complete_pct": safe_getattr(activity, "phys_complete_pct"),
        "total_float_hr_cnt": safe_getattr(activity, "total_float_hr_cnt"),
    }

    if detailed:
        result.update(
            {
                "task_id": safe_getattr(activity, "task_id"),
                "wbs_id": safe_getattr(activity, "wbs_id"),
                "clndr_id": safe_getattr(activity, "clndr_id"),
                "target_start_date": str(safe_getattr(activity, "target_start_date", "")),
                "target_end_date": str(safe_getattr(activity, "target_end_date", "")),
                "act_start_date": str(safe_getattr(activity, "act_start_date", "")),
                "act_end_date": str(safe_getattr(activity, "act_end_date", "")),
                "early_start_date": str(safe_getattr(activity, "early_start_date", "")),
                "early_end_date": str(safe_getattr(activity, "early_end_date", "")),
                "late_start_date": str(safe_getattr(activity, "late_start_date", "")),
                "late_end_date": str(safe_getattr(activity, "late_end_date", "")),
                "free_float_hr_cnt": safe_getattr(activity, "free_float_hr_cnt"),
                "remain_drtn_hr_cnt": safe_getattr(activity, "remain_drtn_hr_cnt"),
                "target_drtn_hr_cnt": safe_getattr(activity, "target_drtn_hr_cnt"),
                "act_work_qty": safe_getattr(activity, "act_work_qty"),
                "remain_work_qty": safe_getattr(activity, "remain_work_qty"),
                "target_work_qty": safe_getattr(activity, "target_work_qty"),
            }
        )

    return result


def format_resource(resource: Any) -> Dict[str, Any]:
    """Format a resource as a dictionary.

    Args:
        resource: Resource object from xerparser.

    Returns:
        Dictionary with resource data.
    """
    return {
        "rsrc_id": safe_getattr(resource, "rsrc_id"),
        "rsrc_short_name": safe_getattr(resource, "rsrc_short_name"),
        "rsrc_name": safe_getattr(resource, "rsrc_name"),
        "rsrc_type": safe_getattr(resource, "rsrc_type"),
        "email_addr": safe_getattr(resource, "email_addr"),
        "parent_rsrc_id": safe_getattr(resource, "parent_rsrc_id"),
    }


def format_project(project: Any) -> Dict[str, Any]:
    """Format a project as a dictionary.

    Args:
        project: Project object from xerparser.

    Returns:
        Dictionary with project data.
    """
    return {
        "proj_id": safe_getattr(project, "proj_id"),
        "proj_short_name": safe_getattr(project, "proj_short_name"),
        "proj_name": safe_getattr(
            project, "proj_name", safe_getattr(project, "proj_short_name")
        ),
        "plan_start_date": str(safe_getattr(project, "plan_start_date", "")),
        "plan_end_date": str(safe_getattr(project, "plan_end_date", "")),
        "scd_end_date": str(safe_getattr(project, "scd_end_date", "")),
        "activity_count": len(list(safe_getattr(project, "activities", []))),
        "wbs_count": len(list(safe_getattr(project, "wbss", []))),
    }


def to_markdown_table(headers: List[str], rows: List[List[Any]]) -> str:
    """Convert data to a markdown table.

    Args:
        headers: List of column header strings.
        rows: List of rows, where each row is a list of cell values.

    Returns:
        Formatted markdown table string.
    """
    if not rows:
        return "No data available."

    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(str(cell)))

    # Build table
    header_line = "| " + " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers)) + " |"
    separator = "|" + "|".join("-" * (w + 2) for w in widths) + "|"

    data_lines = []
    for row in rows:
        cells = [
            str(cell).ljust(widths[i]) if i < len(widths) else str(cell)
            for i, cell in enumerate(row)
        ]
        data_lines.append("| " + " | ".join(cells) + " |")

    return "\n".join([header_line, separator] + data_lines)
