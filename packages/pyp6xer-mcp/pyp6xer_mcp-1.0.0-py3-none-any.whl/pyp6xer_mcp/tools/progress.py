"""Progress and performance tracking tools for PyP6Xer MCP Server."""

import json

from pyp6xer_mcp.server import mcp
from pyp6xer_mcp.models import (
    ProgressSummaryInput,
    EarnedValueInput,
    WbsInput,
    WorkPackageSummaryInput,
    ResponseFormat,
)
from pyp6xer_mcp.core import (
    xer_cache,
    safe_getattr,
    to_markdown_table,
    get_project_from_dict,
)


@mcp.tool(
    name="pyp6xer_progress_summary",
    annotations={
        "title": "Progress Summary",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def pyp6xer_progress_summary(params: ProgressSummaryInput) -> str:
    """Get a summary of project progress including completion rates.

    Args:
        params: ProgressSummaryInput with cache_key and optional project_id.

    Returns:
        str: Progress summary with status breakdown and completion metrics.
    """
    try:
        xer_data = xer_cache.get_raw(params.cache_key)
        project = get_project_from_dict(xer_data, params.project_id)
        activities = list(project.activities)

        # Count by status
        status_counts = {"TK_Complete": 0, "TK_Active": 0, "TK_NotStarted": 0, "Other": 0}

        total_duration = 0
        completed_duration = 0
        total_physical_pct = 0
        activities_with_pct = 0

        for a in activities:
            status = safe_getattr(a, "status_code")
            duration = safe_getattr(a, "duration") or 0
            phys_pct = safe_getattr(a, "phys_complete_pct")

            if status in status_counts:
                status_counts[status] += 1
            else:
                status_counts["Other"] += 1

            total_duration += duration
            if status == "TK_Complete":
                completed_duration += duration
            elif phys_pct:
                completed_duration += duration * (phys_pct / 100)

            if phys_pct is not None:
                total_physical_pct += phys_pct
                activities_with_pct += 1

        total = len(activities)
        completion_rate = (status_counts["TK_Complete"] / total * 100) if total > 0 else 0
        duration_completion = (completed_duration / total_duration * 100) if total_duration > 0 else 0
        avg_physical_pct = (total_physical_pct / activities_with_pct) if activities_with_pct > 0 else 0

        result = {
            "project": safe_getattr(project, "proj_short_name"),
            "total_activities": total,
            "status_breakdown": status_counts,
            "completion_rate_by_count": completion_rate,
            "completion_rate_by_duration": duration_completion,
            "average_physical_complete": avg_physical_pct,
        }

        if params.response_format == ResponseFormat.JSON:
            return json.dumps(result, indent=2, default=str)

        # Markdown format
        lines = [
            f"## Progress Summary",
            f"**Project**: {result['project']}\n",
            f"### Activity Status",
            f"- **Completed**: {status_counts['TK_Complete']} ({status_counts['TK_Complete']/total*100:.1f}%)"
            if total > 0
            else "",
            f"- **In Progress**: {status_counts['TK_Active']} ({status_counts['TK_Active']/total*100:.1f}%)"
            if total > 0
            else "",
            f"- **Not Started**: {status_counts['TK_NotStarted']} ({status_counts['TK_NotStarted']/total*100:.1f}%)"
            if total > 0
            else "",
            f"- **Total**: {total}\n",
            f"### Completion Metrics",
            f"- **By Activity Count**: {completion_rate:.1f}%",
            f"- **By Duration**: {duration_completion:.1f}%",
            f"- **Average Physical %**: {avg_physical_pct:.1f}%\n",
            "### Progress Bar",
        ]

        # Visual progress bar
        filled = int(completion_rate / 5)
        bar = "█" * filled + "░" * (20 - filled)
        lines.append(f"[{bar}] {completion_rate:.1f}%")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


@mcp.tool(
    name="pyp6xer_earned_value",
    annotations={
        "title": "Earned Value Analysis",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def pyp6xer_earned_value(params: EarnedValueInput) -> str:
    """Calculate Earned Value Management (EVM) metrics for a project.

    Calculates:
    - Planned Value (PV/BCWS)
    - Earned Value (EV/BCWP)
    - Actual Cost (AC/ACWP)
    - Cost Performance Index (CPI)
    - Schedule Performance Index (SPI)
    - Cost Variance (CV)
    - Schedule Variance (SV)

    Args:
        params: EarnedValueInput with cache_key and optional project_id.

    Returns:
        str: EVM metrics and performance analysis.
    """
    try:
        xer_data = xer_cache.get_raw(params.cache_key)
        project = get_project_from_dict(xer_data, params.project_id)
        activities = list(project.activities)
        activityresources = xer_data.get("activityresources", [])

        planned_value = 0
        earned_value = 0
        actual_cost = 0

        for activity in activities:
            task_id = safe_getattr(activity, "task_id")
            assignments = [a for a in activityresources if safe_getattr(a, "task_id") == task_id]

            activity_planned = sum(safe_getattr(a, "target_cost") or 0 for a in assignments)
            activity_actual = sum(
                (safe_getattr(a, "act_reg_cost") or 0) + (safe_getattr(a, "act_ot_cost") or 0)
                for a in assignments
            )

            phys_complete = safe_getattr(activity, "phys_complete_pct")
            if phys_complete:
                activity_earned = activity_planned * (phys_complete / 100)
            else:
                activity_earned = 0

            planned_value += activity_planned
            earned_value += activity_earned
            actual_cost += activity_actual

        # Calculate indices
        cpi = earned_value / actual_cost if actual_cost > 0 else 0
        spi = earned_value / planned_value if planned_value > 0 else 0
        cv = earned_value - actual_cost
        sv = earned_value - planned_value

        result = {
            "project": safe_getattr(project, "proj_short_name"),
            "metrics": {
                "planned_value_bcws": planned_value,
                "earned_value_bcwp": earned_value,
                "actual_cost_acwp": actual_cost,
                "cost_variance_cv": cv,
                "schedule_variance_sv": sv,
                "cost_performance_index_cpi": cpi,
                "schedule_performance_index_spi": spi,
            },
            "interpretation": {
                "cost_status": "Under budget" if cpi >= 1 else "Over budget",
                "schedule_status": "Ahead of schedule" if spi >= 1 else "Behind schedule",
            },
        }

        if params.response_format == ResponseFormat.JSON:
            return json.dumps(result, indent=2, default=str)

        # Markdown format
        lines = [
            f"## Earned Value Analysis",
            f"**Project**: {result['project']}\n",
            "### Core Metrics",
            f"- **Planned Value (BCWS)**: ${planned_value:,.2f}",
            f"- **Earned Value (BCWP)**: ${earned_value:,.2f}",
            f"- **Actual Cost (ACWP)**: ${actual_cost:,.2f}\n",
            "### Variances",
            f"- **Cost Variance (CV)**: ${cv:,.2f} {'✅' if cv >= 0 else '❌'}",
            f"- **Schedule Variance (SV)**: ${sv:,.2f} {'✅' if sv >= 0 else '❌'}\n",
            "### Performance Indices",
            f"- **Cost Performance Index (CPI)**: {cpi:.3f} {'✅' if cpi >= 1 else '⚠️'}",
            f"- **Schedule Performance Index (SPI)**: {spi:.3f} {'✅' if spi >= 1 else '⚠️'}\n",
            "### Interpretation",
        ]

        if cpi >= 1:
            lines.append(f"- ✅ **Cost Status**: Under budget by ${cv:,.2f}")
        else:
            lines.append(f"- ❌ **Cost Status**: Over budget by ${abs(cv):,.2f}")

        if spi >= 1:
            lines.append(f"- ✅ **Schedule Status**: Ahead of schedule")
        else:
            lines.append(f"- ⚠️ **Schedule Status**: Behind schedule")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


@mcp.tool(
    name="pyp6xer_wbs_analysis",
    annotations={
        "title": "WBS Analysis",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def pyp6xer_wbs_analysis(params: WbsInput) -> str:
    """Analyze the Work Breakdown Structure hierarchy.

    Args:
        params: WbsInput with cache_key, project_id, and max_depth.

    Returns:
        str: WBS hierarchy with activity counts per element.
    """
    try:
        xer_data = xer_cache.get_raw(params.cache_key)
        project = get_project_from_dict(xer_data, params.project_id)
        wbss = list(project.wbss) if hasattr(project, "wbss") else []
        activities = list(project.activities)

        if not wbss:
            return "No WBS elements found in the project."

        # Build activity count per WBS
        activity_count_by_wbs = {}
        for a in activities:
            wbs_id = safe_getattr(a, "wbs_id")
            if wbs_id:
                activity_count_by_wbs[wbs_id] = activity_count_by_wbs.get(wbs_id, 0) + 1

        wbs_data = []
        for w in wbss:
            wbs_id = safe_getattr(w, "wbs_id")
            wbs_data.append(
                {
                    "wbs_id": wbs_id,
                    "wbs_short_name": safe_getattr(w, "wbs_short_name"),
                    "wbs_name": safe_getattr(w, "wbs_name"),
                    "parent_wbs_id": safe_getattr(w, "parent_wbs_id"),
                    "seq_num": safe_getattr(w, "seq_num"),
                    "activity_count": activity_count_by_wbs.get(wbs_id, 0),
                }
            )

        if params.response_format == ResponseFormat.JSON:
            return json.dumps(
                {
                    "project": safe_getattr(project, "proj_short_name"),
                    "wbs_count": len(wbs_data),
                    "total_activities": len(activities),
                    "wbs_elements": wbs_data,
                },
                indent=2,
                default=str,
            )

        # Markdown format - build hierarchy
        lines = [
            f"## WBS Analysis",
            f"**Project**: {safe_getattr(project, 'proj_short_name')}",
            f"- **WBS Elements**: {len(wbs_data)}",
            f"- **Total Activities**: {len(activities)}\n",
            "### Structure",
        ]

        # Build parent-child relationships
        by_parent = {}
        roots = []
        for w in wbs_data:
            parent = w["parent_wbs_id"]
            if parent:
                if parent not in by_parent:
                    by_parent[parent] = []
                by_parent[parent].append(w)
            else:
                roots.append(w)

        def render_wbs(wbs, depth=0):
            if depth > params.max_depth:
                return []
            indent = "  " * depth
            result = [
                f"{indent}- **{wbs['wbs_short_name']}**: {wbs['wbs_name']} ({wbs['activity_count']} activities)"
            ]
            children = by_parent.get(wbs["wbs_id"], [])
            for child in sorted(children, key=lambda x: x["seq_num"] or 0):
                result.extend(render_wbs(child, depth + 1))
            return result

        for root in roots:
            lines.extend(render_wbs(root))

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


@mcp.tool(
    name="pyp6xer_work_package_summary",
    annotations={
        "title": "Work Package Summary",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def pyp6xer_work_package_summary(params: WorkPackageSummaryInput) -> str:
    """Summarize activities grouped by activity code prefix (work packages).

    Groups activities by user-defined prefixes to provide summary statistics
    for each work package including counts, duration, and completion rates.

    Args:
        params: WorkPackageSummaryInput with cache_key and prefix_list.

    Returns:
        str: Summary statistics for each work package prefix.
    """
    try:
        xer_data = xer_cache.get_raw(params.cache_key)

        if params.project_id:
            project = get_project_from_dict(xer_data, params.project_id)
            activities = list(project.activities)
        else:
            activities = xer_data.get("activities", [])

        # Initialize work packages
        work_packages = {prefix: [] for prefix in params.prefix_list}
        if params.include_unmatched:
            work_packages["Other"] = []

        # Categorize activities by prefix
        for a in activities:
            task_code = safe_getattr(a, "task_code") or ""
            matched = False

            for prefix in params.prefix_list:
                if task_code.upper().startswith(prefix.upper()):
                    work_packages[prefix].append(a)
                    matched = True
                    break

            if not matched and params.include_unmatched:
                work_packages["Other"].append(a)

        # Calculate summary for each work package
        summaries = []
        for prefix, acts in work_packages.items():
            if not acts:
                continue

            total_count = len(acts)
            completed_count = sum(1 for a in acts if safe_getattr(a, "status_code") == "TK_Complete")
            in_progress_count = sum(1 for a in acts if safe_getattr(a, "status_code") == "TK_Active")
            not_started_count = sum(
                1 for a in acts if safe_getattr(a, "status_code") == "TK_NotStarted"
            )

            # Duration calculations
            total_duration_hrs = sum(safe_getattr(a, "target_drtn_hr_cnt") or 0 for a in acts)
            remaining_duration_hrs = sum(safe_getattr(a, "remain_drtn_hr_cnt") or 0 for a in acts)

            # Physical completion (weighted average by duration)
            weighted_complete = 0
            total_weight = 0
            for a in acts:
                duration = safe_getattr(a, "target_drtn_hr_cnt") or 0
                pct = safe_getattr(a, "phys_complete_pct") or 0
                weighted_complete += duration * pct
                total_weight += duration
            avg_complete = weighted_complete / total_weight if total_weight > 0 else 0

            # Float statistics
            floats = [
                safe_getattr(a, "total_float_hr_cnt")
                for a in acts
                if safe_getattr(a, "total_float_hr_cnt") is not None
            ]
            avg_float = sum(floats) / len(floats) if floats else 0
            critical_count = sum(1 for f in floats if f <= 0)

            summaries.append(
                {
                    "prefix": prefix,
                    "total_activities": total_count,
                    "completed": completed_count,
                    "in_progress": in_progress_count,
                    "not_started": not_started_count,
                    "completion_pct": completed_count / total_count * 100 if total_count > 0 else 0,
                    "weighted_complete_pct": avg_complete,
                    "total_duration_days": total_duration_hrs / 8,
                    "remaining_duration_days": remaining_duration_hrs / 8,
                    "avg_float_hours": avg_float,
                    "critical_activities": critical_count,
                }
            )

        # Sort by total activities descending
        summaries.sort(key=lambda x: x["total_activities"], reverse=True)

        if params.response_format == ResponseFormat.JSON:
            return json.dumps(
                {"total_activities": len(activities), "work_packages": summaries},
                indent=2,
                default=str,
            )

        # Markdown format
        lines = [
            "## Work Package Summary\n",
            f"- **Total Activities**: {len(activities)}",
            f"- **Prefixes Analyzed**: {', '.join(params.prefix_list)}",
            f"- **Work Packages Found**: {len([s for s in summaries if s['total_activities'] > 0])}\n",
        ]

        if summaries:
            headers = [
                "Prefix",
                "Activities",
                "Complete",
                "In Progress",
                "Not Started",
                "% Done",
                "Critical",
            ]
            rows = []
            for s in summaries:
                rows.append(
                    [
                        s["prefix"],
                        s["total_activities"],
                        s["completed"],
                        s["in_progress"],
                        s["not_started"],
                        f"{s['completion_pct']:.1f}%",
                        s["critical_activities"],
                    ]
                )
            lines.append(to_markdown_table(headers, rows))

            lines.append("\n### Detailed Metrics")
            for s in summaries:
                if s["total_activities"] > 0:
                    lines.append(f"\n**{s['prefix']}** ({s['total_activities']} activities)")
                    lines.append(
                        f"- Duration: {s['total_duration_days']:.1f} days total, {s['remaining_duration_days']:.1f} days remaining"
                    )
                    lines.append(f"- Weighted % Complete: {s['weighted_complete_pct']:.1f}%")
                    lines.append(
                        f"- Avg Float: {s['avg_float_hours']:.0f} hours ({s['avg_float_hours']/8:.1f} days)"
                    )
        else:
            lines.append("*No activities matched the specified prefixes.*")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"
