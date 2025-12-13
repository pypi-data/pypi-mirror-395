# Effective Context Engineering for AI Agents

**Source:** https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
**Published:** September 29, 2025
**Authors:** Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, Jeremy Hadfield

## Overview

Context represents a finite resource for AI agents. This article explores strategies for curating and managing context effectively to build capable, steerable agents.

## Key Concepts

### Context Engineering vs. Prompt Engineering

Context engineering represents the evolution beyond prompt engineering. While "prompt engineering refers to methods for writing and organizing LLM instructions," context engineering addresses "the set of strategies for curating and maintaining the optimal set of tokens during LLM inference."

The distinction matters: prompt engineering focuses on discrete task optimization, while context engineering is iterative—curation happens each time information passes to the model.

### Why Context Matters

LLMs experience performance degradation as context grows—a phenomenon called context rot. Studies show that "as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases."

This stems from transformer architecture: every token attends to every other token, creating n² pairwise relationships. Longer sequences stretch this attention budget thin, creating diminished precision for information retrieval and long-range reasoning.

## Anatomy of Effective Context

### System Prompts

Effective system prompts strike the "right altitude"—specific enough to guide behavior without brittle hardcoding, yet flexible enough to provide strong heuristics. They should:

- Use simple, direct language
- Organize into distinct sections (`<background_information>`, `<instructions>`, etc.)
- Provide the minimal set of information needed
- Start minimal and add based on failure modes

### Tools

Well-designed tools should be:

- Self-contained and robust to error
- Extremely clear regarding intended use
- Non-overlapping in functionality
- Token-efficient in return values

Bloated tool sets create ambiguity about which tool to use and waste context on unclear decision points.

### Examples

Few-shot prompting remains valuable, but avoid stuffing edge cases into prompts. Instead, "curate a set of diverse, canonical examples that effectively portray the expected behavior of the agent."

## Context Retrieval and Agentic Search

### Just-in-Time Strategies

Rather than pre-loading all relevant data, agents can maintain lightweight identifiers (file paths, web links, queries) and dynamically load data at runtime using tools. This approach:

- Mirrors human cognition
- Enables progressive disclosure of context
- Reduces context window pollution
- Leverages metadata (file structure, naming conventions, timestamps) as signals

### Hybrid Approaches

The most effective agents may combine upfront retrieval for speed with autonomous exploration. Claude Code exemplifies this: CLAUDE.md files load initially while tools like grep enable just-in-time file retrieval.

## Long-Horizon Context Management

For tasks spanning hours—like codebase migrations or research projects—three techniques address context limitations:

### Compaction

Summarizing conversation history and restarting with compressed context. The art lies in selecting what to preserve (architectural decisions, unresolved bugs) versus discard (redundant tool outputs). Start by maximizing recall, then improve precision.

### Structured Note-Taking

Agents maintain external memory (NOTES.md files, to-do lists) outside the context window, pulling relevant notes back when needed. Claude playing Pokémon demonstrates this: the agent tracked thousands of steps—"for the last 1,234 steps I've been training my Pokémon in Route 1, Pikachu has gained 8 levels toward the target of 10."

Anthropic released a memory tool in public beta enabling file-based external knowledge management.

### Sub-Agent Architectures

Specialized sub-agents handle focused tasks with clean context windows, returning condensed summaries (1,000-2,000 tokens) to a coordinating agent. This separates detailed search context from synthesis work.

## Guiding Principle

The overarching principle remains: "find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome." As models improve, less prescriptive engineering becomes necessary, but treating context as precious and finite stays central to building reliable agents.

## Practical Recommendations

- Start with minimal prompts using the best available model
- Design tools for clarity and token efficiency
- Enable just-in-time context retrieval where possible
- Implement compaction for extended interactions
- Use external memory for complex, multi-step tasks
