"""Schedule analysis tools for PyP6Xer MCP Server.

This module provides tools for critical path analysis, float analysis,
schedule quality checks, relationship analysis, slipping activities,
and comprehensive schedule health checks.
"""

import json
from typing import Any, Dict, List

from pyp6xer_mcp.core import (
    format_activity,
    get_project_from_dict,
    safe_getattr,
    to_markdown_table,
    xer_cache,
)
from pyp6xer_mcp.models import (
    CriticalPathInput,
    FloatAnalysisInput,
    RelationshipAnalysisInput,
    ResponseFormat,
    ScheduleHealthCheckInput,
    ScheduleQualityInput,
    SlippingActivitiesInput,
)
from pyp6xer_mcp.server import mcp


@mcp.tool(
    name="pyp6xer_critical_path",
    annotations={
        "title": "Critical Path Analysis",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def pyp6xer_critical_path(params: CriticalPathInput) -> str:
    """Identify critical path activities (activities with zero or negative float).

    Args:
        params: CriticalPathInput with cache_key, project_id, and float_threshold_hours.

    Returns:
        str: List of critical activities sorted by float.
    """
    try:
        xer_data = xer_cache.get_raw(params.cache_key)

        if params.project_id:
            project = get_project_from_dict(xer_data, params.project_id)
            activities = list(project.activities)
        else:
            activities = xer_data.get("activities", [])

        # Find critical activities
        critical = []
        for a in activities:
            total_float = safe_getattr(a, "total_float_hr_cnt")
            if total_float is not None and total_float <= params.float_threshold_hours:
                critical.append(a)

        # Sort by float (most critical first)
        critical.sort(key=lambda x: safe_getattr(x, "total_float_hr_cnt") or 0)

        activity_data = [format_activity(a) for a in critical]

        if params.response_format == ResponseFormat.JSON:
            return json.dumps(
                {
                    "total_activities": len(activities),
                    "critical_count": len(critical),
                    "float_threshold_hours": params.float_threshold_hours,
                    "critical_activities": activity_data,
                },
                indent=2,
                default=str,
            )

        # Markdown format
        lines = [
            f"## Critical Path Analysis",
            f"- **Total Activities**: {len(activities)}",
            f"- **Critical Activities**: {len(critical)} ({len(critical)/len(activities)*100:.1f}% of total)"
            if activities
            else "",
            f"- **Float Threshold**: ≤ {params.float_threshold_hours} hours\n",
        ]

        if critical:
            headers = ["Code", "Name", "Duration", "Status", "Total Float (hrs)"]
            rows = []
            for a in activity_data:
                rows.append(
                    [
                        a["task_code"],
                        (a["task_name"] or "")[:35],
                        a["duration"] or "-",
                        (a["status_code"] or "")[-10:],
                        a["total_float_hr_cnt"],
                    ]
                )
            lines.append(to_markdown_table(headers, rows))
        else:
            lines.append("*No critical activities found with the specified threshold.*")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


@mcp.tool(
    name="pyp6xer_schedule_quality",
    annotations={
        "title": "Schedule Quality Check",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def pyp6xer_schedule_quality(params: ScheduleQualityInput) -> str:
    """Perform schedule quality checks to identify potential issues.

    Checks for:
    - Activities without predecessors (except start milestones)
    - Activities without successors (except finish milestones)
    - Long duration activities
    - Activities with constraints
    - Negative float

    Args:
        params: ScheduleQualityInput with cache_key, project_id, and max_duration_days.

    Returns:
        str: Schedule quality report with identified issues.
    """
    try:
        xer_data = xer_cache.get_raw(params.cache_key)

        if params.project_id:
            project = get_project_from_dict(xer_data, params.project_id)
            activities = list(project.activities)
        else:
            activities = xer_data.get("activities", [])

        issues = {
            "no_predecessors": [],
            "no_successors": [],
            "long_duration": [],
            "negative_float": [],
            "high_float": [],
        }

        for a in activities:
            task_code = safe_getattr(a, "task_code")
            task_name = safe_getattr(a, "task_name")
            task_type = safe_getattr(a, "task_type")
            duration = safe_getattr(a, "duration")
            total_float = safe_getattr(a, "total_float_hr_cnt")

            # Check for missing predecessors (except start milestones)
            predecessors = list(a.predecessors) if hasattr(a, "predecessors") else []
            if not predecessors and task_type != "TT_Mile":
                issues["no_predecessors"].append({"code": task_code, "name": task_name})

            # Check for missing successors (except finish milestones)
            successors = list(a.successors) if hasattr(a, "successors") else []
            if not successors and task_type != "TT_Mile":
                issues["no_successors"].append({"code": task_code, "name": task_name})

            # Check for long duration
            if duration and duration > params.max_duration_days:
                issues["long_duration"].append(
                    {"code": task_code, "name": task_name, "duration": duration}
                )

            # Check for negative float
            if total_float is not None and total_float < 0:
                issues["negative_float"].append(
                    {"code": task_code, "name": task_name, "float": total_float}
                )

            # Check for excessive float (> 6 months ~ 1040 hours)
            if total_float is not None and total_float > 1040:
                issues["high_float"].append(
                    {"code": task_code, "name": task_name, "float": total_float}
                )

        total_issues = sum(len(v) for v in issues.values())

        if params.response_format == ResponseFormat.JSON:
            return json.dumps(
                {"total_activities": len(activities), "total_issues": total_issues, "issues": issues},
                indent=2,
                default=str,
            )

        # Markdown format
        lines = [
            f"## Schedule Quality Report",
            f"- **Total Activities**: {len(activities)}",
            f"- **Total Issues Found**: {total_issues}\n",
        ]

        if issues["negative_float"]:
            lines.append(f"### ❌ Negative Float ({len(issues['negative_float'])})")
            for item in issues["negative_float"][:10]:
                lines.append(f"- **{item['code']}**: {item['name']} (float: {item['float']}h)")
            lines.append("")

        if issues["no_predecessors"]:
            lines.append(f"### ⚠️ No Predecessors ({len(issues['no_predecessors'])})")
            lines.append("*Activities without predecessors may indicate logic gaps.*")
            for item in issues["no_predecessors"][:10]:
                lines.append(f"- **{item['code']}**: {item['name']}")
            if len(issues["no_predecessors"]) > 10:
                lines.append(f"*...and {len(issues['no_predecessors']) - 10} more*")
            lines.append("")

        if issues["no_successors"]:
            lines.append(f"### ⚠️ No Successors ({len(issues['no_successors'])})")
            lines.append("*Activities without successors may indicate open ends.*")
            for item in issues["no_successors"][:10]:
                lines.append(f"- **{item['code']}**: {item['name']}")
            if len(issues["no_successors"]) > 10:
                lines.append(f"*...and {len(issues['no_successors']) - 10} more*")
            lines.append("")

        if issues["long_duration"]:
            lines.append(
                f"### ⚠️ Long Duration (>{params.max_duration_days} days) ({len(issues['long_duration'])})"
            )
            for item in issues["long_duration"][:10]:
                lines.append(f"- **{item['code']}**: {item['name']} ({item['duration']} days)")
            lines.append("")

        if issues["high_float"]:
            lines.append(f"### ℹ️ High Float (>1040 hours) ({len(issues['high_float'])})")
            for item in issues["high_float"][:10]:
                lines.append(f"- **{item['code']}**: {item['name']} ({item['float']}h)")
            lines.append("")

        if total_issues == 0:
            lines.append("✅ **No quality issues detected!**")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


@mcp.tool(
    name="pyp6xer_float_analysis",
    annotations={
        "title": "Float Analysis",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def pyp6xer_float_analysis(params: FloatAnalysisInput) -> str:
    """Analyze float distribution across activities.

    Groups activities by float categories to understand schedule flexibility.

    Args:
        params: FloatAnalysisInput with cache_key, project_id, and optional float_categories.

    Returns:
        str: Float distribution analysis with category breakdown.
    """
    try:
        xer_data = xer_cache.get_raw(params.cache_key)

        if params.project_id:
            project = get_project_from_dict(xer_data, params.project_id)
            activities = list(project.activities)
        else:
            activities = xer_data.get("activities", [])

        # Convert float threshold from days to hours (assuming 8 hour days)
        thresholds = params.float_categories or [0, 5, 10, 20, 40]
        thresholds_hours = [t * 8 for t in thresholds]

        categories = {}
        activities_with_float = []

        for a in activities:
            total_float = safe_getattr(a, "total_float_hr_cnt")
            if total_float is not None:
                activities_with_float.append(
                    {
                        "task_code": safe_getattr(a, "task_code"),
                        "task_name": safe_getattr(a, "task_name"),
                        "total_float_hrs": total_float,
                        "total_float_days": total_float / 8 if total_float else 0,
                    }
                )

        # Categorize
        for i, threshold in enumerate(thresholds_hours):
            if i == 0:
                label = f"Critical (≤{thresholds[0]}d)"
                count = len([a for a in activities_with_float if a["total_float_hrs"] <= threshold])
            elif i == len(thresholds_hours) - 1:
                label = f">{thresholds[-1]}d"
                count = len([a for a in activities_with_float if a["total_float_hrs"] > threshold])
            else:
                prev = thresholds_hours[i - 1] if i > 0 else 0
                label = f"{thresholds[i-1]+1}-{thresholds[i]}d"
                count = len(
                    [a for a in activities_with_float if prev < a["total_float_hrs"] <= threshold]
                )

            categories[label] = count

        # Calculate statistics
        if activities_with_float:
            floats = [a["total_float_hrs"] for a in activities_with_float]
            avg_float = sum(floats) / len(floats)
            min_float = min(floats)
            max_float = max(floats)
        else:
            avg_float = min_float = max_float = 0

        result = {
            "total_activities": len(activities),
            "activities_with_float": len(activities_with_float),
            "statistics": {
                "average_float_hours": avg_float,
                "average_float_days": avg_float / 8,
                "min_float_hours": min_float,
                "max_float_hours": max_float,
            },
            "distribution": categories,
        }

        if params.response_format == ResponseFormat.JSON:
            return json.dumps(result, indent=2, default=str)

        # Markdown format
        lines = [
            "## Float Analysis\n",
            f"- **Total Activities**: {len(activities)}",
            f"- **Activities with Float Data**: {len(activities_with_float)}\n",
            "### Statistics",
            f"- **Average Float**: {avg_float/8:.1f} days ({avg_float:.0f} hours)",
            f"- **Min Float**: {min_float/8:.1f} days ({min_float:.0f} hours)",
            f"- **Max Float**: {max_float/8:.1f} days ({max_float:.0f} hours)\n",
            "### Distribution",
        ]

        total = len(activities_with_float) or 1
        for label, count in categories.items():
            pct = count / total * 100
            bar = "█" * int(pct / 5)
            lines.append(f"- **{label}**: {count} ({pct:.1f}%) {bar}")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


@mcp.tool(
    name="pyp6xer_relationship_analysis",
    annotations={
        "title": "Relationship Analysis",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def pyp6xer_relationship_analysis(params: RelationshipAnalysisInput) -> str:
    """Analyze activity relationships and dependencies.

    Args:
        params: RelationshipAnalysisInput with cache_key and optional filters.

    Returns:
        str: Relationship statistics and breakdown by type.
    """
    try:
        xer_data = xer_cache.get_raw(params.cache_key)
        relations = xer_data.get("relations", [])

        if not relations:
            return "No relationships found in the XER file."

        # Count by type
        by_type = {}
        with_lag = 0
        negative_lag = 0

        for r in relations:
            pred_type = safe_getattr(r, "pred_type") or "Unknown"
            if pred_type not in by_type:
                by_type[pred_type] = []
            by_type[pred_type].append(r)

            lag = safe_getattr(r, "lag_hr_cnt")
            if lag and lag != 0:
                with_lag += 1
                if lag < 0:
                    negative_lag += 1

        # Filter by type if specified
        if params.relationship_type and params.relationship_type in by_type:
            by_type = {params.relationship_type: by_type[params.relationship_type]}

        if params.response_format == ResponseFormat.JSON:
            result = {
                "total_relationships": len(relations),
                "relationships_with_lag": with_lag,
                "relationships_with_negative_lag": negative_lag,
                "by_type": {k: len(v) for k, v in by_type.items()},
            }
            return json.dumps(result, indent=2, default=str)

        # Markdown format
        lines = [
            "## Relationship Analysis\n",
            f"- **Total Relationships**: {len(relations)}",
            f"- **With Lag**: {with_lag}",
            f"- **With Negative Lag**: {negative_lag}\n",
            "### By Type",
        ]

        type_descriptions = {
            "PR_FS": "Finish-to-Start (predecessor must finish before successor starts)",
            "PR_SS": "Start-to-Start (predecessor must start before successor starts)",
            "PR_FF": "Finish-to-Finish (predecessor must finish before successor finishes)",
            "PR_SF": "Start-to-Finish (predecessor must start before successor finishes)",
        }

        for rel_type, rel_list in by_type.items():
            desc = type_descriptions.get(rel_type, "")
            pct = len(rel_list) / len(relations) * 100
            lines.append(f"- **{rel_type}**: {len(rel_list)} ({pct:.1f}%)")
            if desc:
                lines.append(f"  *{desc}*")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


@mcp.tool(
    name="pyp6xer_slipping_activities",
    annotations={
        "title": "Slipping Activities",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def pyp6xer_slipping_activities(params: SlippingActivitiesInput) -> str:
    """Identify activities where forecast finish dates are slipping beyond baseline.

    Compares early_end_date (forecast) vs target_end_date (baseline) to identify
    activities that are forecasting to finish later than originally planned.

    Args:
        params: SlippingActivitiesInput with cache_key, threshold_days, and filters.

    Returns:
        str: List of slipping activities sorted by slip severity.
    """
    try:
        xer_data = xer_cache.get_raw(params.cache_key)

        if params.project_id:
            project = get_project_from_dict(xer_data, params.project_id)
            activities = list(project.activities)
        else:
            activities = xer_data.get("activities", [])

        slipping = []

        for a in activities:
            # Skip completed activities unless requested
            status = safe_getattr(a, "status_code")
            if not params.include_completed and status == "TK_Complete":
                continue

            target_end = safe_getattr(a, "target_end_date")
            early_end = safe_getattr(a, "early_end_date")

            # Need both dates to calculate slip
            if target_end is None or early_end is None:
                continue

            # Calculate slip in days
            try:
                if hasattr(target_end, "date"):
                    target_end = target_end.date() if hasattr(target_end, "date") else target_end
                if hasattr(early_end, "date"):
                    early_end = early_end.date() if hasattr(early_end, "date") else early_end

                slip_delta = (early_end - target_end).days
            except (TypeError, AttributeError):
                continue

            # Only include activities slipping beyond threshold
            if slip_delta > params.threshold_days:
                slipping.append(
                    {
                        "task_code": safe_getattr(a, "task_code"),
                        "task_name": safe_getattr(a, "task_name"),
                        "status_code": status,
                        "target_end_date": str(target_end),
                        "early_end_date": str(early_end),
                        "slip_days": slip_delta,
                        "phys_complete_pct": safe_getattr(a, "phys_complete_pct"),
                        "total_float_hr_cnt": safe_getattr(a, "total_float_hr_cnt"),
                    }
                )

        # Sort by slip severity (most slipping first)
        slipping.sort(key=lambda x: x["slip_days"], reverse=True)

        # Apply limit
        slipping = slipping[: params.limit]

        if params.response_format == ResponseFormat.JSON:
            return json.dumps(
                {
                    "total_activities": len(activities),
                    "slipping_count": len(slipping),
                    "threshold_days": params.threshold_days,
                    "slipping_activities": slipping,
                },
                indent=2,
                default=str,
            )

        # Markdown format
        lines = [
            "## Slipping Activities Analysis\n",
            f"- **Total Activities Analyzed**: {len(activities)}",
            f"- **Activities Slipping**: {len(slipping)}",
            f"- **Threshold**: >{params.threshold_days} days\n",
        ]

        if slipping:
            headers = ["Code", "Name", "Target End", "Forecast End", "Slip (days)", "Status", "% Complete"]
            rows = []
            for a in slipping:
                rows.append(
                    [
                        a["task_code"],
                        (a["task_name"] or "")[:35],
                        a["target_end_date"][:10] if a["target_end_date"] else "-",
                        a["early_end_date"][:10] if a["early_end_date"] else "-",
                        f"+{a['slip_days']}",
                        (a["status_code"] or "")[-10:],
                        f"{a['phys_complete_pct']}%" if a["phys_complete_pct"] is not None else "-",
                    ]
                )
            lines.append(to_markdown_table(headers, rows))

            # Summary statistics
            total_slip = sum(a["slip_days"] for a in slipping)
            avg_slip = total_slip / len(slipping) if slipping else 0
            max_slip = max(a["slip_days"] for a in slipping) if slipping else 0

            lines.append(f"\n### Summary")
            lines.append(f"- **Average Slip**: {avg_slip:.1f} days")
            lines.append(f"- **Maximum Slip**: {max_slip} days")
            lines.append(f"- **Total Slip**: {total_slip} days")
        else:
            lines.append("✅ **No slipping activities found** beyond the threshold.")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


@mcp.tool(
    name="pyp6xer_schedule_health_check",
    annotations={
        "title": "Schedule Health Check",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def pyp6xer_schedule_health_check(params: ScheduleHealthCheckInput) -> str:
    """Perform a comprehensive schedule health assessment.

    Provides a dashboard-style overview combining multiple schedule metrics:
    completion status, float distribution, logic gaps, slipping activities,
    and an overall health score.

    Args:
        params: ScheduleHealthCheckInput with cache_key and optional project_id.

    Returns:
        str: Comprehensive schedule health report with score.
    """
    try:
        xer_data = xer_cache.get_raw(params.cache_key)

        if params.project_id:
            project = get_project_from_dict(xer_data, params.project_id)
            activities = list(project.activities)
            project_name = safe_getattr(project, "proj_short_name") or params.project_id
        else:
            activities = xer_data.get("activities", [])
            project_name = "All Projects"

        total_count = len(activities)
        if total_count == 0:
            return "No activities found to analyze."

        # === 1. Completion Metrics ===
        completed = sum(1 for a in activities if safe_getattr(a, "status_code") == "TK_Complete")
        in_progress = sum(1 for a in activities if safe_getattr(a, "status_code") == "TK_Active")
        not_started = sum(1 for a in activities if safe_getattr(a, "status_code") == "TK_NotStarted")
        completion_pct = completed / total_count * 100

        # Weighted completion by duration
        weighted_complete = 0
        total_weight = 0
        for a in activities:
            duration = safe_getattr(a, "target_drtn_hr_cnt") or 0
            pct = safe_getattr(a, "phys_complete_pct") or 0
            weighted_complete += duration * pct
            total_weight += duration
        weighted_completion_pct = weighted_complete / total_weight if total_weight > 0 else 0

        # === 2. Float Distribution ===
        floats = []
        for a in activities:
            f = safe_getattr(a, "total_float_hr_cnt")
            if f is not None:
                floats.append(f)

        negative_float_count = sum(1 for f in floats if f < 0)
        critical_count = sum(1 for f in floats if f <= 0)
        near_critical_count = sum(1 for f in floats if 0 < f <= 40)  # <=5 days
        healthy_float_count = sum(1 for f in floats if f > 40)

        avg_float = sum(floats) / len(floats) if floats else 0
        min_float = min(floats) if floats else 0
        max_float = max(floats) if floats else 0

        critical_pct = critical_count / len(floats) * 100 if floats else 0

        # === 3. Logic Quality ===
        no_predecessors = 0
        no_successors = 0

        for a in activities:
            task_type = safe_getattr(a, "task_type")
            has_pred = hasattr(a, "predecessors") and len(list(a.predecessors)) > 0
            has_succ = hasattr(a, "successors") and len(list(a.successors)) > 0

            if not has_pred and task_type not in ["TT_Mile", "TT_FinMile"]:
                no_predecessors += 1
            if not has_succ and task_type not in ["TT_Mile", "TT_FinMile"]:
                no_successors += 1

        logic_issues = no_predecessors + no_successors
        logic_quality_pct = (1 - logic_issues / (total_count * 2)) * 100 if total_count > 0 else 100

        # === 4. Slipping Activities ===
        slipping_count = 0
        total_slip_days = 0

        for a in activities:
            if safe_getattr(a, "status_code") == "TK_Complete":
                continue

            target_end = safe_getattr(a, "target_end_date")
            early_end = safe_getattr(a, "early_end_date")

            if target_end and early_end:
                try:
                    if hasattr(target_end, "date"):
                        target_end = target_end.date()
                    if hasattr(early_end, "date"):
                        early_end = early_end.date()
                    slip = (early_end - target_end).days
                    if slip > 0:
                        slipping_count += 1
                        total_slip_days += slip
                except (TypeError, AttributeError):
                    pass

        slipping_pct = slipping_count / total_count * 100 if total_count > 0 else 0

        # === 5. Calculate Health Score (0-100) ===
        # Weights: Completion=20%, Float Health=25%, Logic=25%, Slippage=30%

        # Completion score (higher completion = better)
        completion_score = weighted_completion_pct  # 0-100

        # Float health score (fewer critical = better)
        float_score = max(0, 100 - critical_pct * 2)  # Penalize critical activities

        # Logic score
        logic_score = logic_quality_pct

        # Slippage score (fewer slipping = better)
        slippage_score = max(0, 100 - slipping_pct * 2)  # Penalize slipping activities

        # Weighted health score
        health_score = (
            completion_score * 0.20
            + float_score * 0.25
            + logic_score * 0.25
            + slippage_score * 0.30
        )

        # Health rating
        if health_score >= 80:
            health_rating = "🟢 Healthy"
        elif health_score >= 60:
            health_rating = "🟡 Caution"
        elif health_score >= 40:
            health_rating = "🟠 At Risk"
        else:
            health_rating = "🔴 Critical"

        result = {
            "project": project_name,
            "health_score": round(health_score, 1),
            "health_rating": health_rating,
            "metrics": {
                "total_activities": total_count,
                "completion": {
                    "completed": completed,
                    "in_progress": in_progress,
                    "not_started": not_started,
                    "completion_pct": round(completion_pct, 1),
                    "weighted_completion_pct": round(weighted_completion_pct, 1),
                },
                "float": {
                    "critical_count": critical_count,
                    "critical_pct": round(critical_pct, 1),
                    "negative_float_count": negative_float_count,
                    "near_critical_count": near_critical_count,
                    "avg_float_hours": round(avg_float, 1),
                    "min_float_hours": min_float,
                    "max_float_hours": max_float,
                },
                "logic": {
                    "no_predecessors": no_predecessors,
                    "no_successors": no_successors,
                    "logic_quality_pct": round(logic_quality_pct, 1),
                },
                "slippage": {
                    "slipping_count": slipping_count,
                    "slipping_pct": round(slipping_pct, 1),
                    "total_slip_days": total_slip_days,
                    "avg_slip_days": round(total_slip_days / slipping_count, 1)
                    if slipping_count > 0
                    else 0,
                },
            },
            "component_scores": {
                "completion_score": round(completion_score, 1),
                "float_score": round(float_score, 1),
                "logic_score": round(logic_score, 1),
                "slippage_score": round(slippage_score, 1),
            },
        }

        if params.response_format == ResponseFormat.JSON:
            return json.dumps(result, indent=2, default=str)

        # Markdown format
        lines = [
            f"## Schedule Health Check\n",
            f"**Project**: {project_name}",
            f"**Total Activities**: {total_count}\n",
            f"### Overall Health Score: {health_score:.0f}/100 {health_rating}\n",
            "```",
            f"[{'█' * int(health_score / 5)}{'░' * (20 - int(health_score / 5))}] {health_score:.0f}%",
            "```\n",
            "---\n",
            "### 📊 Completion Status",
            f"- **Completed**: {completed} ({completion_pct:.1f}%)",
            f"- **In Progress**: {in_progress}",
            f"- **Not Started**: {not_started}",
            f"- **Weighted % Complete**: {weighted_completion_pct:.1f}%\n",
            "### ⏱️ Float Distribution",
            f"- **Critical (≤0)**: {critical_count} ({critical_pct:.1f}%)",
            f"- **Negative Float**: {negative_float_count}",
            f"- **Near Critical (1-5 days)**: {near_critical_count}",
            f"- **Healthy (>5 days)**: {healthy_float_count}",
            f"- **Average Float**: {avg_float/8:.1f} days ({avg_float:.0f} hours)\n",
            "### 🔗 Logic Quality",
            f"- **No Predecessors**: {no_predecessors}",
            f"- **No Successors**: {no_successors}",
            f"- **Logic Quality**: {logic_quality_pct:.1f}%\n",
            "### 📉 Schedule Slippage",
            f"- **Slipping Activities**: {slipping_count} ({slipping_pct:.1f}%)",
            f"- **Total Slip**: {total_slip_days} days",
            f"- **Avg Slip**: {total_slip_days / slipping_count:.1f} days"
            if slipping_count > 0
            else "- **Avg Slip**: N/A",
            "\n---\n",
            "### Component Scores",
            f"| Component | Score | Weight |",
            f"|-----------|-------|--------|",
            f"| Completion | {completion_score:.0f} | 20% |",
            f"| Float Health | {float_score:.0f} | 25% |",
            f"| Logic Quality | {logic_score:.0f} | 25% |",
            f"| Slippage | {slippage_score:.0f} | 30% |",
        ]

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"
