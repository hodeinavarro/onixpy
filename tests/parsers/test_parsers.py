"""Tests for ONIX parsers (JSON and XML)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from onix import Header, ONIXMessage, Product
from onix.parsers import (
    json_to_message,
    message_to_dict,
    message_to_json,
    message_to_xml,
    message_to_xml_string,
    save_json,
    save_xml,
    to_reference_tag,
    to_short_tag,
    xml_to_message,
)

from ..conftest import make_header, make_header_dict, make_product, make_product_dict


class TestTagResolver:
    """Tests for tag name resolution."""

    def test_to_short_tag_known_tags(self):
        """Known reference tags should convert to short tags."""
        assert to_short_tag("ONIXMessage") == "ONIXmessage"
        assert to_short_tag("Header") == "header"
        assert to_short_tag("Product") == "product"
        assert to_short_tag("NoProduct") == "x507"

    def test_to_short_tag_unknown_tag(self):
        """Unknown tags should pass through unchanged."""
        assert to_short_tag("UnknownTag") == "UnknownTag"

    def test_to_reference_tag_known_tags(self):
        """Known short tags should convert to reference tags."""
        assert to_reference_tag("ONIXmessage") == "ONIXMessage"
        assert to_reference_tag("header") == "Header"
        assert to_reference_tag("product") == "Product"
        assert to_reference_tag("x507") == "NoProduct"

    def test_to_reference_tag_unknown_tag(self):
        """Unknown tags should pass through unchanged."""
        assert to_reference_tag("unknown") == "unknown"


class TestJSONParser:
    """Tests for JSON parsing."""

    def test_parse_from_dict(self):
        """Parse message from a dict object."""
        data = {"header": make_header_dict(), "products": []}
        msg = json_to_message(data)

        assert isinstance(msg, ONIXMessage)
        assert isinstance(msg.header, Header)
        assert msg.products == []

    def test_parse_from_dict_with_products(self):
        """Parse message with products from dict."""
        data = {
            "header": make_header_dict(),
            "products": [
                make_product_dict(record_reference="ref-001"),
                make_product_dict(record_reference="ref-002"),
            ],
        }
        msg = json_to_message(data)

        assert len(msg.products) == 2
        assert all(isinstance(p, Product) for p in msg.products)

    def test_parse_from_file(self, tmp_path: Path):
        """Parse message from a JSON file."""
        json_file = tmp_path / "message.json"
        data = {"header": make_header_dict(), "products": [make_product_dict()]}
        json_file.write_text(json.dumps(data))

        msg = json_to_message(str(json_file))

        assert isinstance(msg, ONIXMessage)
        assert len(msg.products) == 1

    def test_parse_from_file_not_found(self):
        """Raise error for non-existent file."""
        with pytest.raises(FileNotFoundError):
            json_to_message("/nonexistent/path.json")

    def test_parse_from_iterable(self):
        """Parse and combine messages from iterable of dicts."""
        header1 = make_header_dict()
        header1["message_note"] = "Source1"
        header2 = make_header_dict()
        header2["message_note"] = "Source2"
        messages = [
            {
                "header": header1,
                "products": [make_product_dict(record_reference="ref-001")],
            },
            {
                "header": header2,
                "products": [
                    make_product_dict(record_reference="ref-002"),
                    make_product_dict(record_reference="ref-003"),
                ],
            },
        ]
        msg = json_to_message(iter(messages))

        # Uses first message's header, combines all products
        assert msg.header.message_note == "Source1"
        assert len(msg.products) == 3

    def test_parse_empty_iterable(self):
        """Empty iterable should fail validation (no valid header)."""
        with pytest.raises(Exception):  # ValidationError from Pydantic
            json_to_message(iter([]))


class TestJSONSerializer:
    """Tests for JSON serialization."""

    def test_message_to_dict(self):
        """Convert message to dict."""
        msg = ONIXMessage(Header=make_header(), Product=[make_product()])
        data = message_to_dict(msg)

        assert "header" in data
        assert "products" in data
        assert len(data["products"]) == 1

    def test_message_to_json(self):
        """Serialize message to JSON string."""
        msg = ONIXMessage(Header=make_header(), Product=[])
        json_str = message_to_json(msg)

        parsed = json.loads(json_str)
        assert "header" in parsed

    def test_save_json(self, tmp_path: Path):
        """Save message to JSON file."""
        msg = ONIXMessage(Header=make_header(), Product=[make_product()])
        json_file = tmp_path / "output.json"

        save_json(msg, json_file)

        assert json_file.exists()
        data = json.loads(json_file.read_text())
        assert len(data["products"]) == 1

    def test_roundtrip_json(self):
        """JSON roundtrip preserves data."""
        original = ONIXMessage(
            release="3.1",
            Header=make_header(message_note="TestSource"),
            Product=[
                make_product(RecordReference="ref-001"),
                make_product(RecordReference="ref-002"),
            ],
        )

        json_str = message_to_json(original)
        restored = json_to_message(json.loads(json_str))

        assert restored.release == original.release
        assert restored.header.message_note == original.header.message_note
        assert len(restored.products) == len(original.products)

    def test_pydantic_json_roundtrip_equality(self):
        """Pydantic model -> JSON -> Pydantic yields equal models."""
        a = ONIXMessage(release="3.1", Header=make_header(), Product=[make_product()])
        json_str = message_to_json(a)
        b = json_to_message(json.loads(json_str))

        assert a.model_dump() == b.model_dump()


class TestXMLParser:
    """Tests for XML parsing."""

    def test_parse_from_string(self):
        """Parse message from XML string."""
        xml_str = """<?xml version="1.0"?>
        <ONIXMessage release="3.1">
            <Header>
                <Sender>
                    <SenderName>Test Publisher</SenderName>
                </Sender>
                <SentDateTime>20231201T120000Z</SentDateTime>
            </Header>
        </ONIXMessage>
        """
        msg = xml_to_message(xml_str)

        assert isinstance(msg, ONIXMessage)
        assert msg.release == "3.1"

    def test_parse_from_string_with_products(self):
        """Parse message with products from XML string."""
        xml_str = """<?xml version="1.0"?>
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
        </ONIXMessage>
        """
        msg = xml_to_message(xml_str)

        assert len(msg.products) == 2

    def test_parse_from_file(self, tmp_path: Path):
        """Parse message from XML file."""
        xml_file = tmp_path / "message.xml"
        xml_file.write_text("""<?xml version="1.0"?>
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
        </ONIXMessage>
        """)

        msg = xml_to_message(str(xml_file))

        assert isinstance(msg, ONIXMessage)
        assert len(msg.products) == 1

    def test_parse_from_file_not_found(self):
        """Raise error for non-existent file."""
        with pytest.raises(FileNotFoundError):
            xml_to_message("/nonexistent/path.xml")

    def test_parse_from_pathlike_not_found(self):
        """Raise error for non-existent PathLike file."""
        with pytest.raises(FileNotFoundError):
            xml_to_message(Path("/nonexistent/path.xml"))


class TestXMLSerializer:
    """Tests for XML serialization."""

    def test_message_to_xml(self):
        """Convert message to XML Element."""
        from lxml.etree import QName

        msg = ONIXMessage(Header=make_header(), Product=[make_product()])
        root = message_to_xml(msg)

        assert QName(root.tag).localname == "ONIXMessage"
        assert root.get("release") == "3.1"

    def test_message_to_xml_string(self):
        """Serialize message to XML string."""
        msg = ONIXMessage(Header=make_header(), Product=[])
        xml_str = message_to_xml_string(msg)

        assert "ONIXMessage" in xml_str
        assert "Header" in xml_str

    def test_message_to_xml_with_short_names(self):
        """Serialize with short tag names."""
        from lxml.etree import QName

        msg = ONIXMessage(Header=make_header(), Product=[])
        root = message_to_xml(msg, short_names=True)

        assert QName(root.tag).localname == "ONIXmessage"

    def test_save_xml(self, tmp_path: Path):
        """Save message to XML file."""
        msg = ONIXMessage(Header=make_header(), Product=[make_product()])
        xml_file = tmp_path / "output.xml"

        save_xml(msg, xml_file)

        assert xml_file.exists()
        content = xml_file.read_text()
        assert "ONIXMessage" in content
        assert "Product" in content

    def test_roundtrip_xml(self):
        """XML roundtrip preserves data."""
        original = ONIXMessage(
            release="3.1",
            Header=make_header(),
            Product=[
                make_product(RecordReference="ref-001"),
                make_product(RecordReference="ref-002"),
            ],
        )

        xml_str = message_to_xml_string(original)
        restored = xml_to_message(xml_str)

        assert restored.release == original.release
        assert len(restored.products) == len(original.products)


class TestShortNamesFlag:
    """Tests for short_names flag behavior."""

    def test_json_parse_with_short_names(self):
        """Parse JSON with short tag names."""
        data = {"header": make_header_dict(), "products": []}
        msg = json_to_message(data, short_names=True)

        assert isinstance(msg, ONIXMessage)

    def test_json_serialize_with_short_names(self):
        """Serialize JSON with short tag names."""
        msg = ONIXMessage(Header=make_header(), Product=[])
        data = message_to_dict(msg, short_names=True)

        # Keys should be converted to short names where applicable
        assert isinstance(data, dict)

    def test_xml_parse_with_short_names(self):
        """Parse XML expecting short tag names."""
        xml_str = """<?xml version="1.0"?>
        <ONIXmessage release="3.1">
            <header>
                <sender>
                    <SenderName>Test Publisher</SenderName>
                </sender>
                <SentDateTime>20231201T120000Z</SentDateTime>
            </header>
        </ONIXmessage>
        """
        msg = xml_to_message(xml_str, short_names=True)

        assert isinstance(msg, ONIXMessage)

    def test_xml_serialize_with_short_names(self):
        """Serialize XML with short tag names."""
        msg = ONIXMessage(Header=make_header(), Product=[])
        xml_str = message_to_xml_string(msg, short_names=True)

        assert "ONIXmessage" in xml_str
        assert "header" in xml_str
