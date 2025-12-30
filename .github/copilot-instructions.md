# onixpy Development Guide

## Project Overview
Python library for parsing and working with ONIX for Books metadata (publishing industry standard). Built with Pydantic for type-safe data models.

## Architecture & Structure

### Package Layout
```
src/onix/
├── __init__.py       # Public API: ONIXMessage, Header, Product, ProductIdentifier, etc.
├── message.py        # ONIXMessage, ONIXAttributes models
├── header/
│   ├── __init__.py   # Exports Header, Sender, Addressee, etc.
│   └── header.py     # Header and nested composites with validation
├── product/
│   ├── __init__.py   # Exports Product, ProductIdentifier
│   └── product.py    # Product and ProductIdentifier models
├── parsers/
│   ├── __init__.py   # Parser API: json_to_message, xml_to_message, etc.
│   ├── fields.py     # Tag/field name mapping and model registration
│   ├── json.py       # JSON parsing/serialization
│   ├── xml.py        # XML parsing/serialization (lxml preferred)
│   └── tags.py       # Reference ↔ short tag name resolver
├── validation/
│   ├── __init__.py   # Validation API
│   └── rng.py        # RELAX NG schema validation
└── lists/
    ├── __init__.py   # Code list registry and lookup functions
    ├── models.py     # CodeList, CodeListEntry dataclasses
    ├── list1.py      # List 1: Notification or update type
    ├── list5.py      # List 5: Product identifier type
    ├── list44.py     # List 44: Name identifier type
    ├── list58.py     # List 58: Price type
    ├── list74.py     # List 74: Language code (ISO 639-2/B)
    ├── list96.py     # List 96: Currency code (ISO 4217)
    └── ...           # Additional lists (list2, list9, list12, etc.)
```

### Key Design Decisions
- **Reference names by default**: All parsers/serializers use ONIX reference tag names (e.g., `ONIXMessage`, `Header`). Short names (`ONIXmessage`, `header`, `x507`) require explicit `short_names=True`.
- **Strict validation**: Code list values are validated against their respective lists. Invalid codes raise `ValidationError`.
- **Tag mapping**: XML parser converts CamelCase tags to snake_case field names; serializer does the inverse.
- **XML library**: Prefers `lxml` if available, falls back to stdlib `xml.etree`.
- **Code lists**: Registry in `onix.lists` with `get_list(n)` / `get_code(n, code)` API.

### Core Models
- `ONIXMessage`: Root container with `header`, `products`, `release`, auto-set `no_product`
- `Header`: Message metadata with nested `Sender` (required), `Addressee` (optional), defaults
- `Sender`: Sender info with optional `SenderIdentifier` list (validated against List 44)
- `Addressee`: Addressee info with optional `AddresseeIdentifier` list
- `Product`: Product record with `record_reference`, `notification_type`, `product_identifiers` (min 1)
- `ProductIdentifier`: Product identifier with `product_id_type` (List 5), `id_value`, optional `id_type_name`
- `ONIXAttributes`: Mixin for shared attributes (`datestamp`, `sourcename`, `sourcetype`)

**Public API Convention**: All commonly-used ONIX models are exposed at the package level via `src/onix/__init__.py`. When adding new models to product blocks (DescriptiveDetail, PublishingDetail, etc.), remember to:
1. Export them from `src/onix/product/__init__.py`
2. Re-export them from `src/onix/__init__.py`
3. Update both `__all__` lists

This enables users to import models directly from `onix` rather than navigating submodules:
```python
from onix import Product, DescriptiveDetail, TitleDetail, Contributor
```

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
uv run pydocstyle
```

### Type Checking
```bash
# ty is a new type checker by Astral (creators of ruff/uv)
# Note: ty is experimental/not production-ready but works well most of the time
uv run ty check

# Known limitations with ty:
# - Some complex type narrowing (e.g., PathLike vs Iterable) may need type: ignore
# - lxml nsmap with None key needs type: ignore[arg-type] (stubs type it as Mapping[str, str])
```

## API Examples

### Creating Messages
```python
from onix import ONIXMessage, Header, Product, ProductIdentifier, Sender

