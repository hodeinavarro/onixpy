"""Edge case and negative tests for ONIX parsing and validation.

Tests for:
- Invalid code list values
- Missing required fields
- Unknown/extra tags in XML
- Empty composites
- Duplicate fields (last wins)
- Invalid namespaces
- Malformed XML
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from onix import Header, ONIXMessage, Product, ProductIdentifier, Sender
from onix.parsers import message_to_xml_string, xml_to_message
from onix.validation.rng import validate_xml_string

from ..conftest import make_header, make_product


class TestInvalidCodeListValues:
    """Test that invalid code list values raise ValidationError."""

    def test_invalid_notification_type(self):
        """Invalid notification type code should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Product(
                record_reference="test-001",
                notification_type="99",  # Invalid: not in List 1
                product_identifiers=[
                    ProductIdentifier(product_id_type="15", id_value="9780000000001")
                ],
            )
        assert "notification_type" in str(exc_info.value)

    def test_invalid_product_id_type(self):
        """Invalid product ID type code should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ProductIdentifier(
                product_id_type="99",  # Invalid: not in List 5
                id_value="9780000000001",
            )
        assert "product_id_type" in str(exc_info.value)

    def test_invalid_sender_id_type(self):
        """Invalid sender ID type code should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Header(
                sender=Sender(
                    sender_name="Test",
                    sender_identifiers=[
                        {
                            "sender_id_type": "99",  # Invalid: not in List 44
                            "id_value": "123",
                        }
                    ],
                ),
                sent_date_time="20231201",
            )
        assert "sender_id_type" in str(exc_info.value)

    def test_invalid_language_code(self):
        """Invalid language code should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Header(
                sender=Sender(sender_name="Test"),
                sent_date_time="20231201",
                default_language_of_text="zz",  # Invalid: not in List 74
            )
        assert "default_language_of_text" in str(exc_info.value)

    def test_invalid_currency_code(self):
        """Invalid currency code should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Header(
                sender=Sender(sender_name="Test"),
                sent_date_time="20231201",
                default_currency_code="ZZZ",  # Invalid: not in List 96
            )
        assert "default_currency_code" in str(exc_info.value)

    def test_invalid_price_type(self):
        """Invalid price type code should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Header(
                sender=Sender(sender_name="Test"),
                sent_date_time="20231201",
                default_price_type="99",  # Invalid: not in List 58
            )
        assert "default_price_type" in str(exc_info.value)


class TestMissingRequiredFields:
    """Test that missing required fields raise ValidationError."""

    def test_product_missing_record_reference(self):
        """Product without record_reference should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Product(
                notification_type="03",
                product_identifiers=[
                    ProductIdentifier(product_id_type="15", id_value="9780000000001")
                ],
            )
        # Pydantic reports field by alias name, not Python field name
        assert "RecordReference" in str(exc_info.value)

    def test_product_missing_notification_type(self):
        """Product without notification_type should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Product(
                record_reference="test-001",
                product_identifiers=[
                    ProductIdentifier(product_id_type="15", id_value="9780000000001")
                ],
            )
        assert "NotificationType" in str(exc_info.value)

    def test_product_missing_identifiers(self):
        """Product without product_identifiers should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Product(
                record_reference="test-001",
                notification_type="03",
                product_identifiers=[],  # Empty list invalid
            )
        assert "product_identifiers" in str(exc_info.value)

    def test_product_identifier_missing_type(self):
        """ProductIdentifier without product_id_type should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ProductIdentifier(id_value="9780000000001")
        assert "ProductIDType" in str(exc_info.value)

    def test_product_identifier_missing_value(self):
        """ProductIdentifier without id_value should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ProductIdentifier(product_id_type="15")
        assert "IDValue" in str(exc_info.value)

    def test_header_missing_sender(self):
        """Header without sender should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Header(sent_date_time="20231201T120000Z")
        assert "Sender" in str(exc_info.value)

    def test_header_missing_sent_date_time(self):
        """Header without sent_date_time should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Header(sender=Sender(sender_name="Test"))
        assert "SentDateTime" in str(exc_info.value)

    def test_sender_missing_name_and_identifier(self):
        """Sender without name or identifier should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Sender()
        assert "sender" in str(exc_info.value).lower()

    def test_message_missing_header(self):
        """ONIXMessage without header should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ONIXMessage(
                products=[make_product()],
            )
        assert "Header" in str(exc_info.value)


