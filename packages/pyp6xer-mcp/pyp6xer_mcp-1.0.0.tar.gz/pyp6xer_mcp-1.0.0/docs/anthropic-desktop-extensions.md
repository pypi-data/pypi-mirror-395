# Claude Desktop Extensions: One-click MCP Server Installation

**Source:** https://www.anthropic.com/engineering/desktop-extensions
**Published:** 2025

## Overview

Anthropic has introduced Desktop Extensions (`.mcpb` files), a new packaging format that simplifies installing Model Context Protocol (MCP) servers. Previously, users faced significant barriers including the need for developer tools, manual JSON configuration, dependency management, and no discovery mechanism. The new system reduces installation to three steps: download, double-click, and install.

## Key Problems Addressed

The previous MCP installation process created friction through multiple requirements:

- Developer tools (Node.js, Python) needed beforehand
- Manual editing of configuration files required
- Package conflicts and version mismatches
- No built-in server discovery
- Manual reinstallation needed for updates

These obstacles made MCP servers inaccessible to non-technical users despite their powerful capabilities.

## Architecture

Desktop Extensions are ZIP archives containing:

- **manifest.json** (required) - Extension metadata and configuration
- **server/** directory - MCP server implementation
- **dependencies/** - All required packages
- **icon.png** (optional) - Extension icon

Claude Desktop handles complexity automatically with built-in Node.js runtime, automatic updates, and OS keychain storage for sensitive data.

## Minimal Manifest Structure

Every extension requires a manifest specifying:

- `mcpb_version` - Specification version
- `name` - Machine-readable identifier
- `version` - Semantic versioning
- `description` - Brief purpose statement
- `author` - Creator information (required field)
- `server` - Configuration details

Optional fields include homepage, documentation, screenshots, and compatibility specifications.

## User Configuration Handling

Developers can declare required inputs through the manifest. Claude Desktop automatically:

- Displays user-friendly configuration interfaces
- Validates inputs before enabling extensions
- Securely stores sensitive values
- Passes configuration as environment variables or arguments

Template literals enable dynamic values like `${__dirname}` and `${user_config.api_key}`.

## Development Process

### Step 1: Initialize Manifest
```bash
npx @anthropic-ai/mcpb init
```

### Step 2: Declare User Configuration
Define required inputs with types (string, directory, number) and constraints.

### Step 3: Package Extension
```bash
npx @anthropic-ai/mcpb pack
```

### Step 4: Test Locally
Drag the `.mcpb` file into Claude Desktop Settings to verify installation.

## Advanced Features

**Cross-platform support** allows platform-specific overrides for Windows, macOS, and Linux through configuration blocks.

**Template literals** provide runtime values including system paths and user inputs.

**Feature declaration** helps users understand capabilities through tools and prompts sections.

## Extension Directory

Anthropic provides a curated, built-in directory where users can browse and install extensions with one click, eliminating GitHub searches and code vetting.

## Open Ecosystem Commitment

Anthropic is open-sourcing:

- Complete MCPB specification
- Packaging and validation tools
- Reference implementation code
- TypeScript types and schemas

This approach enables developers to "package once, run anywhere," allows app developers to add extension support without building from scratch, and provides users with consistent experiences across MCP-enabled applications.

## Security and Enterprise Features

**For users:** Sensitive data remains in OS keychain with automatic updates and installation auditing.

**For enterprises:** Group Policy/MDM support, pre-installation of approved extensions, publisher blocklisting, directory disabling, and private extension deployment options.

## Getting Started

Developers should review documentation at the MCPB GitHub repository, then execute initialization and packaging commands locally. Desktop users should update Claude to access the Extensions section in Settings.

## File Extension Note

Extensions use `.mcpb` (MCP Bundle). Legacy `.dxt` extensions remain compatible, but developers should use `.mcpb` for new work.
