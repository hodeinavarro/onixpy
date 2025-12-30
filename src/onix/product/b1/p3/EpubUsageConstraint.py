"""Usage constraint composite (P.3.17-P.3.20).

An optional group of data elements which together describe a usage constraint
on a digital product (or the absence of such a constraint), whether enforced
by DRM technical protection, inherent in the platform used, or specified by
license agreement.
"""

from __future__ import annotations

from pydantic import Field, field_validator

from onix._base import ONIXModel
from onix.lists import get_code
from onix.product.b1.p3.EpubUsageLimit import EpubUsageLimit


class EpubUsageConstraint(ONIXModel):
    """Usage constraint composite (digital products).

    Required fields:
    - epub_usage_type: Code from List 145 specifying the usage type
    - epub_usage_status: Code from List 146 specifying the status (permitted/prohibited)

    Optional fields:
    - epub_usage_limit: List of quantitative limits on usage

    Example:
        >>> EpubUsageConstraint(
        ...     epub_usage_type="05",  # Text-to-speech
        ...     epub_usage_status="03",  # Prohibited
        ... )
    """

    epub_usage_type: str = Field(
        alias="EpubUsageType",
        json_schema_extra={
            "short_tag": "x318",
        },
    )
    epub_usage_status: str = Field(
        alias="EpubUsageStatus",
        json_schema_extra={
            "short_tag": "x319",
        },
    )
    epub_usage_limit: list[EpubUsageLimit] = Field(
        default_factory=list,
        alias="EpubUsageLimit",
        json_schema_extra={
            "short_tag": "epubusagelimit",
        },
    )

    @field_validator("epub_usage_type")
    @classmethod
    def _validate_epub_usage_type(cls, v: str) -> str:
        """Validate epub_usage_type: fixed length, two digits, List 145."""
        if not v.isdigit() or len(v) != 2:
            raise ValueError(
                f"Invalid epub_usage_type '{v}' - must be exactly 2 digits"
            )
        if get_code(145, v) is None:
            raise ValueError(f"Invalid epub_usage_type '{v}' - must be from List 145")
        return v

    @field_validator("epub_usage_status")
    @classmethod
    def _validate_epub_usage_status(cls, v: str) -> str:
        """Validate epub_usage_status: fixed length, two digits, List 146."""
        if not v.isdigit() or len(v) != 2:
            raise ValueError(
                f"Invalid epub_usage_status '{v}' - must be exactly 2 digits"
            )
        if get_code(146, v) is None:
            raise ValueError(f"Invalid epub_usage_status '{v}' - must be from List 146")
        return v
