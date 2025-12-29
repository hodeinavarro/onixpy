"""Comprehensive validation tests for ONIX Block 1 P.3 (Product Form) composites.

Tests cover all P.3 composites with focus on:
- Code list membership validation (List 79, 145, 146, 147, 150, 175, etc.)
- Format and length constraints (2-digit codes, max lengths, character patterns)
- Required conditional fields (e.g., proprietary types require type names)
- Boundary cases (max-length descriptions, percent range 0-100)
- Valid instances exercising all success branches
"""

import pytest

from onix.product.b1 import p3
from onix.product.b1.p11 import Measure


class TestProductFormFeatureValidation:
    """Tests for ProductFormFeature model validation."""

    def test_type_must_be_exactly_two_digits(self):
        """ProductFormFeatureType code must be exactly 2 digits."""
        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            p3.ProductFormFeature(product_form_feature_type="A1")

    def test_type_must_exist_in_list_79(self):
        """ProductFormFeatureType must be valid code from List 79."""
        with pytest.raises(ValueError, match="must be from List 79"):
            p3.ProductFormFeature(product_form_feature_type="99")

    def test_description_rejects_exceeding_max_length_10000(self):
        """ProductFormFeatureDescription cannot exceed 10,000 characters."""
        with pytest.raises(ValueError, match="exceeds maximum length of 10,000"):
            p3.ProductFormFeature(
                product_form_feature_type="02",
                product_form_feature_description=["x" * 10001],
            )

    def test_description_accepts_exactly_max_length_10000(self):
        """ProductFormFeatureDescription of exactly 10,000 characters is valid."""
        pf = p3.ProductFormFeature(
            product_form_feature_type="02",
            product_form_feature_description=["x" * 10000],
        )
        assert len(pf.product_form_feature_description[0]) == 10000

    def test_valid_feature_with_type_and_value(self):
        """Valid ProductFormFeature with type and value."""
        pf = p3.ProductFormFeature(
            product_form_feature_type="02",  # Page edge color
            product_form_feature_value="BLK",
        )
        assert pf.product_form_feature_type == "02"
        assert pf.product_form_feature_value == "BLK"


class TestEpubUsageLimitValidation:
    """Tests for EpubUsageLimit model validation."""

    def test_usage_unit_must_be_exactly_two_digits(self):
        """EpubUsageUnit must be exactly 2 digits."""
        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            p3.EpubUsageLimit(quantity="10", epub_usage_unit="7")

    def test_usage_unit_must_exist_in_list_147(self):
        """EpubUsageUnit must be valid code from List 147."""
        # Code 97 is not defined in List 147
        with pytest.raises(ValueError, match="must be from List 147"):
            p3.EpubUsageLimit(quantity="10", epub_usage_unit="97")

    def test_valid_usage_limit_with_concurrent_users_unit(self):
        """Valid EpubUsageLimit with 'concurrent users' unit (code 07)."""
        limit = p3.EpubUsageLimit(quantity="10", epub_usage_unit="07")
        assert limit.quantity == "10"
        assert limit.epub_usage_unit == "07"


