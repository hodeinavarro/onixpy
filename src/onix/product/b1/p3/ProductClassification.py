"""Product classification composite (P.3.22-P.3.24).

An optional group of data elements which together define a product classification
(not to be confused with a subject classification). The intended use is to enable
national or international trade classifications (commodity codes) to be carried
in an ONIX record.
"""

from __future__ import annotations

from pydantic import Field, field_validator, model_validator

from onix._base import ONIXModel
from onix.lists import get_code


class ProductClassification(ONIXModel):
    """Product classification composite.

    Required fields:
    - product_classification_type: Code from List 9 identifying the scheme
    - product_classification_code: Classification code from the specified scheme

    Optional fields:
    - product_classification_type_name: Name of proprietary scheme
    - percent: Percentage of product value assignable to this classification

    Example:
        >>> ProductClassification(
        ...     product_classification_type="02",  # UNSPSC
        ...     product_classification_code="55101514",  # Sheet music
        ... )
    """

    product_classification_type: str = Field(
        alias="ProductClassificationType",
        json_schema_extra={"short_tag": "b274"},
    )
    product_classification_type_name: str | None = Field(
        default=None,
        alias="ProductClassificationTypeName",
        max_length=50,
        json_schema_extra={"short_tag": "x555"},
    )
    product_classification_code: str = Field(
        alias="ProductClassificationCode",
        json_schema_extra={"short_tag": "b275"},
    )
    percent: str | None = Field(
        default=None,
        alias="Percent",
        max_length=7,
        json_schema_extra={"short_tag": "b337"},
    )

    @field_validator("product_classification_type")
    @classmethod
    def _validate_product_classification_type(cls, v: str) -> str:
        """Validate product_classification_type: fixed length, two digits, List 9."""
        if not v.isdigit() or len(v) != 2:
            raise ValueError(
                f"Invalid product_classification_type '{v}' - must be exactly 2 digits"
            )
        if get_code(9, v) is None:
            raise ValueError(
                f"Invalid product_classification_type '{v}' - must be from List 9"
            )
        return v

    @field_validator("percent")
    @classmethod
    def _validate_percent(cls, v: str | None) -> str | None:
        """Validate percent: real number 0-100."""
        if v is not None:
            try:
                percent_val = float(v)
                if percent_val < 0 or percent_val > 100:
                    raise ValueError(
                        f"percent must be between 0 and 100 (got {percent_val})"
                    )
            except ValueError as e:
                if "could not convert" in str(e):
                    raise ValueError(f"percent must be a valid number (got '{v}')")
                raise
        return v

    @model_validator(mode="after")
    def _validate_proprietary_type_name(self) -> "ProductClassification":
        """Ensure proprietary types have type name."""
        # List 9 code "01" is "Proprietary"
        if self.product_classification_type == "01":
            if not self.product_classification_type_name:
                raise ValueError(
                    "product_classification_type_name is required when "
                    "product_classification_type is '01' (Proprietary)"
                )
        return self
