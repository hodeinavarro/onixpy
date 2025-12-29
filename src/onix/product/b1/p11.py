"""ONIX Block 1, P.11: Extents and other content.

Measure and Extent composites for product dimensions and extent information.
"""

from __future__ import annotations

from pydantic import Field, field_validator

from onix._base import ONIXModel
from onix.lists import get_code


class Measure(ONIXModel):
    """Measure composite.

    Provides measurement information for the product (e.g., height, width, weight).

    Required fields:
    - measure_type: Code from List 48
    - measurement: Numeric measurement value
    - measure_unit_code: Unit of measurement from List 50
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

    Required fields:
    - extent_type: Code from List 23
    - extent_value: Numeric extent value
    - extent_unit: Unit of extent
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
