# Effective Harnesses for Long-Running Agents

**Source:** https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
**Published:** November 26, 2025
**Author:** Justin Young

## Overview

Anthropic's research addresses a critical challenge in AI agent development: getting agents to make consistent progress across multiple context windows remains an open problem. The team developed a solution featuring an **initializer agent** and **coding agent** architecture to enable Claude to work effectively on extended projects that span multiple sessions.

## The Core Problem

Long-running agents face a fundamental limitation: each new session begins without memory of previous work. As the article notes, "each new session begins with no memory of what came before."

The authors use an apt analogy: imagine engineers working shifts where each newcomer has no knowledge of the previous shift's work.

### Failure Patterns

**Pattern 1 - "One-shotting" (Over-ambition):**
- Claude attempted to complete entire applications simultaneously
- Agents exhausted context windows mid-implementation
- Features were left half-built and undocumented

**Pattern 2 - Premature Completion:**
- Later agent instances observed partial progress
- Agents declared projects finished despite incomplete features
- Work was abandoned before reaching production quality

## Two-Part Solution Architecture

### 1. Initializer Agent

The first session establishes the development environment and tracking infrastructure:

**Key Artifacts Created:**
- **`init.sh` script** - For running the development server
- **`claude-progress.txt` file** - Tracking agent activities across sessions
- **Initial git commit** - Documenting baseline file additions
- **Comprehensive feature list** - All end-to-end features marked as "failing"

### 2. Coding Agent

Subsequent sessions follow these directives:
- Work on a **single feature per session**
- Make **incremental progress**
- Leave **clean, production-ready code** suitable for merging
- Commit changes with **descriptive messages**
- Update **progress documentation**

## Environment Management Strategies

### Feature Lists in JSON Format

The team chose JSON specifically because "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files."

**Feature Structure Example:**

```json
{
    "category": "functional",
    "description": "New chat button creates a fresh conversation",
    "steps": [
      "Navigate to main interface",
      "Click the 'New Chat' button",
      "Verify a new conversation is created",
      "Check that chat area shows welcome state",
      "Verify conversation appears in sidebar"
    ],
    "passes": false
}
```

### Testing Framework and Browser Automation

**Improved Approach (Puppeteer):**
- Prompted to use **Puppeteer MCP** for browser automation
- Agents performed testing as a human user would
- Included screenshot capture during testing

**Remaining Limitations:**
- "Claude can't see browser-native alert modals through the Puppeteer MCP"
- Vision-based bugs remain difficult to detect

## Session Workflow Pattern

Each coding session follows a structured sequence:

```
[Assistant] I'll start by getting my bearings and understanding the
current state of the project.
[Tool Use] <bash - pwd>
[Tool Use] <read - claude-progress.txt>
[Tool Use] <read - feature_list.json>
[Assistant] Let me check the git log to see recent work.
[Tool Use] <bash - git log --oneline -20>
[Assistant] Now let me check if there's an init.sh script to restart
the servers.
<Starts the development server>
```

### Detailed Session Steps:

1. **Environment Check**: Run `pwd` to confirm working directory
2. **Context Gathering**: Review git logs and progress files
3. **Feature Selection**: Consult feature list to identify highest-priority incomplete feature
4. **Server Initialization**: Start development server via `init.sh`
5. **Basic Verification**: Conduct end-to-end testing of existing functionality
6. **Feature Implementation**: Work on selected single feature
7. **Documentation**: Commit changes with descriptive messages and update progress

## Prompt Engineering and Constraints

The research employed strongly-worded instructions: "we use strongly-worded instructions like 'It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality.'"

### Coding Agent Constraints:
- Must work on exactly one feature per session
- Cannot skip or delete tests
- Required to update progress documentation
- Must commit working code with descriptive messages
- Must verify features through end-to-end testing

## Technical Implementation

- **Model**: Claude Opus 4.5
- **Infrastructure**: Claude Agent SDK
- **Tools**: Puppeteer MCP, Git, Bash

## Key Insight

Success required borrowing practices from effective human software engineers:
- **Clear documentation** - Progress files and commit messages
- **Incremental progress tracking** - Feature lists and status
- **Deliberate session handoffs** - Structured startup sequences
- **Comprehensive testing** - End-to-end verification with browser automation

## Remaining Challenges

1. **Multi-Agent Architecture**: Would specialized agents (testing, QA, cleanup) outperform a single general-purpose coding agent?
2. **Generalization**: Can these approaches extend beyond web development?
3. **Vision-Based Testing**: How to improve detection of visual bugs?

## Core Files and Artifacts

- **`init.sh`** - Script for running the development server
- **`claude-progress.txt`** - Log tracking agent work across sessions
- **`feature_list.json`** - Structured requirements with pass/fail status
- **Git repository** - Version history with descriptive commit messages
