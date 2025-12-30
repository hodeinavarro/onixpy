"""Digital product license date composite (P.3.20a).

An optional group of date elements which together specify a date associated
with the license in an occurrence of the <EpubLicense> composite.
"""

from __future__ import annotations

from pydantic import Field, field_validator

from onix._base import ONIXModel
from onix.lists import get_code


class EpubLicenseDate(ONIXModel):
    """Digital product license date composite (new in 3.1).

    Required fields:
    - epub_license_date_role: Code from List 260 indicating the date significance
    - date: The date (YYYYMMDD format or with dateformat attribute)

    Example:
        >>> EpubLicenseDate(
        ...     epub_license_date_role="14",  # License becomes effective
        ...     date="20221028",
        ... )
    """

    epub_license_date_role: str = Field(
        alias="EpubLicenseDateRole",
        json_schema_extra={
            "short_tag": "x585",
        },
    )
    date: str = Field(
        alias="Date",
        json_schema_extra={
            "short_tag": "b306",
        },
    )

    @field_validator("epub_license_date_role")
    @classmethod
    def _validate_epub_license_date_role(cls, v: str) -> str:
        """Validate epub_license_date_role: fixed length, two digits, List 260."""
        if not v.isdigit() or len(v) != 2:
            raise ValueError(
                f"Invalid epub_license_date_role '{v}' - must be exactly 2 digits"
            )
        if get_code(260, v) is None:
            raise ValueError(
                f"Invalid epub_license_date_role '{v}' - must be from List 260"
            )
        return v
