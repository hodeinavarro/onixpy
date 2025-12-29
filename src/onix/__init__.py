"""pyonix - ONIX for Books Library.

A Python library for parsing and working with ONIX for Books metadata.

Core models:
- ONIXMessage: Root container for an ONIX message
- Header: Message header with sender/addressee info
- Product: Product record with metadata
- ProductIdentifier: Product identifier (ISBN, GTIN, etc.)

Parsing and serialization:
- Use `onix.parsers` for JSON/XML parsing and serialization

Code lists:
- Use `onix.lists` to access ONIX code lists

Example:
    >>> from onix import ONIXMessage, Header, Product, ProductIdentifier
    >>> from onix.parsers import json_to_message, xml_to_message
    >>>
    >>> # Create a message programmatically
    >>> message = ONIXMessage(
    ...     release="3.1",
    ...     header=Header(),
    ...     products=[
    ...         Product(
    ...             record_reference="com.example.001",
    ...             notification_type="03",
    ...             product_identifiers=[
    ...                 ProductIdentifier(product_id_type="15", id_value="9780000000001")
    ...             ],
    ...         )
    ...     ],
    ... )
    >>>
    >>> # Parse from JSON or XML
    >>> message = json_to_message("/path/to/message.json")
    >>> message = xml_to_message("/path/to/message.xml")
"""

from onix.header import (
    Addressee,
    AddresseeIdentifier,
    Header,
    Sender,
    SenderIdentifier,
)
from onix.message import ONIXAttributes, ONIXMessage
from onix.product import Product, ProductIdentifier

__all__ = [
    "ONIXMessage",
    "Header",
    "Sender",
    "SenderIdentifier",
    "Addressee",
    "AddresseeIdentifier",
    "Product",
    "ProductIdentifier",
    "ONIXAttributes",
]
