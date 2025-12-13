# Agent Instructions for extended-data-types

## Overview

Extended data type utilities for Python.

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
- `feat(edt): new feature` → minor
- `fix(edt): bug fix` → patch

## Important Notes

- Use absolute imports (`from extended_data_types...`)
- Include `from __future__ import annotations`
- Type hints required
