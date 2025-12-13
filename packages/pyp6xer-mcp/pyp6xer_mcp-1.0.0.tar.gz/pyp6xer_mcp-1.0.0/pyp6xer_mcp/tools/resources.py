"""Resource management tools for PyP6Xer MCP Server."""

import json

from pyp6xer_mcp.server import mcp
from pyp6xer_mcp.models import ResourceUtilizationInput, XerCacheKeyInput, ResponseFormat
from pyp6xer_mcp.core import (
    xer_cache,
    format_resource,
    safe_getattr,
    to_markdown_table,
)


@mcp.tool(
    name="pyp6xer_list_resources",
    annotations={
        "title": "List Resources",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def pyp6xer_list_resources(params: XerCacheKeyInput) -> str:
    """List all resources in the XER file.

    Args:
        params: XerCacheKeyInput with cache_key and response_format.

    Returns:
        str: List of resources with their types and basic information.
    """
    try:
        xer_data = xer_cache.get_raw(params.cache_key)
        resources = xer_data.get("resources", [])

        if not resources:
            return "No resources found in the XER file."

        resource_data = [format_resource(r) for r in resources]

        if params.response_format == ResponseFormat.JSON:
            return json.dumps({"resources": resource_data}, indent=2, default=str)

        # Markdown format
        lines = [f"## Resources ({len(resources)} total)\n"]

        # Group by type
        by_type = {}
        for r in resource_data:
            rtype = r["rsrc_type"] or "Unknown"
            if rtype not in by_type:
                by_type[rtype] = []
            by_type[rtype].append(r)

        for rtype, rlist in by_type.items():
            lines.append(f"### {rtype} ({len(rlist)})")
            headers = ["ID", "Short Name", "Name"]
            rows = [
                [r["rsrc_id"], r["rsrc_short_name"], (r["rsrc_name"] or "")[:40]]
                for r in rlist
            ]
            lines.append(to_markdown_table(headers, rows))
            lines.append("")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


@mcp.tool(
    name="pyp6xer_resource_utilization",
    annotations={
        "title": "Resource Utilization Analysis",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def pyp6xer_resource_utilization(params: ResourceUtilizationInput) -> str:
    """Analyze resource utilization and find potential overallocations.

    Args:
        params: ResourceUtilizationInput with cache_key and optional resource_type filter.

    Returns:
        str: Resource utilization summary including hours allocated and potential issues.
    """
    try:
        xer_data = xer_cache.get_raw(params.cache_key)
        resources = xer_data.get("resources", [])
        activityresources = xer_data.get("activityresources", [])

        if not resources:
            return "No resources found in the XER file."

        # Filter by type if specified
        if params.resource_type:
            resources = [r for r in resources if safe_getattr(r, "rsrc_type") == params.resource_type]

        utilization_data = []
        for resource in resources:
            rsrc_id = safe_getattr(resource, "rsrc_id")
            assignments = [a for a in activityresources if safe_getattr(a, "rsrc_id") == rsrc_id]

            total_target_qty = sum(safe_getattr(a, "target_qty") or 0 for a in assignments)
            total_target_cost = sum(safe_getattr(a, "target_cost") or 0 for a in assignments)
            total_actual_qty = sum(safe_getattr(a, "act_reg_qty") or 0 for a in assignments)
            total_remaining = sum(safe_getattr(a, "remain_qty") or 0 for a in assignments)

            utilization_data.append(
                {
                    "rsrc_id": rsrc_id,
                    "rsrc_name": safe_getattr(resource, "rsrc_name"),
                    "rsrc_short_name": safe_getattr(resource, "rsrc_short_name"),
                    "rsrc_type": safe_getattr(resource, "rsrc_type"),
                    "assignment_count": len(assignments),
                    "total_target_qty": total_target_qty,
                    "total_target_cost": total_target_cost,
                    "total_actual_qty": total_actual_qty,
                    "total_remaining_qty": total_remaining,
                    "potentially_overallocated": total_target_qty
                    > 2080,  # More than 40h/week for a year
                }
            )

        # Sort by total quantity (most utilized first)
        utilization_data.sort(key=lambda x: x["total_target_qty"], reverse=True)

        if params.response_format == ResponseFormat.JSON:
            return json.dumps({"resource_utilization": utilization_data}, indent=2, default=str)

        # Markdown format
        overallocated = [u for u in utilization_data if u["potentially_overallocated"]]

        lines = [
            f"## Resource Utilization Analysis",
            f"- **Total Resources**: {len(utilization_data)}",
            f"- **Potentially Overallocated**: {len(overallocated)}\n",
        ]

        if overallocated:
            lines.append("### ⚠️ Potentially Overallocated Resources")
            headers = ["Name", "Type", "Assignments", "Target Qty", "Actual Qty"]
            rows = [
                [
                    (u["rsrc_name"] or u["rsrc_short_name"] or "")[:30],
                    u["rsrc_type"],
                    u["assignment_count"],
                    f"{u['total_target_qty']:.0f}",
                    f"{u['total_actual_qty']:.0f}",
                ]
                for u in overallocated
            ]
            lines.append(to_markdown_table(headers, rows))
            lines.append("")

        lines.append("### All Resources")
        headers = ["Name", "Type", "Assignments", "Target Qty", "Remaining"]
        rows = [
            [
                (u["rsrc_name"] or u["rsrc_short_name"] or "")[:30],
                u["rsrc_type"],
                u["assignment_count"],
                f"{u['total_target_qty']:.0f}",
                f"{u['total_remaining_qty']:.0f}",
            ]
            for u in utilization_data[:20]
        ]
        lines.append(to_markdown_table(headers, rows))

        if len(utilization_data) > 20:
            lines.append(f"\n*Showing top 20 of {len(utilization_data)} resources.*")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"
