"""Descriptive detail composite (P.3).

The descriptive detail block covers data Groups P.3 to P.13, all of which are
essentially part of the factual description of the form and content of a product.
The block as a whole is non-repeating. It is mandatory in any <Product> record
unless the <NotificationType> in Group P.1 indicates that the record is an update
notice which carries only those blocks in which changes have occurred.
"""

from __future__ import annotations

from pydantic import Field, field_validator

from onix._base import ONIXModel
from onix.lists import get_code
from onix.product.b1.p3.EpubLicense import EpubLicense
from onix.product.b1.p3.EpubUsageConstraint import EpubUsageConstraint
from onix.product.b1.p3.ProductClassification import ProductClassification
from onix.product.b1.p3.ProductFormFeature import ProductFormFeature
from onix.product.b1.p11 import Measure


class DescriptiveDetail(ONIXModel):
    """Descriptive detail composite.

    Required fields (P.3 Product form):
    - product_composition: Code from List 2 (single/multiple items)
    - product_form: Code from List 150 (primary form)

    Optional fields (P.3 Product form):
    - product_form_details: List of codes from List 175 (added detail)
    - product_form_features: List of ProductFormFeature composites
    - product_packaging: Code from List 80 (packaging type)
    - product_form_descriptions: List of text descriptions (with language)
    - trade_category: Code from List 12 (trade category)
    - primary_content_type: Code from List 81 (primary content type)
    - product_content_types: List of codes from List 81 (other content types)
    - measures: List of Measure composites (dimensions, weight, etc)
    - country_of_manufacture: Code from List 91 (ISO 3166-1 country code)
    - epub_technical_protections: List of codes from List 144 (DRM types)
    - epub_usage_constraints: List of EpubUsageConstraint composites
    - epub_licenses: List of EpubLicense composites
    - map_scales: List of map scale values
    - product_classifications: List of ProductClassification composites

    Example:
        >>> DescriptiveDetail(
        ...     product_composition="00",  # Single-item product
        ...     product_form="BB",  # Hardback book
        ...     product_form_details=["B206"],  # Pop-up book
        ...     measures=[
        ...         Measure(measure_type="01", measurement="8.25", measure_unit_code="in"),
        ...     ],
        ... )
    """

    # P.3.1 Product composition (mandatory)
    product_composition: str = Field(
        alias="ProductComposition",
        json_schema_extra={"short_tag": "x314"},
    )
    # P.3.2 Product form code (mandatory)
    product_form: str = Field(
        alias="ProductForm",
        json_schema_extra={"short_tag": "b012"},
    )
    # P.3.3 Product form detail (optional, repeatable)
    product_form_details: list[str] = Field(
        default_factory=list,
        alias="ProductFormDetail",
        json_schema_extra={"short_tag": "b333"},
    )
    # P.3.4-P.3.6 Product form feature composite (optional, repeatable)
    product_form_features: list[ProductFormFeature] = Field(
        default_factory=list,
        alias="ProductFormFeature",
        json_schema_extra={"short_tag": "productformfeature"},
    )
    # P.3.7 Product packaging type code (optional)
    product_packaging: str | None = Field(
        default=None,
        alias="ProductPackaging",
        json_schema_extra={"short_tag": "b225"},
    )
    # P.3.8 Product form description (optional, repeatable)
    product_form_descriptions: list[str] = Field(
        default_factory=list,
        alias="ProductFormDescription",
        json_schema_extra={"short_tag": "b014"},
    )
    # P.3.9 Trade category code (optional)
    trade_category: str | None = Field(
        default=None,
        alias="TradeCategory",
        json_schema_extra={"short_tag": "b384"},
    )
    # P.3.10 Primary content type code (optional)
    primary_content_type: str | None = Field(
        default=None,
        alias="PrimaryContentType",
        json_schema_extra={"short_tag": "x416"},
    )
    # P.3.11 Product content type code (optional, repeatable)
    product_content_types: list[str] = Field(
        default_factory=list,
        alias="ProductContentType",
        json_schema_extra={"short_tag": "b385"},
    )
    # P.3.12-P.3.14 Measure composite (optional, repeatable)
    measures: list[Measure] = Field(
        default_factory=list,
        alias="Measure",
        json_schema_extra={"short_tag": "measure"},
    )
    # P.3.15 Country of manufacture (optional)
    country_of_manufacture: str | None = Field(
        default=None,
        alias="CountryOfManufacture",
        json_schema_extra={"short_tag": "x316"},
    )
    # P.3.16 Digital product technical protection (optional, repeatable)
    epub_technical_protections: list[str] = Field(
        default_factory=list,
        alias="EpubTechnicalProtection",
        json_schema_extra={"short_tag": "x317"},
    )
    # P.3.17-P.3.20 Usage constraint composite (optional, repeatable)
    epub_usage_constraints: list[EpubUsageConstraint] = Field(
        default_factory=list,
        alias="EpubUsageConstraint",
        json_schema_extra={"short_tag": "epubusageconstraint"},
    )
    # P.3.20a-P.3.20f Digital product license composite (optional, repeatable)
    epub_licenses: list[EpubLicense] = Field(
        default_factory=list,
        alias="EpubLicense",
        json_schema_extra={"short_tag": "epublicense"},
    )
    # P.3.21 Map scale (optional, repeatable)
    map_scales: list[str] = Field(
        default_factory=list,
        alias="MapScale",
        json_schema_extra={"short_tag": "b063"},
    )
    # P.3.22-P.3.24 Product classification composite (optional, repeatable)
    product_classifications: list[ProductClassification] = Field(
        default_factory=list,
        alias="ProductClassification",
        json_schema_extra={"short_tag": "productclassification"},
    )

    @field_validator("product_composition")
    @classmethod
    def _validate_product_composition(cls, v: str) -> str:
        """Validate product_composition: fixed length, two digits, List 2."""
        if not v.isdigit() or len(v) != 2:
            raise ValueError(
                f"Invalid product_composition '{v}' - must be exactly 2 digits"
            )
        if get_code(2, v) is None:
            raise ValueError(f"Invalid product_composition '{v}' - must be from List 2")
        return v

    @field_validator("product_form")
    @classmethod
    def _validate_product_form(cls, v: str) -> str:
        """Validate product_form: fixed length, two letters or digits 00, List 150."""
        if len(v) != 2:
            raise ValueError(
                f"Invalid product_form '{v}' - must be exactly 2 characters"
            )
        if v != "00" and not (v.isalpha() and v.isupper()):
            raise ValueError(
                f"Invalid product_form '{v}' - must be two uppercase letters or '00'"
            )
        if get_code(150, v) is None:
            raise ValueError(f"Invalid product_form '{v}' - must be from List 150")
        return v

    @field_validator("product_form_details")
    @classmethod
    def _validate_product_form_details(cls, v: list[str]) -> list[str]:
        """Validate product_form_details: fixed length, one letter + three digits, List 175."""
        for code in v:
            if len(code) != 4 or not (code[0].isalpha() and code[1:].isdigit()):
                raise ValueError(
                    f"Invalid product_form_detail '{code}' - must be one letter followed by three digits"
                )
            if get_code(175, code) is None:
                raise ValueError(
                    f"Invalid product_form_detail '{code}' - must be from List 175"
                )
        return v

    @field_validator("product_form_descriptions")
    @classmethod
    def _validate_product_form_descriptions(cls, v: list[str]) -> list[str]:
        """Validate product_form_descriptions: max 200 characters each."""
        for desc in v:
            if len(desc) > 200:
                raise ValueError(
                    f"product_form_description exceeds maximum length of 200 characters (got {len(desc)})"
                )
        return v

    @field_validator("product_packaging")
    @classmethod
    def _validate_product_packaging(cls, v: str | None) -> str | None:
        """Validate product_packaging: fixed length, two digits, List 80."""
        if v is not None:
            if not v.isdigit() or len(v) != 2:
                raise ValueError(
                    f"Invalid product_packaging '{v}' - must be exactly 2 digits"
                )
            if get_code(80, v) is None:
                raise ValueError(
                    f"Invalid product_packaging '{v}' - must be from List 80"
                )
        return v

    @field_validator("trade_category")
    @classmethod
    def _validate_trade_category(cls, v: str | None) -> str | None:
        """Validate trade_category: fixed length, two digits, List 12."""
        if v is not None:
            if not v.isdigit() or len(v) != 2:
                raise ValueError(
                    f"Invalid trade_category '{v}' - must be exactly 2 digits"
                )
            if get_code(12, v) is None:
                raise ValueError(f"Invalid trade_category '{v}' - must be from List 12")
        return v

    @field_validator("primary_content_type")
    @classmethod
    def _validate_primary_content_type(cls, v: str | None) -> str | None:
        """Validate primary_content_type: fixed length, two digits, List 81."""
        if v is not None:
            if not v.isdigit() or len(v) != 2:
                raise ValueError(
                    f"Invalid primary_content_type '{v}' - must be exactly 2 digits"
                )
            if get_code(81, v) is None:
                raise ValueError(
                    f"Invalid primary_content_type '{v}' - must be from List 81"
                )
        return v

    @field_validator("product_content_types")
    @classmethod
    def _validate_product_content_types(cls, v: list[str]) -> list[str]:
        """Validate product_content_types: fixed length, two digits each, List 81."""
        for code in v:
            if not code.isdigit() or len(code) != 2:
                raise ValueError(
                    f"Invalid product_content_type '{code}' - must be exactly 2 digits"
                )
            if get_code(81, code) is None:
                raise ValueError(
                    f"Invalid product_content_type '{code}' - must be from List 81"
                )
        return v

    @field_validator("country_of_manufacture")
    @classmethod
    def _validate_country_of_manufacture(cls, v: str | None) -> str | None:
        """Validate country_of_manufacture: fixed length, two uppercase letters, List 91."""
        if v is not None:
            if len(v) != 2 or not (v.isalpha() and v.isupper()):
                raise ValueError(
                    f"Invalid country_of_manufacture '{v}' - must be exactly 2 uppercase letters"
                )
            if get_code(91, v) is None:
                raise ValueError(
                    f"Invalid country_of_manufacture '{v}' - must be from List 91"
                )
        return v

    @field_validator("epub_technical_protections")
    @classmethod
    def _validate_epub_technical_protections(cls, v: list[str]) -> list[str]:
        """Validate epub_technical_protections: fixed length, two digits each, List 144."""
        for code in v:
            if not code.isdigit() or len(code) != 2:
                raise ValueError(
                    f"Invalid epub_technical_protection '{code}' - must be exactly 2 digits"
                )
            if get_code(144, code) is None:
                raise ValueError(
                    f"Invalid epub_technical_protection '{code}' - must be from List 144"
                )
        return v

    @field_validator("map_scales")
    @classmethod
    def _validate_map_scales(cls, v: list[str]) -> list[str]:
        """Validate map_scales: positive integer, max 8 digits each."""
        for scale in v:
            if not scale.isdigit():
                raise ValueError(
                    f"Invalid map_scale '{scale}' - must be a positive integer"
                )
            if len(scale) > 8:
                raise ValueError(
                    f"map_scale exceeds maximum length of 8 digits (got {len(scale)})"
                )
        return v
