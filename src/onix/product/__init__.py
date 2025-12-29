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

from onix.product.product import Product, ProductIdentifier

__all__ = [
    "Product",
    "ProductIdentifier",
]
