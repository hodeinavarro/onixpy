# pyonix Development Guide

## Project Overview
Python library for parsing and working with ONIX for Books metadata (publishing industry standard). Built with Pydantic for type-safe data models.

## Architecture & Structure
- **Package**: `onix` (installed from `src/onix/`)
- **Core dependency**: Pydantic ≥2.12.5 for data validation and serialization
- **Type checking**: `py.typed` marker enables type checking in consuming projects
- **Python version**: 3.10+ required

## Development Workflow

### Environment Setup
```bash
# Project uses uv for dependency management (uv.lock is gitignored)
uv sync
```

### Testing
```bash
# Run tests with pytest
uv run pytest

# Test markers available:
# - @pytest.mark.slow - for slower tests
# - @pytest.mark.integration - for integration tests
```

### Code Quality
```bash
# Format and lint with ruff
uv run ruff check .
uv run ruff format .
```

## Project Conventions

### Test Structure
- Test files: `test_*.py` in `tests/` directory
- Test classes: `Test*` prefix
- Test functions: `test_*` prefix
- Use pytest markers (`@pytest.mark.slow`, `@pytest.mark.integration`) for test categorization

### Type Safety
- All public APIs should have type annotations
- `py.typed` marker ensures consumers get type checking support
- Pydantic models should be used for ONIX data structures

### File Organization
- Source code: `src/onix/`
- Tests mirror source structure in `tests/`
- ONIX specification files are gitignored (`*Specification_*.md`, `*Specification_*.pdf`)

## Key Files
- [pyproject.toml](../pyproject.toml) - Project metadata, dependencies, and tool configuration
- [src/onix/__init__.py](../src/onix/__init__.py) - Package public API exports
- [.python-version](../.python-version) - Python 3.10 requirement for version managers

## Collaboration Notes
- User is new to Pydantic: offer quick guidance (e.g., derive models from `pydantic.BaseModel`, use type hints for fields, leverage `model_validate`/`model_dump` for IO) and propose minimal examples before larger changes.
- If the user’s intent seems inconsistent with ONIX or Python best practices, pause, explain the concern, and ask if they want to proceed anyway.
- Confirm assumptions explicitly; do not proceed on contested points without user acknowledgement.
