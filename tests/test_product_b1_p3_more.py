import pytest

from onix.product.b1.p3 import (
    DescriptiveDetail,
    EpubLicense,
    EpubLicenseDate,
    EpubLicenseExpression,
    ProductClassification,
    ProductFormFeature,
)
from onix.product.b1.p11 import Measure


class TestProductB1P3More:
    def test_product_form_feature_description_too_long(self):
        long_desc = "x" * 10001
        with pytest.raises(ValueError):
            ProductFormFeature(
                product_form_feature_type="02",
                product_form_feature_description=[long_desc],
            )

    def test_epub_license_expression_link_too_long(self):
        long_link = "http://" + "x" * 301
        with pytest.raises(ValueError):
            EpubLicenseExpression(
                epub_license_expression_type="10",
                epub_license_expression_link=long_link,
            )

    def test_epub_license_name_too_long(self):
        long_name = "A" * 101
        with pytest.raises(ValueError):
            EpubLicense(epub_license_name=[long_name])

    def test_epub_license_date_invalid_role(self):
        with pytest.raises(ValueError):
            EpubLicenseDate(epub_license_date_role="A", date="20220101")
        with pytest.raises(ValueError):
            EpubLicenseDate(epub_license_date_role="99", date="20220101")

    def test_product_classification_percent_edge_values(self):
        pc0 = ProductClassification(
            product_classification_type="02",
            product_classification_code="55101514",
            percent="0",
        )
        assert pc0.percent == "0"
        pc100 = ProductClassification(
            product_classification_type="02",
            product_classification_code="55101514",
            percent="100",
        )
        assert pc100.percent == "100"

    def test_descriptive_detail_primary_and_content_types_and_measures(self):
        # Valid primary content type and product content types
        dd = DescriptiveDetail(
            product_composition="00",
            product_form="BB",
            primary_content_type="10",
            product_content_types=["11"],
        )
        assert dd.primary_content_type == "10"
        assert dd.product_content_types == ["11"]

        # Invalid primary content type
        with pytest.raises(ValueError):
            DescriptiveDetail(
                product_composition="00", product_form="BB", primary_content_type="99"
            )

        # Invalid product_content_types element
        with pytest.raises(ValueError):
            DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                product_content_types=["99"],
            )

        # Measures: valid measure should work
        m = Measure(measure_type="01", measurement="8.25", measure_unit_code="mm")
        dd2 = DescriptiveDetail(
            product_composition="00", product_form="BB", measures=[m]
        )
        assert dd2.measures[0].measurement == "8.25"

    def test_descriptive_detail_epub_technical_protections_and_map_scales(self):
        with pytest.raises(ValueError):
            DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                epub_technical_protections=["99"],
            )

        with pytest.raises(ValueError):
            DescriptiveDetail(
                product_composition="00", product_form="BB", map_scales=["123456789"]
            )  # >8 digits

    def test_product_form_descriptions_too_long(self):
        long_desc = "x" * 201
        with pytest.raises(ValueError):
            DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                product_form_descriptions=[long_desc],
            )

    def test_product_form_detail_valid_and_invalid(self):
        # Valid example from spec
        dd = DescriptiveDetail(
            product_composition="00", product_form="BB", product_form_details=["B206"]
        )
        assert dd.product_form_details == ["B206"]
        # Invalid pattern
        with pytest.raises(ValueError):
            DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                product_form_details=["1234"],
            )
