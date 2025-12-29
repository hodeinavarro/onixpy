"""ONIX Product model.

The Product composite is the central element of an ONIX message,
containing all metadata for a single product.
"""

from __future__ import annotations

from onix.product.base import ProductBase


class Product(ProductBase):
    """ONIX product record.

    Contains all metadata for a single product (book, ebook, etc.).

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
        >>> product = Product()
    """

    pass
