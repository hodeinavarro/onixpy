"""Tests for parser edge cases and less common input types."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest
from pydantic import ValidationError

from onix.parsers.json import json_to_message
from onix.parsers.xml import xml_to_message


class TestJSONParserEdgeCases:
    """Test JSON parser with edge cases."""

    def test_pathlike_input_json(self):
        """Test JSON parser with PathLike input objects."""
        # Create a temporary JSON file

        test_data = {
            "header": {
                "sender": {"sender_name": "Test Publisher"},
                "sent_date_time": "20231201T120000Z",
            },
            "products": [
                {
                    "record_reference": "test-ref",
                    "notification_type": "03",
                    "product_identifiers": [
                        {"product_id_type": "15", "id_value": "9780000000001"}
                    ],
                }
            ],
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(test_data, f)
            temp_path = Path(f.name)

        try:
            # Test with Path object (PathLike)
            msg = json_to_message(temp_path)
            assert msg.products[0].record_reference == "test-ref"

            # Test with string path
            msg2 = json_to_message(str(temp_path))
            assert msg2.products[0].record_reference == "test-ref"
        finally:
            temp_path.unlink()

    def test_empty_iterable_input_json(self):
        """Test JSON parser with empty iterable input."""
        # Empty list should raise ValidationError due to missing required header fields
        with pytest.raises(ValidationError):
            json_to_message([])


class TestXMLParserEdgeCases:
    """Test XML parser with edge cases."""

    def test_single_product_handling(self):
        """Test that single Product elements get converted to lists."""
        xml_str = """<?xml version="1.0" encoding="UTF-8"?>
<ONIXMessage xmlns="http://ns.editeur.org/onix/3.1/reference">
    <Header>
        <Sender>
            <SenderName>Test Publisher</SenderName>
        </Sender>
        <SentDateTime>20231201T120000Z</SentDateTime>
    </Header>
    <Product>
        <RecordReference>test-ref</RecordReference>
        <NotificationType>03</NotificationType>
        <ProductIdentifier>
            <ProductIDType>15</ProductIDType>
            <IDValue>9780000000001</IDValue>
        </ProductIdentifier>
    </Product>
</ONIXMessage>"""

        msg = xml_to_message(xml_str)
        assert isinstance(msg.products, list)
        assert len(msg.products) == 1
        assert msg.products[0].record_reference == "test-ref"

    def test_pathlike_input_xml(self):
        """Test XML parser with PathLike input objects."""

        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ONIXMessage xmlns="http://ns.editeur.org/onix/3.1/reference">
    <Header>
        <Sender>
            <SenderName>Test Publisher</SenderName>
        </Sender>
        <SentDateTime>20231201T120000Z</SentDateTime>
    </Header>
    <Product>
        <RecordReference>test-ref</RecordReference>
        <NotificationType>03</NotificationType>
        <ProductIdentifier>
            <ProductIDType>15</ProductIDType>
            <IDValue>9780000000001</IDValue>
        </ProductIdentifier>
    </Product>
</ONIXMessage>"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False) as f:
            f.write(xml_content)
            temp_path = Path(f.name)

        try:
            # Test with Path object (PathLike)
            msg = xml_to_message(temp_path)
            assert msg.products[0].record_reference == "test-ref"

            # Test with string path
            msg2 = xml_to_message(str(temp_path))
            assert msg2.products[0].record_reference == "test-ref"
        finally:
            temp_path.unlink()

    def test_empty_iterable_input_xml(self):
        """Test XML parser with empty iterable input."""
        # Empty list should raise ValidationError due to missing required header fields
        with pytest.raises(ValidationError):
            xml_to_message([])
