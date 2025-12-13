# PyP6Xer MCP Server

**AI-powered analysis for Primavera P6 schedules** — Parse XER files, analyze critical paths, track progress, and generate insights using Claude Desktop, ChatGPT, or any MCP-compatible AI.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## Quick Start

### Claude Desktop (Recommended)

**1. Install via uvx (easiest):**

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pyp6xer": {
      "command": "uvx",
      "args": ["pyp6xer-mcp"]
    }
  }
}
```

**2. Restart Claude Desktop**

**3. Start analyzing:**
```
"Load the file at /path/to/project.xer and analyze the critical path"
```

That's it! No installation needed — `uvx` automatically downloads and runs the latest version.

<details>
<summary><strong>Alternative: Install locally with pip</strong></summary>

```bash
pip install pyp6xer-mcp
```

Then configure Claude Desktop:

```json
{
  "mcpServers": {
    "pyp6xer": {
      "command": "pyp6xer-mcp"
    }
  }
}
```

</details>

<details>
<summary><strong>Alternative: Run via Docker</strong></summary>

```bash
docker compose up
```

Then point Claude Desktop to the HTTP endpoint:

```json
{
  "mcpServers": {
    "pyp6xer": {
      "url": "http://localhost:5000/mcp"
    }
  }
}
```

</details>

---

## What Can It Do?

### 📊 Schedule Analysis
```
"What's on the critical path?"
"Show me activities with negative float"
"Run a DCMA 14-point schedule health check"
"Which activities are slipping?"
```

### 📈 Progress & Performance
```
"What's the current progress summary?"
"Calculate earned value metrics (SPI, CPI)"
"Show me work package status by responsible manager"
"Compare baseline to actual performance"
```

### 🔍 Resource Management
```
"List all resources and their assignments"
"Show me resource utilization over time"
"Which resources are over-allocated?"
```

### 📁 Data Export
```
"Export the critical path to CSV"
"Generate an executive summary report"
"Export schedule dashboard for Excel"
```

**22 tools** • **5 workflow prompts** • **3 data resources** — See [TOOLS.md](TOOLS.md) for complete reference.

---

## Installation Methods

### Method 1: uvx (Recommended)
No installation needed! Just add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pyp6xer": {
      "command": "uvx",
      "args": ["pyp6xer-mcp"]
    }
  }
}
```

### Method 2: pip
```bash
pip install pyp6xer-mcp
```

### Method 3: Docker
```bash
# Clone repo
git clone <repo-url>
cd pyp6xer_mcp

# One-command setup
docker compose up
```

### Method 4: From Source (Developers)
```bash
# Clone repo
git clone <repo-url>
cd pyp6xer_mcp

# Install with uv
uv pip install -e .

# Run tests
pytest
```

---

## Example Workflows

### 🎯 Critical Path Analysis

**You:** "Load the file at `/Users/me/Desktop/Q1_Project.xer` and show me the critical path"

**Claude:**
- Loads the XER file
- Identifies critical activities
- Shows duration, dates, and relationships
- Highlights longest path through the network

### 🏥 Schedule Health Check

**You:** "Run a schedule health check on the loaded project"

**Claude:**
- Checks for DCMA 14-point compliance
- Identifies missing logic, constraints, lags
- Flags activities with high/negative float
- Provides recommendations

### 📊 Progress Dashboard

**You:** "Generate a progress summary and export to CSV"

**Claude:**
- Calculates percent complete by project, WBS, activity
- Shows planned vs actual dates
- Exports formatted CSV for Excel pivot tables

### 🔄 Baseline Comparison

**You:** "Compare baseline to actual and identify variances"

**Claude:**
- Compares planned vs actual start/finish dates
- Calculates schedule variance
- Identifies slipping activities
- Recommends corrective actions

### 💼 Executive Summary

**You:** "Create an executive summary for the steering committee"

**Claude:**
- Overall project status (on track, at risk, behind)
- Key milestones and dates
- Critical path activities
- Resource concerns
- Recommendations

---

## Configuration

### Claude Desktop Config Location

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

**Linux:** `~/.config/Claude/claude_desktop_config.json`

### Environment Variables

Create a `.env` file for local development:

```bash
# Optional: API key for HTTP mode
API_KEY=your_secret_key_here

# Optional: Port (defaults to 5000)
PORT=5000
```

---

## Running as HTTP Server

For remote access or web UI integration:

```bash
# Without auth (development only!)
python -m pyp6xer_mcp.cli streamable-http

# With auth (production)
API_KEY=your_secret_key python -m pyp6xer_mcp.cli streamable-http
```

**Live deployment:** https://pyp6xer-mcp.fly.dev/mcp

### Upload Files via HTTP

```bash
curl -X POST -H "Authorization: Bearer <api_key>" \
  -F "file=@project.xer" \
  https://pyp6xer-mcp.fly.dev/upload
```

Response:
```json
{
  "cache_key": "abc123",
  "projects": [...],
  "activity_count": 250,
  "message": "XER loaded. Use cache_key 'abc123' with MCP tools."
}
```