class TestEpubUsageConstraintValidation:
    """Tests for EpubUsageConstraint model validation."""

    def test_usage_type_must_be_exactly_two_digits(self):
        """EpubUsageType must be exactly 2 digits."""
        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            p3.EpubUsageConstraint(epub_usage_type="5", epub_usage_status="03")

    def test_usage_type_must_exist_in_list_145(self):
        """EpubUsageType must be valid code from List 145."""
        with pytest.raises(ValueError, match="must be from List 145"):
            p3.EpubUsageConstraint(epub_usage_type="99", epub_usage_status="03")

    def test_usage_status_must_be_exactly_two_digits(self):
        """EpubUsageStatus must be exactly 2 digits."""
        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            p3.EpubUsageConstraint(epub_usage_type="05", epub_usage_status="3")

    def test_usage_status_must_exist_in_list_146(self):
        """EpubUsageStatus must be valid code from List 146."""
        with pytest.raises(ValueError, match="must be from List 146"):
            p3.EpubUsageConstraint(epub_usage_type="05", epub_usage_status="99")

    def test_valid_constraint_prohibiting_text_to_speech(self):
        """Valid EpubUsageConstraint prohibiting text-to-speech."""
        constraint = p3.EpubUsageConstraint(
            epub_usage_type="05",  # Text-to-speech
            epub_usage_status="03",  # Prohibited
        )
        assert constraint.epub_usage_type == "05"
        assert constraint.epub_usage_status == "03"

    def test_valid_constraint_with_usage_limits(self):
        """Valid EpubUsageConstraint with embedded usage limits."""
        limit = p3.EpubUsageLimit(quantity="5", epub_usage_unit="04")  # Pages
        constraint = p3.EpubUsageConstraint(
            epub_usage_type="02",  # Extract
            epub_usage_status="02",  # Permitted with limit
            epub_usage_limit=[limit],
        )
        assert len(constraint.epub_usage_limit) == 1
        assert constraint.epub_usage_limit[0].quantity == "5"


class TestEpubLicenseDateValidation:
    """Tests for EpubLicenseDate model validation."""

    def test_date_role_must_be_exactly_two_digits(self):
        """EpubLicenseDateRole must be exactly 2 digits."""
        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            p3.EpubLicenseDate(epub_license_date_role="1", date="20230101")

    def test_date_role_must_exist_in_list_260(self):
        """EpubLicenseDateRole must be valid code from List 260."""
        with pytest.raises(ValueError, match="must be from List 260"):
            p3.EpubLicenseDate(epub_license_date_role="99", date="20230101")

    def test_valid_license_date_becomes_effective(self):
        """Valid EpubLicenseDate marking when license becomes effective."""
        ld = p3.EpubLicenseDate(
            epub_license_date_role="14",  # License becomes effective
            date="20220101",
        )
        assert ld.epub_license_date_role == "14"
        assert ld.date == "20220101"


class TestEpubLicenseExpressionValidation:
    """Tests for EpubLicenseExpression model validation."""

    def test_expression_type_must_be_exactly_two_digits(self):
        """EpubLicenseExpressionType must be exactly 2 digits."""
        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            p3.EpubLicenseExpression(
                epub_license_expression_type="1",
                epub_license_expression_link="http://example.com/license",
            )

    def test_expression_type_must_exist_in_list_218(self):
        """EpubLicenseExpressionType must be valid code from List 218."""
        with pytest.raises(ValueError, match="must be from List 218"):
            p3.EpubLicenseExpression(
                epub_license_expression_type="99",
                epub_license_expression_link="http://example.com/license",
            )

    def test_proprietary_type_requires_type_name(self):
        """Proprietary type (01) requires EpubLicenseExpressionTypeName."""
        with pytest.raises(
            ValueError,
            match="epub_license_expression_type_name is required when",
        ):
            p3.EpubLicenseExpression(
                epub_license_expression_type="01",  # Proprietary
                epub_license_expression_link="http://example.com/license",
            )

    def test_proprietary_with_required_type_name_passes(self):
        """Proprietary type with type name is valid."""
        expr = p3.EpubLicenseExpression(
            epub_license_expression_type="01",
            epub_license_expression_type_name="MyFormat",
            epub_license_expression_link="http://example.com/license",
        )
        assert expr.epub_license_expression_type_name == "MyFormat"

    def test_expression_link_rejects_exceeding_max_length_300(self):
        """EpubLicenseExpressionLink cannot exceed 300 characters."""
        long_link = "http://" + "x" * 301
        with pytest.raises(ValueError, match="(exceeds maximum length of 300|at most 300)"):
            p3.EpubLicenseExpression(
                epub_license_expression_type="10",
                epub_license_expression_link=long_link,
            )

    def test_valid_standard_format_onix_pl(self):
        """Valid EpubLicenseExpression with standard ONIX-PL format."""
        expr = p3.EpubLicenseExpression(
            epub_license_expression_type="10",  # ONIX-PL
            epub_license_expression_link="http://example.com/license.xml",
        )
        assert expr.epub_license_expression_type == "10"


