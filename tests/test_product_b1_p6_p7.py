import pytest

from onix.product.b1.p6 import TitleDetail, TitleElement
from onix.product.b1.p7 import (
    Contributor,
    NameIdentifier,
    Website,
)


class TestProductB1P6P7:
    def test_title_element_and_detail_validation(self):
        # Valid TitleElement with title_text
        te = TitleElement(title_element_level="01", title_text="A Title")
        assert te.title_text == "A Title"

        # Missing required fields
        with pytest.raises(ValueError):
            TitleElement(title_element_level="01")

        # title_text cannot be combined with title_prefix
        with pytest.raises(ValueError):
            TitleElement(title_element_level="01", title_text="X", title_prefix="Y")

        # title_without_prefix requires prefix or no_prefix
        with pytest.raises(ValueError):
            TitleElement(title_element_level="01", title_without_prefix="X")

        # mutually exclusive prefix/no_prefix
        with pytest.raises(ValueError):
            TitleElement(
                title_element_level="01",
                title_without_prefix="X",
                title_prefix="P",
                no_prefix=True,
            )

        # TitleDetail requires at least one TitleElement
        with pytest.raises(ValueError):
            TitleDetail(title_type="01", title_elements=[])

        # Valid TitleDetail
        td = TitleDetail(
            title_type="01",
            title_elements=[{"TitleElementLevel": "01", "TitleText": "X"}],
        )
        assert td.title_type == "01"

    def test_contributor_related_validations(self):
        # NameIdentifier invalid code
        with pytest.raises(ValueError):
            NameIdentifier(name_id_type="99", id_value="x")

        # Website requires link
        with pytest.raises(ValueError):
            Website(website_role="01", website_link=[])

        # Contributor: structured parts require key_names
        with pytest.raises(ValueError):
            Contributor(contributor_role=["A01"], titles_before_names="Prof")

        # Contributor: translator languages only valid for translator roles
        with pytest.raises(ValueError):
            Contributor(contributor_role=["A01"], from_language=["eng"])
