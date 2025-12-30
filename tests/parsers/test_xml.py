"""Tests for XML parsing and serialization internals."""

from pathlib import Path

from lxml import etree

from onix import ONIXMessage
from onix.parsers.xml import (
    _dict_to_element,
    _element_to_dict,
    _normalize_input,
    _parse_xml_string,
    message_to_xml,
    message_to_xml_string,
    xml_to_message,
)

from ..conftest import make_header, make_product


class TestXMLNormalizationAndElementHandling:
    """Tests for XML input normalization and element conversion."""

    def test_message_to_xml_no_product(self):
        """XML serialization includes NoProduct element when set."""
        msg = ONIXMessage(release="3.1", Header=make_header())

        # Explicitly set no_product
        msg.no_product = True
        elem = message_to_xml(msg)
        # Should contain NoProduct element
        tags = [etree.QName(child).localname for child in elem]
        assert "NoProduct" in tags

    def test_dict_to_element_namespace_and_short_names(self):
        """Element creation respects namespace and short name settings."""
        data = {"sender": {"sender_name": "Acme"}}
        # Use short names and a namespace
        elem = _dict_to_element(
            "Header", data, short_names=True, namespace="http://ns.test/"
        )
        # Tag should be namespaced and localname Header (short name applied on child keys)
        assert etree.QName(elem).namespace == "http://ns.test/"
        child = elem.find("{http://ns.test/}sender")
        assert child is not None

    def test_normalize_input_iterable_combines_products(self):
        """Parsing multiple XML elements combines products into one message."""
        # Two minimal messages with one product each
        xml1 = _parse_xml_string(
            """<ONIXMessage><Header><Sender><SenderName>A</SenderName></Sender><SentDateTime>20231201</SentDateTime></Header><Product><RecordReference>r1</RecordReference><NotificationType>03</NotificationType><ProductIdentifier><ProductIDType>15</ProductIDType><IDValue>9780000000001</IDValue></ProductIdentifier></Product></ONIXMessage>"""
        )
        xml2 = _parse_xml_string(
            """<ONIXMessage><Header><Sender><SenderName>B</SenderName></Sender><SentDateTime>20231201</SentDateTime></Header><Product><RecordReference>r2</RecordReference><NotificationType>03</NotificationType><ProductIdentifier><ProductIDType>15</ProductIDType><IDValue>9780000000002</IDValue></ProductIdentifier></Product></ONIXMessage>"""
        )

        msg = xml_to_message([xml1, xml2])
        assert len(msg.products) == 2
        assert {p.record_reference for p in msg.products} == {"r1", "r2"}

    def test_message_to_xml_string_options(self, tmp_path: Path):
        """XML string serialization respects declaration and file options."""
        # Minimal valid message
        msg = ONIXMessage(
            release="3.1",
            Header=make_header(),
            Product=[make_product(RecordReference="r")],
        )

        xml_decl = message_to_xml_string(msg, xml_declaration=True)
        assert xml_decl.strip().startswith("<?xml")

        xml_no_decl = message_to_xml_string(msg, xml_declaration=False)
        assert not xml_no_decl.strip().startswith("<?xml")

        # Save to file path via _normalize_input string path handling
        p = tmp_path / "m.xml"
        p.write_text(xml_no_decl)
        loaded = _normalize_input(str(p))
        assert etree.QName(loaded).localname == "ONIXMessage"

    def test_normalize_input_element_passthrough(self):
        """_normalize_input returns lxml Element unchanged."""
        # Create an element and pass it directly
        elem = etree.Element("Test")
        result = _normalize_input(elem)
        assert result is elem  # Should return the same object

    def test_dict_to_element_no_namespace(self):
        """_dict_to_element creates elements without namespace."""
        data = {"sender_name": "Test"}
        elem = _dict_to_element("Sender", data)
        assert elem.tag == "Sender"  # No namespace
        name = elem.find("SenderName")
        assert name is not None
        assert name.text == "Test"

    def test_dict_to_element_with_attributes(self):
        """_dict_to_element sets datestamp/sourcename/sourcetype as attributes."""
        data = {
            "datestamp": "20231201",
            "sourcename": "TestSource",
            "sourcetype": "01",
            "sender_name": "Test",
        }
        elem = _dict_to_element("Header", data)
        assert elem.get("datestamp") == "20231201"
        assert elem.get("sourcename") == "TestSource"
        assert elem.get("sourcetype") == "01"
        name = elem.find("SenderName")
        assert name is not None
        assert name.text == "Test"

    def test_dict_to_element_list_items_no_namespace(self):
        """_dict_to_element creates list item elements without namespace."""
        data = {"sender_identifiers": [{"name_id_type": "01", "id_value": "123"}]}
        elem = _dict_to_element("Sender", data)
        # List items are direct children with the singular tag
        identifier_elem = elem.find("SenderIdentifier")
        assert identifier_elem is not None
        assert identifier_elem.tag == "SenderIdentifier"  # No namespace

    def test_dict_to_element_list_strings_no_namespace(self):
        """_dict_to_element creates list string elements without namespace."""
        data = {"contributor_roles": ["A01", "B01"]}
        elem = _dict_to_element("Contributor", data)
        # List string items are direct children
        role_elems = elem.findall("ContributorRoles")
        assert len(role_elems) == 2
        assert all(
            elem.tag == "ContributorRoles" for elem in role_elems
        )  # No namespace
        assert role_elems[0].text == "A01"
        assert role_elems[1].text == "B01"

    def test_element_to_dict_empty_no_product(self):
        """_element_to_dict handles empty NoProduct elements."""
        xml_str = """<ONIXMessage xmlns="http://ns.editeur.org/onix/3.1/reference">
            <Header><Sender><SenderName>Test</SenderName></Sender><SentDateTime>20231201</SentDateTime></Header>
            <NoProduct/>
        </ONIXMessage>"""
        root = _parse_xml_string(xml_str)
        data = _element_to_dict(root)
        assert data["no_product"] is True

    def test_xml_to_message_ensures_products_is_list(self):
        """xml_to_message ensures products is always a list."""
        from unittest.mock import patch

        # Mock _element_to_dict to return data with products as non-list
        mock_data = {
            "header": {
                "sender": {"sender_name": "Test"},
                "sent_date_time": "20231201T120000Z",
            },
            "products": {  # Not a list
                "record_reference": "test",
                "notification_type": "03",
                "product_identifiers": [{"product_id_type": "15", "id_value": "123"}],
            },
        }

        with patch("onix.parsers.xml._element_to_dict", return_value=mock_data):
            with patch("onix.parsers.xml._normalize_input", return_value=None):
                msg = xml_to_message("dummy")
                assert isinstance(msg.products, list)
                assert len(msg.products) == 1
