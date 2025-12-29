"""Pytest configuration and shared fixtures."""

from __future__ import annotations

import pytest

from onix import Header, Sender


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
