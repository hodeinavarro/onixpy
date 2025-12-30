"""Tests for ONIXModel base class normalization and validation."""

from __future__ import annotations

import pytest
from pydantic import Field

from onix._base import ONIXModel


class SimpleTestModel(ONIXModel):
    """Simple test model for base functionality."""

    name: str | None = Field(
        default=None,
    )
    value: int | None = Field(
        default=None,
    )


class NestedTestModel(ONIXModel):
    """Test model with nested structures for normalization testing."""

    name: str | None = Field(default=None)
    items: list[str | None] = Field(default_factory=list)
    nested: dict[str, str | None] | None = Field(default=None)


class TestONIXModelNormalization:
    """Test ONIXModel string normalization (empty strings become None)."""

    def test_empty_string_normalization(self):
        """Empty strings in input should be normalized to None."""
        # Test with dict input containing empty strings
        data = {"name": "", "value": 42}
        model = SimpleTestModel.model_validate(data)
        assert model.name is None
        assert model.value == 42

        # Test with constructor - this should also trigger normalization
        model2 = SimpleTestModel(name="", value=42)
        assert model2.name is None
        assert model2.value == 42

    def test_mixed_empty_and_valid_strings(self):
        """Mix of empty and valid strings should be handled correctly."""
        model = SimpleTestModel(name="valid", value=0)
        assert model.name == "valid"
        assert model.value == 0

    def test_nested_empty_string_normalization(self):
        """Empty strings in nested structures should be normalized recursively."""
        data = {
            "name": "test",
            "items": ["valid", "", "another"],
            "nested": {"key1": "value1", "key2": "", "key3": "value3"},
        }
        model = NestedTestModel.model_validate(data)
        assert model.name == "test"
        assert model.items == ["valid", None, "another"]
        assert model.nested == {"key1": "value1", "key2": None, "key3": "value3"}

    def test_non_dict_input_raises_error(self):
        """Non-dict inputs should raise TypeError."""
        with pytest.raises(TypeError, match="ONIXModel expects a dict input, got str"):
            SimpleTestModel.model_validate("not a dict")
