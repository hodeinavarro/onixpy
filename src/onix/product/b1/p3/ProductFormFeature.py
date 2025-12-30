"""Product form feature composite (P.3.4).

An optional group of data elements which together describe an aspect of
product form that is too specific to be covered in the <ProductForm> and
<ProductFormDetail> elements.
"""

from __future__ import annotations

from pydantic import Field, field_validator

from onix._base import ONIXModel
from onix.lists import get_code


class ProductFormFeature(ONIXModel):
    """Product form feature composite.

    Required fields:
    - product_form_feature_type: Code from List 79 specifying the feature type

    Optional fields:
    - product_form_feature_value: Controlled value (depends on feature type)
    - product_form_feature_description: Free text description (repeatable, with language)

    Example:
        >>> ProductFormFeature(
        ...     product_form_feature_type="02",  # Page edge color
        ...     product_form_feature_value="BLK",  # Black
        ... )
    """

    product_form_feature_type: str = Field(
        alias="ProductFormFeatureType",
        json_schema_extra={"short_tag": "b334"},
    )
    product_form_feature_value: str | None = Field(
        default=None,
        alias="ProductFormFeatureValue",
        json_schema_extra={"short_tag": "b335"},
    )
    # Per-item length limits are enforced by the custom validator below
    product_form_feature_description: list[str] = Field(
        default_factory=list,
        alias="ProductFormFeatureDescription",
        json_schema_extra={"short_tag": "b336"},
    )

    @field_validator("product_form_feature_type")
    @classmethod
    def _validate_product_form_feature_type(cls, v: str) -> str:
        """Validate product_form_feature_type: fixed length, two digits, List 79."""
        if not v.isdigit() or len(v) != 2:
            raise ValueError(
                f"Invalid product_form_feature_type '{v}' - must be exactly 2 digits"
            )
        if get_code(79, v) is None:
            raise ValueError(
                f"Invalid product_form_feature_type '{v}' - must be from List 79"
            )
        return v

    @field_validator("product_form_feature_description")
    @classmethod
    def _validate_product_form_feature_description(cls, v: list[str]) -> list[str]:
        """Validate product_form_feature_description: max 10,000 characters each."""
        for desc in v:
            if len(desc) > 10000:
                raise ValueError(
                    f"product_form_feature_description exceeds maximum length of 10,000 characters (got {len(desc)})"
                )
        return v
