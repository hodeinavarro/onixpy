"""Shared ONIX BaseModel with common pydantic configuration.

This central base provides flexible construction allowing both snake_case
field names and XML alias names. Models are configured with
`validate_by_name=True` and `validate_by_alias=True` for flexible
construction, and `serialize_by_alias=True` so XML tag names are used
during serialization. A `before` validator normalizes empty strings to
None before validation.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator


def validate_proprietary_id_type(
    id_type: str, id_type_name: str | None, field_name: str
) -> None:
    """Validate that proprietary ID types require an IDTypeName.

    Args:
        id_type: The ID type code (e.g., "01" for proprietary)
        id_type_name: The name of the proprietary scheme
        field_name: The field name for error messages (e.g., "SenderIDType")

    Raises:
        ValueError: If id_type is "01" but id_type_name is not provided
    """
    if id_type == "01" and not id_type_name:
        raise ValueError(f"IDTypeName is required for proprietary {field_name} '01'")


class ONIXModel(BaseModel):
    """Base Pydantic model for all ONIX data structures.

    Configures Pydantic to:
    - Forbid extra fields not defined in the model
    - Validate by both field names and aliases (for flexible construction)
    - Serialize using aliases (XML tag names)
    - Normalize empty strings to None before validation
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
        serialize_by_alias=True,
    )

    @model_validator(mode="before")
    @classmethod
    def _normalize_strings(cls, values: Any):
        """Before-validation hook.

        Normalize empty-string inputs to None for string fields. Allow
        both snake_case field names and alias names to be passed to
        constructors; pydantic is configured to validate by alias.
        """
        if not isinstance(values, dict):
            raise TypeError(
                f"ONIXModel expects a dict input, got {type(values).__name__}"
            )

        def normalize(value):
            if isinstance(value, dict):
                return {k: normalize(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [normalize(item) for item in value]
            elif value == "":
                return None
            else:
                return value

        return {k: normalize(v) for k, v in values.items()}
