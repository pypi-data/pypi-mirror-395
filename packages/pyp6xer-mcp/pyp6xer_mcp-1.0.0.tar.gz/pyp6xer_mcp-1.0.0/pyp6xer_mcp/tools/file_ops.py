"""File operation tools for PyP6Xer MCP Server.

This module contains tools for:
- Loading XER files (local paths, URLs, or base64 content)
- Writing modified XER files
- Exporting data to CSV format
- Clearing the cache
"""

import base64
import csv
import json
import os
import tempfile
from typing import Optional

from pyp6xer_mcp.core import (
    format_project,
    safe_getattr,
    xer_cache,
)
from pyp6xer_mcp.core.helpers import get_project_from_dict
from pyp6xer_mcp.models import (
    CsvExportInput,
    ExportType,
    LoadXerInput,
    ResponseFormat,
    WriteXerInput,
)
from pyp6xer_mcp.server import mcp


@mcp.tool(
    name="pyp6xer_load_file",
    annotations={
        "title": "Load XER File",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def pyp6xer_load_file(params: LoadXerInput) -> str:
    """Load and parse a Primavera P6 XER file.

    This tool reads an XER file and caches it for subsequent operations.
    Must be called before using other PyP6Xer tools.

    Args:
        params: LoadXerInput containing file_path and optional cache_key.
                file_path can be a local path or a URL (http:// or https://).

    Returns:
        str: Summary of the loaded XER file including project count and activity count.
    """
    try:
        from xerparser.reader import Reader
    except ImportError:
        return "Error: PyP6Xer library not installed. Install with: pip install PyP6XER"

    file_path = params.file_path
    file_content = params.file_content

    # Validate that at least one input method is provided
    if not file_path and not file_content:
        return "Error: Either file_path or file_content must be provided."

    # Determine cache key
    if params.cache_key:
        cache_key = params.cache_key
    elif file_path:
        cache_key = file_path
    else:
        cache_key = "uploaded_file"

    # Handle base64 file content (for AI sandbox uploads)
    if file_content:
        try:
            decoded_content = base64.b64decode(file_content)
            # Write to temp file for xerparser
            with tempfile.NamedTemporaryFile(mode="wb", suffix=".xer", delete=False) as tmp:
                tmp.write(decoded_content)
                file_path = tmp.name
        except Exception as e:
            return f"Error decoding base64 file_content: {type(e).__name__}: {str(e)}"
    # Handle URL downloads
    elif file_path.startswith(("http://", "https://")):
        try:
            import httpx

            # Create safe filename from cache_key
            safe_name = cache_key.replace("/", "_").replace(":", "_").replace("?", "_")
            local_path = f"/tmp/{safe_name}.xer"

            async with httpx.AsyncClient(follow_redirects=True, timeout=60.0) as client:
                response = await client.get(file_path)
                response.raise_for_status()
                with open(local_path, "wb") as f:
                    f.write(response.content)
            file_path = local_path
        except ImportError:
            return "Error: httpx library not installed. Install with: pip install httpx"
        except httpx.HTTPStatusError as e:
            return f"Error downloading XER file: HTTP {e.response.status_code}"
        except Exception as e:
            return f"Error downloading XER file: {type(e).__name__}: {str(e)}"

    if not os.path.exists(file_path):
        return f"Error: File not found: {file_path}"

    try:
        xer = Reader(file_path)

        # Cache both the reader and the data lists (generators can only be consumed once)
        projects = list(xer.projects)
        activities = list(xer.activities) if hasattr(xer, "activities") else []
        resources = list(xer.resources) if hasattr(xer, "resources") else []
        calendars = list(xer.calendars) if hasattr(xer, "calendars") else []

        # Try to get activityresources and relations, but don't fail if they cause errors
        try:
            activityresources = (
                list(xer.activityresources) if hasattr(xer, "activityresources") else []
            )
        except (AttributeError, Exception):
            activityresources = []

        try:
            relations = list(xer.relations) if hasattr(xer, "relations") else []
        except (AttributeError, Exception):
            relations = []

        # Store in cache
        xer_cache.set_from_dict(
            cache_key,
            {
                "reader": xer,
                "projects": projects,
                "activities": activities,
                "resources": resources,
                "calendars": calendars,
                "activityresources": activityresources,
                "relations": relations,
                "file_path": file_path,
            },
        )

        summary = {
            "status": "success",
            "cache_key": cache_key,
            "file_path": file_path,
            "projects_count": len(projects),
            "total_activities": len(activities),
            "total_resources": len(resources),
            "total_calendars": len(calendars),
            "projects": [format_project(p) for p in projects],
        }

        return json.dumps(summary, indent=2, default=str)

    except Exception as e:
        return f"Error loading XER file: {type(e).__name__}: {str(e)}"


@mcp.tool(
    name="pyp6xer_write_file",
    annotations={
        "title": "Write XER File",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def pyp6xer_write_file(params: WriteXerInput) -> str:
    """Write the (modified) XER data to a new file.

    Args:
        params: WriteXerInput with cache_key and output_path.

    Returns:
        str: Confirmation of the file write.
    """
    try:
        xer_data = xer_cache.get_raw(params.cache_key)

        # Ensure output directory exists
        output_dir = os.path.dirname(params.output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Write the file
        xer = xer_data.get("reader")
        if xer and hasattr(xer, "write"):
            xer.write(params.output_path)
        else:
            return "Error: The loaded XER reader does not support writing. This may be a read-only version."

        return f"Successfully wrote XER file to: {params.output_path}"

    except Exception as e:
        return f"Error writing XER file: {type(e).__name__}: {str(e)}"


@mcp.tool(
    name="pyp6xer_export_csv",
    annotations={
        "title": "Export to CSV",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def pyp6xer_export_csv(params: CsvExportInput) -> str:
    """Export XER data to CSV file for Excel analysis.

    Exports various types of data to CSV format for easy analysis in Excel or other tools.
    Supports activities, critical path, float analysis, resources, WBS, and schedule quality exports.

    Args:
        params: CsvExportInput with cache_key, output_path, export_type, and optional filters.

    Returns:
        str: Confirmation message with file path and row count.
    """
    try:
        xer_data = xer_cache.get_raw(params.cache_key)

        # Ensure output directory exists
        output_dir = os.path.dirname(params.output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        rows_written = 0

        if params.export_type == ExportType.ACTIVITIES:
            # Export activities with all key fields
            if params.project_id:
                project = get_project_from_dict(xer_data, params.project_id)
                activities = list(project.activities)
            else:
                activities = xer_data.get("activities", [])

            # Apply status filter if provided
            if params.status_filter:
                activities = [
                    a for a in activities if safe_getattr(a, "status_code") == params.status_filter
                ]

            with open(params.output_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                # Write header
                writer.writerow(
                    [
                        "Activity Code",
                        "Activity Name",
                        "Status",
                        "Duration (days)",
                        "Total Float (hours)",
                        "Total Float (days)",
                        "% Complete",
                        "Target Start",
                        "Target Finish",
                        "Early Start",
                        "Early Finish",
                        "Late Start",
                        "Late Finish",
                        "Actual Start",
                        "Actual Finish",
                        "WBS ID",
                        "Calendar ID",
                        "Type",
                    ]
                )

                # Write data rows
                for activity in activities:
                    float_hrs = safe_getattr(activity, "total_float_hr_cnt")
                    float_days = round(float_hrs / 8, 1) if float_hrs is not None else None

                    writer.writerow(
                        [
                            safe_getattr(activity, "task_code", ""),
                            safe_getattr(activity, "task_name", ""),
                            safe_getattr(activity, "status_code", ""),
                            safe_getattr(activity, "target_drtn_hr_cnt", 0) / 8
                            if safe_getattr(activity, "target_drtn_hr_cnt")
                            else 0,
                            float_hrs,
                            float_days,
                            safe_getattr(activity, "phys_complete_pct", 0),
                            str(safe_getattr(activity, "target_start_date", "")),
                            str(safe_getattr(activity, "target_end_date", "")),
                            str(safe_getattr(activity, "early_start_date", "")),
                            str(safe_getattr(activity, "early_end_date", "")),
                            str(safe_getattr(activity, "late_start_date", "")),
                            str(safe_getattr(activity, "late_end_date", "")),
                            str(safe_getattr(activity, "act_start_date", "")),
                            str(safe_getattr(activity, "act_end_date", "")),
                            safe_getattr(activity, "wbs_id", ""),
                            safe_getattr(activity, "clndr_id", ""),
                            safe_getattr(activity, "task_type", ""),
                        ]
                    )
                rows_written = len(activities)

        elif params.export_type == ExportType.CRITICAL_PATH:
            # Export critical path activities (float <= 0)
            if params.project_id:
                project = get_project_from_dict(xer_data, params.project_id)
                activities = list(project.activities)
            else:
                activities = xer_data.get("activities", [])

            # Filter for critical activities
            critical_activities = [
                a
                for a in activities
                if safe_getattr(a, "total_float_hr_cnt") is not None
                and safe_getattr(a, "total_float_hr_cnt") <= 0
            ]

            # Sort by float (most negative first)
            critical_activities.sort(key=lambda a: safe_getattr(a, "total_float_hr_cnt", 0))

            with open(params.output_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    [
                        "Activity Code",
                        "Activity Name",
                        "Status",
                        "Total Float (hours)",
                        "Total Float (days)",
                        "Duration (days)",
                        "% Complete",
                        "Target Start",
                        "Target Finish",
                        "WBS ID",
                    ]
                )

                for activity in critical_activities:
                    float_hrs = safe_getattr(activity, "total_float_hr_cnt")
                    writer.writerow(
                        [
                            safe_getattr(activity, "task_code", ""),
                            safe_getattr(activity, "task_name", ""),
                            safe_getattr(activity, "status_code", ""),
                            float_hrs,
                            round(float_hrs / 8, 1) if float_hrs is not None else None,
                            safe_getattr(activity, "target_drtn_hr_cnt", 0) / 8
                            if safe_getattr(activity, "target_drtn_hr_cnt")
                            else 0,
                            safe_getattr(activity, "phys_complete_pct", 0),
                            str(safe_getattr(activity, "target_start_date", "")),
                            str(safe_getattr(activity, "target_end_date", "")),
                            safe_getattr(activity, "wbs_id", ""),
                        ]
                    )
                rows_written = len(critical_activities)

        elif params.export_type == ExportType.FLOAT_ANALYSIS:
            # Export float distribution
            if params.project_id:
                project = get_project_from_dict(xer_data, params.project_id)
                activities = list(project.activities)
            else:
                activities = xer_data.get("activities", [])

            # Filter activities with float data
            activities_with_float = [
                a for a in activities if safe_getattr(a, "total_float_hr_cnt") is not None
            ]

            with open(params.output_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    [
                        "Activity Code",
                        "Activity Name",
                        "Total Float (hours)",
                        "Total Float (days)",
                        "Status",
                        "% Complete",
                        "Duration (days)",
                    ]
                )

                for activity in activities_with_float:
                    float_hrs = safe_getattr(activity, "total_float_hr_cnt")
                    writer.writerow(
                        [
                            safe_getattr(activity, "task_code", ""),
                            safe_getattr(activity, "task_name", ""),
                            float_hrs,
                            round(float_hrs / 8, 1) if float_hrs is not None else None,
                            safe_getattr(activity, "status_code", ""),
                            safe_getattr(activity, "phys_complete_pct", 0),
                            safe_getattr(activity, "target_drtn_hr_cnt", 0) / 8
                            if safe_getattr(activity, "target_drtn_hr_cnt")
                            else 0,
                        ]
                    )
                rows_written = len(activities_with_float)

        elif params.export_type == ExportType.RESOURCES:
            # Export resources
            resources = xer_data.get("resources", [])

            with open(params.output_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Resource ID", "Resource Name", "Resource Type", "Unit"])

                for resource in resources:
                    writer.writerow(
                        [
                            safe_getattr(resource, "rsrc_id", ""),
                            safe_getattr(resource, "rsrc_name", ""),
                            safe_getattr(resource, "rsrc_type", ""),
                            safe_getattr(resource, "unit_name", ""),
                        ]
                    )
                rows_written = len(resources)

        elif params.export_type == ExportType.SCHEDULE_QUALITY:
            # Export schedule quality issues
            if params.project_id:
                project = get_project_from_dict(xer_data, params.project_id)
                activities = list(project.activities)
            else:
                activities = xer_data.get("activities", [])

            with open(params.output_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    [
                        "Activity Code",
                        "Activity Name",
                        "Issue Type",
                        "Total Float (days)",
                        "Duration (days)",
                        "Has Predecessors",
                        "Has Successors",
                        "Status",
                    ]
                )

                for activity in activities:
                    issues = []
                    float_hrs = safe_getattr(activity, "total_float_hr_cnt")

                    # Check for issues
                    has_pred = hasattr(activity, "predecessors") and len(
                        list(activity.predecessors)
                    ) > 0
                    has_succ = hasattr(activity, "successors") and len(
                        list(activity.successors)
                    ) > 0
                    duration_days = (
                        safe_getattr(activity, "target_drtn_hr_cnt", 0) / 8
                        if safe_getattr(activity, "target_drtn_hr_cnt")
                        else 0
                    )

                    if float_hrs is not None and float_hrs < 0:
                        issues.append("Negative Float")
                    if not has_pred and safe_getattr(activity, "task_type") != "TT_Mile":
                        issues.append("No Predecessors")
                    if not has_succ and safe_getattr(activity, "task_type") != "TT_FinMile":
                        issues.append("No Successors")
                    if duration_days > 20:
                        issues.append("Long Duration")

                    # Only write rows with issues
                    if issues:
                        writer.writerow(
                            [
                                safe_getattr(activity, "task_code", ""),
                                safe_getattr(activity, "task_name", ""),
                                "; ".join(issues),
                                round(float_hrs / 8, 1) if float_hrs is not None else "",
                                duration_days,
                                "Yes" if has_pred else "No",
                                "Yes" if has_succ else "No",
                                safe_getattr(activity, "status_code", ""),
                            ]
                        )
                        rows_written += 1

        else:
            return f"Error: Unsupported export type: {params.export_type}"

        return f"Successfully exported {rows_written} rows to: {params.output_path}\nExport type: {params.export_type}"

    except Exception as e:
        return f"Error exporting to CSV: {type(e).__name__}: {str(e)}"


@mcp.tool(
    name="pyp6xer_clear_cache",
    annotations={
        "title": "Clear Cache",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def pyp6xer_clear_cache(cache_key: Optional[str] = None) -> str:
    """Clear cached XER data.

    Args:
        cache_key: Optional specific cache key to clear. If not provided, clears all.

    Returns:
        str: Confirmation of cache clearing.
    """
    if cache_key:
        if xer_cache.delete(cache_key):
            return f"Cleared cache for key: {cache_key}"
        return f"No cache found for key: {cache_key}"

    count = xer_cache.clear()
    return f"Cleared all {count} cached XER file(s)."