class TestEpubLicenseValidation:
    """Tests for EpubLicense model validation."""

    def test_license_name_rejects_exceeding_max_length_100(self):
        """EpubLicenseName cannot exceed 100 characters."""
        with pytest.raises(ValueError, match="exceeds maximum length of 100"):
            p3.EpubLicense(epub_license_name=["x" * 101])

    def test_license_name_accepts_exactly_max_length_100(self):
        """EpubLicenseName of exactly 100 characters is valid."""
        lic = p3.EpubLicense(epub_license_name=["x" * 100])
        assert len(lic.epub_license_name[0]) == 100

    def test_valid_license_with_name_only(self):
        """Valid EpubLicense with just a name."""
        lic = p3.EpubLicense(epub_license_name=["Elsevier EULA v5"])
        assert lic.epub_license_name == ["Elsevier EULA v5"]

    def test_valid_license_with_expressions_and_dates(self):
        """Valid EpubLicense with embedded expressions and dates."""
        expr = p3.EpubLicenseExpression(
            epub_license_expression_type="10",
            epub_license_expression_link="http://example.com",
        )
        date = p3.EpubLicenseDate(epub_license_date_role="14", date="20230101")
        lic = p3.EpubLicense(
            epub_license_name=["My License"],
            epub_license_expression=[expr],
            epub_license_date=[date],
        )
        assert len(lic.epub_license_expression) == 1
        assert len(lic.epub_license_date) == 1


class TestProductClassificationValidation:
    """Tests for ProductClassification model validation."""

    def test_classification_type_must_be_exactly_two_digits(self):
        """ProductClassificationType must be exactly 2 digits."""
        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            p3.ProductClassification(
                product_classification_type="2",
                product_classification_code="55101514",
            )

    def test_classification_type_must_exist_in_list_9(self):
        """ProductClassificationType must be valid code from List 9."""
        with pytest.raises(ValueError, match="must be from List 9"):
            p3.ProductClassification(
                product_classification_type="99",
                product_classification_code="55101514",
            )

    def test_percent_rejects_non_numeric(self):
        """Percent must be a valid number."""
        # 'not-a-number' exceeds max 7 chars; use short non-numeric string
        with pytest.raises(ValueError, match="must be a valid number"):
            p3.ProductClassification(
                product_classification_type="02",
                product_classification_code="55101514",
                percent="abc",
            )

    def test_percent_rejects_out_of_range(self):
        """Percent must be between 0 and 100."""
        with pytest.raises(ValueError, match="must be between 0 and 100"):
            p3.ProductClassification(
                product_classification_type="02",
                product_classification_code="55101514",
                percent="200",
            )

    def test_percent_accepts_boundary_values(self):
        """Percent accepts 0, 100, and values in between."""
        pc_low = p3.ProductClassification(
            product_classification_type="02",
            product_classification_code="55101514",
            percent="0",
        )
        assert pc_low.percent == "0"

        pc_high = p3.ProductClassification(
            product_classification_type="02",
            product_classification_code="55101514",
            percent="100",
        )
        assert pc_high.percent == "100"

        pc_mid = p3.ProductClassification(
            product_classification_type="02",
            product_classification_code="55101514",
            percent="66.67",
        )
        assert pc_mid.percent == "66.67"

    def test_proprietary_type_requires_type_name(self):
        """Proprietary type (01) requires ProductClassificationTypeName."""
        with pytest.raises(
            ValueError,
            match="product_classification_type_name is required when",
        ):
            p3.ProductClassification(
                product_classification_type="01",  # Proprietary
                product_classification_code="X",
            )

    def test_proprietary_with_required_type_name_passes(self):
        """Proprietary type with type name is valid."""
        pc = p3.ProductClassification(
            product_classification_type="01",
            product_classification_type_name="MyScheme",
            product_classification_code="CUSTOM-123",
        )
        assert pc.product_classification_type_name == "MyScheme"

    def test_valid_unspsc_classification(self):
        """Valid ProductClassification with UNSPSC code."""
        pc = p3.ProductClassification(
            product_classification_type="02",  # UNSPSC
            product_classification_code="55101514",  # Sheet music
        )
        assert pc.product_classification_type == "02"


