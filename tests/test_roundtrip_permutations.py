"""Comprehensive roundtrip tests for all format/tag-style permutations.

Tests cover:
- XML (reference) ↔ Model ↔ XML (reference) + RNG validation
- XML (short) ↔ Model ↔ XML (short) + RNG validation
- Cross-style serialization (ref→short, short→ref) + RNG validation
- JSON ↔ Model ↔ XML + RNG validation
- Model construction via alias (reference tags) and field names
- Plural tag handling (singular XML tags → plural model fields)
"""

from __future__ import annotations

from pathlib import Path

from onix import Header, ONIXMessage, Sender
from onix.parsers import (
    json_to_message,
    message_to_json,
    message_to_xml_string,
    save_xml,
    xml_to_message,
)
from onix.product import Product, ProductIdentifier
from onix.validation import validate_xml_file, validate_xml_string

from .conftest import make_header, make_product, make_product_dict


class TestXMLReferenceRoundtrips:
    """Test XML with reference tag names."""

    def test_xml_ref_parse_serialize_roundtrip(self):
        """Parse reference XML → serialize reference XML → models match."""
        xml_ref = """<?xml version="1.0"?>
<ONIXMessage xmlns="http://ns.editeur.org/onix/3.1/reference" release="3.1">
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

        # Parse
        msg1 = xml_to_message(xml_ref)
        assert msg1.header.sender.sender_name == "Test Publisher"
        assert len(msg1.products) == 1
        assert msg1.products[0].record_reference == "ref-001"

        # Serialize back
        xml_out = message_to_xml_string(msg1)

        # Parse again and compare
        msg2 = xml_to_message(xml_out)
        assert msg1.model_dump() == msg2.model_dump()

    def test_xml_ref_roundtrip_validates_rng(self):
        """Reference XML roundtrip passes RNG validation."""
        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            products=[make_product()],
        )

        # Serialize to reference XML
        xml_str = message_to_xml_string(msg)

        # Validate against RNG
        validate_xml_string(xml_str)

        # Parse and serialize again
        msg_roundtrip = xml_to_message(xml_str)
        xml_roundtrip = message_to_xml_string(msg_roundtrip)

        # Validate roundtrip
        validate_xml_string(xml_roundtrip)

    def test_xml_ref_file_roundtrip_validates(self, tmp_path: Path):
        """Reference XML saved to file and reloaded validates."""
        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            products=[make_product()],
        )

        # Save to file
        xml_file = tmp_path / "message_ref.xml"
        save_xml(msg, xml_file)

        # Validate file
        validate_xml_file(xml_file)

        # Parse from file
        msg_loaded = xml_to_message(str(xml_file))

        # Serialize and validate again
        xml_str = message_to_xml_string(msg_loaded)
        validate_xml_string(xml_str)


class TestXMLShortRoundtrips:
    """Test XML with short tag names."""

    def test_xml_short_parse_serialize_roundtrip(self):
        """Parse short XML → serialize short XML → models match."""
        xml_short = """<?xml version="1.0"?>
<ONIXmessage xmlns="http://ns.editeur.org/onix/3.1/short" release="3.1">
  <header>
    <sender>
      <SenderName>Test Publisher</SenderName>
    </sender>
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

        # Parse with short_names=True
        msg1 = xml_to_message(xml_short, short_names=True)
        assert msg1.header.sender.sender_name == "Test Publisher"
        assert len(msg1.products) == 1

        # Serialize back to short tags
        xml_out = message_to_xml_string(msg1, short_names=True)
        assert "<product>" in xml_out
        assert "<header>" in xml_out

        # Parse again and compare
        msg2 = xml_to_message(xml_out, short_names=True)
        assert msg1.model_dump() == msg2.model_dump()

    def test_xml_short_roundtrip_validates_rng(self):
        """Short XML roundtrip → convert to ref → validate RNG."""
        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            products=[make_product()],
        )

        # Serialize to short XML
        xml_short = message_to_xml_string(msg, short_names=True)
        assert "<product>" in xml_short
        assert "<header>" in xml_short

        # Parse back
        msg_roundtrip = xml_to_message(xml_short, short_names=True)

        # Convert to reference and validate
        xml_ref = message_to_xml_string(msg_roundtrip)
        validate_xml_string(xml_ref)

    def test_xml_short_file_roundtrip(self, tmp_path: Path):
        """Short XML saved to file and reloaded works."""
        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            products=[make_product()],
        )

        # Save to file with short names
        xml_file = tmp_path / "message_short.xml"
        save_xml(msg, xml_file, short_names=True)

        # Parse from file
        msg_loaded = xml_to_message(str(xml_file), short_names=True)

        # Verify content
        assert msg.model_dump() == msg_loaded.model_dump()


