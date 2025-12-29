"""ONIX Product model.

The Product composite is the central element of an ONIX message,
containing all metadata for a single product.
"""

from __future__ import annotations

from pydantic import Field

from onix.product.base import ONIXAttributes, ProductBase


class ProductIdentifier(ONIXAttributes):
    """Product identifier composite.

    Identifies a product using a standard or proprietary scheme.

    Required fields:
    - product_id_type: Code from List 5 indicating the identifier type
    - id_value: The identifier value

    Optional fields:
    - id_type_name: Name of proprietary identifier scheme (required if type is "01")

    Example:
        >>> from onix.product.product import ProductIdentifier
        >>> isbn = ProductIdentifier(
        ...     product_id_type="15",  # ISBN-13
        ...     id_value="9780007232833",
        ... )
    """

    product_id_type: str = Field(alias="ProductIDType")
    id_type_name: str | None = Field(default=None, alias="IDTypeName")
    id_value: str = Field(alias="IDValue")


class Product(ProductBase):
    """ONIX product record.

    Contains all metadata for a single product (book, ebook, etc.).

    Required fields for a minimal valid Product:
    - record_reference: Unique identifier for this record
    - notification_type: Code from List 1 (e.g., "03" for confirmed)
    - product_identifiers: At least one ProductIdentifier

    ONIX 3.0 Product structure (blocks to be implemented):
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
        >>> from onix.product.product import ProductIdentifier
        >>> product = Product(
        ...     record_reference="com.example.product.001",
        ...     notification_type="03",
        ...     product_identifiers=[
        ...         ProductIdentifier(
        ...             product_id_type="15",
        ...             id_value="9780000000001",
        ...         )
        ...     ],
        ... )
    """

    # Record metadata (gp.record_metadata)
    record_reference: str = Field(alias="RecordReference")
    notification_type: str = Field(alias="NotificationType")

    # Product identifiers (gp.product_numbers)
    product_identifiers: list[ProductIdentifier] = Field(
        alias="ProductIdentifier", min_length=1
    )
