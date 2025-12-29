"""Tests for ONIX message models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from onix import Header, ONIXMessage, Product


class TestONIXMessageValidation:
    """Tests for ONIXMessage validation logic."""

    def test_no_products_sets_no_product_true(self):
        """When products list is empty, no_product should be True."""
        msg = ONIXMessage(header=Header())
        assert msg.products == []
        assert msg.no_product is True

    def test_with_products_no_product_false(self):
        """When products are provided, no_product should be False."""
        msg = ONIXMessage(header=Header(), products=[Product()])
        assert len(msg.products) == 1
        assert msg.no_product is False

    def test_cannot_have_products_and_no_product(self):
        """Cannot specify both products and no_product=True."""
        with pytest.raises(ValidationError) as exc_info:
            ONIXMessage(header=Header(), products=[Product()], no_product=True)

        assert "Cannot have both 'products' and 'no_product=True'" in str(
            exc_info.value
        )

    def test_explicit_no_product_without_products(self):
        """Can explicitly set no_product=True when no products."""
        msg = ONIXMessage(header=Header(), no_product=True)
        assert msg.products == []
        assert msg.no_product is True


class TestONIXMessageAttributes:
    """Tests for ONIXMessage shared attributes."""

    def test_default_release(self):
        """Default release should be 3.1."""
        msg = ONIXMessage(header=Header())
        assert msg.release == "3.1"

    def test_custom_release(self):
        """Can specify custom release version."""
        msg = ONIXMessage(header=Header(), release="3.0")
        assert msg.release == "3.0"

    def test_shared_attributes(self):
        """ONIXMessage should support shared ONIX attributes."""
        msg = ONIXMessage(
            header=Header(),
            datestamp="20231201",
            sourcename="TestPublisher",
            sourcetype="01",
        )
        assert msg.datestamp == "20231201"
        assert msg.sourcename == "TestPublisher"
        assert msg.sourcetype == "01"