class TestCrossStyleSerialization:
    """Test converting between reference and short tag styles."""

    def test_ref_to_short_cross_serialize(self):
        """Parse reference XML → serialize short XML → validate."""
        xml_ref = """<?xml version="1.0"?>
<ONIXMessage xmlns="http://ns.editeur.org/onix/3.1/reference" release="3.1">
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

        # Parse reference XML
        msg = xml_to_message(xml_ref)

        # Serialize to short tags
        xml_short = message_to_xml_string(msg, short_names=True)
        assert "<product>" in xml_short
        assert "<header>" in xml_short
        assert "ONIXmessage" in xml_short

        # Parse short XML and convert back to ref
        msg_short = xml_to_message(xml_short, short_names=True)
        xml_ref_out = message_to_xml_string(msg_short)

        # Validate reference output
        validate_xml_string(xml_ref_out)

    def test_short_to_ref_cross_serialize(self):
        """Parse short XML → serialize reference XML → validate."""
        xml_short = """<?xml version="1.0"?>
<ONIXmessage xmlns="http://ns.editeur.org/onix/3.1/short" release="3.1">
  <header>
    <sender>
      <SenderName>Test Publisher</SenderName>
    </sender>
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

        # Parse short XML
        msg = xml_to_message(xml_short, short_names=True)

        # Serialize to reference tags
        xml_ref = message_to_xml_string(msg, short_names=False)
        assert "<Product>" in xml_ref
        assert "<Header>" in xml_ref
        assert "ONIXMessage" in xml_ref

        # Validate reference output
        validate_xml_string(xml_ref)

    def test_model_to_both_styles_validates(self):
        """Pydantic model → both ref and short XML → both validate."""
        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            products=[make_product()],
        )

        # Serialize to both styles
        xml_ref = message_to_xml_string(msg, short_names=False)
        xml_short = message_to_xml_string(msg, short_names=True)

        # Reference validates
        validate_xml_string(xml_ref)

        # Short parses and converts to ref for validation
        msg_from_short = xml_to_message(xml_short, short_names=True)
        xml_ref_from_short = message_to_xml_string(msg_from_short)
        validate_xml_string(xml_ref_from_short)


class TestJSONRoundtrips:
    """Test JSON parsing and serialization."""

    def test_json_ref_roundtrip(self):
        """JSON (reference) → parse → JSON → parse → models match."""
        json_data = {
            "Header": {
                "Sender": {"SenderName": "Test Publisher"},
                "SentDateTime": "20231201T120000Z",
            },
            "Product": [
                {
                    "RecordReference": "ref-001",
                    "NotificationType": "03",
                    "ProductIdentifier": [
                        {"ProductIDType": "15", "IDValue": "9780000000001"}
                    ],
                }
            ],
        }

        # Parse
        msg1 = json_to_message(json_data)

        # Serialize to JSON
        json_str = message_to_json(msg1)

        # Parse again
        import json

        json_out = json.loads(json_str)
        msg2 = json_to_message(json_out)

        # Compare
        assert msg1.model_dump() == msg2.model_dump()

    def test_json_to_xml_ref_validates(self):
        """JSON → parse → XML (reference) → validate RNG."""
        json_data = {
            "Header": {
                "Sender": {"SenderName": "Test Publisher"},
                "SentDateTime": "20231201T120000Z",
            },
            "Product": [make_product_dict()],
        }

        # Parse JSON
        msg = json_to_message(json_data)

        # Serialize to XML
        xml_str = message_to_xml_string(msg)

        # Validate
        validate_xml_string(xml_str)

    def test_json_short_to_xml_short(self):
        """JSON (short) → parse → XML (short) → parse → validate."""
        json_data = {
            "header": {
                "sender": {"SenderName": "Test Publisher"},
                "SentDateTime": "20231201T120000Z",
            },
            "product": [make_product_dict()],
        }

        # Parse JSON with short names
        msg = json_to_message(json_data, short_names=True)

        # Serialize to short XML
        xml_short = message_to_xml_string(msg, short_names=True)
        assert "<product>" in xml_short

        # Parse short XML
        msg_from_xml = xml_to_message(xml_short, short_names=True)

        # Convert to reference and validate
        xml_ref = message_to_xml_string(msg_from_xml)
        validate_xml_string(xml_ref)