msg = ONIXMessage(
    release="3.1",
    header=Header(
        sender=Sender(sender_name="MyPublisher"),
        sent_date_time="20231201T120000Z",
    ),
    products=[
        Product(
            record_reference="com.mypublisher.001",
            notification_type="03",  # Notification confirmed
            product_identifiers=[
                ProductIdentifier(product_id_type="15", id_value="9780000000001")
            ],
        ),
    ],
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

### Pydantic Field Style
- Always end `Field()` declarations with trailing commas
- Use multi-line format for all Field declarations:
  ```python
  # Correct:
  name_id_type: str = Field(
      alias="NameIDType",
  )

  title: str | None = Field(
      default=None,
      alias="Title",
  )

  # Incorrect:
  name_id_type: str = Field(alias="NameIDType")
  ```
- This ensures consistent formatting and cleaner diffs when fields are modified

### Test Structure
- Test files: `test_*.py` in `tests/`
- Test classes: `Test*` prefix
- Test functions: `test_*` prefix

Prefer class-based tests following the project's existing style: define a `Test*`
class and place individual test cases as methods named `test_*` on that class.
This keeps tests consistent and makes fixtures easier to scope.

Example:
```python
class TestMyFeature:
    def test_happy_path(self):
        assert do_stuff() == expected

    def test_edge_case(self):
        assert do_stuff(None) is None
```

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
- [src/onix/parsers/fields.py](../src/onix/parsers/fields.py) - Tag/field mapping and model registration
- [src/onix/lists/__init__.py](../src/onix/lists/__init__.py) - Code list interface
- [pyproject.toml](../pyproject.toml) - Project config and dependencies

## Parser Model Registration

When adding new Pydantic models to the ONIX structure, they must be registered with the XML parser for proper tag↔field mapping.

### `register_model(model_class)`
Registers a model's `Field(alias=...)` definitions for tag/field name conversion:
```python
from onix.parsers.fields import register_model
from onix.product.product import ProductIdentifier

register_model(ProductIdentifier)
```

### `register_plural_mapping(tag, field_name)`
For list fields where XML uses singular tags but Python uses plural field names:
```python
from onix.parsers.fields import register_plural_mapping

# XML: <ProductIdentifier>...</ProductIdentifier> (repeated)
# Python: product_identifiers: list[ProductIdentifier]
register_plural_mapping("ProductIdentifier", "product_identifiers")
```

This also marks the field as a list field via `is_list_field()`, ensuring single-element lists aren't flattened during XML parsing.

### Registration Location
Model registration happens in `src/onix/parsers/xml.py` at module load time. When adding new models:
1. Import the model class
2. Call `register_model(ModelClass)`
3. If it's a list field with singular XML tags, call `register_plural_mapping("Tag", "field_name")`

## Minimal Product Requirements

A valid ONIX Product requires (per RNG schema):
- `record_reference` (str): Unique identifier for the record
- `notification_type` (str): Code from List 1 (e.g., "03" = Notification confirmed)
- `product_identifiers` (list[ProductIdentifier]): At least one identifier

### ProductIdentifier Structure
```python
class ProductIdentifier(ONIXModel):
    product_id_type: str = Field(alias="ProductIDType")  # List 5
    id_type_name: str | None = Field(default=None, alias="IDTypeName")
    id_value: str = Field(alias="IDValue")
```

### Test Helpers
Use `make_product()` and `make_product_dict()` from `tests/conftest.py` for creating valid minimal products in tests:
```python
from conftest import make_product, make_product_dict

# Create a minimal valid Product model
product = make_product()

# Create a minimal valid product dict (for JSON/XML parsing tests)
product_dict = make_product_dict()
```

## Code List Generation

Generate code lists from ONIX specification using:
```bash
cd scripts
uv run python generate_codelist.py <list_number>
# Example: uv run python generate_codelist.py 44
```

Generated lists go to `src/onix/lists/list<N>.py`. Remember to register new lists in `src/onix/lists/__init__.py`.

## XML Namespace Handling

When creating XML elements programmatically for RNG validation, use Clark notation for the root element:
```python
namespace = "http://ns.editeur.org/onix/3.1/reference"
root = etree.Element(f"{{{namespace}}}ONIXMessage", nsmap={None: namespace})
```

This ensures in-memory elements have proper namespace qualification for RNG schema validation.

## Collaboration Notes
- User is new to Pydantic: offer quick guidance (e.g., derive models from `pydantic.BaseModel`, use type hints for fields, leverage `model_validate`/`model_dump` for IO) and propose minimal examples before larger changes.
- If the user’s intent seems inconsistent with ONIX or Python best practices, pause, explain the concern, and ask if they want to proceed anyway.
- Confirm assumptions explicitly; do not proceed on contested points without user acknowledgement.
