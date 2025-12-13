# Agent Instructions for lifecyclelogging

## Overview

Lifecycle-aware logging utilities for Python.

## Before Starting

```bash
cat memory-bank/activeContext.md
```

## Development Commands

```bash
# Install dependencies
uv sync --extra tests

# Run tests
uv run pytest tests/ -v

# Lint
uvx ruff check src/ tests/
uvx ruff format src/ tests/

# Build
uv build
```

## Commit Messages

Use conventional commits:
- `feat(logging): new feature` → minor
- `fix(logging): bug fix` → patch

## Important Notes

- Use absolute imports (`from lifecyclelogging...`)
- Include `from __future__ import annotations`
- Type hints required
