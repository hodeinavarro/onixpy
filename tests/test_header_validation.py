"""Tests for ONIX Header validation rules.

Tests validators for SenderIdentifier, AddresseeIdentifier, and Header
fields to ensure they enforce ONIX specification requirements.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from onix import Header, Sender
from onix.header import AddresseeIdentifier, SenderIdentifier


class TestSenderIdentifierValidation:
    """Tests for SenderIdentifier validators."""

    def test_proprietary_with_id_type_name_valid(self):
        """Proprietary SenderIDType with IDTypeName should validate."""
        identifier = SenderIdentifier(
            sender_id_type="01",
            id_type_name="MyScheme",
            id_value="12345",
        )
        assert identifier.sender_id_type == "01"
        assert identifier.id_type_name == "MyScheme"
        assert identifier.id_value == "12345"

    def test_proprietary_without_id_type_name_raises_error(self):
        """Proprietary SenderIDType without IDTypeName should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            SenderIdentifier(
                sender_id_type="01",
                id_value="12345",
            )

        errors = exc_info.value.errors()
        assert any(
            "IDTypeName is required for proprietary SenderIDType '01'" in str(e)
            for e in errors
        )

    def test_non_proprietary_without_id_type_name_valid(self):
        """Non-proprietary SenderIDType without IDTypeName should validate."""
        identifier = SenderIdentifier(
            sender_id_type="16",  # ISNI
            id_value="0000000121032683",
        )
        assert identifier.sender_id_type == "16"
        assert identifier.id_type_name is None
        assert identifier.id_value == "0000000121032683"

    def test_invalid_list_44_code_raises_error(self):
        """Invalid List 44 code should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            SenderIdentifier(
                sender_id_type="99",  # Invalid code
                id_value="12345",
            )

        errors = exc_info.value.errors()
        assert any("Invalid SenderIDType" in str(e) for e in errors)
        assert any("not a valid List 44 code" in str(e) for e in errors)

    def test_empty_string_id_type_name_treated_as_none(self):
        """Empty string for id_type_name should be normalized to None by ONIXModel."""
        # This tests that empty-string normalization works before validators run
        with pytest.raises(ValidationError) as exc_info:
            SenderIdentifier(
                sender_id_type="01",
                id_type_name="",  # Empty string normalized to None
                id_value="12345",
            )

        errors = exc_info.value.errors()
        assert any(
            "IDTypeName is required for proprietary SenderIDType '01'" in str(e)
            for e in errors
        )


class TestAddresseeIdentifierValidation:
    """Tests for AddresseeIdentifier validators."""

    def test_proprietary_with_id_type_name_valid(self):
        """Proprietary AddresseeIDType with IDTypeName should validate."""
        identifier = AddresseeIdentifier(
            addressee_id_type="01",
            id_type_name="CompanyScheme",
            id_value="ABC123",
        )
        assert identifier.addressee_id_type == "01"
        assert identifier.id_type_name == "CompanyScheme"
        assert identifier.id_value == "ABC123"

    def test_proprietary_without_id_type_name_raises_error(self):
        """Proprietary AddresseeIDType without IDTypeName should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            AddresseeIdentifier(
                addressee_id_type="01",
                id_value="ABC123",
            )

        errors = exc_info.value.errors()
        assert any(
            "IDTypeName is required for proprietary AddresseeIDType '01'" in str(e)
            for e in errors
        )

    def test_non_proprietary_without_id_type_name_valid(self):
        """Non-proprietary AddresseeIDType without IDTypeName should validate."""
        identifier = AddresseeIdentifier(
            addressee_id_type="16",  # ISNI
            id_value="0000000121032683",
        )
        assert identifier.addressee_id_type == "16"
        assert identifier.id_type_name is None

    def test_invalid_list_44_code_raises_error(self):
        """Invalid List 44 code should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            AddresseeIdentifier(
                addressee_id_type="999",  # Invalid code
                id_value="ABC123",
            )

        errors = exc_info.value.errors()
        assert any("Invalid AddresseeIDType" in str(e) for e in errors)
        assert any("not a valid List 44 code" in str(e) for e in errors)


class TestHeaderSentDateTimeValidation:
    """Tests for Header sent_date_time field validation."""

    def test_date_only_format_valid(self):
        """YYYYMMDD format should validate."""
        header = Header(
            sender=Sender(sender_name="TestSender"),
            sent_date_time="20231201",
        )
        assert header.sent_date_time == "20231201"

    def test_date_time_with_minutes_valid(self):
        """YYYYMMDDThhmm format should validate."""
        header = Header(
            sender=Sender(sender_name="TestSender"),
            sent_date_time="20231201T1200",
        )
        assert header.sent_date_time == "20231201T1200"

    def test_date_time_with_minutes_and_z_valid(self):
        """YYYYMMDDThhmmZ format should validate."""
        header = Header(
            sender=Sender(sender_name="TestSender"),
            sent_date_time="20231201T1200Z",
        )
        assert header.sent_date_time == "20231201T1200Z"

    def test_date_time_with_seconds_valid(self):
        """YYYYMMDDThhmmss format should validate."""
        header = Header(
            sender=Sender(sender_name="TestSender"),
            sent_date_time="20231201T120000",
        )
        assert header.sent_date_time == "20231201T120000"

    def test_date_time_with_seconds_and_z_valid(self):
        """YYYYMMDDThhmmssZ format should validate."""
        header = Header(
            sender=Sender(sender_name="TestSender"),
            sent_date_time="20231201T120000Z",
        )
        assert header.sent_date_time == "20231201T120000Z"

    def test_invalid_format_with_dashes_raises_error(self):
        """ISO 8601 format with dashes should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Header(
                sender=Sender(sender_name="TestSender"),
                sent_date_time="2023-12-01T12:00:00",
            )

        errors = exc_info.value.errors()
        assert any("Invalid SentDateTime format" in str(e) for e in errors)

    def test_invalid_format_nonsense_raises_error(self):
        """Nonsense date/time string should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Header(
                sender=Sender(sender_name="TestSender"),
                sent_date_time="not-a-date",
            )

        errors = exc_info.value.errors()
        assert any("Invalid SentDateTime format" in str(e) for e in errors)

    def test_invalid_date_values_raises_error(self):
        """Invalid date values (e.g., month 13) should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Header(
                sender=Sender(sender_name="TestSender"),
                sent_date_time="20231301",  # Month 13 doesn't exist
            )

        errors = exc_info.value.errors()
        assert any("Invalid SentDateTime format" in str(e) for e in errors)


