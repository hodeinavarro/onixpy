# pyonix - ONIX for Books Library

A Python library for parsing and working with ONIX for Books metadata (publishing industry standard). Built with Pydantic for type-safe data models.

## Features

- **ONIX 3.1 support** - Parse and create ONIX 3.1 messages
- **Type-safe models** - Pydantic-based models with full type annotations
- **XML & JSON support** - Parse from and serialize to both formats
 - **Model behavior** - Constructors accept snake_case field names, validate by
     field name (`validate_by_name=True`) and serialize using XML aliases
     (`serialize_by_alias=True`). Empty-string inputs for string fields are
     normalized to `None` to avoid storing blank values.
- **Code list validation** - Built-in ONIX code lists with validation
- **RNG schema validation** - Validate messages against RELAX NG schema

## Installation

```bash
pip install onix
```

## Quick Start

### Creating an ONIX Message

```python
from onix import ONIXMessage, Header, Product, ProductIdentifier, Sender

message = ONIXMessage(
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

### Parsing ONIX

```python
from onix.parsers import json_to_message, xml_to_message

# From JSON file or dict
message = json_to_message("/path/to/message.json")

# From XML file or string
message = xml_to_message("/path/to/message.xml")
```

### Serializing ONIX

```python
from onix.parsers import message_to_json, message_to_xml_string, save_xml

# To JSON string
json_str = message_to_json(message)

# To XML string
xml_str = message_to_xml_string(message)

# Save to file
save_xml(message, "/path/to/output.xml")
```

### Code Lists

```python
from onix.lists import get_list, get_code

# Get a code list
list_5 = get_list(5)  # Product identifier type

# Get a specific code
isbn_13 = get_code(5, "15")
print(isbn_13.heading)  # "ISBN-13"
```

## Requirements

- Python 3.10+
- pydantic >= 2.0
- lxml >= 6.0

## Development

```bash
# Clone and install dependencies
git clone https://github.com/yourusername/pyonix.git
cd pyonix
uv sync

# Run tests
uv run pytest --cov=src/onix --cov-report=term-missing --cov-report=html

# Code quality
uv run ruff check .
uv run ruff format .
```

## License

MIT
