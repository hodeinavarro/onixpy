"""ONIX DescriptiveDetail composite models.

Contains product descriptive information including titles, collections,
measurements, and extent.
"""

from __future__ import annotations

from pydantic import Field, field_validator

from onix._base import ONIXModel
from onix.lists import get_code
from onix.product.contributor import Contributor

# =============================================================================
# Title Composites
# =============================================================================


class TitleElement(ONIXModel):
    """Title element component (part of TitleDetail).

    Elements:
    - TitleElementLevel (B.202): Code from List 149 - required
    - TitleText (B.203): The title text - required
    - Subtitle (B.204): Optional subtitle
    """

    title_element_level: str = Field(
        alias="TitleElementLevel",
    )
    title_text: str = Field(
        alias="TitleText",
    )
    subtitle: str | None = Field(
        default=None,
        alias="Subtitle",
    )


class TitleDetail(ONIXModel):
    """Title detail composite.

    Provides detailed title information including title type and elements.

    Elements:
    - TitleType (B.201): Code from List 15 - required
    - TitleElement (0…n): Title elements
    """

    title_type: str = Field(
        alias="TitleType",
    )
    title_elements: list[TitleElement] = Field(
        default_factory=list,
        alias="TitleElement",
    )


# =============================================================================
# Measure and Extent Composites
# =============================================================================


class Measure(ONIXModel):
    """Measure composite.

    Provides measurement information for the product (e.g., height, width, weight).

    Elements:
    - MeasureType (B.328): Code from List 48 - required
    - Measurement (B.329): Numeric measurement value - required
    - MeasureUnitCode (B.330): Unit of measurement from List 50 - required
    """

    measure_type: str = Field(
        alias="MeasureType",
    )
    measurement: str = Field(
        alias="Measurement",
    )
    measure_unit_code: str = Field(
        alias="MeasureUnitCode",
    )

    @field_validator("measure_type")
    @classmethod
    def validate_measure_type(cls, v: str) -> str:
        """Validate measure_type is a valid List 48 code."""
        if get_code(48, v) is None:
            raise ValueError(f"Invalid MeasureType: '{v}' is not a valid List 48 code")
        return v

    @field_validator("measure_unit_code")
    @classmethod
    def validate_measure_unit_code(cls, v: str) -> str:
        """Validate measure_unit_code is a valid List 50 code."""
        if get_code(50, v) is None:
            raise ValueError(
                f"Invalid MeasureUnitCode: '{v}' is not a valid List 50 code"
            )
        return v


class Extent(ONIXModel):
    """Extent composite.

    Provides extent information (page count, duration, etc.).

    Elements:
    - ExtentType (B.301): Code from List 23 - required
    - ExtentValue (B.302): Numeric extent value - required
    - ExtentUnit (B.303): Unit of extent - required
    """

    extent_type: str = Field(
        alias="ExtentType",
    )
    extent_value: str = Field(
        alias="ExtentValue",
    )
    extent_unit: str = Field(
        alias="ExtentUnit",
    )


class Collection(ONIXModel):
    """Collection composite.

    Groups products into a collection or series.

    Elements:
    - CollectionType (B.360): Code from List 148 - required
    - CollectionSequenceNumber (B.365): Position in collection
    - CollectionTitle (B.366): Name of the collection
    """

    collection_type: str = Field(
        alias="CollectionType",
    )
    collection_sequence_number: str | None = Field(
        default=None,
        alias="CollectionSequenceNumber",
    )
    collection_title: str | None = Field(
        default=None,
        alias="CollectionTitle",
    )

    @field_validator("collection_type")
    @classmethod
    def validate_collection_type(cls, v: str) -> str:
        """Validate collection_type is a valid List 148 code."""
        if get_code(148, v) is None:
            raise ValueError(
                f"Invalid CollectionType: '{v}' is not a valid List 148 code"
            )
        return v


class DescriptiveDetail(ONIXModel):
    """DescriptiveDetail composite (Product Block 2).

    Contains descriptive information about the product including titles,
    contributors, subject information, and related details.

    Elements:
    - ProductComposition (B.200): Code indicating product composition
    - TitleDetail (0…n): Title details (including title, subtitle)
    - Contributor (0…n): Contributors (authors, editors, etc.)
    - Collection (0…n): Collection/series information
    - Measure (0…n): Measurements (height, width, weight, etc.)
    - Extent (0…n): Extent details (page count, duration, etc.)
    """

    product_composition: str | None = Field(
        default=None,
        alias="ProductComposition",
    )
    title_details: list[TitleDetail] = Field(
        default_factory=list,
        alias="TitleDetail",
    )
    contributors: list[Contributor] = Field(
        default_factory=list,
        alias="Contributor",
    )
    collections: list[Collection] = Field(
        default_factory=list,
        alias="Collection",
    )
    measures: list[Measure] = Field(
        default_factory=list,
        alias="Measure",
    )
    extents: list[Extent] = Field(
        default_factory=list,
        alias="Extent",
    )
