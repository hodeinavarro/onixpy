"""Tests for JSON parsing and serialization internals."""

import pytest

from onix.parsers.json import (
    _convert_reference_to_short,
    _normalize_input,
    _normalize_json_keys,
)


class TestJSONNormalizationAndKeyConversion:
    """Tests for JSON input normalization and key conversion utilities."""

    def test_normalize_input_file_not_found(self):
        """Non-existent files raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            _normalize_input("/nonexistent/file.json")

    def test_normalize_input_pathlike_file_not_found(self):
        """Non-existent PathLike files raise FileNotFoundError."""
        from pathlib import Path

        with pytest.raises(FileNotFoundError):
            _normalize_input(Path("/nonexistent/file.json"))

    def test_normalize_input_iterable_empty(self):
        """Empty iterable produces default structure."""
        data = _normalize_input([])
        assert data == {"header": {}, "products": []}

    def test_normalize_json_keys_short_to_reference(self):
        """Normalizing short tag names converts to reference names."""
        data = {"x507": True, "header": {"sender": {"sender_name": "X"}}}
        # x507 should map to NoProduct when normalized
        normalized = _normalize_json_keys(data)
        assert "NoProduct" in normalized

    def test_convert_reference_to_short(self):
        """Converting reference tags to short names works correctly."""
        data = {"Header": {"Sender": {"SenderName": "X"}}, "NoProduct": True}
        converted = _convert_reference_to_short(data)
        assert "header" in converted
        assert "x507" in converted
        assert converted["header"]["sender"]["x298"] == "X"

    def test_convert_reference_to_short_with_lists(self):
        """Converting reference tags to short names works with nested lists."""
        data = {
            "Header": {"Sender": {"SenderName": "X"}},
            "Product": [
                {"RecordReference": "123", "NotificationType": "03"},
                {"RecordReference": "456", "NotificationType": "02"},
            ],
        }
        converted = _convert_reference_to_short(data)
        assert "header" in converted
        assert "product" in converted
        assert len(converted["product"]) == 2
        assert converted["product"][0]["a001"] == "123"
        assert converted["product"][0]["a002"] == "03"
        assert converted["product"][1]["a001"] == "456"
        assert converted["product"][1]["a002"] == "02"
