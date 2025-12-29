"""ONIX Header composite models.

Contains the Header and its nested composites: Sender, Addressee, and their
identifier composites.

All fields use Field(alias=...) to define the XML reference tag name.
This is the single source of truth for tag/field name mapping.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import Field, field_validator, model_validator

from onix._base import ONIXModel
from onix.lists import get_code


class SenderIdentifier(ONIXModel):
    """Sender identifier composite.

    A group of data elements which together define an identifier of the sender.

    Elements:
    - SenderIDType (H.1): Code from List 44 - required
    - IDTypeName (H.2): Name of proprietary ID scheme - optional
    - IDValue (H.3): The identifier value - required
    """

    sender_id_type: str = Field(
        alias="SenderIDType",
    )
    id_type_name: str | None = Field(
        default=None,
        alias="IDTypeName",
    )
    id_value: str = Field(
        alias="IDValue",
    )

    @field_validator("sender_id_type")
    @classmethod
    def validate_sender_id_type(cls, v: str) -> str:
        """Validate sender_id_type is a valid List 44 code."""
        if get_code(44, v) is None:
            raise ValueError(f"Invalid SenderIDType: '{v}' is not a valid List 44 code")
        return v

    @model_validator(mode="after")
    def _require_id_type_name_for_proprietary(self):
        """Require id_type_name when sender_id_type is '01' (proprietary)."""
        if self.sender_id_type == "01" and not self.id_type_name:
            raise ValueError("IDTypeName is required for proprietary SenderIDType '01'")
        return self


class Sender(ONIXModel):
    """Sender composite.

    A group of data elements which together specify the sender of an ONIX
    message. Required and non-repeating.

    Elements:
    - SenderIdentifier (0…n): Identifiers for the sender
    - SenderName (H.4): Name of the sender - optional
    - ContactName (H.5): Contact person name - optional
    - TelephoneNumber (H.5a): Contact telephone - optional
    - EmailAddress (H.6): Contact email - optional
    """

    sender_identifiers: list[SenderIdentifier] = Field(
        default_factory=list,
        alias="SenderIdentifier",
    )
    sender_name: str | None = Field(
        default=None,
        alias="SenderName",
    )
    contact_name: str | None = Field(
        default=None,
        alias="ContactName",
    )
    telephone_number: str | None = Field(
        default=None,
        alias="TelephoneNumber",
    )
    email_address: str | None = Field(
        default=None,
        alias="EmailAddress",
    )

    @model_validator(mode="after")
    def _ensure_not_empty(self):
        """Ensure Sender isn't an empty container.

        A `Sender` must provide at least a name or one identifier; an
        empty `Sender()` should be considered invalid when used in a
        `Header` (the element is required and must contain useful data).
        """
        if not self.sender_name and not self.sender_identifiers:
            raise ValueError(
                "Sender must include at least one of `sender_name` or `sender_identifiers`"
            )
        return self


class AddresseeIdentifier(ONIXModel):
    """Addressee identifier composite.

    A group of data elements which together define an identifier of the addressee.

    Elements:
    - AddresseeIDType (H.7): Code from List 44 - required
    - IDTypeName (H.8): Name of proprietary ID scheme - optional
    - IDValue (H.9): The identifier value - required
    """

    addressee_id_type: str = Field(
        alias="AddresseeIDType",
    )
    id_type_name: str | None = Field(
        default=None,
        alias="IDTypeName",
    )
    id_value: str = Field(
        alias="IDValue",
    )

    @field_validator("addressee_id_type")
    @classmethod
    def validate_addressee_id_type(cls, v: str) -> str:
        """Validate addressee_id_type is a valid List 44 code."""
        if get_code(44, v) is None:
            raise ValueError(
                f"Invalid AddresseeIDType: '{v}' is not a valid List 44 code"
            )
        return v

    @model_validator(mode="after")
    def _require_id_type_name_for_proprietary(self):
        """Require id_type_name when addressee_id_type is '01' (proprietary)."""
        if self.addressee_id_type == "01" and not self.id_type_name:
            raise ValueError(
                "IDTypeName is required for proprietary AddresseeIDType '01'"
            )
        return self


class Addressee(ONIXModel):
    """Addressee composite.

    A group of data elements which together specify the addressee of an ONIX
    message. Optional and repeatable.

    Elements:
    - AddresseeIdentifier (0…n): Identifiers for the addressee
    - AddresseeName (H.10): Name of the addressee - optional
    - ContactName (H.11): Contact person name - optional
    - TelephoneNumber (H.11a): Contact telephone - optional
    - EmailAddress (H.12): Contact email - optional
    """

    addressee_identifiers: list[AddresseeIdentifier] = Field(
        default_factory=list,
        alias="AddresseeIdentifier",
    )
    addressee_name: str | None = Field(
        default=None,
        alias="AddresseeName",
    )
    contact_name: str | None = Field(
        default=None,
        alias="ContactName",
    )
    telephone_number: str | None = Field(
        default=None,
        alias="TelephoneNumber",
    )
    email_address: str | None = Field(
        default=None,
        alias="EmailAddress",
    )


class Header(ONIXModel):
    """ONIX message header.

    A group of data elements which together constitute a message header.
    Required and non-repeating in each ONIX message.

    Elements:
    - Sender (required): Information about the sender
    - Addressee (H.7-H.12, 0…n): Information about addressee(s)
    - MessageNumber (H.13, 0…1): Sequence number of message
    - MessageRepeat (H.14, 0…1): Repeat number if resending
    - SentDateTime (H.15, required): Date/time message was sent
    - MessageNote (H.16, 0…1): Free text note
    - DefaultLanguageOfText (H.17, 0…1): Default language code (List 74)
    - DefaultPriceType (H.18, 0…1): Default price type (List 58)
    - DefaultCurrencyCode (H.19, 0…1): Default currency (List 96)
    """

    sender: Sender = Field(
        alias="Sender",
    )
    addressees: list[Addressee] = Field(
        default_factory=list,
        alias="Addressee",
    )
    message_number: str | None = Field(
        default=None,
        alias="MessageNumber",
    )
    message_repeat: str | None = Field(
        default=None,
        alias="MessageRepeat",
    )
    sent_date_time: str = Field(
        alias="SentDateTime",
    )
    message_note: str | None = Field(
        default=None,
        alias="MessageNote",
    )
    default_language_of_text: str | None = Field(
        default=None,
        alias="DefaultLanguageOfText",
    )
    default_price_type: str | None = Field(
        default=None,
        alias="DefaultPriceType",
    )
    default_currency_code: str | None = Field(
        default=None,
        alias="DefaultCurrencyCode",
    )

    @field_validator("sent_date_time")
    @classmethod
    def validate_sent_date_time(cls, v: str) -> str:
        """Validate sent_date_time conforms to ONIX date/time formats.

        Accepts:
        - YYYYMMDD
        - YYYYMMDDThhmm or YYYYMMDDThhmmZ
        - YYYYMMDDThhmmss or YYYYMMDDThhmmssZ
        """
        # Strip optional trailing 'Z' (UTC indicator)
        test_value = v.rstrip("Z")

        # Try parsing with accepted formats
        formats = ["%Y%m%d", "%Y%m%dT%H%M", "%Y%m%dT%H%M%S"]
        for fmt in formats:
            try:
                datetime.strptime(test_value, fmt)
                return v  # Return original with Z if present
            except ValueError:
                continue

        raise ValueError(
            "Invalid SentDateTime format: expected one of YYYYMMDD, "
            "YYYYMMDDThhmmZ, YYYYMMDDThhmmssZ, YYYYMMDDThhmm or YYYYMMDDThhmmss"
        )

    @field_validator("message_number")
    @classmethod
    def validate_message_number(cls, v: str | None) -> str | None:
        """Validate message_number is numeric string up to 8 digits."""
        if v is not None:
            if not v.isdigit() or len(v) > 8:
                raise ValueError(
                    "Invalid MessageNumber: must be numeric string up to 8 digits"
                )
        return v

    @field_validator("message_repeat")
    @classmethod
    def validate_message_repeat(cls, v: str | None) -> str | None:
        """Validate message_repeat is numeric string up to 4 digits."""
        if v is not None:
            if not v.isdigit() or len(v) > 4:
                raise ValueError(
                    "Invalid MessageRepeat: must be numeric string up to 4 digits"
                )
        return v

    @field_validator("default_language_of_text")
    @classmethod
    def validate_default_language(cls, v: str | None) -> str | None:
        """Validate default_language_of_text is a valid List 74 code."""
        if v is not None and get_code(74, v) is None:
            raise ValueError(
                f"Invalid DefaultLanguageOfText: '{v}' is not a valid List 74 code"
            )
        return v

    @field_validator("default_price_type")
    @classmethod
    def validate_default_price_type(cls, v: str | None) -> str | None:
        """Validate default_price_type is a valid List 58 code."""
        if v is not None and get_code(58, v) is None:
            raise ValueError(
                f"Invalid DefaultPriceType: '{v}' is not a valid List 58 code"
            )
        return v

    @field_validator("default_currency_code")
    @classmethod
    def validate_default_currency(cls, v: str | None) -> str | None:
        """Validate default_currency_code is a valid List 96 code."""
        if v is not None and get_code(96, v) is None:
            raise ValueError(
                f"Invalid DefaultCurrencyCode: '{v}' is not a valid List 96 code"
            )
        return v