class TestModelConstruction:
    """Test model construction via field names and aliases."""

    def test_construction_via_field_names(self):
        """Construct models using Python field names."""
        product = Product(
            record_reference="ref-001",
            notification_type="03",
            product_identifiers=[
                ProductIdentifier(
                    product_id_type="15",
                    id_value="9780000000001",
                )
            ],
        )

        assert product.record_reference == "ref-001"
        assert product.notification_type == "03"

    def test_construction_via_aliases(self):
        """Construct models using ONIX reference tag names (aliases)."""
        product = Product(
            RecordReference="ref-001",
            NotificationType="03",
            ProductIdentifier=[
                ProductIdentifier(
                    ProductIDType="15",
                    IDValue="9780000000001",
                )
            ],
        )

        assert product.record_reference == "ref-001"
        assert product.notification_type == "03"

    def test_mixed_construction_field_and_alias(self):
        """Mix field names and aliases in construction."""
        # Outer uses field names, inner uses aliases
        product = Product(
            record_reference="ref-001",
            notification_type="03",
            product_identifiers=[
                ProductIdentifier(
                    ProductIDType="15",
                    IDValue="9780000000001",
                )
            ],
        )

        msg = ONIXMessage(
            release="3.1",
            Header=Header(
                Sender=Sender(SenderName="Test"),
                SentDateTime="20231201",
            ),
            products=[product],
        )

        assert msg.header.sender.sender_name == "Test"


class TestPluralTagHandling:
    """Test singular XML tags mapping to plural model fields."""

    def test_single_product_not_flattened(self):
        """Single <Product> tag creates list with one element."""
        xml_str = """<?xml version="1.0"?>
<ONIXMessage xmlns="http://ns.editeur.org/onix/3.1/reference" release="3.1">
  <Header>
    <Sender>
      <SenderName>Test</SenderName>
    </Sender>
    <SentDateTime>20231201</SentDateTime>
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

        msg = xml_to_message(xml_str)

        # products should be a list, not flattened to single object
        assert isinstance(msg.products, list)
        assert len(msg.products) == 1

    def test_multiple_products_all_parsed(self):
        """Multiple <Product> tags create list with multiple elements."""
        xml_str = """<?xml version="1.0"?>
