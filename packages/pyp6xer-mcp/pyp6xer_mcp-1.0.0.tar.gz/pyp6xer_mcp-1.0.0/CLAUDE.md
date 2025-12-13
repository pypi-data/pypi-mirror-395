# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyP6Xer MCP Server is a Model Context Protocol (MCP) server that provides tools for parsing, analyzing, and manipulating Primavera P6 XER (eXchange ERport) files. It exposes 22 tools, 5 prompts, and 3 resources for schedule analysis, resource management, progress tracking, and earned value calculations.

This project uses uv and a .venv for dependency management.

**Live Deployment**: https://pyp6xer-mcp.fly.dev/mcp

## Commands

### Development Setup
```bash
uv pip install -e .                           # Install in editable mode
uv pip install -e ".[dev]"                    # Install with dev dependencies
```

### Running the Server
```bash
uv python -m pyp6xer_mcp.cli                  # Run stdio (default, for Claude Desktop)
uv python -m pyp6xer_mcp.cli streamable-http  # Run HTTP server on port 5000
uv pyp6xer-mcp                                # Run via entry point (stdio)
```

### Deployment
```bash
fly deploy                                 # Deploy to Fly.io
fly secrets set API_KEY="pyp6xer_xxx"      # Set API key for auth
fly logs                                   # View logs
```

### Linting and Formatting
```bash
black --line-length 100 .                  # Format code
ruff check .                               # Lint code
mypy .                                     # Type checking
```

### Testing
```bash
pytest                                     # Run all tests (27 tests)
pytest -x                                  # Stop on first failure
pytest tests/test_modular_structure.py     # Run modular structure tests
pytest tests/test_server.py                # Run backward compatibility tests
```

## Architecture

### Package Structure

```
pyp6xer_mcp/                  # Main package
├── __init__.py               # Package entry point with backward compat
├── server.py                 # FastMCP server instance and imports
├── cli.py                    # CLI entry point (stdio/http)
├── models/                   # Pydantic input models
│   ├── common.py             # ResponseFormat, ExportType, base models
│   ├── file_ops.py           # LoadXerInput, WriteXerInput, CsvExportInput
│   ├── activities.py         # Activity-related input models
│   ├── analysis.py           # Analysis tool input models
│   └── resources.py          # Resource/calendar/progress input models
├── core/                     # Core utilities
│   ├── cache.py              # XerCache class (encapsulated cache)
│   ├── formatters.py         # Format functions (activity, resource, project)
│   └── helpers.py            # Helper functions (get_project, etc.)
├── tools/                    # MCP tool implementations (22 tools)
│   ├── file_ops.py           # load_file, write_file, clear_cache, export_csv
│   ├── projects.py           # list_projects
│   ├── activities.py         # list/get/search/update activities
│   ├── analysis.py           # critical_path, float, schedule_quality, etc.
│   ├── resources.py          # list_resources, resource_utilization
│   ├── progress.py           # progress_summary, earned_value, work_package
│   └── calendars.py          # list_calendars
├── prompts/                  # MCP prompts (5 workflow prompts)
│   └── analysis.py           # analyze_critical_path, export_dashboard, etc.
├── resources/                # MCP resources (3 resources)
│   └── schedule.py           # schedule://projects, summary, critical
├── context/                  # Context helpers
│   └── xer_context.py        # get_xer_files_context() helper
└── http/                     # HTTP layer
    ├── middleware.py         # APIKeyAuthMiddleware
    └── routes.py             # health_check, upload_file handlers
```

### Key Components

**MCP Server**: Uses FastMCP from the `mcp` library. The server instance is in `server.py`:
```python
from pyp6xer_mcp.server import mcp
```

**XerCache**: Encapsulated cache class in `core/cache.py`:
```python
from pyp6xer_mcp.core import xer_cache
xer_cache.set(key, data)  # Store XER data
data = xer_cache.get(key)  # Retrieve data
```

