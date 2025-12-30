"""Usage limit composite (P.3.17).

An optional group of data elements which together specify a quantitative
limit on a particular type of usage of a digital product.
"""

from __future__ import annotations

from pydantic import Field, field_validator

from onix._base import ONIXModel
from onix.lists import get_code


class EpubUsageLimit(ONIXModel):
    """Usage limit composite (digital products).

    Required fields:
    - quantity: Maximum permitted quantity
    - epub_usage_unit: Code from List 147 indicating the unit

    Example:
        >>> EpubUsageLimit(
        ...     quantity="10",
        ...     epub_usage_unit="07",  # Maximum number of concurrent users
        ... )
    """

    quantity: str = Field(
        alias="Quantity",
        json_schema_extra={
            "short_tag": "x320",
        },
    )
    epub_usage_unit: str = Field(
        alias="EpubUsageUnit",
        json_schema_extra={
            "short_tag": "x321",
        },
    )

    @field_validator("epub_usage_unit")
    @classmethod
    def _validate_epub_usage_unit(cls, v: str) -> str:
        """Validate epub_usage_unit: fixed length, two digits, List 147."""
        if not v.isdigit() or len(v) != 2:
            raise ValueError(
                f"Invalid epub_usage_unit '{v}' - must be exactly 2 digits"
            )
        if get_code(147, v) is None:
            raise ValueError(f"Invalid epub_usage_unit '{v}' - must be from List 147")
        return v
