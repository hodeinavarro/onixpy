from pathlib import Path

import pytest
from lxml import etree

from onix.parsers.rng_validator import (
    RNGValidationError,
    _get_rng_validator,
    validate_xml_element,
    validate_xml_file,
    validate_xml_string,
)


class TestRNGValidatorExtra:
    def test_get_rng_validator_file_not_found(self, tmp_path: Path):
        missing = tmp_path / "no-schema.rng"
        with pytest.raises(FileNotFoundError):
            _get_rng_validator(missing)

    def test_get_rng_validator_returns_relaxng(self):
        validator = _get_rng_validator()
        assert isinstance(validator, etree.RelaxNG)

    def test_validate_xml_element_reports_errors(self):
        # Missing Header should cause RNG validation failure
        elem = etree.fromstring(b"<ONIXMessage release='3.1'/>")
        with pytest.raises(RNGValidationError) as exc_info:
            validate_xml_element(elem)
        assert exc_info.value.errors

    def test_validate_xml_string_malformed_raises(self):
        bad_xml = "<ONIXMessage><Header></ONIXMessage>"
        with pytest.raises(etree.XMLSyntaxError):
            validate_xml_string(bad_xml)

    def test_validate_xml_file_not_found(self, tmp_path: Path):
        with pytest.raises(FileNotFoundError):
            validate_xml_file(tmp_path / "nope.xml")

    def test_custom_schema_validation_success_and_failure(self, tmp_path: Path):
        # Create a minimal relax-ng grammar accepting <root/> elements
        rng_path = tmp_path / "simple.rng"
        rng_path.write_text(
            """
            <grammar xmlns="http://relaxng.org/ns/structure/1.0">
              <start>
                <element name="root">
                  <empty/>
                </element>
              </start>
            </grammar>
            """,
            encoding="utf-8",
        )

        validator = _get_rng_validator(rng_path)
        assert isinstance(validator, etree.RelaxNG)

        # Valid XML
        elem = etree.fromstring(b"<root/>")
        # Should not raise
        validate_xml_element(elem, schema_path=rng_path)
        validate_xml_string("<root/>", schema_path=rng_path)

        # Invalid XML should raise RNGValidationError and capture errors
        bad_elem = etree.fromstring(b"<other/>")
        with pytest.raises(RNGValidationError) as exc_info:
            validate_xml_element(bad_elem, schema_path=rng_path)
        assert exc_info.value.errors

        # Validate via file path
        xml_file = tmp_path / "f.xml"
        xml_file.write_text("<root/>", encoding="utf-8")
        validate_xml_file(xml_file, schema_path=rng_path)

        xml_bad_file = tmp_path / "b.xml"
        xml_bad_file.write_text("<other/>", encoding="utf-8")
        with pytest.raises(RNGValidationError):
            validate_xml_file(xml_bad_file, schema_path=rng_path)

    def test_invalid_rng_raises_relaxngparseerror(self, tmp_path: Path):
        bad_rng = tmp_path / "bad.rng"
        # Well-formed XML but not a valid RNG grammar
        bad_rng.write_text("<root/>", encoding="utf-8")
        with pytest.raises(etree.RelaxNGParseError):
            _get_rng_validator(bad_rng)