**Input Models**: Pydantic models in `models/` with strict validation:
```python
from pyp6xer_mcp.models import LoadXerInput, CriticalPathInput
```

**Response Format**: All analysis tools support `ResponseFormat.MARKDOWN` (default) or `ResponseFormat.JSON`.

### Tool Categories

1. **File Operations** (4 tools): `pyp6xer_load_file`, `pyp6xer_write_file`, `pyp6xer_clear_cache`, `pyp6xer_export_csv`
2. **Project/Activity Management** (5 tools): `pyp6xer_list_projects`, `pyp6xer_list_activities`, `pyp6xer_get_activity`, `pyp6xer_search_activities`, `pyp6xer_update_activity`
3. **Schedule Analysis** (6 tools): `pyp6xer_critical_path`, `pyp6xer_float_analysis`, `pyp6xer_schedule_quality`, `pyp6xer_relationship_analysis`, `pyp6xer_slipping_activities`, `pyp6xer_schedule_health_check`
4. **Resource Management** (2 tools): `pyp6xer_list_resources`, `pyp6xer_resource_utilization`
5. **Progress/Performance** (4 tools): `pyp6xer_progress_summary`, `pyp6xer_earned_value`, `pyp6xer_work_package_summary`, `pyp6xer_wbs_analysis`
6. **Structure** (1 tool): `pyp6xer_list_calendars`

### Prompts (5)

- `analyze_critical_path` - Critical path analysis workflow
- `export_schedule_dashboard` - Export to CSV for Excel
- `compare_baseline_to_actual` - Baseline vs actual comparison
- `identify_schedule_quality_issues` - DCMA-style quality checks
- `generate_executive_summary` - Executive briefing

### Resources (3)

- `schedule://projects` - List all loaded projects
- `schedule://{cache_key}/summary` - Schedule summary
- `schedule://{cache_key}/critical` - Critical activities

### File Loading Methods

`pyp6xer_load_file` supports three input methods:
1. **Local paths** - For Claude Desktop: `file_path="/path/to/file.xer"`
2. **URLs** - For remote files: `file_path="https://example.com/file.xer"`
3. **Base64 content** - For AI sandbox uploads: `file_content="<base64_encoded_data>"`

### HTTP Upload Endpoint

For Claude.ai web users, the `/upload` endpoint provides a cleaner alternative to base64:

```bash
curl -X POST -H "Authorization: Bearer <api_key>" \
  -F "file=@project.xer" \
  https://pyp6xer-mcp.fly.dev/upload
```

### Dependencies

- `mcp>=1.0.0` - MCP protocol implementation
- `pydantic>=2.0.0` - Input validation
- `PyP6XER>=0.1.0` - XER file parsing (uses `xerparser.reader.Reader`)
- `httpx>=0.24.0` - HTTP client for URL-based file loading
- `uvicorn>=0.23.0` - ASGI server for HTTP transport

## Authentication

When `API_KEY` environment variable is set and running in HTTP mode:
- Requests must include API key via header (`Authorization: Bearer <key>`) or query param (`?api_key=<key>`)
- Health check endpoint `/health` is unauthenticated
- Upload endpoint `/upload` requires authentication

## Tool Annotations

All tools use MCP annotations to describe their behavior:
- `readOnlyHint: True/False` - Whether the tool modifies state
- `destructiveHint: True/False` - Whether changes are irreversible
- `idempotentHint: True` - Tools can be safely retried
- `openWorldHint: True/False` - Whether the tool accesses external resources

## Backward Compatibility

The original monolith (`pyp6xer_mcp.py`) is archived in `archive/`. The modular package is now the primary codebase. Both import styles work:

```python
# Recommended modular imports
from pyp6xer_mcp.server import mcp
from pyp6xer_mcp.models import LoadXerInput

# Legacy imports (still supported)
from pyp6xer_mcp import mcp, LoadXerInput
```

## Additional Documentation

- **[TOOLS.md](TOOLS.md)** - Complete reference for all 22 tools
- **[README.md](README.md)** - User documentation
