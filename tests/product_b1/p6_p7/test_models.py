"""Tests for Block 1, Sections 6-7 (P.6-P.7) - Titles and Contributors."""

import pytest

from onix.product.b1.p6 import TitleDetail, TitleElement
from onix.product.b1.p7 import (
    Contributor,
    NameIdentifier,
    Website,
)


class TestTitleElementAndDetailValidation:
    """Tests for TitleElement and TitleDetail models."""

    def test_title_element_valid_with_title_text(self):
        """Valid TitleElement with title_text."""
        te = TitleElement(TitleElementLevel="01", title_text="A Title")
        assert te.title_text == "A Title"

    def test_title_element_missing_required_fields(self):
        """TitleElement requires either title_text or structured parts."""
        with pytest.raises(ValueError):
            TitleElement(TitleElementLevel="01")

    def test_title_element_text_excludes_prefix_combination(self):
        """title_text cannot be combined with title_prefix."""
        with pytest.raises(ValueError):
            TitleElement(TitleElementLevel="01", title_text="X", title_prefix="Y")

    def test_title_element_without_prefix_requires_content(self):
        """title_without_prefix requires either title_prefix or no_prefix."""
        with pytest.raises(ValueError):
            TitleElement(TitleElementLevel="01", title_without_prefix="X")

    def test_title_element_prefix_no_prefix_mutually_exclusive(self):
        """title_prefix and no_prefix are mutually exclusive."""
        with pytest.raises(ValueError):
            TitleElement(
                TitleElementLevel="01",
                title_without_prefix="X",
                title_prefix="P",
                no_prefix=True,
            )

    def test_title_detail_requires_at_least_one_element(self):
        """TitleDetail requires at least one TitleElement."""
        with pytest.raises(ValueError):
            TitleDetail(TitleType="01", TitleElement=[])

    def test_title_detail_valid(self):
        """Valid TitleDetail with title_elements."""
        td = TitleDetail(
            TitleType="01",
            TitleElement=[
                TitleElement(
                    TitleElementLevel="01",
                    title_text="X",
                )
            ],
        )
        assert td.title_type == "01"


class TestContributorRelatedValidations:
    """Tests for Contributor, NameIdentifier, and Website models."""

    def test_name_identifier_invalid_code(self):
        """NameIdentifier type code must be valid from List 44."""
        with pytest.raises(ValueError):
            NameIdentifier(NameIDType="99", IDValue="x")

    def test_website_requires_link(self):
        """Website requires at least one link."""
        with pytest.raises(ValueError):
            Website(website_role="01", WebsiteLink=[])

    def test_contributor_structured_parts_require_key_names(self):
        """Contributor: structured parts require key_names."""
        with pytest.raises(ValueError):
            Contributor(ContributorRole=["A01"], titles_before_names="Prof")

    def test_contributor_translator_languages_only_for_translators(self):
        """from_language only valid for translator roles."""
        with pytest.raises(ValueError):
            Contributor(ContributorRole=["A01"], FromLanguage=["eng"])
