"""Digital product license expression composite (P.3.20b).

An optional composite that carries details of a link to an expression of
the license terms, which may be in human-readable or machine-readable form.
"""

from __future__ import annotations

from pydantic import Field, field_validator, model_validator

from onix._base import ONIXModel, validate_proprietary_id_type
from onix.lists import get_code


class EpubLicenseExpression(ONIXModel):
    """Digital product license expression composite (new in 3.0.2).

    Required fields:
    - epub_license_expression_type: Code from List 218 identifying the format
    - epub_license_expression_link: URI for the license expression

    Optional fields:
    - epub_license_expression_type_name: Name of proprietary encoding scheme

    Example:
        >>> EpubLicenseExpression(
        ...     epub_license_expression_type="10",  # ONIX-PL
        ...     epub_license_expression_link="http://example.com/license.xml",
        ... )
    """

    epub_license_expression_type: str = Field(
        alias="EpubLicenseExpressionType",
        json_schema_extra={
            "short_tag": "x508",
        },
    )
    epub_license_expression_type_name: str | None = Field(
        default=None,
        alias="EpubLicenseExpressionTypeName",
        max_length=50,
        json_schema_extra={
            "short_tag": "x509",
        },
    )
    epub_license_expression_link: str = Field(
        alias="EpubLicenseExpressionLink",
        max_length=300,
        json_schema_extra={
            "short_tag": "x510",
        },
    )

    @field_validator("epub_license_expression_type")
    @classmethod
    def _validate_epub_license_expression_type(cls, v: str) -> str:
        """Validate epub_license_expression_type: fixed length, two digits, List 218."""
        if not v.isdigit() or len(v) != 2:
            raise ValueError(
                f"Invalid epub_license_expression_type '{v}' - must be exactly 2 digits"
            )
        if get_code(218, v) is None:
            raise ValueError(
                f"Invalid epub_license_expression_type '{v}' - must be from List 218"
            )
        return v

    @model_validator(mode="after")
    def _validate_proprietary_type_name(self) -> "EpubLicenseExpression":
        """Ensure proprietary types have type name."""
        validate_proprietary_id_type(
            self.epub_license_expression_type,
            self.epub_license_expression_type_name,
            "EpubLicenseExpressionType",
        )
        return self
