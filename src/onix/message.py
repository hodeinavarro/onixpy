"""ONIX message models.

Core Pydantic models representing an ONIX for Books message structure.
Models use reference tag names by default; short-tag serialization is
controlled via parser/serializer options.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator


class ONIXAttributes(BaseModel):
    """Shared ONIX attributes that may appear on any element.

    These attributes carry metadata about the data itself:
    - datestamp: Date/time the data was created or last updated
    - sourcename: Name of the source of the data
    - sourcetype: Code from List 3 indicating the type of source
    """

    model_config = ConfigDict(extra="allow")

    datestamp: Optional[str] = None
    sourcename: Optional[str] = None
    sourcetype: Optional[str] = None


class Header(ONIXAttributes):
    """ONIX message header.

    Contains information about the sender, addressee, and message metadata.
    This is a placeholder; fields will be expanded as needed.
    """

    pass


class Product(ONIXAttributes):
    """ONIX product record.

    Contains all metadata for a single product (book, ebook, etc.).
    This is a placeholder; fields will be expanded with ONIX blocks:
    - Block 1: Product description
    - Block 2: Marketing collateral detail
    - Block 3: Content detail
    - Block 4: Publishing detail
    - Block 5: Related material
    - Block 6: Product supply
    - Block 7: Promotion detail
    - Block 8: Production detail
    """

    pass


class ONIXMessage(ONIXAttributes):
    """Root ONIX message container.

    An ONIX message contains:
    - A Header with sender/addressee information
    - Zero or more Product records
    - A NoProduct flag (automatically True when no products are included)

    The 'release' attribute indicates the ONIX version (e.g., "3.1").

    Note:
        The `products` list and `no_product` flag are mutually exclusive.
        When `products` is empty, `no_product` is automatically set to True.

    Example usage:
        >>> from onix import ONIXMessage, Header, Product
        >>> message = ONIXMessage(
        ...     release="3.1",
        ...     header=Header(),
        ...     products=[Product(), Product()],
        ... )
    """

    release: str = "3.1"
    header: Header
    products: list[Product] = []
    no_product: bool = False

    @model_validator(mode="after")
    def _validate_products_no_product(self) -> "ONIXMessage":
        """Ensure products and no_product are mutually exclusive."""
        if self.products and self.no_product:
            raise ValueError(
                "Cannot have both 'products' and 'no_product=True'. "
                "Either provide products or set no_product=True, not both."
            )
        if not self.products:
            self.no_product = True
        return self
