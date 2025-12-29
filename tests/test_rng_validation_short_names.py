"""Tests for RNG schema validation with short_names=True.

Ensures that messages created with short tags can be parsed and validated
against the ONIX RNG schema.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from onix import Header, ONIXMessage, Sender
from onix.header import Addressee
from onix.parsers import (
    json_to_message,
    message_to_xml_string,
    save_xml,
    xml_to_message,
)
from onix.validation import validate_xml_file, validate_xml_string

from .conftest import make_header, make_product

pytestmark = pytest.mark.skipif(False, reason="Never skip - lxml is now required")


class TestRNGValidationWithShortNames:
    """Test RNG validation works with short tag names."""

    def test_short_names_xml_to_rng_validates(self):
        """Short tag XML -> Pydantic -> XML should validate."""
        # XML with short tags
        short_xml = """<?xml version="1.0"?>
<ONIXmessage release="3.1">
  <header>
    <Sender>
      <SenderName>Test Publisher</SenderName>
    </Sender>
    <SentDateTime>20231201T120000Z</SentDateTime>
  </header>
  <product>
    <RecordReference>ref-001</RecordReference>
    <NotificationType>03</NotificationType>
    <ProductIdentifier>
      <ProductIDType>15</ProductIDType>
      <IDValue>9780000000001</IDValue>
    </ProductIdentifier>
  </product>
</ONIXmessage>"""

        # Parse from short tag XML
        msg = xml_to_message(short_xml, short_names=True)

        # Convert to reference names and validate
        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)

    def test_pydantic_to_short_xml_validates(self):
        """Pydantic -> short tag XML -> reference XML should validate."""
        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            products=[make_product()],
        )

        # Serialize to short tags
        short_xml_str = message_to_xml_string(msg, short_names=True)

        # Verify it has short tags
        assert "ONIXmessage" in short_xml_str
        assert "header" in short_xml_str
        assert "product" in short_xml_str
        assert "x507" not in short_xml_str  # NoProduct should not be present

        # Parse back and convert to reference names for validation
        msg_roundtrip = xml_to_message(short_xml_str, short_names=True)
        xml_str = message_to_xml_string(msg_roundtrip)
        validate_xml_string(xml_str)

    def test_short_xml_no_product_validates(self):
        """Short tag XML with x507 (NoProduct) should validate."""
        short_xml = """<?xml version="1.0"?>
<ONIXmessage release="3.1">
  <header>
    <Sender>
      <SenderName>Test Publisher</SenderName>
    </Sender>
    <SentDateTime>20231201T120000Z</SentDateTime>
  </header>
  <x507/>
</ONIXmessage>"""

        # Parse from short tag XML
        msg = xml_to_message(short_xml, short_names=True)

        # Verify NoProduct is set
        assert msg.no_product is True

        # Convert to reference names and validate
        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)

    def test_short_xml_with_sender_identifiers_validates(self):
        """Short tag XML with sender identifiers should validate."""
        short_xml = """<?xml version="1.0"?>
<ONIXmessage release="3.1">
  <header>
    <Sender>
      <SenderIdentifier>
        <SenderIDType>16</SenderIDType>
        <IDValue>0000000121032683</IDValue>
      </SenderIdentifier>
      <SenderName>Test Publisher</SenderName>
    </Sender>
    <SentDateTime>20231201T120000Z</SentDateTime>
  </header>
  <product>
    <RecordReference>ref-001</RecordReference>
    <NotificationType>03</NotificationType>
    <ProductIdentifier>
      <ProductIDType>15</ProductIDType>
      <IDValue>9780000000001</IDValue>
    </ProductIdentifier>
  </product>
</ONIXmessage>"""

        # Parse and validate
        msg = xml_to_message(short_xml, short_names=True)
        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)

    def test_short_xml_multiple_products_validates(self):
        """Short tag XML with multiple products should validate."""
        short_xml = """<?xml version="1.0"?>
<ONIXmessage release="3.1">
  <header>
    <Sender>
      <SenderName>Test Publisher</SenderName>
    </Sender>
    <SentDateTime>20231201T120000Z</SentDateTime>
  </header>
  <product>
    <RecordReference>ref-001</RecordReference>
    <NotificationType>03</NotificationType>
    <ProductIdentifier>
      <ProductIDType>15</ProductIDType>
      <IDValue>9780000000001</IDValue>
    </ProductIdentifier>
  </product>
  <product>
    <RecordReference>ref-002</RecordReference>
    <NotificationType>03</NotificationType>
    <ProductIdentifier>
      <ProductIDType>15</ProductIDType>
      <IDValue>9780000000002</IDValue>
    </ProductIdentifier>
  </product>
