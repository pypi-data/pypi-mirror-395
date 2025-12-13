# Code Execution with MCP: Building More Efficient Agents

**Source:** https://www.anthropic.com/engineering/code-execution-with-mcp
**Published:** November 4, 2025
**Authors:** Adam Jones and Conor Kelly

## Summary

"Direct tool calls consume context for each definition and result. Agents scale better by writing code to call tools instead."

## Introduction

The Model Context Protocol (MCP) is an open standard for connecting AI agents to external systems. Since its November 2024 launch, adoption has been rapid with thousands of community-built MCP servers and SDKs available across major programming languages.

However, as developers connect agents to hundreds or thousands of tools across multiple servers, two efficiency problems emerge: tool definitions overload the context window, and intermediate results consume excessive tokens.

## Problem 1: Tool Definitions Overload Context

Most MCP clients load all tool definitions upfront directly into the model's context. These definitions occupy significant space, increasing latency and costs. When agents connect to thousands of tools, they process hundreds of thousands of tokens before even reading a user request.

## Problem 2: Intermediate Results Consume Tokens

When agents call MCP tools sequentially, every intermediate result must pass through the model. For example, retrieving a meeting transcript and attaching it to a Salesforce record means the full transcript flows through twice—potentially adding 50,000 tokens for a two-hour meeting.

## Solution: Code Execution with MCP

Rather than direct tool calls, agents can write code that interacts with MCP servers. This approach allows agents to:

- Load only needed tool definitions on demand
- Process data in the execution environment before returning results
- Reduce token usage by up to 98.7% compared to traditional approaches

### Implementation Structure

Tools can be organized as a filesystem:

```
servers/
├── google-drive/
│   ├── getDocument.ts
│   └── index.ts
├── salesforce/
│   ├── updateRecord.ts
│   └── index.ts
```

Agents discover tools by exploring the filesystem and read only necessary definitions. The Google Drive to Salesforce example reduces token consumption from 150,000 to 2,000 tokens.

## Key Benefits

### Progressive Disclosure
Models excel at navigating filesystems. Tools presented as code can be read on-demand rather than loaded upfront. A `search_tools` function with detail-level parameters helps agents find and load tools efficiently.

### Context-Efficient Results
Agents filter and transform large datasets in code before returning them to the model. Processing a 10,000-row spreadsheet becomes returning only relevant rows.

### Powerful Control Flow
Loops, conditionals, and error handling use familiar programming patterns instead of chaining individual tool calls, improving efficiency and reducing "time to first token" latency.

### Privacy-Preserving Operations
Intermediate results remain in the execution environment by default. Agents only see explicitly logged data. For sensitive information, the MCP client can tokenize personally identifiable information automatically before it reaches the model, enabling secure data flows between systems.

### State Persistence and Skills
Agents can write intermediate results to files, resuming work and tracking progress. They can also save working code as reusable functions, gradually building higher-level capabilities.

## Important Considerations

Code execution introduces operational complexity. Running agent-generated code requires secure sandboxing, resource limits, and monitoring infrastructure. These requirements add overhead and security considerations that direct tool calls avoid. Benefits of reduced costs and latency must be weighed against implementation costs.

## Conclusion

MCP provides a foundational protocol for agent connectivity, but scaling to many servers causes token inefficiency. Code execution applies proven software engineering patterns to agents, enabling them to interact with MCP servers more efficiently using familiar programming constructs.
