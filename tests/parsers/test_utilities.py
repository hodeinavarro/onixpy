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