class TestDescriptiveDetailValidation:
    """Tests for DescriptiveDetail model validation."""

    # Product Composition validation
    def test_product_composition_must_be_exactly_two_digits(self):
        """ProductComposition must be exactly 2 digits."""
        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            p3.DescriptiveDetail(product_composition="0", product_form="BB")

    def test_product_composition_must_exist_in_list_2(self):
        """ProductComposition must be valid code from List 2."""
        with pytest.raises(ValueError, match="must be from List 2"):
            p3.DescriptiveDetail(product_composition="99", product_form="BB")

    # Product Form validation
    def test_product_form_must_be_exactly_two_characters(self):
        """ProductForm must be exactly 2 characters (letters or '00')."""
        with pytest.raises(ValueError, match="must be exactly 2 characters"):
            p3.DescriptiveDetail(product_composition="00", product_form="B")

    def test_product_form_must_be_uppercase_letters_or_00(self):
        """ProductForm must be uppercase letters or '00'."""
        with pytest.raises(ValueError, match="must be two uppercase letters"):
            p3.DescriptiveDetail(product_composition="00", product_form="b1")

    def test_product_form_must_exist_in_list_150(self):
        """ProductForm must be valid code from List 150."""
        with pytest.raises(ValueError, match="must be from List 150"):
            p3.DescriptiveDetail(product_composition="00", product_form="QZ")

    # Product Form Details validation
    def test_product_form_details_must_have_correct_format(self):
        """ProductFormDetail must be 1 letter + 3 digits."""
        with pytest.raises(ValueError, match="must be one letter followed by three digits"):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                product_form_details=["1234"],
            )

    def test_product_form_details_must_exist_in_list_175(self):
        """ProductFormDetail must be valid code from List 175."""
        with pytest.raises(ValueError, match="must be from List 175"):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                product_form_details=["Z999"],
            )

    # Product Form Descriptions validation
    def test_product_form_descriptions_reject_exceeding_max_length_200(self):
        """ProductFormDescription cannot exceed 200 characters."""
        with pytest.raises(ValueError, match="exceeds maximum length of 200"):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                product_form_descriptions=["x" * 201],
            )

    def test_product_form_descriptions_accept_exactly_max_length_200(self):
        """ProductFormDescription of exactly 200 characters is valid."""
        dd = p3.DescriptiveDetail(
            product_composition="00",
            product_form="BB",
            product_form_descriptions=["x" * 200],
        )
        assert len(dd.product_form_descriptions[0]) == 200

    # Product Packaging validation
    def test_product_packaging_must_be_exactly_two_digits(self):
        """ProductPackaging must be exactly 2 digits."""
        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                product_packaging="X1",
            )

    def test_product_packaging_must_exist_in_list_80(self):
        """ProductPackaging must be valid code from List 80."""
        with pytest.raises(ValueError, match="must be from List 80"):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                product_packaging="99",
            )

    # Trade Category validation
    def test_trade_category_must_be_exactly_two_digits(self):
        """TradeCategory must be exactly 2 digits."""
        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                trade_category="X1",
            )

    def test_trade_category_must_exist_in_list_12(self):
        """TradeCategory must be valid code from List 12."""
        with pytest.raises(ValueError, match="must be from List 12"):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                trade_category="99",
            )

    # Content Type validation
    def test_primary_content_type_must_be_exactly_two_digits(self):
        """PrimaryContentType must be exactly 2 digits."""
        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                primary_content_type="X1",
            )

    def test_primary_content_type_must_exist_in_list_81(self):
        """PrimaryContentType must be valid code from List 81."""
        with pytest.raises(ValueError, match="must be from List 81"):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                primary_content_type="99",
            )

    def test_product_content_types_must_be_exactly_two_digits_each(self):
        """ProductContentType codes must each be exactly 2 digits."""
        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                product_content_types=["X1"],
            )

    def test_product_content_types_must_exist_in_list_81(self):
        """ProductContentType codes must be valid from List 81."""
        with pytest.raises(ValueError, match="must be from List 81"):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                product_content_types=["99"],
            )

    # Country of Manufacture validation
    def test_country_of_manufacture_must_be_exactly_two_uppercase_letters(self):
        """CountryOfManufacture must be exactly 2 uppercase letters."""
        with pytest.raises(ValueError, match="must be exactly 2 uppercase letters"):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                country_of_manufacture="usa",
            )

    def test_country_of_manufacture_must_exist_in_list_91(self):
        """CountryOfManufacture must be valid code from List 91."""
        with pytest.raises(ValueError, match="must be from List 91"):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                country_of_manufacture="ZZ",
            )

    # E-publication Technical Protection validation
    def test_epub_technical_protections_must_be_exactly_two_digits_each(self):
        """EpubTechnicalProtection codes must each be exactly 2 digits."""
        with pytest.raises(ValueError, match="must be exactly 2 digits"):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                epub_technical_protections=["X1"],
            )

    def test_epub_technical_protections_must_exist_in_list_144(self):
        """EpubTechnicalProtection codes must be valid from List 144."""
        with pytest.raises(ValueError, match="must be from List 144"):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                epub_technical_protections=["99"],
            )

    # Map Scale validation
    def test_map_scales_must_be_positive_integers(self):
        """MapScale must be a positive integer."""
        with pytest.raises(ValueError, match="must be a positive integer"):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                map_scales=["abc"],
            )

    def test_map_scales_must_not_exceed_8_digits(self):
        """MapScale cannot exceed 8 digits."""
        with pytest.raises(ValueError, match="exceeds maximum length of 8 digits"):
            p3.DescriptiveDetail(
                product_composition="00",
                product_form="BB",
                map_scales=["123456789"],
            )

    def test_map_scales_accept_exactly_8_digits(self):
        """MapScale of exactly 8 digits is valid."""
        dd = p3.DescriptiveDetail(
            product_composition="00",
            product_form="BB",
            map_scales=["12345678"],
        )
        assert dd.map_scales == ["12345678"]

    # Measures validation
    def test_valid_measures_with_all_fields(self):
        """Valid Measures with height, width, and weight."""
        m1 = Measure(measure_type="01", measurement="8.25", measure_unit_code="mm")
        m2 = Measure(measure_type="02", measurement="10.5", measure_unit_code="in")
        dd = p3.DescriptiveDetail(
            product_composition="00",
            product_form="BB",
            measures=[m1, m2],
        )
        assert len(dd.measures) == 2

    # Comprehensive valid instance
    def test_valid_comprehensive_descriptive_detail(self):
        """Valid DescriptiveDetail with many fields populated."""
        dd = p3.DescriptiveDetail(
            product_composition="00",  # Single-item product
            product_form="BB",  # Hardback
            product_form_details=["B206"],  # Pop-up book
            product_packaging="05",  # Jewel case
            trade_category="03",  # Sonderausgabe
            primary_content_type="10",  # Eye-readable text
            product_content_types=["11"],  # Musical notation
            country_of_manufacture="US",
            epub_technical_protections=["03"],  # Has digital watermarking
            map_scales=["50000"],  # 1:50,000
        )
        assert dd.product_composition == "00"
        assert dd.product_form == "BB"
        assert dd.product_form_details == ["B206"]
        assert dd.country_of_manufacture == "US"
        assert dd.map_scales == ["50000"]
