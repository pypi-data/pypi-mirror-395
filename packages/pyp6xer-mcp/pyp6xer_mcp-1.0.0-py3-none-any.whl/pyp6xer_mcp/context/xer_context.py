"""Context helpers for PyP6Xer MCP Server.

NOTE: MCP's FastMCP doesn't currently support @mcp.context() decorators.
This module provides helper functions that can be used by prompts or resources
to get information about loaded XER files.

Future versions of FastMCP may add context support.
"""

from pyp6xer_mcp.core import xer_cache, safe_getattr


def get_xer_files_context() -> str:
    """Get information about loaded XER files.

    Returns a markdown summary of all loaded XER files, including:
    - File path and cache key
    - Number of projects and activities
    - Critical activity count and completion percentage

    Can be used by prompts or resources to provide context.
    """
    if not xer_cache:
        return "No Primavera P6 XER files are currently loaded."

    context_parts = ["# Loaded Primavera P6 XER Files\n"]

    for cache_key in xer_cache.keys():
        data = xer_cache.get_raw(cache_key)
        file_path = data.get("file_path", cache_key)
        projects = data.get("projects", [])
        activities = data.get("activities", [])

        # Calculate critical path count
        critical_count = len(
            [
                a
                for a in activities
                if safe_getattr(a, "total_float_hr_cnt") is not None
                and safe_getattr(a, "total_float_hr_cnt") <= 0
            ]
        )

        # Calculate status breakdown
        status_counts = {}
        for activity in activities:
            status = safe_getattr(activity, "status_code", "Unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

        context_parts.append(f"\n## File: {file_path}")
        context_parts.append(f"- Cache Key: `{cache_key}`")
        context_parts.append(f"- Projects: {len(projects)}")
        context_parts.append(f"- Total Activities: {len(activities)}")
        context_parts.append(
            f"- Critical Activities: {critical_count} "
            f"({round(critical_count / len(activities) * 100, 1) if activities else 0}%)"
        )

        if status_counts:
            completed = status_counts.get("TK_Complete", 0)
            context_parts.append(
                f"- Completion: {round(completed / len(activities) * 100, 1) if activities else 0}%"
            )

        # List projects
        if projects:
            context_parts.append("\n### Projects:")
            for proj in projects:
                proj_name = safe_getattr(proj, "proj_short_name") or safe_getattr(
                    proj, "proj_name"
                )
                context_parts.append(f"  - {proj_name}")

    context_parts.append(
        "\n*Use pyp6xer tools for detailed analysis, or export to CSV for Excel visualization.*"
    )

    return "\n".join(context_parts)
