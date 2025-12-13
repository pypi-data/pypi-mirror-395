# Advanced Tool Use on the Claude Developer Platform

**Source:** https://www.anthropic.com/engineering/advanced-tool-use
**Published:** November 24, 2025
**Author:** Bin Wu

## Overview

Anthropic has released three beta features enabling Claude to dynamically discover, learn, and execute tools more efficiently. These capabilities address fundamental constraints in building sophisticated AI agents that work across hundreds of tools simultaneously.

## The Core Problem

Traditional approaches to tool use create scalability bottlenecks. Tool definitions consume significant context—a five-server setup with 58 tools can require approximately 55K tokens before any work begins. Additionally, agents struggle with correct tool selection and parameter handling when working with extensive tool libraries.

## Three New Features

### 1. Tool Search Tool

**Purpose:** Enable Claude to discover tools on-demand rather than loading all definitions upfront.

**Key Benefits:**
- Reduces token consumption by 85% compared to traditional approaches
- Improves accuracy significantly (Opus 4: 49% to 74%; Opus 4.5: 79.5% to 88.1%)
- Preserves 95% of the context window while maintaining access to complete tool libraries

**Implementation:**
Mark tools with `defer_loading: true` to make them discoverable.

```json
{
  "tools": [
    {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
    {
      "name": "github.createPullRequest",
      "defer_loading": true
    }
  ]
}
```

**When to Use:**
- Tool definitions exceed 10K tokens
- Working with 10+ tools
- Experiencing tool selection accuracy issues

### 2. Programmatic Tool Calling

**Purpose:** Allow Claude to orchestrate tools through code execution rather than sequential API calls.

**Key Benefits:**
- Reduces token consumption by 37% on complex tasks
- Eliminates multiple inference passes by batching tool calls
- Improves accuracy through explicit orchestration logic

**How It Works:**
Claude writes Python code that calls multiple tools, processes results, and controls what enters its context.

```python
team = await get_team_members("engineering")
levels = list(set(m["level"] for m in team))
budget_results = await asyncio.gather(*[
    get_budget_by_level(level) for level in levels
])
budgets = {level: budget for level, budget in zip(levels, budget_results)}
expenses = await asyncio.gather(*[
    get_expenses(m["id"], "Q3") for m in team
])
exceeded = []
for member, exp in zip(team, expenses):
    budget = budgets[member["level"]]
    total = sum(e["amount"] for e in exp)
    if total > budget["travel_limit"]:
        exceeded.append({
            "name": member["name"],
            "spent": total,
            "limit": budget["travel_limit"]
        })
print(json.dumps(exceeded))
```

**When to Use:**
- Processing large datasets for aggregates/summaries
- Multi-step workflows with 3+ dependent tool calls
- Parallel operations across many items
- Tasks where intermediate data shouldn't influence reasoning

### 3. Tool Use Examples

**Purpose:** Provide concrete usage patterns beyond what JSON schemas express.

**Key Benefits:**
- Improved accuracy from 72% to 90% on complex parameter handling
- Clarifies format conventions, nested structures, and parameter correlations

**Example:**
```json
{
  "name": "create_ticket",
  "input_schema": { /* schema */ },
  "input_examples": [
    {
      "title": "Login page returns 500 error",
      "priority": "critical",
      "labels": ["bug", "authentication", "production"],
      "reporter": {
        "id": "USR-12345",
        "name": "Jane Smith"
      },
      "due_date": "2024-11-06",
      "escalation": {
        "level": 2,
        "notify_manager": true,
        "sla_hours": 4
      }
    }
  ]
}
```

**When to Use:**
- Complex nested structures with context-dependent patterns
- Tools with many optional parameters
- APIs with domain-specific conventions
- Similar tools needing clarification

## Best Practices

**Layer Features Strategically:** Address the biggest bottleneck first:
- Context bloat → Tool Search Tool
- Large intermediate results → Programmatic Tool Calling
- Parameter errors → Tool Use Examples

**Tool Search Setup:** Use clear, descriptive definitions. Keep 3-5 most-used tools always loaded, defer the rest.

**Programmatic Calling:** Document return formats clearly so Claude writes correct parsing logic.

**Tool Examples:** Keep realistic, minimal data (1-5 examples per tool). Focus on ambiguous cases.

## Getting Started

Enable via beta header:
```python
client.beta.messages.create(
    betas=["advanced-tool-use-2025-11-20"],
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    tools=[
        {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
        {"type": "code_execution_20250825", "name": "code_execution"},
    ]
)
```

## Resources

- Tool Search Tool: Documentation and cookbook
- Programmatic Tool Calling: Documentation and cookbook
- Tool Use Examples: Documentation
