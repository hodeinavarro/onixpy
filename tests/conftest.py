"""Pytest configuration and shared fixtures."""

from __future__ import annotations

import pytest

from onix import Header, Product, ProductIdentifier, Sender


@pytest.fixture
def valid_sender() -> Sender:
    """Create a valid Sender for testing."""
    return Sender(sender_name="Test Publisher")


@pytest.fixture
def valid_header(valid_sender: Sender) -> Header:
    """Create a valid Header with required fields for testing."""
    return Header(
        sender=valid_sender,
        sent_date_time="20231201T120000Z",
    )


@pytest.fixture
def valid_product() -> Product:
    """Create a valid minimal Product for testing."""
    return make_product()


def make_header(**kwargs) -> Header:
    """Create a valid Header with optional overrides.

    Provides sensible defaults for required fields.
    """
    defaults = {
        "sender": Sender(sender_name="Test Publisher"),
        "sent_date_time": "20231201T120000Z",
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
    record_reference: str = "com.test.product.001",
    notification_type: str = "03",
    **kwargs,
) -> Product:
    """Create a valid minimal Product with optional overrides.

    Provides sensible defaults for required fields:
    - record_reference: Unique record reference
    - notification_type: List 1 code (default "03" = confirmed on publication)
    - product_identifiers: At least one ProductIdentifier (default ISBN-13)
    """
    if "product_identifiers" not in kwargs:
        kwargs["product_identifiers"] = [
            ProductIdentifier(product_id_type="15", id_value="9780000000001")
        ]
    return Product(
        record_reference=record_reference,
        notification_type=notification_type,
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
