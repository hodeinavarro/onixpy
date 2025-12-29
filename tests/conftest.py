"""Pytest configuration and shared fixtures."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from onix import Header, ONIXMessage, Product, ProductIdentifier, Sender
from onix.parsers import message_to_xml_string
from onix.validation.rng import validate_xml_string


@pytest.fixture
def valid_sender() -> Sender:
    """Create a valid Sender for testing."""
    return Sender(
        sender_name="Test Publisher",
    )


@pytest.fixture
def valid_header(valid_sender: Sender) -> Header:
    """Create a valid Header with required fields for testing."""
    return Header(
        Sender=valid_sender,
        SentDateTime="20231201T120000Z",
    )


@pytest.fixture
def valid_product() -> Product:
    """Create a valid minimal Product for testing."""
    return make_product()


def make_header(**kwargs) -> Header:
    """Create a valid Header with optional overrides.

    Provides sensible defaults for required fields.
    """
    defaults: dict[str, Any] = {
        "Sender": Sender(sender_name="Test Publisher"),
        "SentDateTime": "20231201T120000Z",
    }
    defaults.update(kwargs)
    return Header(**defaults)


def make_header_dict(**kwargs) -> dict:
    """Create a valid Header dict for JSON/XML parsing tests."""
    defaults = {
        "sender": {"sender_name": "Test Publisher"},
        "sent_date_time": "20231201T120000Z",
    }
    defaults.update(kwargs)
    return defaults


def make_product(
    RecordReference: str = "com.test.product.001",
    NotificationType: str = "03",
    **kwargs,
) -> Product:
    """Create a valid minimal Product with optional overrides.

    Provides sensible defaults for required fields:
    - RecordReference: Unique record reference
    - NotificationType: List 1 code (default "03" = confirmed on publication)
    - ProductIdentifier: At least one ProductIdentifier (default ISBN-13)
    """
    if "ProductIdentifier" not in kwargs:
        kwargs["ProductIdentifier"] = [
            ProductIdentifier(
                ProductIDType="15",
                IDValue="9780000000001",
            )
        ]
    return Product(
        RecordReference=RecordReference,
        NotificationType=NotificationType,
        **kwargs,
    )


def make_product_dict(
    record_reference: str = "com.test.product.001",
    notification_type: str = "03",
    **kwargs,
) -> dict:
    """Create a valid minimal Product dict for JSON/XML parsing tests.

    Provides sensible defaults for required fields.
    """
    defaults = {
        "record_reference": record_reference,
        "notification_type": notification_type,
        "product_identifiers": [{"product_id_type": "15", "id_value": "9780000000001"}],
    }
    defaults.update(kwargs)
    return defaults


def make_message(
    release: str = "3.1",
    header: Header | dict | None = None,
    products: list[Product] | list[dict] | None = None,
    no_product: bool = False,
    **kwargs,
) -> ONIXMessage:
    """Create a valid ONIXMessage with optional overrides.

    Provides sensible defaults for required fields.
    """
    if header is None:
        header = make_header()
    elif isinstance(header, dict):
        header = Header(**header)

    # Normalize products to a concrete list[Product]
    if products is None:
        products_list: list[Product] = [] if no_product else [make_product()]
    else:
        products_list = [
            p if isinstance(p, Product) else Product(**p) for p in products
        ]

    return ONIXMessage(
        release=release,
        Header=header,
        Product=products_list,
        no_product=no_product,
        **kwargs,
    )


def make_message_dict(
    ref: bool = True,
    minimal: bool = True,
    **kwargs,
) -> dict:
    """Create a valid ONIXMessage dict for JSON/XML parsing tests.

    Args:
        ref: If True, use reference tag names. If False, use short tag names.
        minimal: If True, create minimal message. If False, include extra fields.
        **kwargs: Override any default fields.

    Returns:
        Dictionary suitable for json_to_message or xml_to_message.
    """
    if ref:
        header_key = "header"
        products_key = "products"
        sender_key = "sender"
        sender_name_key = "sender_name"
        sent_date_time_key = "sent_date_time"
    else:
        header_key = "header"  # composite short tags same as ref
        products_key = "product"
        sender_key = "sender"  # composite short tags same as ref
        sender_name_key = "x298"
        sent_date_time_key = "x307"

    defaults: dict[str, Any] = {
        header_key: {
            sender_key: {sender_name_key: "Test Publisher"},
            sent_date_time_key: "20231201T120000Z",
        },
        products_key: [make_product_dict()],
    }

    if not minimal:
        # Add optional fields for non-minimal messages
        header_dict: dict[str, Any] = defaults[header_key]
        header_dict["message_number" if ref else "m180"] = "1234"
        header_dict["message_repeat" if ref else "m181"] = "1"

    defaults.update(kwargs)
    return defaults


def make_message_xml(ref: bool = True, minimal: bool = True, **kwargs) -> str:
    """Create a valid ONIXMessage XML string.

    Args:
        ref: If True, use reference tag names. If False, use short tag names.
        minimal: If True, create minimal message. If False, include extra fields.
        **kwargs: Override any default fields for make_message.

    Returns:
        XML string representation of the message.
    """
    msg = make_message(**kwargs) if minimal else make_message(minimal=False, **kwargs)
    return message_to_xml_string(msg, short_names=not ref)


def assert_valid_rng(xml_str: str, short: bool = False) -> None:
    """Assert that XML string validates against ONIX RNG schema.

    Args:
        xml_str: XML string to validate
        short: If True, convert short tags to reference before validating

    Raises:
        AssertionError: If validation fails
    """
    if short:
        # Parse with short names, serialize with reference names for validation
        from onix.parsers import message_to_xml_string, xml_to_message

        msg = xml_to_message(xml_str, short_names=True)
        xml_str = message_to_xml_string(msg, short_names=False)

    try:
        validate_xml_string(xml_str)
    except Exception as e:
        pytest.fail(f"RNG validation failed: {e}")


def save_and_validate(
    xml_str: str,
    tmp_path: Path,
    short: bool = False,
) -> Path:
    """Save XML string to file and validate against RNG schema.

    Args:
        xml_str: XML string to save and validate
        tmp_path: Temporary directory path from pytest fixture
        short: If True, convert short tags to reference before validating

    Returns:
        Path to the saved file

    Raises:
        AssertionError: If validation fails
    """
    xml_file = tmp_path / "test_message.xml"
    xml_file.write_text(xml_str)

    assert_valid_rng(xml_str, short=short)

    return xml_file
