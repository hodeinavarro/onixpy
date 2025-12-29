"""Tests for ONIX message models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from onix import Header, ONIXMessage, Sender

from ..conftest import make_header, make_product


class TestONIXMessageValidation:
    """Tests for ONIXMessage validation logic."""

    def test_no_products_sets_no_product_true(self):
        """When products list is empty, no_product should be True."""
        msg = ONIXMessage(header=make_header())
        assert msg.products == []
        assert msg.no_product is True

    def test_with_products_no_product_false(self):
        """When products are provided, no_product should be False."""
        msg = ONIXMessage(header=make_header(), products=[make_product()])
        assert len(msg.products) == 1
        assert msg.no_product is False

    def test_cannot_have_products_and_no_product(self):
        """Cannot specify both products and no_product=True."""
        with pytest.raises(ValidationError) as exc_info:
            ONIXMessage(
                header=make_header(), products=[make_product()], no_product=True
            )

        assert "Cannot have both 'products' and 'no_product=True'" in str(
            exc_info.value
        )

    def test_explicit_no_product_without_products(self):
        """Can explicitly set no_product=True when no products."""
        msg = ONIXMessage(header=make_header(), no_product=True)
        assert msg.products == []
        assert msg.no_product is True


class TestONIXMessageAttributes:
    """Tests for ONIXMessage shared attributes."""

    def test_default_release(self):
        """Default release should be 3.1."""
        msg = ONIXMessage(header=make_header())
        assert msg.release == "3.1"

    def test_custom_release(self):
        """Can specify custom release version."""
        msg = ONIXMessage(header=make_header(), release="3.0")
        assert msg.release == "3.0"

    def test_shared_attributes(self):
        """ONIXMessage should support shared ONIX attributes."""
        msg = ONIXMessage(
            header=make_header(),
            datestamp="20231201",
            sourcename="TestPublisher",
            sourcetype="01",
        )
        assert msg.datestamp == "20231201"
        assert msg.sourcename == "TestPublisher"
        assert msg.sourcetype == "01"


class TestHeaderValidation:
    """Tests for Header validation."""

    def test_header_requires_sender(self):
        """Header requires a sender."""
        with pytest.raises(ValidationError) as exc_info:
            Header(sent_date_time="20231201T120000Z")
        # Check for either field name or alias in error message
        error_str = str(exc_info.value).lower()
        assert "sender" in error_str

    def test_header_requires_sent_date_time(self):
        """Header requires sent_date_time."""
        with pytest.raises(ValidationError) as exc_info:
            Header(sender=Sender(sender_name="Test"))
        # Check for either field name or alias in error message
        error_str = str(exc_info.value).lower()
        assert "sentdatetime" in error_str or "sent_date_time" in error_str

    def test_valid_header(self):
        """Valid header with required fields."""
        header = make_header()
        assert header.sender.sender_name == "Test Publisher"
        assert header.sent_date_time == "20231201T120000Z"

    def test_header_with_defaults(self):
        """Header with default language, price type, currency."""
        header = make_header(
            default_language_of_text="eng",
            default_price_type="01",
            default_currency_code="USD",
        )
        assert header.default_language_of_text == "eng"
        assert header.default_price_type == "01"
        assert header.default_currency_code == "USD"

    def test_invalid_language_code(self):
        """Invalid language code should fail validation."""
        with pytest.raises(ValidationError) as exc_info:
            make_header(default_language_of_text="invalid")
        assert "List 74" in str(exc_info.value)

    def test_invalid_price_type(self):
        """Invalid price type should fail validation."""
        with pytest.raises(ValidationError) as exc_info:
            make_header(default_price_type="99")
        assert "List 58" in str(exc_info.value)

    def test_invalid_currency_code(self):
        """Invalid currency code should fail validation."""
        with pytest.raises(ValidationError) as exc_info:
            make_header(default_currency_code="XXX")
        assert "List 96" in str(exc_info.value)