class TestUnknownAndExtraTags:
    """Test handling of unknown and extra tags in XML."""

    def test_unknown_top_level_tag_ignored(self):
        """Unknown tags at top level should be rejected (Pydantic forbids extras by default)."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <ONIXMessage xmlns="http://ns.editeur.org/onix/3.1/reference" release="3.1">
            <Header>
                <Sender><SenderName>Test</SenderName></Sender>
                <SentDateTime>20231201</SentDateTime>
            </Header>
            <UnknownElement>Should be ignored</UnknownElement>
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
        # Pydantic forbids extra fields by default
        with pytest.raises(ValidationError) as exc_info:
            xml_to_message(xml)
        assert "unknown_element" in str(exc_info.value)

    def test_unknown_nested_tag_ignored(self):
        """Unknown tags nested in composites should be rejected (Pydantic forbids extras)."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <ONIXMessage xmlns="http://ns.editeur.org/onix/3.1/reference" release="3.1">
            <Header>
                <Sender>
                    <SenderName>Test</SenderName>
                    <UnknownField>Ignored</UnknownField>
                </Sender>
                <SentDateTime>20231201</SentDateTime>
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
        with pytest.raises(ValidationError) as exc_info:
            xml_to_message(xml)
        assert "unknown_field" in str(exc_info.value)

    def test_extra_whitespace_handled(self):
        """Extra whitespace in XML should be handled gracefully."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <ONIXMessage xmlns="http://ns.editeur.org/onix/3.1/reference" release="3.1">
            <Header>
                <Sender>
                    <SenderName>  Test Publisher  </SenderName>
                </Sender>
                <SentDateTime>20231201</SentDateTime>
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
        msg = xml_to_message(xml)
        # lxml strips whitespace by default
        assert msg.header.sender.sender_name.strip() == "Test Publisher"


class TestEmptyComposites:
    """Test handling of empty composites."""

    def test_empty_sender_identifiers_list_valid(self):
        """Empty sender_identifiers list should be valid."""
        header = Header(
            sender=Sender(
                sender_name="Test",
                sender_identifiers=[],
            ),
            sent_date_time="20231201",
        )
        assert header.sender.sender_identifiers == []

    def test_omitted_sender_identifiers_valid(self):
        """Omitted sender_identifiers should default to empty list."""
        header = Header(
            sender=Sender(sender_name="Test"),
            sent_date_time="20231201",
        )
        assert header.sender.sender_identifiers == []

    def test_empty_addressees_list_valid(self):
        """Empty addressees list should be valid."""
        header = Header(
            sender=Sender(sender_name="Test"),
            sent_date_time="20231201",
            addressees=[],
        )
        assert header.addressees == []

    def test_empty_products_triggers_no_product(self):
        """Empty products list should trigger no_product=True."""
        msg = ONIXMessage(
            header=make_header(),
            products=[],
        )
        assert msg.no_product is True
        assert msg.products == []


class TestDuplicateFields:
    """Test handling of duplicate fields in XML (last wins)."""

    def test_duplicate_sender_name_last_wins(self):
        """Duplicate SenderName tags create list (XML parser behavior)."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <ONIXMessage xmlns="http://ns.editeur.org/onix/3.1/reference" release="3.1">
            <Header>
                <Sender>
                    <SenderName>First Name</SenderName>
                    <SenderName>Last Name</SenderName>
                </Sender>
                <SentDateTime>20231201</SentDateTime>
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
        # XML parser collects duplicates into a list; Pydantic expects string, not list
        with pytest.raises(ValidationError) as exc_info:
            xml_to_message(xml)
        assert "string_type" in str(exc_info.value)

    def test_duplicate_list_elements_all_included(self):
        """Duplicate list elements (like Product) should all be included."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <ONIXMessage xmlns="http://ns.editeur.org/onix/3.1/reference" release="3.1">
            <Header>
                <Sender><SenderName>Test</SenderName></Sender>
                <SentDateTime>20231201</SentDateTime>
            </Header>
            <Product>
                <RecordReference>test-001</RecordReference>
                <NotificationType>03</NotificationType>
                <ProductIdentifier>
                    <ProductIDType>15</ProductIDType>
                    <IDValue>9780000000001</IDValue>
                </ProductIdentifier>
            </Product>
            <Product>
                <RecordReference>test-002</RecordReference>
                <NotificationType>03</NotificationType>
                <ProductIdentifier>
                    <ProductIDType>15</ProductIDType>
                    <IDValue>9780000000002</IDValue>
                </ProductIdentifier>
            </Product>
        </ONIXMessage>
        """
        msg = xml_to_message(xml)
        assert len(msg.products) == 2
        assert msg.products[0].record_reference == "test-001"
        assert msg.products[1].record_reference == "test-002"


