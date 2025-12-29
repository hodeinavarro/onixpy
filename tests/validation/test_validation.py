"""Tests for RNG schema validation.

Note: Current Product model is a placeholder without required fields.
The ONIX 3.1 RNG schema requires Product elements to have:
- RecordReference
- NotificationType
- At least one ProductIdentifier

Tests with empty Product() instances will fail RNG validation until
the Product model is fully implemented. These tests are marked to skip
or adjusted to test other validation scenarios.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from onix import Header, ONIXMessage, Sender
from onix.parsers import (
    json_to_message,
    message_to_xml,
    message_to_xml_string,
    save_xml,
    xml_to_message,
)
from onix.validation import (
    RNGValidationError,
    validate_xml_element,
    validate_xml_file,
    validate_xml_string,
)

from ..conftest import make_header, make_header_dict, make_product, make_product_dict

pytestmark = pytest.mark.skipif(False, reason="Never skip - lxml is now required")


class TestRNGValidator:
    """Test RNG validation module functions."""

    def test_validate_minimal_message_element(self):
        """Validate a minimal valid ONIX message as Element."""
        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            products=[make_product()],
        )
        element = message_to_xml(msg)

        # Should not raise
        validate_xml_element(element)

    def test_validate_minimal_message_string(self):
        """Validate a minimal valid ONIX message as string."""
        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            products=[make_product()],
        )
        xml_str = message_to_xml_string(msg)

        # Should not raise
        validate_xml_string(xml_str)

    def test_validate_minimal_message_file(self, tmp_path: Path):
        """Validate a minimal valid ONIX message from file."""
        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            products=[make_product()],
        )
        xml_file = tmp_path / "message.xml"
        save_xml(msg, xml_file)

        # Should not raise
        validate_xml_file(xml_file)

    def test_validate_no_product_message(self):
        """Validate message with NoProduct element."""
        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            no_product=True,
        )
        xml_str = message_to_xml_string(msg)

        # Should not raise
        validate_xml_string(xml_str)

    def test_validate_message_with_attributes(self):
        """Validate message with ONIX attributes."""
        msg = ONIXMessage(
            release="3.1",
            header=Header(
                sender=Sender(sender_name="Test Publisher"),
                sent_date_time="20231201T120000Z",
            ),
            products=[make_product()],
            datestamp="20231201",
            sourcename="TestSource",
        )
        xml_str = message_to_xml_string(msg)

        # Should not raise
        validate_xml_string(xml_str)

    def test_validate_invalid_xml_raises(self):
        """Invalid XML should raise RNGValidationError."""
        # Create malformed XML - missing required Header
        invalid_xml = '<?xml version="1.0"?><ONIXMessage release="3.1"></ONIXMessage>'

        with pytest.raises(RNGValidationError) as exc_info:
            validate_xml_string(invalid_xml)

        assert len(exc_info.value.errors) > 0

    def test_validate_file_not_found(self):
        """Non-existent file should raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            validate_xml_file("/nonexistent/path.xml")

    def test_validate_schema_not_found(self, tmp_path: Path):
        """Non-existent schema should raise FileNotFoundError."""
        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            products=[make_product()],
        )
        element = message_to_xml(msg)

        with pytest.raises(FileNotFoundError):
            validate_xml_element(element, schema_path=tmp_path / "nonexistent.rng")


class TestJSONToPydanticToXMLValidation:
    """Test validation flow: JSON -> Pydantic -> XML -> RNG Validate."""

    def test_json_dict_to_xml_validates(self):
        """JSON dict -> Pydantic -> XML should validate."""
        data = {
            "header": make_header_dict(),
            "products": [make_product_dict()],
        }

        # Parse from JSON
        msg = json_to_message(data)

        # Convert to XML and validate
        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)

    def test_json_file_to_xml_validates(self, tmp_path: Path):
        """JSON file -> Pydantic -> XML should validate."""
        json_file = tmp_path / "message.json"
        data = {
            "header": make_header_dict(),
            "products": [make_product_dict()],
        }
        json_file.write_text(json.dumps(data))

        # Parse from JSON file
        msg = json_to_message(str(json_file))

        # Convert to XML and validate
        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)

    def test_json_with_attributes_to_xml_validates(self):
        """JSON with ONIX attributes -> Pydantic -> XML should validate."""
        data = {
            "header": {
                "sender": {"sender_name": "Test Publisher"},
                "sent_date_time": "20231201T120000Z",
            },
            "products": [make_product_dict()],
            "datestamp": "20231201",
            "sourcename": "TestSource",
        }

        msg = json_to_message(data)
        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)

    def test_json_multiple_products_to_xml_validates(self):
        """JSON with multiple products -> Pydantic -> XML should validate."""
        data = {
            "header": make_header_dict(),
            "products": [
                make_product_dict(record_reference="ref-001"),
                make_product_dict(record_reference="ref-002"),
                make_product_dict(record_reference="ref-003"),
            ],
        }

        msg = json_to_message(data)
        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)

        msg = json_to_message(data)
        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)


