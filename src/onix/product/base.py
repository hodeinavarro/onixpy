"""Base model for ONIX Product.

Provides the ProductBase class with shared ONIX attributes.
This is separated from product.py to avoid circular imports
when block models need to reference shared attributes.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ONIXAttributes(BaseModel):
    """Shared ONIX attributes that may appear on any element.

    These attributes carry metadata about the data itself:
    - datestamp: Date/time the data was created or last updated
    - sourcename: Name of the source of the data
    - sourcetype: Code from List 3 indicating the type of source
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    datestamp: str | None = None
    sourcename: str | None = None
    sourcetype: str | None = None


class ProductBase(ONIXAttributes):
    """Base class for Product with shared ONIX attributes.

    Block models will be added as fields in the Product subclass.
    """

    pass
