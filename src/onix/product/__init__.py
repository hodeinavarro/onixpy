"""ONIX Product models.

The Product record is the core of an ONIX message, containing all metadata
for a single product (book, ebook, audiobook, etc.).

Product structure follows ONIX 3.0 blocks:
- Block 1: Product description (identifiers, form, extent, etc.)
- Block 2: Marketing collateral detail (descriptions, cover images)
- Block 3: Content detail (contributors, subjects, audience)
- Block 4: Publishing detail (publisher, imprint, dates)
- Block 5: Related material (related products, works)
- Block 6: Product supply (availability, pricing)
- Block 7: Promotion detail (promotional info)
- Block 8: Production detail (manufacturing info)

Example:
    >>> from onix import Product
    >>> from onix.product import Product, ProductIdentifier
    >>>
    >>> product = Product(
    ...     record_reference="com.example.001",
    ...     notification_type="03",
    ...     product_identifiers=[
    ...         ProductIdentifier(product_id_type="15", id_value="9780000000001")
    ...     ],
    ... )
"""

from pydantic import Field, field_validator, model_validator

from onix._base import ONIXModel
from onix.lists import List1, get_code

# P.1 Record source and deletion
from onix.product.b1.p1 import RecordSourceIdentifier

# P.2 Product identifiers
from onix.product.b1.p2 import Barcode, ProductIdentifier

# Block 1: Product description (p3 only)
from onix.product.b1.p3 import (
    DescriptiveDetail,
    EpubLicense,
    EpubLicenseDate,
    EpubLicenseExpression,
    EpubUsageConstraint,
    EpubUsageLimit,
    ProductClassification,
    ProductFormFeature,
)


class Product(ONIXModel):
    """ONIX Product with all block fields.

    Contains minimal required metadata for a product plus optional fields for each ONIX block.

    Required fields for a minimal valid Product:
    - record_reference: Unique identifier for this record
    - notification_type: Code from List 1 (e.g., "03" for confirmed)
    - product_identifiers: At least one ProductIdentifier
    """

    # P.1.1 Record reference (mandatory)
    record_reference: str = Field(
        alias="RecordReference",
        json_schema_extra={"short_tag": "a001"},
        max_length=100,
    )
    # P.1.2 Notification or update type code (mandatory)
    notification_type: str = Field(
        alias="NotificationType",
        json_schema_extra={"short_tag": "a002"},
        max_length=2,
    )

    # P.1.3 Reason for deletion (optional, repeatable)
    deletion_texts: list[str] = Field(
        default_factory=list,
        alias="DeletionText",
        json_schema_extra={"short_tag": "a199"},
    )

    # P.1.4 Record source type code (optional)
    record_source_type: str | None = Field(
        default=None,
        alias="RecordSourceType",
        json_schema_extra={"short_tag": "a194"},
        max_length=2,
    )
    # P.1.5-P.1.7 Record source identifier composite (optional, repeatable)
    record_source_identifiers: list[RecordSourceIdentifier] = Field(
        default_factory=list,
        alias="RecordSourceIdentifier",
        json_schema_extra={"short_tag": "recordsourceidentifier"},
    )
    # P.1.8 Record source name (optional)
    record_source_name: str | None = Field(
        default=None,
        alias="RecordSourceName",
        json_schema_extra={"short_tag": "a197"},
        max_length=100,
    )

    # P.2.1-P.2.3 Product identifier composite (mandatory, repeatable)
    product_identifiers: list[ProductIdentifier] = Field(
        alias="ProductIdentifier",
        json_schema_extra={"short_tag": "productidentifier"},
        min_length=1,
    )

    # P.2.4 Barcode composite (optional, repeatable)
    barcodes: list[Barcode] = Field(
        default_factory=list,
        alias="Barcode",
        json_schema_extra={"short_tag": "barcode"},
    )

    # Block 1: Product description > P.3 Descriptive detail composite (optional)
    descriptive_detail: DescriptiveDetail | None = Field(
        default=None,
        alias="DescriptiveDetail",
        json_schema_extra={"short_tag": "descriptivedetail"},
    )

    @field_validator("notification_type")
    @classmethod
    def validate_notification_type(cls, v: str) -> str:
        """Validate notification_type is in List 1."""
        if v not in List1:
            raise ValueError(f"Invalid notification_type '{v}': must be from List 1")
        return v

    @field_validator("record_source_type")
    @classmethod
    def _validate_record_source_type(cls, v: str | None) -> str | None:
        """Validate record_source_type: fixed length, two digits, List 3."""
        if v is not None:
            if not v.isdigit() or len(v) != 2:
                raise ValueError(
                    f"Invalid record_source_type '{v}' - must be exactly 2 digits"
                )
            if get_code(3, v) is None:
                raise ValueError(
                    f"Invalid record_source_type '{v}' - must be from List 3"
                )
        return v

    @field_validator("deletion_texts")
    @classmethod
    def _validate_deletion_texts(cls, v: list[str]) -> list[str]:
        """Validate deletion_texts: max 100 characters each."""
        for txt in v:
            if len(txt) > 100:
                raise ValueError(
                    f"DeletionText exceeds maximum length of 100 characters (got {len(txt)})"
                )
        return v

    @model_validator(mode="after")
    def _validate_deletion_texts_allowed(self) -> "Product":
        """Ensure DeletionText only occurs when NotificationType is '05'."""
        if self.deletion_texts and self.notification_type != "05":
            raise ValueError(
                "DeletionText entries may only be provided when NotificationType is '05' (Delete)"
            )
        return self


__all__ = [
    # Core model
    "Product",
    # P.1 Record source and deletion
    "RecordSourceIdentifier",
    # P.2 Product identifiers
    "ProductIdentifier",
    "Barcode",
    # P.3 Product description
    "DescriptiveDetail",
    "ProductFormFeature",
    "EpubUsageLimit",
    "EpubUsageConstraint",
    "EpubLicenseDate",
    "EpubLicenseExpression",
    "EpubLicense",
    "ProductClassification",
]
