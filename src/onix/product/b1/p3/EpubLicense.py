"""Digital product license composite (P.3.20c).

An optional composite carrying the name or title of the license governing
use of the product, a link to the license terms in eye-readable or
machine-readable form, and optional dates when the license is valid.
"""

from __future__ import annotations

from pydantic import Field, field_validator

from onix._base import ONIXModel
from onix.product.b1.p3.EpubLicenseDate import EpubLicenseDate
from onix.product.b1.p3.EpubLicenseExpression import EpubLicenseExpression


class EpubLicense(ONIXModel):
    """Digital product license composite (new in 3.0.2).

    Required fields:
    - epub_license_name: Name/title of the license (repeatable for multiple languages)

    Optional fields:
    - epub_license_expression: List of links to license expressions
    - epub_license_date: List of dates associated with the license

    Example:
        >>> EpubLicense(
        ...     epub_license_name=["Elsevier e-book EULA v5"],
        ... )
    """

    epub_license_name: list[str] = Field(
        min_length=1,
        alias="EpubLicenseName",
        json_schema_extra={
            "short_tag": "x511",
        },
    )
    epub_license_expression: list[EpubLicenseExpression] = Field(
        default_factory=list,
        alias="EpubLicenseExpression",
        json_schema_extra={
            "short_tag": "epublicenseexpression",
        },
    )
    epub_license_date: list[EpubLicenseDate] = Field(
        default_factory=list,
        alias="EpubLicenseDate",
        json_schema_extra={
            "short_tag": "epublicensedate",
        },
    )

    @field_validator("epub_license_name")
    @classmethod
    def _validate_epub_license_name(cls, v: list[str]) -> list[str]:
        """Validate epub_license_name: max 100 characters each."""
        for name in v:
            if len(name) > 100:
                raise ValueError(
                    f"epub_license_name exceeds maximum length of 100 characters (got {len(name)})"
                )
        return v
