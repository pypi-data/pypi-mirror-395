# Sample XER Files

This directory contains sample Primavera P6 XER files for testing and demonstration purposes.

## Usage

### With Docker Compose
Sample files are automatically mounted to `/samples` in the container:

```bash
docker compose up
# Files available at /samples/*.xer inside the container
```

### With Claude Desktop
Tell Claude to load sample files from this directory:

```
"Load the sample project at samples/demo.xer and show me the critical path"
```

## Adding Your Own Samples

1. Place XER files in this directory
2. Ensure they don't contain sensitive project data
3. Keep files small (<1MB) for faster loading
4. Use descriptive filenames (e.g., `construction_sample.xer`, `it_project_demo.xer`)

## Gitignore

By default, `*.xer` files are gitignored to prevent accidentally committing client data. To commit sample files, add them explicitly:

```bash
git add -f samples/your_sample.xer
```

Or update `.gitignore` to allow samples:

```gitignore
# XER files (may contain client data)
*.xer
!samples/*.xer  # Allow sample files
```

## Sample File Requirements

Good sample files should:
- Be realistic but anonymized
- Include 50-200 activities (enough to be useful, not too large)
- Have a mix of activity types (critical, near-critical, non-critical)
- Include resources and calendars
- Show typical scheduling patterns
