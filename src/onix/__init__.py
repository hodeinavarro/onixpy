"""pyonix - ONIX for Books Library.

A Python library for parsing and working with ONIX for Books metadata.

Core models:
- ONIXMessage: Root container for an ONIX message
- Header: Message header with sender/addressee info
- Product: Product record with metadata

Parsing and serialization:
- Use `onix.parsers` for JSON/XML parsing and serialization

Code lists:
- Use `onix.lists` to access ONIX code lists

Example:
    >>> from onix import ONIXMessage, Header, Product
    >>> from onix.parsers import json_to_message, xml_to_message
    >>>
    >>> # Create a message programmatically
    >>> message = ONIXMessage(
    ...     release="3.1",
    ...     header=Header(),
    ...     products=[Product()],
    ... )
    >>>
    >>> # Parse from JSON or XML
    >>> message = json_to_message("/path/to/message.json")
    >>> message = xml_to_message("/path/to/message.xml")
"""

from onix.message import Header, ONIXAttributes, ONIXMessage, Product

__all__ = [
    "ONIXMessage",
    "Header",
    "Product",
    "ONIXAttributes",
]
