"""Record source identifier composite (P.1.4).

A group of data elements which together define an identifier of the
organization which is the source of the ONIX record.
"""

from __future__ import annotations

from pydantic import Field, field_validator, model_validator

from onix._base import ONIXModel, validate_proprietary_id_type
from onix.lists import get_code


class RecordSourceIdentifier(ONIXModel):
    """Record source identifier composite.

    Elements:
    - RecordSourceIDType: Code from List 44 (required)
    - IDTypeName: Name of proprietary scheme (optional; required when type='01')
    - IDValue: Identifier value (required)
    """

    # P.1.5 Record source ID type (mandatory)
    record_source_id_type: str = Field(
        alias="RecordSourceIDType",
        json_schema_extra={
            "short_tag": "x311",
        },
    )
    # P.1.6 ID type name (optional)
    id_type_name: str | None = Field(
        default=None,
        alias="IDTypeName",
        max_length=100,
        json_schema_extra={
            "short_tag": "b233",
        },
    )
    # P.1.7 ID value (mandatory)
    id_value: str = Field(
        alias="IDValue",
        json_schema_extra={
            "short_tag": "b244",
        },
    )

    @field_validator("record_source_id_type")
    @classmethod
    def _validate_record_source_id_type(cls, v: str) -> str:
        if len(v) != 2 or not v.isdigit():
            raise ValueError(
                f"Invalid RecordSourceIDType format: '{v}' must be exactly 2 digits"
            )
        if get_code(44, v) is None:
            raise ValueError(
                f"Invalid RecordSourceIDType: '{v}' is not a valid List 44 code"
            )
        return v

    @model_validator(mode="after")
    def _require_id_type_name_for_proprietary(self) -> "RecordSourceIdentifier":
        """Require id_type_name when record_source_id_type is '01' (proprietary)."""
        validate_proprietary_id_type(
            self.record_source_id_type, self.id_type_name, "RecordSourceIDType"
        )
        return self
