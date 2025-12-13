# Development Guidelines

## Core Philosophy

Write clean, tested, production-ready code. No shortcuts, no placeholders.

## Development Flow

1. **Read the requirements** from specs or issues
2. **Write tests first** (TDD approach)
3. **Implement the feature** completely
4. **Run linting**: `uvx ruff check src/ tests/`
5. **Run tests**: `uv run pytest tests/`
6. **Commit** with conventional commits

## Testing Commands

```bash
# Install dependencies
uv sync --extra tests

# Run tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src/ --cov-report=term-missing

# Linting
uvx ruff check src/ tests/
uvx ruff format src/ tests/

# Type checking
uvx mypy src/
```

## Commit Messages

Use conventional commits:
- `feat(scope): description` → minor bump
- `fix(scope): description` → patch bump
- `feat!: breaking change` → major bump

## Quality Standards

- ✅ All tests passing
- ✅ No linter errors
- ✅ Complete type annotations
- ✅ Proper error handling
- ❌ No TODOs or placeholders
- ❌ No shortcuts
