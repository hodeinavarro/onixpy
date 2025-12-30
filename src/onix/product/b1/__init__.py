"""ONIX Product Block 1: Product description.

Exports all Block 1 (Product description) composites.
"""

from onix.product.b1.p1 import RecordSourceIdentifier
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
from onix.product.b1.p11 import Extent, Measure

__all__ = [
    # P.1 Record source and deletion
    "RecordSourceIdentifier",
    # P.3 Product form composites
    "DescriptiveDetail",
    "ProductFormFeature",
    "EpubUsageLimit",
    "EpubUsageConstraint",
    "EpubLicenseDate",
    "EpubLicenseExpression",
    "EpubLicense",
    "ProductClassification",
    # P.11 Extents and other content
    "Measure",
    "Extent",
]
