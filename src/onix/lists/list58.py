"""ONIX Code List 58: Price type.

Indicates the type of price, e.g. RRP, wholesale, etc.
"""

from onix.lists.models import CodeList, CodeListEntry

_ENTRIES = {
    "01": CodeListEntry(
        list_number=58,
        code="01",
        heading="RRP excluding tax",
        notes="Recommended Retail Price, excluding any sales tax or VAT.",
        added_version=1,
    ),
    "02": CodeListEntry(
        list_number=58,
        code="02",
        heading="RRP including tax",
        notes="Recommended Retail Price, including sales tax or VAT if applicable.",
        added_version=1,
    ),
    "03": CodeListEntry(
        list_number=58,
        code="03",
        heading="Fixed retail price excluding tax",
        notes="Fixed Retail Price, excluding any sales tax or VAT.",
        added_version=1,
    ),
    "04": CodeListEntry(
        list_number=58,
        code="04",
        heading="Fixed retail price including tax",
        notes="Fixed Retail Price, including sales tax or VAT if applicable.",
        added_version=1,
    ),
    "05": CodeListEntry(
        list_number=58,
        code="05",
        heading="Supplier's net price excluding tax",
        notes="Unit price charged to reseller, excluding any sales tax or VAT.",
        added_version=1,
    ),
    "06": CodeListEntry(
        list_number=58,
        code="06",
        heading="Supplier's net price including tax",
        notes="Unit price charged to reseller, including sales tax or VAT.",
        added_version=1,
    ),
    "41": CodeListEntry(
        list_number=58,
        code="41",
        heading="Publishers retail price excluding tax",
        notes="Publisher's suggested retail price excluding tax.",
        added_version=21,
    ),
    "42": CodeListEntry(
        list_number=58,
        code="42",
        heading="Publishers retail price including tax",
        notes="Publisher's suggested retail price including tax.",
        added_version=21,
    ),
}

List58 = CodeList(
    number=58,
    heading="Price type",
    scope_note="Used with <PriceType>, <DefaultPriceType>.",
    entries=_ENTRIES,
)

# Alias by name
PriceType = List58