class TestXMLToPydanticToXMLValidation:
    """Test validation flow: XML -> Pydantic -> XML -> RNG Validate."""

    def test_xml_string_roundtrip_validates(self):
        """XML string -> Pydantic -> XML should validate."""
        original_xml = """<?xml version="1.0"?>
<ONIXMessage release="3.1">
  <Header>
    <Sender>
      <SenderName>Test Publisher</SenderName>
    </Sender>
    <SentDateTime>20231201T120000Z</SentDateTime>
  </Header>
  <Product>
    <RecordReference>ref-001</RecordReference>
    <NotificationType>03</NotificationType>
    <ProductIdentifier>
      <ProductIDType>15</ProductIDType>
      <IDValue>9780000000001</IDValue>
    </ProductIdentifier>
  </Product>
</ONIXMessage>"""

        # Parse from XML
        msg = xml_to_message(original_xml)

        # Convert back to XML and validate
        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)

    def test_xml_file_roundtrip_validates(self, tmp_path: Path):
        """XML file -> Pydantic -> XML should validate."""
        xml_file = tmp_path / "input.xml"
        original_xml = """<?xml version="1.0"?>
<ONIXMessage release="3.1">
  <Header>
    <Sender>
      <SenderName>Test Publisher</SenderName>
    </Sender>
    <SentDateTime>20231201T120000Z</SentDateTime>
  </Header>
  <Product>
    <RecordReference>ref-001</RecordReference>
    <NotificationType>03</NotificationType>
    <ProductIdentifier>
      <ProductIDType>15</ProductIDType>
      <IDValue>9780000000001</IDValue>
    </ProductIdentifier>
  </Product>
</ONIXMessage>"""
        xml_file.write_text(original_xml)

        # Parse from XML file
        msg = xml_to_message(str(xml_file))

        # Convert back to XML and validate
        output_file = tmp_path / "output.xml"
        save_xml(msg, output_file)
        validate_xml_file(output_file)

    def test_xml_with_attributes_roundtrip_validates(self):
        """XML with attributes -> Pydantic -> XML should validate."""
        original_xml = """<?xml version="1.0"?>
<ONIXMessage release="3.1" datestamp="20231201" sourcename="TestSource">
  <Header>
    <Sender>
      <SenderName>Test Publisher</SenderName>
    </Sender>
    <SentDateTime>20231201T120000Z</SentDateTime>
  </Header>
  <Product>
    <RecordReference>ref-001</RecordReference>
    <NotificationType>03</NotificationType>
    <ProductIdentifier>
      <ProductIDType>15</ProductIDType>
      <IDValue>9780000000001</IDValue>
    </ProductIdentifier>
  </Product>
</ONIXMessage>"""

        msg = xml_to_message(original_xml)
        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)

    def test_xml_multiple_products_roundtrip_validates(self):
        """XML with multiple products -> Pydantic -> XML should validate."""
        original_xml = """<?xml version="1.0"?>
<ONIXMessage release="3.1">
  <Header>
    <Sender>
      <SenderName>Test Publisher</SenderName>
    </Sender>
    <SentDateTime>20231201T120000Z</SentDateTime>
  </Header>
  <Product>
    <RecordReference>ref-001</RecordReference>
    <NotificationType>03</NotificationType>
    <ProductIdentifier>
      <ProductIDType>15</ProductIDType>
      <IDValue>9780000000001</IDValue>
    </ProductIdentifier>
  </Product>
  <Product>
    <RecordReference>ref-002</RecordReference>
    <NotificationType>03</NotificationType>
    <ProductIdentifier>
      <ProductIDType>15</ProductIDType>
      <IDValue>9780000000002</IDValue>
    </ProductIdentifier>
  </Product>
  <Product>
    <RecordReference>ref-003</RecordReference>
    <NotificationType>03</NotificationType>
    <ProductIdentifier>
      <ProductIDType>15</ProductIDType>
      <IDValue>9780000000003</IDValue>
    </ProductIdentifier>
  </Product>
</ONIXMessage>"""

        msg = xml_to_message(original_xml)
        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)


class TestPydanticToXMLValidation:
    """Test validation flow: Pydantic -> XML -> RNG Validate."""

    def test_minimal_message_validates(self):
        """Minimal Pydantic message -> XML should validate."""
        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            products=[make_product()],
        )

        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)

    def test_message_with_sender_identifiers_validates(self):
        """Message with sender identifiers -> XML should validate."""
        from onix.header import SenderIdentifier

        msg = ONIXMessage(
            release="3.1",
            header=Header(
                sender=Sender(
                    sender_name="Test Publisher",
                    sender_identifiers=[
                        SenderIdentifier(
                            sender_id_type="16",  # ISNI
                            id_value="0000000121032683",
                        )
                    ],
                ),
                sent_date_time="20231201T120000Z",
            ),
            products=[make_product()],
        )

        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)

    def test_message_with_addressee_validates(self):
        """Message with addressee -> XML should validate."""
        from onix.header import Addressee

        msg = ONIXMessage(
            release="3.1",
            header=Header(
                sender=Sender(sender_name="Test Publisher"),
                sent_date_time="20231201T120000Z",
                addressees=[Addressee(addressee_name="Test Recipient")],
            ),
            products=[make_product()],
        )

        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)

    def test_message_multiple_products_validates(self):
        """Message with multiple products -> XML should validate."""
        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            products=[
                make_product(record_reference="ref-001"),
                make_product(record_reference="ref-002"),
                make_product(record_reference="ref-003"),
            ],
        )

        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)

    def test_message_no_product_validates(self):
        """Message with NoProduct -> XML should validate."""
        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            no_product=True,
        )

        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)

    def test_message_with_all_attributes_validates(self):
        """Message with all ONIX attributes -> XML should validate."""
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

        xml_str = message_to_xml_string(msg)
        validate_xml_string(xml_str)

    def test_message_saves_to_valid_file(self, tmp_path: Path):
        """Pydantic message saved to file should validate."""
        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            products=[make_product()],
        )

        xml_file = tmp_path / "output.xml"
        save_xml(msg, xml_file)

        # Validate the saved file
        validate_xml_file(xml_file)