---

## Troubleshooting

### "Server not found" in Claude Desktop

1. Check that `claude_desktop_config.json` is in the correct location
2. Ensure JSON is valid (no trailing commas)
3. Restart Claude Desktop completely (Quit, not just close window)
4. Check Claude Desktop logs:
   - **macOS:** `~/Library/Logs/Claude/mcp*.log`
   - **Windows:** `%APPDATA%\Claude\logs\mcp*.log`

### "ModuleNotFoundError: No module named 'pyp6xer_mcp'"

Using `uvx`? No action needed — it auto-installs.

Using `pip`? Run:
```bash
pip install pyp6xer-mcp
```

### "Failed to parse XER file"

- Ensure file is valid P6 XER format (not XML, not .xls)
- Try opening in P6 to verify file integrity
- Check file size (very large files may timeout)

### Permission Denied

```bash
# macOS/Linux: Grant file access
chmod +r /path/to/file.xer

# Or move file to accessible location
mv /restricted/path/file.xer ~/Desktop/
```

---

## Architecture

### Package Structure

```
pyp6xer_mcp/
├── __init__.py           # Package entry point
├── server.py             # FastMCP server instance
├── cli.py                # CLI entry point
├── models/               # Pydantic input models
│   ├── common.py         # ResponseFormat, ExportType
│   ├── file_ops.py       # Load, write, export models
│   ├── activities.py     # Activity models
│   ├── analysis.py       # Analysis models
│   └── resources.py      # Resource models
├── core/                 # Core utilities
│   ├── cache.py          # XerCache (in-memory)
│   ├── formatters.py     # Format functions
│   └── helpers.py        # Helper functions
├── tools/                # 22 MCP tools
│   ├── file_ops.py       # load, write, export, clear
│   ├── projects.py       # list_projects
│   ├── activities.py     # list, get, search, update
│   ├── analysis.py       # critical_path, float, quality
│   ├── resources.py      # list_resources, utilization
│   ├── progress.py       # progress, earned_value
│   └── calendars.py      # list_calendars
├── prompts/              # 5 workflow prompts
│   └── analysis.py       # Preset workflows
├── resources/            # 3 MCP resources
│   └── schedule.py       # Direct data access
└── http/                 # HTTP layer
    ├── middleware.py     # Auth middleware
    └── routes.py         # Health, upload endpoints
```

### Tool Categories

| Category | Count | Tools |
|----------|-------|-------|
| **File Operations** | 4 | `load_file`, `write_file`, `clear_cache`, `export_csv` |
| **Project/Activity** | 5 | `list_projects`, `list_activities`, `get_activity`, `search_activities`, `update_activity` |
| **Schedule Analysis** | 6 | `critical_path`, `float_analysis`, `schedule_quality`, `relationship_analysis`, `slipping_activities`, `schedule_health_check` |
| **Resource Management** | 2 | `list_resources`, `resource_utilization` |
| **Progress/Performance** | 4 | `progress_summary`, `earned_value`, `work_package_summary`, `wbs_analysis` |
| **Structure** | 1 | `list_calendars` |

See [TOOLS.md](TOOLS.md) for complete documentation.

---

## Development

### Run Tests

```bash
# All tests (27 tests)
pytest

# With coverage
pytest --cov=pyp6xer_mcp

# Specific test file
pytest tests/test_modular_structure.py -v
```

### Linting & Formatting

```bash
black --line-length 100 .
ruff check .
mypy .
```

### Build & Publish

```bash
# Build package
python -m build

# Publish to PyPI
python -m twine upload dist/*
```

---

## Requirements

- **Python:** 3.10+
- **Dependencies:**
  - `mcp>=1.0.0` - MCP protocol
  - `pydantic>=2.0.0` - Input validation
  - `PyP6XER>=0.1.0` - XER parsing
  - `httpx>=0.24.0` - HTTP client
  - `uvicorn>=0.23.0` - ASGI server

---

## Need Help?

### 💼 Consulting Services

Need custom schedule analysis, integration, or P6 automation?

**Contact:** [Your consulting page/email]

**Services:**
- Custom MCP tool development
- P6 schedule optimization
- Integration with project management systems
- Training and workshops

**Minimum engagement:** $800

### 🐛 Bug Reports & Feature Requests

Open an issue on [GitHub Issues](#) (coming soon)

### 📚 Documentation

- **[TOOLS.md](TOOLS.md)** - Complete tool reference
- **[CLAUDE.md](CLAUDE.md)** - Developer documentation
- **[Model Context Protocol Docs](https://modelcontextprotocol.io/)**

---

## License

MIT License - see [LICENSE](LICENSE) for details.

Free for commercial and personal use. No attribution required.

---

## Acknowledgments

- [PyP6Xer](https://github.com/HassanEmam/PyP6Xer) by Hassan Emam - XER parsing library
- [Model Context Protocol](https://modelcontextprotocol.io/) by Anthropic - Protocol specification
- [FastMCP](https://github.com/jlowin/fastmcp) - Python MCP framework
