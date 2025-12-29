import pytest

from onix.product.b1.p3 import (
    DescriptiveDetail,
    EpubLicenseExpression,
    EpubUsageConstraint,
    EpubUsageLimit,
    ProductClassification,
    ProductFormFeature,
)


class TestProductB1P3:
    def test_product_form_feature_valid_and_invalid(self):
        # Valid
        pf = ProductFormFeature(
            product_form_feature_type="02", product_form_feature_value="BLK"
        )
        assert pf.product_form_feature_type == "02"

        # Invalid format
        with pytest.raises(ValueError):
            ProductFormFeature(product_form_feature_type="2")

        # Invalid code (not in list)
        with pytest.raises(ValueError):
            ProductFormFeature(product_form_feature_type="99")

    def test_epub_usage_limit_and_constraint_validations(self):
        # Valid limit
        lim = EpubUsageLimit(quantity="10", epub_usage_unit="07")
        assert lim.quantity == "10"

        # Invalid unit (non-digit)
        with pytest.raises(ValueError):
            EpubUsageLimit(quantity="10", epub_usage_unit="AA")

        # Constraint valid with limit
        c = EpubUsageConstraint(
            epub_usage_type="05",
            epub_usage_status="03",
            epub_usage_limit=[{"Quantity": "5", "EpubUsageUnit": "07"}],
        )
        assert c.epub_usage_type == "05"

        # Invalid type format
        with pytest.raises(ValueError):
            EpubUsageConstraint(epub_usage_type="5", epub_usage_status="03")

        # Invalid status code
        with pytest.raises(ValueError):
            EpubUsageConstraint(epub_usage_type="05", epub_usage_status="99")

    def test_epub_license_expression_proprietary_requires_name(self):
        # Proprietary type '01' requires type name
        with pytest.raises(ValueError):
            EpubLicenseExpression(
                epub_license_expression_type="01",
                epub_license_expression_link="http://x",
            )

        # Non-proprietary ok
        EpubLicenseExpression(
            epub_license_expression_type="10", epub_license_expression_link="http://x"
        )

    def test_product_classification_percent_and_proprietary(self):
        # Valid classification
        pc = ProductClassification(
            product_classification_type="02", product_classification_code="55101514"
        )
        assert pc.product_classification_type == "02"

        # Percent non-numeric
        with pytest.raises(ValueError):
            ProductClassification(
                product_classification_type="02",
                product_classification_code="55101514",
                percent="abc",
            )

        # Percent out of range
        with pytest.raises(ValueError):
            ProductClassification(
                product_classification_type="02",
                product_classification_code="55101514",
                percent="200",
            )

        # Proprietary type requires name
        with pytest.raises(ValueError):
            ProductClassification(
                product_classification_type="01", product_classification_code="x"
            )

    def test_descriptive_detail_validations(self):
        # Valid minimal descriptive detail
        dd = DescriptiveDetail(product_composition="00", product_form="BB")
        assert dd.product_composition == "00"

        # Invalid product_composition format
        with pytest.raises(ValueError):
            DescriptiveDetail(product_composition="0", product_form="BB")

        # Invalid product_form format
        with pytest.raises(ValueError):
            DescriptiveDetail(product_composition="00", product_form="B")

        # product_form_details invalid pattern
        with pytest.raises(ValueError):
            DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                product_form_details=["1234"],
            )

        # product_packaging invalid
        with pytest.raises(ValueError):
            DescriptiveDetail(
                product_composition="00", product_form="BB", product_packaging="X"
            )

        # country_of_manufacture invalid
        with pytest.raises(ValueError):
            DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                country_of_manufacture="USA",
            )

        # map_scales invalid
        with pytest.raises(ValueError):
            DescriptiveDetail(
                product_composition="00", product_form="BB", map_scales=["abc"]
            )
