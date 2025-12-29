# pyonix Development Guide

## Project Overview
Python library for parsing and working with ONIX for Books metadata (publishing industry standard). Built with Pydantic for type-safe data models.

## Architecture & Structure

### Package Layout
```
src/onix/
├── __init__.py       # Public API: ONIXMessage, Header, Product, ONIXAttributes
├── message.py        # ONIXMessage, Header, ONIXAttributes models
├── product/
│   ├── __init__.py   # Exports Product
│   ├── base.py       # ProductBase with shared ONIX attributes
│   └── product.py    # Product model (will import blocks)
├── parsers/
│   ├── __init__.py   # Parser API: json_to_message, xml_to_message, etc.
│   ├── json.py       # JSON parsing/serialization
│   ├── xml.py        # XML parsing/serialization (lxml preferred)
│   └── tags.py       # Reference ↔ short tag name resolver
└── lists/
    ├── __init__.py   # Code list registry and lookup functions
    ├── models.py     # CodeList, CodeListEntry dataclasses
    └── list44.py     # List 44: Name identifier type
```

### Key Design Decisions
- **Reference names by default**: All parsers/serializers use ONIX reference tag names (e.g., `ONIXMessage`, `Header`). Short names (`ONIXmessage`, `header`, `x507`) require explicit `short_names=True`.
- **Tag mapping**: Minimal internal mapping in `parsers/tags.py`; will expand from ONIX spec later.
- **XML library**: Prefers `lxml` if available, falls back to stdlib `xml.etree`.
- **Code lists**: Placeholder in `onix.lists` with `get_list(n)` / `get_code(n, code)` API.

### Core Models
- `ONIXMessage`: Root container with `header`, `products`, `release`, optional `no_product`
- `Header`: Message metadata (sender, addressee) - placeholder for fields
- `Product`: Product record - placeholder for ONIX blocks 1-8
- `ONIXAttributes`: Mixin for shared attributes (`datestamp`, `sourcename`, `sourcetype`)

## Development Workflow

### Environment Setup
```bash
# Project uses uv for dependency management
uv sync
```

### Testing
```bash
# Run all tests
uv run pytest

# Test markers:
# - @pytest.mark.slow - slower tests
# - @pytest.mark.integration - integration tests
```

### Code Quality
```bash
uv run ruff check .
uv run ruff format .
```

## API Examples

### Creating Messages
```python
from onix import ONIXMessage, Header, Product

msg = ONIXMessage(
    release="3.1",
    header=Header(sourcename="MyPublisher"),
    products=[Product(), Product()],
)
```

### Parsing
```python
from onix.parsers import json_to_message, xml_to_message

# JSON: path, dict, or iterable of dicts
msg = json_to_message("/path/to/message.json")
msg = json_to_message({"header": {}, "products": [{}]})

# XML: path, string, etree Element, or iterable
msg = xml_to_message("<ONIXMessage>...</ONIXMessage>")
msg = xml_to_message("/path/to/message.xml")

# Short names require explicit flag
msg = json_to_message(data, short_names=True)
```

### Serializing
```python
from onix.parsers import message_to_json, message_to_xml_string, save_xml

json_str = message_to_json(msg)
xml_str = message_to_xml_string(msg, short_names=True)
save_xml(msg, "/path/to/output.xml")
```

### Code Lists
```python
from onix.lists import get_list, get_code

list_44 = get_list(44)  # Name identifier type
isni = get_code(44, "16")
print(isni.heading)  # "ISNI"
```

## Project Conventions

### Python 3.10+ Style
- Use `X | None` instead of `Optional[X]`
- Use `A | B` instead of `Union[A, B]`
- Use `list[X]`, `dict[K, V]` instead of `List[X]`, `Dict[K, V]`
- Use `from __future__ import annotations` for forward references
- Pattern matching (`match`/`case`) where it improves readability

### Test Structure
- Test files: `test_*.py` in `tests/`
- Test classes: `Test*` prefix
- Test functions: `test_*` prefix

### Type Safety
- All public APIs have type annotations
- `py.typed` marker for consumer type checking
- Pydantic models for ONIX structures

### File Organization
- Source: `src/onix/`
- Tests: `tests/`
- ONIX specs gitignored (`*Specification_*.md`, `*Specification_*.pdf`)

## Key Files
- [src/onix/message.py](../src/onix/message.py) - Core Pydantic models
- [src/onix/parsers/__init__.py](../src/onix/parsers/__init__.py) - Parser public API
- [src/onix/lists/__init__.py](../src/onix/lists/__init__.py) - Code list interface
- [pyproject.toml](../pyproject.toml) - Project config and dependencies

## Collaboration Notes
- User is new to Pydantic: offer quick guidance (e.g., derive models from `pydantic.BaseModel`, use type hints for fields, leverage `model_validate`/`model_dump` for IO) and propose minimal examples before larger changes.
- If the user’s intent seems inconsistent with ONIX or Python best practices, pause, explain the concern, and ask if they want to proceed anyway.
- Confirm assumptions explicitly; do not proceed on contested points without user acknowledgement.
