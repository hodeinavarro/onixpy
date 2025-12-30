"""Product identifier composite (P.2.1).

A group of data elements which together specify an identifier of a product
in accordance with a particular scheme.
"""

from __future__ import annotations

from pydantic import Field, field_validator, model_validator

from onix._base import ONIXModel, validate_proprietary_id_type
from onix.lists import List5


class ProductIdentifier(ONIXModel):
    """Product identifier composite.

    Identifies a product using a standard or proprietary scheme.

    Required fields:
    - product_id_type: Code from List 5 indicating the identifier type
    - id_value: The identifier value

    Optional fields:
    - id_type_name: Name of proprietary identifier scheme (required if type is "01")
    """

    # P.2.1 Product ID type (mandatory)
    product_id_type: str = Field(
        alias="ProductIDType",
        json_schema_extra={"short_tag": "b221"},
        max_length=2,
    )
    # P.2.2 ID type name (optional)
    id_type_name: str | None = Field(
        default=None,
        alias="IDTypeName",
        json_schema_extra={"short_tag": "b233"},
        max_length=100,
    )
    # P.2.3 ID value (mandatory)
    id_value: str = Field(
        alias="IDValue",
        json_schema_extra={"short_tag": "b244"},
        max_length=300,
    )

    @field_validator("product_id_type")
    @classmethod
    def validate_product_id_type(cls, v: str) -> str:
        """Validate product_id_type is in List 5."""
        if v not in List5:
            raise ValueError(f"Invalid product_id_type '{v}': must be from List 5")
        return v

    @model_validator(mode="after")
    def _require_id_type_name_for_proprietary(self) -> "ProductIdentifier":
        """Require id_type_name when product_id_type is '01' (proprietary)."""
        validate_proprietary_id_type(
            self.product_id_type, self.id_type_name, "ProductIDType"
        )
        return self
