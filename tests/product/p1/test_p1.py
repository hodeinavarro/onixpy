"""Tests for P.1 (Record reference, type and source) composites."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from onix import Header, ONIXMessage, Product, Sender
from onix.parsers import message_to_xml_string
from onix.product import ProductIdentifier
from onix.product.b1.p1 import RecordSourceIdentifier
from onix.product.b1.p2 import Barcode
from onix.validation.rng import validate_xml_string


class TestProductRecordSourceType:
    """Test Product record_source_type validation."""

    def test_invalid_record_source_type_format(self):
        """record_source_type must be exactly 2 digits."""
        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            Product(
                RecordReference="test-001",
                NotificationType="03",
                ProductIdentifier=[
                    ProductIdentifier(ProductIDType="15", IDValue="9780000000001")
                ],
                record_source_type="1",  # Too short
            )

    def test_invalid_record_source_type_code(self):
        """record_source_type must be valid List 3 code."""
        with pytest.raises(ValueError, match="must be from List 3"):
            Product(
                RecordReference="test-001",
                NotificationType="03",
                ProductIdentifier=[
                    ProductIdentifier(ProductIDType="15", IDValue="9780000000001")
                ],
                record_source_type="99",  # Invalid code
            )

    def test_valid_record_source_identifier(self):
        rsi = RecordSourceIdentifier(RecordSourceIDType="03", IDValue="DISTR-001")
        assert rsi.record_source_id_type == "03"

    def test_proprietary_requires_id_type_name(self):
        with pytest.raises(ValueError):
            RecordSourceIdentifier(RecordSourceIDType="01", IDValue="X")

        rsi = RecordSourceIdentifier(
            RecordSourceIDType="01", id_type_name="ACME", IDValue="X"
        )
        assert rsi.id_type_name == "ACME"

    def test_invalid_record_source_id_type_format(self):
        """RecordSourceIDType must be exactly 2 digits."""
        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            RecordSourceIdentifier(RecordSourceIDType="1", IDValue="TEST")  # Too short

        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            RecordSourceIdentifier(RecordSourceIDType="123", IDValue="TEST")  # Too long

        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            RecordSourceIdentifier(
                RecordSourceIDType="AB", IDValue="TEST"
            )  # Non-digits

    def test_invalid_record_source_id_type_code(self):
        """RecordSourceIDType must be valid List 44 code."""
        with pytest.raises(ValueError, match="not a valid List 44 code"):
            RecordSourceIdentifier(
                RecordSourceIDType="99", IDValue="TEST"
            )  # Invalid code


class TestDeletionText:
    def test_deletion_text_length(self):
        long_text = "x" * 101
        with pytest.raises(ValueError):
            # Use Product constructor to exercise deletion_texts validation
            Product(
                RecordReference="r1",
                NotificationType="05",
                ProductIdentifier=[
                    ProductIdentifier(ProductIDType="15", IDValue="9780000000001")
                ],
                DeletionText=[long_text],
            )

        p = Product(
            RecordReference="r2",
            NotificationType="05",
            ProductIdentifier=[
                ProductIdentifier(ProductIDType="15", IDValue="9780000000001")
            ],
            DeletionText=["Removed in error"],
        )
        assert p.deletion_texts == ["Removed in error"]

    def test_deletion_text_requires_delete_notification(self):
        with pytest.raises(ValueError):
            Product(
                RecordReference="r3",
                NotificationType="03",
                ProductIdentifier=[
                    ProductIdentifier(ProductIDType="15", IDValue="9780000000001")
                ],
                DeletionText=["Should fail because not a delete notification"],
            )

    def test_deletion_text_field_validation(self):
        """Test deletion_texts field validation on Product model."""
        # Valid text
        p = Product(
            RecordReference="ref-001",
            NotificationType="05",
            ProductIdentifier=[
                ProductIdentifier(ProductIDType="15", IDValue="9780000000001")
            ],
            DeletionText=["Product discontinued"],
        )
        assert p.deletion_texts == ["Product discontinued"]

        # Text exactly at max length (100 chars)
        max_text = "x" * 100
        p = Product(
            RecordReference="ref-002",
            NotificationType="05",
            ProductIdentifier=[
                ProductIdentifier(ProductIDType="15", IDValue="9780000000002")
            ],
            DeletionText=[max_text],
        )
        assert p.deletion_texts == [max_text]

        # Text exceeding max length
        with pytest.raises(
            ValidationError, match="DeletionText exceeds maximum length of 100"
        ):
            Product(
                RecordReference="ref-003",
                NotificationType="05",
                ProductIdentifier=[
                    ProductIdentifier(ProductIDType="15", IDValue="9780000000003")
                ],
                DeletionText=["x" * 101],
            )


def test_message_with_p1_and_barcode_roundtrip_validates():
    """Integration test for P.1 and P.2 models together."""
    p = Product(
        RecordReference="ref-001",
        NotificationType="05",
        ProductIdentifier=[
            ProductIdentifier(ProductIDType="15", IDValue="9780000000001")
        ],
        record_source_type="03",
        RecordSourceIdentifier=[
            RecordSourceIdentifier(RecordSourceIDType="03", IDValue="DISTR-001")
        ],
        DeletionText=["Issued in error"],
        Barcode=[Barcode(BarcodeType="03", position_on_product="01")],
    )

    # Header is required by RNG; use minimal header
    hdr = Header(
        Sender=Sender(sender_name="Test Publisher"), SentDateTime="20231201T120000Z"
    )
    msg = ONIXMessage(release="3.1", Header=hdr, Product=[p])

    xml_str = message_to_xml_string(msg)
    validate_xml_string(xml_str)
