# PyP6Xer MCP Tools Reference

Complete reference for all 22 MCP tools provided by the PyP6Xer MCP Server.

## Quick Reference

| Category | Tools |
|----------|-------|
| File Operations | 4 tools |
| Project/Activity | 5 tools |
| Schedule Analysis | 6 tools |
| Resource Management | 2 tools |
| Progress/Performance | 4 tools |
| Structure | 1 tool |

---

## File Operations (4 tools)

### pyp6xer_load_file

Load and parse a Primavera P6 XER file.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| file_path | string | No* | Path to XER file (local or URL) |
| file_content | string | No* | Base64-encoded XER file content |
| cache_key | string | No | Key for referencing this file |

*Either `file_path` or `file_content` is required.

**Example:**
```json
{"file_path": "/data/project.xer", "cache_key": "main"}
```

---

### pyp6xer_write_file

Write the (modified) XER data to a new file.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| output_path | string | Yes | Destination file path |

---

### pyp6xer_clear_cache

Clear cached XER data.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | No | Specific key to clear (omit for all) |

---

### pyp6xer_export_csv

Export XER data to CSV file for Excel analysis.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| output_path | string | Yes | Destination CSV path |
| export_type | string | No | Type: activities, critical_path, float_analysis, resources, wbs, schedule_quality |
| project_id | string | No | Filter by project |
| status_filter | string | No | Filter by status |

---

## Project/Activity Management (5 tools)

### pyp6xer_list_projects

List all projects in the loaded XER file.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| response_format | string | No | markdown (default) or json |

---

### pyp6xer_list_activities

List activities/tasks with optional filtering.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| project_id | string | No | Filter by project |
| status_filter | string | No | TK_Complete, TK_Active, TK_NotStarted, or all |
| wbs_id | string | No | Filter by WBS element |
| limit | integer | No | Max results (default: 50) |
| offset | integer | No | Skip N results |
| response_format | string | No | markdown or json |

---

### pyp6xer_get_activity

Get detailed information about a specific activity.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| activity_code | string | Yes | Activity code to look up |
| response_format | string | No | markdown or json |

---

### pyp6xer_search_activities

Search for activities by code or name.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| search_term | string | Yes | Text to search for |
| project_id | string | No | Filter by project |
| limit | integer | No | Max results (default: 50) |
| response_format | string | No | markdown or json |

---

### pyp6xer_update_activity

Update an activity's properties.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| activity_code | string | Yes | Activity code to update |
| phys_complete_pct | number | No | Physical completion (0-100) |
| status_code | string | No | TK_Complete, TK_Active, TK_NotStarted |

---

## Schedule Analysis (6 tools)

### pyp6xer_critical_path

Identify critical path activities (zero or negative float).

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| project_id | string | No | Filter by project |
| float_threshold_hours | integer | No | Critical threshold (default: 0) |
| response_format | string | No | markdown or json |

---

### pyp6xer_float_analysis

Analyze float distribution across activities.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| project_id | string | No | Filter by project |
| float_categories | array | No | Custom thresholds (default: [0, 5, 10, 20, 40]) |
| response_format | string | No | markdown or json |

---

### pyp6xer_schedule_quality

Perform schedule quality checks to identify potential issues.

**Checks performed:**
- Activities without predecessors
- Activities without successors
- Long duration activities
- Activities with constraints
- Negative float

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| project_id | string | No | Filter by project |
| max_duration_days | integer | No | Flag activities > N days (default: 20) |
| response_format | string | No | markdown or json |

---

### pyp6xer_relationship_analysis

Analyze activity relationships and dependencies.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| project_id | string | No | Filter by project |
| relationship_type | string | No | PR_FS, PR_SS, PR_FF, PR_SF |
| response_format | string | No | markdown or json |

---

### pyp6xer_slipping_activities

Identify activities where forecast finish dates are slipping beyond baseline.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| project_id | string | No | Filter by project |
| threshold_days | number | No | Only show slip > N days |
| include_completed | boolean | No | Include completed activities |
| limit | integer | No | Max results (default: 50) |
| response_format | string | No | markdown or json |

---

### pyp6xer_schedule_health_check

Perform a comprehensive schedule health assessment.

Returns an overall health score (0-100) with breakdown of:
- Completion status
- Float distribution
- Logic gaps
- Slipping activities

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| project_id | string | No | Filter by project |
| response_format | string | No | markdown or json |

---

## Resource Management (2 tools)

### pyp6xer_list_resources

List all resources in the XER file.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| response_format | string | No | markdown or json |

---

### pyp6xer_resource_utilization

Analyze resource utilization and find potential overallocations.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| resource_type | string | No | RT_Labor, RT_Mat, RT_Equip |
| response_format | string | No | markdown or json |

---

## Progress/Performance (4 tools)

### pyp6xer_progress_summary

Get a summary of project progress including completion rates.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| project_id | string | No | Filter by project |
| response_format | string | No | markdown or json |

---

### pyp6xer_earned_value

Calculate Earned Value Management (EVM) metrics.

**Metrics calculated:**
- Planned Value (PV/BCWS)
- Earned Value (EV/BCWP)
- Actual Cost (AC/ACWP)
- Cost Performance Index (CPI)
- Schedule Performance Index (SPI)
- Cost Variance (CV)
- Schedule Variance (SV)

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| project_id | string | No | Filter by project |
| response_format | string | No | markdown or json |

---

### pyp6xer_work_package_summary

Summarize activities grouped by activity code prefix (work packages).

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| prefix_list | array | Yes | Prefixes to group by (e.g., ["KH-", "MoS-"]) |
| project_id | string | No | Filter by project |
| include_unmatched | boolean | No | Include "Other" category |
| response_format | string | No | markdown or json |

---

### pyp6xer_wbs_analysis

Analyze the Work Breakdown Structure hierarchy.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| project_id | string | No | Filter by project |
| max_depth | integer | No | Max depth to traverse (default: 10) |
| response_format | string | No | markdown or json |

---

## Structure (1 tool)

### pyp6xer_list_calendars

List calendars in the XER file.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cache_key | string | Yes | Cache key of loaded XER |
| calendar_id | string | No | Get details for specific calendar |
| response_format | string | No | markdown or json |

---

## MCP Prompts (5)

Pre-configured analysis workflows:

| Prompt | Description |
|--------|-------------|
| `analyze_critical_path` | Critical path analysis workflow |
| `export_schedule_dashboard` | Export data to CSV for Excel |
| `compare_baseline_to_actual` | Baseline vs actual comparison |
| `identify_schedule_quality_issues` | DCMA-style quality checks |
| `generate_executive_summary` | Executive briefing |

---

## MCP Resources (3)

Direct data access URIs:

| Resource | Description |
|----------|-------------|
| `schedule://projects` | List all loaded projects |
| `schedule://{cache_key}/summary` | Schedule summary |
| `schedule://{cache_key}/critical` | Critical activities (top 50) |
