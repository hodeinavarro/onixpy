"""Tests for P.2 (Product identifiers) composites."""

from __future__ import annotations

import pytest

from onix.product.b1.p2 import Barcode, ProductIdentifier


class TestBarcode:
    def test_barcode_validation(self):
        # Valid barcode: choose codes present in List 141 / 142
        b = Barcode(BarcodeType="03", position_on_product="01")
        assert b.barcode_type == "03"
        assert b.position_on_product == "01"

        with pytest.raises(ValueError):
            Barcode(BarcodeType="ZZ")

        with pytest.raises(ValueError):
            Barcode(BarcodeType="03", position_on_product="99")

    def test_barcode_type_format_validation(self):
        """BarcodeType must be exactly 2 digits."""
        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            Barcode(BarcodeType="1")

        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            Barcode(BarcodeType="123")

    def test_position_on_product_format_validation(self):
        """PositionOnProduct must be exactly 2 digits."""
        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            Barcode(BarcodeType="03", position_on_product="1")

        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            Barcode(BarcodeType="03", position_on_product="123")

    def test_barcode_type_list_validation(self):
        """BarcodeType must be from List 141."""
        with pytest.raises(ValueError, match="must be from List 141"):
            Barcode(BarcodeType="99")


class TestProductIdentifier:
    def test_product_identifier_validation(self):
        """Valid ProductIdentifier creation."""
        pi = ProductIdentifier(ProductIDType="15", IDValue="9780000000001")
        assert pi.product_id_type == "15"
        assert pi.id_value == "9780000000001"
        assert pi.id_type_name is None

    def test_proprietary_with_id_type_name_valid(self):
        """Proprietary ProductIDType '01' with IDTypeName is valid."""
        pi = ProductIdentifier(
            ProductIDType="01",
            id_type_name="Custom SKU",
            IDValue="ABC123",
        )
        assert pi.product_id_type == "01"
        assert pi.id_type_name == "Custom SKU"

    def test_proprietary_without_id_type_name_raises_error(self):
        """Proprietary ProductIDType '01' without IDTypeName raises error."""
        with pytest.raises(
            ValueError,
            match="IDTypeName is required for proprietary ProductIDType '01'",
        ):
            ProductIdentifier(ProductIDType="01", IDValue="ABC123")

    def test_non_proprietary_without_id_type_name_valid(self):
        """Non-proprietary ProductIDType without IDTypeName is valid."""
        pi = ProductIdentifier(ProductIDType="15", IDValue="9780000000001")
        assert pi.id_type_name is None

    def test_invalid_product_id_type_raises_error(self):
        """Invalid ProductIDType raises error."""
        with pytest.raises(ValueError, match="must be from List 5"):
            ProductIdentifier(ProductIDType="99", IDValue="test")