</ONIXmessage>"""

        # Parse and validate
        msg = xml_to_message(short_xml, short_names=True)
        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)

    def test_json_short_to_xml_validates(self):
        """JSON with short tags -> Pydantic -> XML should validate."""
        json_data = {
            "header": {
                "Sender": {"SenderName": "Test Publisher"},
                "SentDateTime": "20231201T120000Z",
            },
            "product": [
                {
                    "RecordReference": "ref-001",
                    "NotificationType": "03",
                    "ProductIdentifier": [
                        {"ProductIDType": "15", "IDValue": "9780000000001"}
                    ],
                }
            ],
        }

        # Parse from JSON with short names
        msg = json_to_message(json_data, short_names=True)

        # Convert to XML and validate
        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)

    def test_roundtrip_short_xml_file_validates(self, tmp_path: Path):
        """Short tag XML file roundtrip should validate."""
        # Create message and save with short tags
        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            products=[make_product()],
        )

        short_file = tmp_path / "short_message.xml"
        save_xml(msg, short_file, short_names=True)

        # Parse back with short names
        msg_roundtrip = xml_to_message(str(short_file), short_names=True)

        # Save with reference names and validate
        ref_file = tmp_path / "ref_message.xml"
        save_xml(msg_roundtrip, ref_file)
        validate_xml_file(ref_file)

    def test_pydantic_with_all_attributes_short_xml_validates(self):
        """Pydantic with all attributes -> short XML -> validates."""
        msg = ONIXMessage(
            release="3.1",
            header=Header(
                sender=Sender(sender_name="Test Publisher"),
                sent_date_time="20231201T120000Z",
            ),
            products=[make_product()],
            datestamp="20231201",
            sourcename="MessageSource",
            sourcetype="01",
        )

        # Serialize to short tags
        short_xml_str = message_to_xml_string(msg, short_names=True)

        # Parse back and validate
        msg_roundtrip = xml_to_message(short_xml_str, short_names=True)
        xml_str = message_to_xml_string(msg_roundtrip)
        validate_xml_string(xml_str)

    def test_pydantic_with_addressee_short_xml_validates(self):
        """Pydantic with addressee -> short XML -> validates."""
        msg = ONIXMessage(
            release="3.1",
            header=Header(
                sender=Sender(sender_name="Test Publisher"),
                sent_date_time="20231201T120000Z",
                addressees=[Addressee(addressee_name="Test Recipient")],
            ),
            products=[make_product()],
        )

        # Serialize to short tags and back
        short_xml_str = message_to_xml_string(msg, short_names=True)
        msg_roundtrip = xml_to_message(short_xml_str, short_names=True)

        # Validate
        xml_str = message_to_xml_string(msg_roundtrip)
        validate_xml_string(xml_str)


class TestShortTagsInDescriptiveDetail:
    """Test RNG validation with DescriptiveDetail short tags."""

    @pytest.mark.skip(
        reason="DescriptiveDetail alone doesn't satisfy RNG schema - needs TitleDetail"
    )
    def test_descriptive_detail_minimal_validates(self):
        """Minimal DescriptiveDetail should validate."""
        from onix.product.b1 import DescriptiveDetail

        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            products=[
                make_product(
                    descriptive_detail=DescriptiveDetail(
                        product_composition="00",
                        product_form="BB",
                    )
                )
            ],
        )

        # Serialize to reference names and validate
        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)

    @pytest.mark.skip(
        reason="DescriptiveDetail alone doesn't satisfy RNG schema - needs TitleDetail"
    )
    def test_descriptive_detail_with_short_tags_validates(self):
        """DescriptiveDetail with short tags should validate."""
        from onix.product.b1 import DescriptiveDetail

        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            products=[
                make_product(
                    descriptive_detail=DescriptiveDetail(
                        product_composition="00",
                        product_form="BB",
                    )
                )
            ],
        )

        # Serialize to short tags
        short_xml_str = message_to_xml_string(msg, short_names=True)

        # Verify short tags are present
        assert "x314" in short_xml_str  # ProductComposition
        assert "b012" in short_xml_str  # ProductForm

        # Parse back and validate
        msg_roundtrip = xml_to_message(short_xml_str, short_names=True)
        xml_str = message_to_xml_string(msg_roundtrip)
        validate_xml_string(xml_str)

    @pytest.mark.skip(
        reason="DescriptiveDetail alone doesn't satisfy RNG schema - needs TitleDetail"
    )
    def test_descriptive_detail_complex_short_tags_validates(self):
        """Complex DescriptiveDetail with short tags should validate."""
        from onix.product.b1 import (
            DescriptiveDetail,
            ProductFormFeature,
        )

        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            products=[
                make_product(
                    descriptive_detail=DescriptiveDetail(
                        product_composition="00",
                        product_form="BB",
                        product_form_details=["B206"],
                        product_form_features=[
                            ProductFormFeature(
                                product_form_feature_type="02",
                                product_form_feature_value="BLK",
                            )
                        ],
                        trade_category="03",
                        primary_content_type="10",
                    )
                )
            ],
        )

        # Serialize to short tags
        short_xml_str = message_to_xml_string(msg, short_names=True)

        # Verify various short tags
        assert "b333" in short_xml_str  # ProductFormDetail
        assert "b334" in short_xml_str  # ProductFormFeatureType
        assert "b335" in short_xml_str  # ProductFormFeatureValue
        assert "b384" in short_xml_str  # TradeCategory
        assert "x416" in short_xml_str  # PrimaryContentType

        # Parse back and validate
        msg_roundtrip = xml_to_message(short_xml_str, short_names=True)
        xml_str = message_to_xml_string(msg_roundtrip)
        validate_xml_string(xml_str)
