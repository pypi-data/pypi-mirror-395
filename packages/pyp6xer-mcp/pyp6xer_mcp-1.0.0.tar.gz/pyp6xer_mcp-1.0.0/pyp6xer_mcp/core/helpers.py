"""Helper functions for PyP6Xer MCP Server.

This module provides utility functions for working with cached XER data.
"""

from typing import Any, Dict, Optional

from .cache import CachedXer


def get_project(xer_data: CachedXer, project_id: Optional[str] = None) -> Any:
    """Get a project from the cached XER data, optionally by ID or name.

    Args:
        xer_data: CachedXer containing the parsed XER file.
        project_id: Optional project ID or short name. If not provided,
                    returns the first project.

    Returns:
        Project object from xerparser.

    Raises:
        ValueError: If no projects found or specified project not found.
    """
    projects = xer_data.projects
    if not projects:
        raise ValueError("No projects found in the XER file.")

    if project_id is None:
        return projects[0]

    for proj in projects:
        if (hasattr(proj, "proj_id") and str(proj.proj_id) == project_id) or (
            hasattr(proj, "proj_short_name") and proj.proj_short_name == project_id
        ):
            return proj

    available = [getattr(p, "proj_short_name", "?") for p in projects]
    raise ValueError(f"Project '{project_id}' not found. Available projects: {available}")


def get_project_from_dict(xer_data: Dict[str, Any], project_id: Optional[str] = None) -> Any:
    """Get a project from cached XER data dictionary (backward compatibility).

    Args:
        xer_data: Dictionary with 'projects' key containing project list.
        project_id: Optional project ID or short name.

    Returns:
        Project object from xerparser.

    Raises:
        ValueError: If no projects found or specified project not found.
    """
    projects = xer_data.get("projects", [])
    if not projects:
        raise ValueError("No projects found in the XER file.")

    if project_id is None:
        return projects[0]

    for proj in projects:
        if (hasattr(proj, "proj_id") and str(proj.proj_id) == project_id) or (
            hasattr(proj, "proj_short_name") and proj.proj_short_name == project_id
        ):
            return proj

    available = [getattr(p, "proj_short_name", "?") for p in projects]
    raise ValueError(f"Project '{project_id}' not found. Available projects: {available}")
