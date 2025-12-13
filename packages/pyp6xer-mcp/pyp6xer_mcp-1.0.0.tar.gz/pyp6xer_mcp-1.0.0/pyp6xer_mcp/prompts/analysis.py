"""Pre-configured analysis workflow prompts for PyP6Xer MCP Server.

These prompts guide Claude through common schedule analysis workflows.
"""

from pyp6xer_mcp.server import mcp
from pyp6xer_mcp.core import xer_cache


@mcp.prompt()
def analyze_critical_path() -> str:
    """Analyze the critical path and identify schedule risks.

    This prompt performs a comprehensive critical path analysis including:
    - Top critical activities by negative float
    - Schedule quality issues
    - Recommendations for recovery
    """
    if not xer_cache:
        return "No XER files loaded. Please load a file first using the pyp6xer_load_file tool."

    cache_key = xer_cache.keys()[0]

    return f"""Please perform a critical path analysis on the loaded XER file.

Use these tools in sequence:
1. pyp6xer_critical_path - Get critical activities (float ≤ 0)
2. pyp6xer_schedule_quality - Identify quality issues
3. pyp6xer_float_analysis - Understand float distribution

Focus on:
- Activities with most severe negative float
- Root causes of schedule delays
- Logic gaps (missing predecessors/successors)
- Recommendations for schedule recovery

Cache key: {cache_key}
"""


@mcp.prompt()
def export_schedule_dashboard() -> str:
    """Export comprehensive schedule data to CSV files for Excel analysis.

    Creates multiple CSV exports for stakeholder reporting and visualization.
    """
    if not xer_cache:
        return "No XER files loaded. Please load a file first using the pyp6xer_load_file tool."

    cache_key = xer_cache.keys()[0]

    return f"""Please export the schedule data to CSV files for Excel analysis.

Create these exports using pyp6xer_export_csv:
1. critical_path.csv - All critical activities sorted by severity
2. schedule_quality.csv - Activities with identified issues
3. all_activities.csv - Complete activity list with dates and float
4. float_analysis.csv - Float distribution data

Save all files to the 'exports/' directory.

After export, summarize:
- Number of rows in each file
- Key findings from the data
- Suggested Excel visualizations (pivot tables, charts)

Cache key: {cache_key}
"""


@mcp.prompt()
def compare_baseline_to_actual() -> str:
    """Compare baseline schedule to actual progress.

    Analyzes variances between planned and actual dates, identifying delays.
    """
    if not xer_cache:
        return "No XER files loaded. Please load a file first using the pyp6xer_load_file tool."

    cache_key = xer_cache.keys()[0]

    return f"""Please analyze the schedule baseline vs actual performance.

Use these tools:
1. pyp6xer_progress_summary - Get overall completion status
2. pyp6xer_float_analysis - Understand schedule pressure
3. pyp6xer_earned_value - Calculate performance metrics (if available)

Analyze:
- Completion percentage (by count and duration)
- Schedule variance (SPI, float trends)
- Activities behind schedule (negative float)
- Root causes of delays

Provide recommendations for:
- Schedule recovery actions
- Re-baseline requirements
- Risk mitigation strategies

Cache key: {cache_key}
"""


@mcp.prompt()
def identify_schedule_quality_issues() -> str:
    """Identify and prioritize schedule quality problems.

    Performs DCMA 14-point assessment style quality checks.
    """
    if not xer_cache:
        return "No XER files loaded. Please load a file first using the pyp6xer_load_file tool."

    cache_key = xer_cache.keys()[0]

    return f"""Please perform a comprehensive schedule quality assessment.

Use these tools:
1. pyp6xer_schedule_quality - Identify quality issues
2. pyp6xer_relationship_analysis - Check logic patterns
3. pyp6xer_float_analysis - Assess schedule health

Check for:
- Missing logic (no predecessors/successors)
- Negative float and causes
- Long duration activities (>20 days)
- Unusual relationship types (SF, negative lags)
- Activities without resources
- Hard constraints driving dates

Prioritize issues by severity and provide:
- Count of each issue type
- Top 10 most critical problems
- Recommended fixes
- Impact on schedule credibility

Cache key: {cache_key}
"""


@mcp.prompt()
def generate_executive_summary() -> str:
    """Generate an executive summary of the project schedule.

    Creates a high-level overview for stakeholders and management.
    """
    if not xer_cache:
        return "No XER files loaded. Please load a file first using the pyp6xer_load_file tool."

    cache_key = xer_cache.keys()[0]

    return f"""Please generate an executive summary of the project schedule.

Use these tools:
1. pyp6xer_list_projects - Get project overview
2. pyp6xer_progress_summary - Overall completion
3. pyp6xer_critical_path - Schedule risks
4. pyp6xer_float_analysis - Schedule health

Create a summary including:
- Project name and key dates (planned start/finish, forecast finish)
- Overall completion percentage
- Schedule health (% critical, average float)
- Top 5 schedule risks (critical activities)
- Schedule quality score
- Key findings and recommendations

Format as a concise executive briefing suitable for management review.

Cache key: {cache_key}
"""
