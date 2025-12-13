# Agent Instructions for vendor-connectors

## Overview

Universal vendor connectors including Meshy AI for 3D asset generation.

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

## Meshy AI Usage

```python
from vendor_connectors import meshy

# Generate 3D model
model = meshy.text3d.generate("a medieval sword")

# Rig for animation
rigged = meshy.rigging.rig(model.id)

# Apply animation
animated = meshy.animate.apply(rigged.id, animation_id=0)
```

## Commit Messages

Use conventional commits:
- `feat(aws): new AWS feature` → minor
- `feat(meshy): Meshy feature` → minor
- `fix(connector): bug fix` → patch

## Important Notes

- Python 3.10+ required (crewai dependency)
- Meshy was merged from mesh-toolkit
- All agent tool integrations in meshy.agent_tools