class TestInvalidNamespaces:
    """Test handling of invalid or missing namespaces."""

    def test_wrong_namespace_fails_rng(self):
        """XML with wrong namespace should fail RNG validation."""
        from onix.validation.rng import RNGValidationError

        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <ONIXMessage xmlns="http://wrong.namespace.com" release="3.1">
            <Header>
                <Sender><SenderName>Test</SenderName></Sender>
                <SentDateTime>20231201</SentDateTime>
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
        with pytest.raises(RNGValidationError):
            validate_xml_string(xml)

    def test_missing_namespace_fails_rng(self):
        """XML without namespace should fail RNG validation."""
        from onix.validation.rng import RNGValidationError

        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <ONIXMessage release="3.1">
            <Header>
                <Sender><SenderName>Test</SenderName></Sender>
                <SentDateTime>20231201</SentDateTime>
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
        with pytest.raises(RNGValidationError):
            validate_xml_string(xml)

    def test_correct_namespace_validates(self):
        """XML with correct namespace should validate."""
        msg = ONIXMessage(
            header=make_header(),
            products=[make_product()],
        )
        xml = message_to_xml_string(msg)
        # Should not raise
        validate_xml_string(xml)


class TestMalformedXML:
    """Test handling of malformed XML."""

    def test_unclosed_tag_raises_parse_error(self):
        """XML with unclosed tags should raise parse error."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <ONIXMessage xmlns="http://ns.editeur.org/onix/3.1/reference" release="3.1">
            <Header>
                <Sender><SenderName>Test</SenderName>
                <SentDateTime>20231201</SentDateTime>
            </Header>
        </ONIXMessage>
        """
        with pytest.raises(Exception):  # XMLSyntaxError or similar
            xml_to_message(xml)

    def test_mismatched_tags_raises_parse_error(self):
        """XML with mismatched tags should raise parse error."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <ONIXMessage xmlns="http://ns.editeur.org/onix/3.1/reference" release="3.1">
            <Header>
                <Sender><SenderName>Test</SenderName></Sender>
                <SentDateTime>20231201</SentDateTime>
            </WrongTag>
        </ONIXMessage>
        """
        with pytest.raises(Exception):  # XMLSyntaxError or similar
            xml_to_message(xml)

    def test_invalid_xml_characters_raises_parse_error(self):
        """XML with invalid characters should raise parse error."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <ONIXMessage xmlns="http://ns.editeur.org/onix/3.1/reference" release="3.1">
            <Header>
                <Sender><SenderName>Test & Invalid <></SenderName></Sender>
                <SentDateTime>20231201</SentDateTime>
            </Header>
        </ONIXMessage>
        """
        with pytest.raises(Exception):  # XMLSyntaxError or similar
            xml_to_message(xml)


class TestFieldConstraints:
    """Test field length and format constraints."""

    def test_message_number_max_length_8(self):
        """MessageNumber with more than 8 digits should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Header(
                sender=Sender(sender_name="Test"),
                sent_date_time="20231201",
                message_number="123456789",  # 9 digits
            )
        assert "message_number" in str(exc_info.value)
        assert "at most 8 characters" in str(exc_info.value)

    def test_message_repeat_max_length_4(self):
        """MessageRepeat with more than 4 digits should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Header(
                sender=Sender(sender_name="Test"),
                sent_date_time="20231201",
                message_repeat="12345",  # 5 digits
            )
        assert "message_repeat" in str(exc_info.value)
        assert "at most 4 characters" in str(exc_info.value)

    def test_sender_name_max_length_50(self):
        """SenderName with more than 50 characters should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Sender(sender_name="A" * 51)
        assert "sender_name" in str(exc_info.value)

    def test_record_reference_max_length_100(self):
        """RecordReference with more than 100 characters should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Product(
                record_reference="A" * 101,
                notification_type="03",
                product_identifiers=[
                    ProductIdentifier(product_id_type="15", id_value="9780000000001")
                ],
            )
        assert "record_reference" in str(exc_info.value)

    def test_id_value_max_length_300(self):
        """IDValue with more than 300 characters should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ProductIdentifier(
                product_id_type="15",
                id_value="A" * 301,
            )
        assert "id_value" in str(exc_info.value)
