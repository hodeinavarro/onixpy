from onix.parsers import fields, tags


class TestParsersFieldsTagsExtra:
    def test_camel_snake_edge_cases(self):
        assert fields._camel_to_snake("ISBNNumber") == "isbn_number"
        assert fields._camel_to_snake("XMLHTTPServer") == "xmlhttp_server"
        assert fields._snake_to_camel("isni_code") == "ISNICode"
        assert fields._snake_to_camel("xml_url") == "XMLURL"

    def test_tag_mappings_load_and_idempotent(self):
        # Clear any existing caches and ensure mappings can be built deterministically
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

    def test_unknown_tag_passthrough(self):
        # Unknown tags should be returned unchanged
        assert tags.to_short_tag("UnknownTag") == "UnknownTag"
        assert tags.to_reference_tag("unknowntag") == "unknowntag"
