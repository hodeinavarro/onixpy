from pathlib import Path

from lxml import etree

from onix import ONIXMessage
from onix.parsers.xml import (
    _dict_to_element,
    _normalize_input,
    _parse_xml_string,
    message_to_xml,
    message_to_xml_string,
    xml_to_message,
)

from .conftest import make_header, make_product


class TestParsersXMLExtra:
    def test_message_to_xml_no_product(self):
        msg = ONIXMessage(release="3.1", header=make_header())

        # Explicitly set no_product
        msg.no_product = True
        elem = message_to_xml(msg)
        # Should contain NoProduct element
        tags = [etree.QName(child).localname for child in elem]
        assert "NoProduct" in tags

    def test_dict_to_element_namespace_and_short_names(self):
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
        # Minimal valid message
        msg = ONIXMessage(
            release="3.1",
            header=make_header(),
            products=[make_product(record_reference="r")],
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
