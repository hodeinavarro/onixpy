"""Tests for parser utility functions and model registration."""

from pydantic import BaseModel, Field

from onix.parsers import fields
from onix.parsers.xml import _element_to_dict, _parse_xml_string


class TestRegisterModelAndPluralMapping:
    """Tests for model registration and plural field mapping."""

    def test_register_model_and_plural_mapping_and_clear_caches(self):
        """Model registration and cache clearing work correctly."""

        class Dummy(BaseModel):
            my_field: str = Field(
                alias="MyField", json_schema_extra={"short_tag": "myfield"}
            )

        # Ensure caches are clear first
        fields.clear_caches()

        # Register model and assert mapping takes effect
        fields.register_model(Dummy)
        assert fields.tag_to_field_name("MyField") == "my_field"
        assert fields.field_name_to_tag("my_field") == "MyField"

        # Register plural mapping and list-field behavior
        fields.register_plural_mapping("Product", "products")
        assert fields.tag_to_field_name("Product") == "products"
        assert fields.field_name_to_tag("products") == "Product"
        assert fields.is_list_field("products")

        # Clear caches resets plural/list registrations, then restore canonical mappings
        fields.clear_caches()
        assert not fields.is_list_field("products")
        # Re-register the canonical models so later tests aren't affected
        from onix.parsers.xml import _register_models

        _register_models()

    def test_field_overrides_functionality(self):
        """Test that field overrides work for special cases."""
        from onix.parsers import fields

        # Clear caches to start fresh
        fields.clear_caches()

        # Save originals
        original_field_overrides = fields._FIELD_OVERRIDES.copy()
        original_tag_overrides = fields._TAG_OVERRIDES.copy()

        try:
            # Test tag_to_field_name override
            fields._FIELD_OVERRIDES["SpecialTag"] = "special_field"

            assert fields.tag_to_field_name("SpecialTag") == "special_field"
            # Non-override should still work
            assert fields.tag_to_field_name("NormalTag") == "normal_tag"

            # Clear caches between sections
            fields.clear_caches()

            # Test field_name_to_tag override
            fields._TAG_OVERRIDES["special_field"] = "SpecialTag"

            assert fields.field_name_to_tag("special_field") == "SpecialTag"
            # Non-override should still work
            assert fields.field_name_to_tag("normal_field") == "NormalField"
        finally:
            # Restore original overrides
            fields._FIELD_OVERRIDES.clear()
            fields._FIELD_OVERRIDES.update(original_field_overrides)
            fields._TAG_OVERRIDES.clear()
            fields._TAG_OVERRIDES.update(original_tag_overrides)

            # Clear caches and re-register models
            fields.clear_caches()
            from onix.parsers.xml import _register_models

            _register_models()


class TestElementToDictNormalization:
    """Tests for XML element to dictionary conversion."""

    def test_element_to_dict_normalizes_short_tags(self):
        """Element to dict conversion normalizes tag names correctly."""
        # Mix reference Header with a short-name Sender inside
        xml = """<ONIXMessage>
<Header>
<sender>
<SenderName>Acme Publishing</SenderName>
</sender>
</Header>
</ONIXMessage>"""
        root = _parse_xml_string(xml)
        data = _element_to_dict(root, normalize_tags=True)

        # Header -> header, Sender -> sender -> sender_name
        assert "header" in data
        header = data["header"]
        if isinstance(header, list):
            header = header[0]
        assert header["sender"]["sender_name"] == "Acme Publishing"
