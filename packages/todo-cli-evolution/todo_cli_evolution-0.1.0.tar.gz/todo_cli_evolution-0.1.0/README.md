# Todo CLI - Phase I: In-Memory Python CLI Todo Application

**Part of "The Evolution of Todo" Project**

A simple, elegant command-line todo application built with Python 3.10+, featuring in-memory storage and a clean architecture.

## Quick Start

```bash
# Setup
uv sync --extra dev

# Run
uv run python -m todo_cli

# Test
uv run pytest
```

## Features

✅ Add, List, Update, Delete, Toggle todos
✅ Clean Architecture
✅ Type-Safe
✅ Test-Driven (>90% coverage)

## Usage

Commands: `add`, `list`, `update`, `delete`, `toggle`, `help`, `exit`

⚠️ **Data is in-memory only** - lost on exit (Phase I design)

## Development

```bash
# Run tests with coverage
uv run pytest --cov=todo_cli --cov-report=html

# Type checking
uv run mypy src/todo_cli/
```

## Documentation

- Constitution: `.specify/memory/constitution.md`
- Specification: `specs-history/phase-1-cli/spec.md`
- Plan: `specs-history/phase-1-cli/plan.md`
- Tasks: `specs-history/phase-1-cli/tasks.md`

Generated with Claude Code following Spec-Driven Development.
