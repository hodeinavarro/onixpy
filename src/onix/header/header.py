"""ONIX Header composite models.

Contains the Header and its nested composites: Sender, Addressee, and their
identifier composites.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, field_validator

from onix.lists import get_code


class SenderIdentifier(BaseModel):
    """Sender identifier composite.

    A group of data elements which together define an identifier of the sender.

    Elements:
    - SenderIDType (H.1): Code from List 44 - required
    - IDTypeName (H.2): Name of proprietary ID scheme - optional
    - IDValue (H.3): The identifier value - required
    """

    model_config = ConfigDict(extra="forbid")

    sender_id_type: str
    id_type_name: str | None = None
    id_value: str

    @field_validator("sender_id_type")
    @classmethod
    def validate_sender_id_type(cls, v: str) -> str:
        """Validate sender_id_type is a valid List 44 code."""
        if get_code(44, v) is None:
            raise ValueError(f"Invalid SenderIDType: '{v}' is not a valid List 44 code")
        return v


class Sender(BaseModel):
    """Sender composite.

    A group of data elements which together specify the sender of an ONIX
    message. Required and non-repeating.

    Elements:
    - SenderIdentifier (0…n): Identifiers for the sender
    - SenderName (H.4): Name of the sender - optional
    - ContactName (H.5): Contact person name - optional
    - TelephoneNumber (H.5a): Contact telephone - optional (deprecated)
    - EmailAddress (H.6): Contact email - optional
    """

    model_config = ConfigDict(extra="forbid")

    sender_identifiers: list[SenderIdentifier] = []
    sender_name: str | None = None
    contact_name: str | None = None
    telephone_number: str | None = None
    email_address: str | None = None


class AddresseeIdentifier(BaseModel):
    """Addressee identifier composite.

    A group of data elements which together define an identifier of the addressee.

    Elements:
    - AddresseeIDType (H.7): Code from List 44 - required
    - IDTypeName (H.8): Name of proprietary ID scheme - optional
    - IDValue (H.9): The identifier value - required
    """

    model_config = ConfigDict(extra="forbid")

    addressee_id_type: str
    id_type_name: str | None = None
    id_value: str

    @field_validator("addressee_id_type")
    @classmethod
    def validate_addressee_id_type(cls, v: str) -> str:
        """Validate addressee_id_type is a valid List 44 code."""
        if get_code(44, v) is None:
            raise ValueError(
                f"Invalid AddresseeIDType: '{v}' is not a valid List 44 code"
            )
        return v


class Addressee(BaseModel):
    """Addressee composite.

    A group of data elements which together specify the addressee of an ONIX
    message. Optional and repeatable.

    Elements:
    - AddresseeIdentifier (0…n): Identifiers for the addressee
    - AddresseeName (H.10): Name of the addressee - optional
    - ContactName (H.11): Contact person name - optional
    - TelephoneNumber (H.11a): Contact telephone - optional (deprecated)
    - EmailAddress (H.12): Contact email - optional
    """

    model_config = ConfigDict(extra="forbid")

    addressee_identifiers: list[AddresseeIdentifier] = []
    addressee_name: str | None = None
    contact_name: str | None = None
    telephone_number: str | None = None
    email_address: str | None = None


class Header(BaseModel):
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

    model_config = ConfigDict(extra="forbid")

    sender: Sender
    addressees: list[Addressee] = []
    message_number: str | None = None
    message_repeat: str | None = None
    sent_date_time: str
    message_note: str | None = None
    default_language_of_text: str | None = None
    default_price_type: str | None = None
    default_currency_code: str | None = None

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