<ONIXMessage xmlns="http://ns.editeur.org/onix/3.1/reference" release="3.1">
  <Header>
    <Sender>
      <SenderName>Test</SenderName>
    </Sender>
    <SentDateTime>20231201</SentDateTime>
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
</ONIXMessage>"""

        msg = xml_to_message(xml_str)

        assert len(msg.products) == 2
        assert msg.products[0].record_reference == "ref-001"
        assert msg.products[1].record_reference == "ref-002"

    def test_single_product_identifier_not_flattened(self):
        """Single <ProductIdentifier> creates list with one element."""
        product = make_product()

        assert isinstance(product.product_identifiers, list)
        assert len(product.product_identifiers) == 1


class TestCrossStyleEquivalence:
    """Test that ref→short and short→short paths produce identical results.

    Verifies: XML ref → Model → XML short === XML short → Model → XML short
    """

    def test_ref_to_short_equals_short_to_short(self):
        """Parsing ref XML and serializing to short should equal parsing short and serializing to short."""
        # Create reference XML
        xml_ref = """<?xml version="1.0" encoding="UTF-8"?>
        <ONIXMessage xmlns="http://ns.editeur.org/onix/3.1/reference" release="3.1">
            <Header>
                <Sender>
                    <SenderName>Test Publisher</SenderName>
                    <ContactName>John Doe</ContactName>
                    <EmailAddress>john@example.com</EmailAddress>
                </Sender>
                <SentDateTime>20231201T120000Z</SentDateTime>
                <MessageNumber>1234</MessageNumber>
            </Header>
            <Product>
                <RecordReference>test-001</RecordReference>
                <NotificationType>03</NotificationType>
                <ProductIdentifier>
                    <ProductIDType>15</ProductIDType>
                    <IDValue>9780000000001</IDValue>
                </ProductIdentifier>
                <ProductIdentifier>
                    <ProductIDType>03</ProductIDType>
                    <IDValue>0000000001</IDValue>
                </ProductIdentifier>
            </Product>
        </ONIXMessage>
        """

        # Create equivalent short XML
        xml_short = """<?xml version="1.0" encoding="UTF-8"?>
        <ONIXmessage xmlns="http://ns.editeur.org/onix/3.1/short" release="3.1">
            <header>
                <sender>
                    <x298>Test Publisher</x298>
                    <x299>John Doe</x299>
                    <j272>john@example.com</j272>
                </sender>
                <x307>20231201T120000Z</x307>
                <m180>1234</m180>
            </header>
            <product>
                <a001>test-001</a001>
                <a002>03</a002>
                <productidentifier>
                    <b221>15</b221>
                    <b244>9780000000001</b244>
                </productidentifier>
                <productidentifier>
                    <b221>03</b221>
                    <b244>0000000001</b244>
                </productidentifier>
            </product>
        </ONIXmessage>
        """

        # Path 1: XML ref → Model → XML short
        msg1 = xml_to_message(xml_ref, short_names=False)
        xml_short_from_ref = message_to_xml_string(msg1, short_names=True)

        # Path 2: XML short → Model → XML short
        msg2 = xml_to_message(xml_short, short_names=True)
        xml_short_from_short = message_to_xml_string(msg2, short_names=True)

        # Both paths should produce identical models
        assert msg1 == msg2

        # Both paths should produce identical short XML (ignoring whitespace)
        assert xml_short_from_ref.replace(" ", "").replace(
            "\n", ""
        ) == xml_short_from_short.replace(" ", "").replace("\n", "")

    def test_short_to_ref_equals_ref_to_ref(self):
        """Parsing short XML and serializing to ref should equal parsing ref and serializing to ref."""
        # Create short XML
        xml_short = """<?xml version="1.0" encoding="UTF-8"?>
        <ONIXmessage xmlns="http://ns.editeur.org/onix/3.1/short" release="3.1">
            <header>
                <sender>
                    <x298>Test Publisher</x298>
                </sender>
                <x307>20231201T120000Z</x307>
            </header>
            <product>
                <a001>test-001</a001>
                <a002>03</a002>
                <productidentifier>
                    <b221>15</b221>
                    <b244>9780000000001</b244>
                </productidentifier>
            </product>
        </ONIXmessage>
        """

        # Create equivalent reference XML
        xml_ref = """<?xml version="1.0" encoding="UTF-8"?>
        <ONIXMessage xmlns="http://ns.editeur.org/onix/3.1/reference" release="3.1">
            <Header>
                <Sender>
                    <SenderName>Test Publisher</SenderName>
                </Sender>
                <SentDateTime>20231201T120000Z</SentDateTime>
            </Header>
            <Product>
                <RecordReference>test-001</RecordReference>
                <NotificationType>03</NotificationType>
                <ProductIdentifier>
                    <ProductIDType>15</ProductIDType>
                    <IDValue>9780000000001</IDValue>
                </ProductIdentifier>
            </Product>
        </ONIXMessage>
        """

        # Path 1: XML short → Model → XML ref
        msg1 = xml_to_message(xml_short, short_names=True)
        xml_ref_from_short = message_to_xml_string(msg1, short_names=False)

        # Path 2: XML ref → Model → XML ref
        msg2 = xml_to_message(xml_ref, short_names=False)
        xml_ref_from_ref = message_to_xml_string(msg2, short_names=False)

        # Both paths should produce identical models
        assert msg1 == msg2

        # Both paths should produce identical reference XML (ignoring whitespace)
        assert xml_ref_from_short.replace(" ", "").replace(
            "\n", ""
        ) == xml_ref_from_ref.replace(" ", "").replace("\n", "")

    def test_bidirectional_conversion_with_complex_message(self):
        """Test ref↔short conversion with complex message including multiple elements."""
        # Create a complex model
        msg = ONIXMessage(
            release="3.1",
            header=Header(
                sender=Sender(
                    sender_name="Complex Publisher",
                    contact_name="Jane Smith",
                    telephone_number="+1234567890",
                    email_address="jane@example.com",
                ),
                sent_date_time="20231215T153045Z",
                message_number="5678",
                message_repeat="2",
            ),
            products=[
                make_product(
                    record_reference="complex-001",
                    notification_type="03",
                    product_identifiers=[
                        ProductIdentifier(
                            product_id_type="15", id_value="9781234567890"
                        ),
                        ProductIdentifier(product_id_type="03", id_value="1234567890"),
                    ],
                ),
                make_product(
                    record_reference="complex-002",
                    notification_type="04",
                ),
            ],
        )

        # Convert to both formats
        xml_ref = message_to_xml_string(msg, short_names=False)
        xml_short = message_to_xml_string(msg, short_names=True)

        # Parse both back
        msg_from_ref = xml_to_message(xml_ref, short_names=False)
        msg_from_short = xml_to_message(xml_short, short_names=True)

        # All models should be identical
        assert msg == msg_from_ref == msg_from_short

        # Cross-convert and verify
        xml_short_from_ref = message_to_xml_string(msg_from_ref, short_names=True)
        xml_ref_from_short = message_to_xml_string(msg_from_short, short_names=False)

        # Parse cross-converted XML
        msg_cross_1 = xml_to_message(xml_short_from_ref, short_names=True)
        msg_cross_2 = xml_to_message(xml_ref_from_short, short_names=False)

        # All should still be identical
        assert msg == msg_cross_1 == msg_cross_2
