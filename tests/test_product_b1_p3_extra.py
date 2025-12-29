import pytest

from onix.product.b1 import p3


class TestProductFormFeatureValidators:
    def test_invalid_product_form_feature_type_non_digit(self):
        with pytest.raises(ValueError):
            p3.ProductFormFeature(product_form_feature_type="A1")

    def test_invalid_product_form_feature_type_not_in_list(self):
        # '99' is not defined in List 79
        with pytest.raises(ValueError):
            p3.ProductFormFeature(product_form_feature_type="99")

    def test_product_form_feature_description_too_long(self):
        long_desc = "x" * 10001
        with pytest.raises(ValueError):
            p3.ProductFormFeature(
                product_form_feature_type="02",
                product_form_feature_description=[long_desc],
            )


class TestEpubUsageAndLicenseValidators:
    def test_epub_usage_unit_invalid(self):
        with pytest.raises(ValueError):
            p3.EpubUsageLimit(quantity="10", epub_usage_unit="7")  # wrong length

    def test_epub_usage_type_invalid(self):
        with pytest.raises(ValueError):
            p3.EpubUsageConstraint(epub_usage_type="X5", epub_usage_status="03")

    def test_epub_usage_status_invalid(self):
        with pytest.raises(ValueError):
            p3.EpubUsageConstraint(epub_usage_type="05", epub_usage_status="3")

    def test_epub_license_expression_invalid_type_and_missing_name_for_proprietary(
        self,
    ):
        # Invalid type format
        with pytest.raises(ValueError):
            p3.EpubLicenseExpression(
                epub_license_expression_type="X1",
                epub_license_expression_link="http://x",
            )

        # Proprietary type '01' requires a type name
        with pytest.raises(ValueError):
            p3.EpubLicenseExpression(
                epub_license_expression_type="01",
                epub_license_expression_link="http://x",
            )

        # Proper proprietary use passes
        e = p3.EpubLicenseExpression(
            epub_license_expression_type="01",
            epub_license_expression_type_name="MyFormat",
            epub_license_expression_link="http://x",
        )
        assert e.epub_license_expression_type_name == "MyFormat"

    def test_epub_license_name_too_long(self):
        big_name = "a" * 101
        with pytest.raises(ValueError):
            p3.EpubLicense(epub_license_name=[big_name])


class TestProductClassificationAndPercent:
    def test_percent_not_a_number(self):
        with pytest.raises(ValueError):
            p3.ProductClassification(
                product_classification_type="02",
                product_classification_code="55101514",
                percent="not-a-number",
            )

    def test_percent_out_of_range(self):
        with pytest.raises(ValueError):
            p3.ProductClassification(
                product_classification_type="02",
                product_classification_code="55101514",
                percent="200",
            )

    def test_proprietary_classification_requires_name(self):
        # '01' is proprietary and requires a name
        with pytest.raises(ValueError):
            p3.ProductClassification(
                product_classification_type="01",
                product_classification_code="X",
                percent="50",
            )

        # With name, it passes
        pc = p3.ProductClassification(
            product_classification_type="01",
            product_classification_type_name="MyScheme",
            product_classification_code="X",
        )
        assert pc.product_classification_type_name == "MyScheme"


class TestDescriptiveDetailValidators:
    def test_product_composition_invalid(self):
        with pytest.raises(ValueError):
            p3.DescriptiveDetail(product_composition="A", product_form="BB")

    def test_product_form_invalid_length_and_format(self):
        with pytest.raises(ValueError):
            p3.DescriptiveDetail(product_composition="00", product_form="B")
        with pytest.raises(ValueError):
            p3.DescriptiveDetail(product_composition="00", product_form="b1")

    def test_product_form_not_in_list(self):
        # Use a code not present in List 150
        with pytest.raises(ValueError):
            p3.DescriptiveDetail(product_composition="00", product_form="QZ")

    def test_product_form_details_invalid_format_and_not_in_list(self):
        with pytest.raises(ValueError):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                product_form_details=["1234"],
            )  # bad format
        with pytest.raises(ValueError):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                product_form_details=["Z999"],
            )  # not in list

    def test_product_form_descriptions_too_long(self):
        long_desc = "x" * 201
        with pytest.raises(ValueError):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                product_form_descriptions=[long_desc],
            )

    def test_product_packaging_invalid(self):
        with pytest.raises(ValueError):
            p3.DescriptiveDetail(
                product_composition="00", product_form="BB", product_packaging="X1"
            )

    def test_trade_category_invalid(self):
        with pytest.raises(ValueError):
            p3.DescriptiveDetail(
                product_composition="00", product_form="BB", trade_category="X1"
            )

    def test_primary_and_product_content_types_invalid(self):
        with pytest.raises(ValueError):
            p3.DescriptiveDetail(
                product_composition="00", product_form="BB", primary_content_type="X1"
            )
        with pytest.raises(ValueError):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                product_content_types=["X1"],
            )

    def test_country_of_manufacture_invalid(self):
        with pytest.raises(ValueError):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                country_of_manufacture="usa",
            )
        with pytest.raises(ValueError):
            p3.DescriptiveDetail(
                product_composition="00", product_form="BB", country_of_manufacture="ZZ"
            )

    def test_epub_technical_protections_invalid(self):
        with pytest.raises(ValueError):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                epub_technical_protections=["X1"],
            )

    def test_map_scales_invalid(self):
        with pytest.raises(ValueError):
            p3.DescriptiveDetail(
                product_composition="00", product_form="BB", map_scales=["abc"]
            )
        with pytest.raises(ValueError):
            p3.DescriptiveDetail(
                product_composition="00", product_form="BB", map_scales=["123456789"]
            )  # 9 digits

    def test_valid_cases_exercise_success_branches(self):
        # ProductFormFeature valid boundary desc length
        pf = p3.ProductFormFeature(
            product_form_feature_type="02",
            product_form_feature_description=["x" * 10000],
        )
        assert pf.product_form_feature_type == "02"

        # EpubUsageLimit and EpubUsageConstraint valid
        limit = p3.EpubUsageLimit(quantity="10", epub_usage_unit="07")
        assert limit.epub_usage_unit == "07"
        constraint = p3.EpubUsageConstraint(
            epub_usage_type="05", epub_usage_status="03", epub_usage_limit=[limit]
        )
        assert constraint.epub_usage_limit[0].quantity == "10"

        # EpubLicenseDate valid
        ed = p3.EpubLicenseDate(epub_license_date_role="14", date="20230101")
        assert ed.epub_license_date_role == "14"

        # EpubLicenseExpression non-proprietary (doesn't require type name)
        elex = p3.EpubLicenseExpression(
            epub_license_expression_type="10", epub_license_expression_link="http://x"
        )
        assert elex.epub_license_expression_type == "10"

        # EpubLicense with valid name
        el = p3.EpubLicense(epub_license_name=["My License"])
        assert el.epub_license_name == ["My License"]

        # DescriptiveDetail with many valid fields
        dd = p3.DescriptiveDetail(
            product_composition="00",
            product_form="BB",
            product_form_details=["B206"],
            product_packaging="05",
            trade_category="03",
            primary_content_type="10",
            product_content_types=["11"],
            country_of_manufacture="US",
            epub_technical_protections=["03"],
            map_scales=["50000"],
        )
        assert dd.product_form == "BB"
        assert dd.product_form_details == ["B206"]
        assert dd.country_of_manufacture == "US"
