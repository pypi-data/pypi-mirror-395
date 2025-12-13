"""HTTP route handlers for PyP6Xer MCP Server."""

import os
import tempfile
import uuid

from starlette.responses import JSONResponse

from pyp6xer_mcp.core import xer_cache


async def health_check(request):
    """Health check endpoint."""
    return JSONResponse({"status": "ok", "server": "pyp6xer_mcp"})


async def upload_file(request):
    """Upload XER file directly via HTTP POST.

    This endpoint allows users to upload XER files directly via HTTP,
    which is useful for Claude.ai web users who can't use local file paths.
    """
    from xerparser.reader import Reader

    try:
        form = await request.form()
        uploaded_file = form.get("file")

        if not uploaded_file:
            return JSONResponse(
                {"error": "No file uploaded. Use form field 'file'."}, status_code=400
            )

        content = await uploaded_file.read()
        if isinstance(content, bytes):
            content = content.decode("utf-8", errors="replace")

        cache_key = form.get("cache_key") or f"upload_{uuid.uuid4().hex[:8]}"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".xer", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            xer = Reader(tmp_path)

            # Cache in same format as pyp6xer_load_file
            projects = list(xer.projects)
            activities = list(xer.activities) if hasattr(xer, "activities") else []
            resources = list(xer.resources) if hasattr(xer, "resources") else []
            calendars = list(xer.calendars) if hasattr(xer, "calendars") else []

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
                    "file_path": f"upload:{uploaded_file.filename}",
                },
            )
        finally:
            os.unlink(tmp_path)

        projects_response = [
            {"id": getattr(p, "proj_id", None), "short_name": getattr(p, "proj_short_name", None)}
            for p in projects
        ]
        activity_count = len(activities)

        return JSONResponse(
            {
                "cache_key": cache_key,
                "projects": projects_response,
                "activity_count": activity_count,
                "message": f"XER loaded. Use cache_key '{cache_key}' with MCP tools.",
            }
        )
    except Exception as e:
        return JSONResponse({"error": f"Failed to parse XER: {str(e)}"}, status_code=400)