class TestHeaderMessageNumberValidation:
    """Tests for Header message_number field validation."""

    def test_valid_numeric_string_1_digit(self):
        """Single digit numeric string should validate."""
        header = Header(
            sender=Sender(sender_name="TestSender"),
            sent_date_time="20231201T120000Z",
            message_number="1",
        )
        assert header.message_number == "1"

    def test_valid_numeric_string_8_digits(self):
        """8 digit numeric string (max length) should validate."""
        header = Header(
            sender=Sender(sender_name="TestSender"),
            sent_date_time="20231201T120000Z",
            message_number="12345678",
        )
        assert header.message_number == "12345678"

    def test_invalid_9_digits_raises_error(self):
        """9 digit numeric string should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Header(
                sender=Sender(sender_name="TestSender"),
                sent_date_time="20231201T120000Z",
                message_number="123456789",
            )

        errors = exc_info.value.errors()
        assert any("Invalid MessageNumber" in str(e) for e in errors)
        assert any("must be numeric string up to 8 digits" in str(e) for e in errors)

    def test_non_numeric_raises_error(self):
        """Non-numeric string should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Header(
                sender=Sender(sender_name="TestSender"),
                sent_date_time="20231201T120000Z",
                message_number="abc123",
            )

        errors = exc_info.value.errors()
        assert any("Invalid MessageNumber" in str(e) for e in errors)

    def test_none_value_valid(self):
        """None value (optional field) should validate."""
        header = Header(
            sender=Sender(sender_name="TestSender"),
            sent_date_time="20231201T120000Z",
            message_number=None,
        )
        assert header.message_number is None


class TestHeaderMessageRepeatValidation:
    """Tests for Header message_repeat field validation."""

    def test_valid_numeric_string_1_digit(self):
        """Single digit numeric string should validate."""
        header = Header(
            sender=Sender(sender_name="TestSender"),
            sent_date_time="20231201T120000Z",
            message_repeat="1",
        )
        assert header.message_repeat == "1"

    def test_valid_numeric_string_4_digits(self):
        """4 digit numeric string (max length) should validate."""
        header = Header(
            sender=Sender(sender_name="TestSender"),
            sent_date_time="20231201T120000Z",
            message_repeat="1234",
        )
        assert header.message_repeat == "1234"

    def test_invalid_5_digits_raises_error(self):
        """5 digit numeric string should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Header(
                sender=Sender(sender_name="TestSender"),
                sent_date_time="20231201T120000Z",
                message_repeat="12345",
            )

        errors = exc_info.value.errors()
        assert any("Invalid MessageRepeat" in str(e) for e in errors)
        assert any("must be numeric string up to 4 digits" in str(e) for e in errors)

    def test_non_numeric_raises_error(self):
        """Non-numeric string should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Header(
                sender=Sender(sender_name="TestSender"),
                sent_date_time="20231201T120000Z",
                message_repeat="abc",
            )

        errors = exc_info.value.errors()
        assert any("Invalid MessageRepeat" in str(e) for e in errors)

    def test_none_value_valid(self):
        """None value (optional field) should validate."""
        header = Header(
            sender=Sender(sender_name="TestSender"),
            sent_date_time="20231201T120000Z",
            message_repeat=None,
        )
        assert header.message_repeat is None


class TestAliasKeyConstruction:
    """Tests to ensure validators work with both alias and field name construction."""

    def test_sender_identifier_via_alias_keys(self):
        """Constructing SenderIdentifier via alias keys should trigger validators."""
        # Valid construction with alias keys
        identifier = SenderIdentifier(
            **{
                "SenderIDType": "16",  # ISNI
                "IDValue": "0000000121032683",
            }
        )
        assert identifier.sender_id_type == "16"

        # Invalid construction should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            SenderIdentifier(
                **{
                    "SenderIDType": "01",  # Proprietary - requires IDTypeName
                    "IDValue": "12345",
                }
            )
        errors = exc_info.value.errors()
        assert any(
            "IDTypeName is required for proprietary SenderIDType '01'" in str(e)
            for e in errors
        )

    def test_header_via_alias_keys(self):
        """Constructing Header via alias keys should trigger validators."""
        # Valid construction with alias keys
        header = Header(
            **{
                "Sender": {"SenderName": "TestSender"},
                "SentDateTime": "20231201T120000Z",
            }
        )
        assert header.sent_date_time == "20231201T120000Z"

        # Invalid sent_date_time should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            Header(
                **{
                    "Sender": {"SenderName": "TestSender"},
                    "SentDateTime": "2023-12-01",  # Invalid format
                }
            )
        errors = exc_info.value.errors()
        assert any("Invalid SentDateTime format" in str(e) for e in errors)
