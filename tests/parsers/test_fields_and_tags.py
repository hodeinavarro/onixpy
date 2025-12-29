"""Tests for tag and field name conversion utilities."""

from onix.parsers import fields, tags


class TestCamelSnakeConversions:
    """Tests for CamelCase to snake_case conversions."""

    def test_camel_snake_edge_cases(self):
        """Test edge cases in CamelCase to snake_case conversion."""
        assert fields._camel_to_snake("ISBNNumber") == "isbn_number"
        assert fields._camel_to_snake("XMLHTTPServer") == "xmlhttp_server"
        assert fields._snake_to_camel("isni_code") == "ISNICode"
        assert fields._snake_to_camel("xml_url") == "XMLURL"

    def test_camel_and_snake_conversions(self):
        """Test basic CamelCase and snake_case conversions."""
        assert fields._camel_to_snake("IDType") == "id_type"
        assert fields._camel_to_snake("ProductIdentifier") == "product_identifier"
        assert fields._snake_to_camel("product_id") == "ProductID"
        assert fields._snake_to_camel("record_reference") == "RecordReference"


class TestTagMappingsAndLoadingBehavior:
    """Tests for tag mapping registration and lazy loading."""

    def test_tag_mappings_load_and_idempotent(self):
        """Verify tag mappings load deterministically and are idempotent."""
        # Clear any existing caches
        fields.clear_caches()
        tags._REFERENCE_TO_SHORT.clear()
        tags._SHORT_TO_REFERENCE.clear()

        # First build
        tags._ensure_mappings_loaded()
        assert tags._REFERENCE_TO_SHORT.get("ONIXMessage") == "ONIXmessage"
        # Known field mapping extracted from Header should exist
        assert tags.to_short_tag("Sender") == "sender"
        assert tags.to_reference_tag("sender") == "Sender"

        # Idempotent: calling again does not raise and keeps mappings
        tags._ensure_mappings_loaded()
        assert tags.to_short_tag("Sender") == "sender"

        # Restore canonical field mappings for downstream tests
        from onix.parsers.xml import _register_models

        _register_models()

    def test_tag_mapping_functions_from_models(self):
        """Test tag mapping functions work on registered models."""
        # Ensure tag mappings are (lazily) loaded
        short = tags.to_short_tag("Sender")
        ref = tags.to_reference_tag(short)
        assert tags.is_short_tag(short)
        assert tags.is_reference_tag(ref)
        assert ref == "Sender"


class TestUnknownTagPassthrough:
    """Tests for handling of unknown tags."""

    def test_unknown_tag_passthrough(self):
        """Unknown tags should be returned unchanged."""
        # Unknown tags should be returned unchanged
        assert tags.to_short_tag("UnknownTag") == "UnknownTag"
        assert tags.to_reference_tag("unknowntag") == "unknowntag"
