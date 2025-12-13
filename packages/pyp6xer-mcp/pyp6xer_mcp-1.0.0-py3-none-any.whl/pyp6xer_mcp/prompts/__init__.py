"""Prompts for PyP6Xer MCP Server.

Pre-configured analysis workflow prompts:
- analyze_critical_path
- export_schedule_dashboard
- compare_baseline_to_actual
- identify_schedule_quality_issues
- generate_executive_summary
"""

from . import analysis

__all__ = ["analysis"]
