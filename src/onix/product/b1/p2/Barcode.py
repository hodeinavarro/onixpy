"""Barcode composite (P.2.2).

A group of data elements which together specify a barcode.
"""

from __future__ import annotations

from pydantic import Field, field_validator

from onix._base import ONIXModel
from onix.lists import get_code


class Barcode(ONIXModel):
    """Barcode composite.

    Elements:
    - barcode_type: Code from List 141 (required)
    - position_on_product: Code from List 142 (optional)
    """

    # P.2.4 Barcode type (mandatory)
    barcode_type: str = Field(
        alias="BarcodeType",
        json_schema_extra={
            "short_tag": "x312",
        },
    )
    # P.2.5 Position on product (optional)
    position_on_product: str | None = Field(
        default=None,
        alias="PositionOnProduct",
        json_schema_extra={
            "short_tag": "x313",
        },
    )

    @field_validator("barcode_type")
    @classmethod
    def _validate_barcode_type(cls, v: str) -> str:
        if not v.isdigit() or len(v) != 2:
            raise ValueError(f"Invalid BarcodeType '{v}' - must be exactly 2 digits")
        if get_code(141, v) is None:
            raise ValueError(f"Invalid BarcodeType '{v}' - must be from List 141")
        return v

    @field_validator("position_on_product")
    @classmethod
    def _validate_position_on_product(cls, v: str | None) -> str | None:
        if v is not None:
            if not v.isdigit() or len(v) != 2:
                raise ValueError(
                    f"Invalid PositionOnProduct '{v}' - must be exactly 2 digits"
                )
            if get_code(142, v) is None:
                raise ValueError(
                    f"Invalid PositionOnProduct '{v}' - must be from List 142"
                )
        return v
