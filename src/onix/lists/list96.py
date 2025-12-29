"""ONIX Code List 96: Currency code – ISO 4217.

Based on ISO 4217 three-letter currency codes.
"""

from onix.lists.models import CodeList, CodeListEntry

_ENTRIES = {
    "USD": CodeListEntry(
        list_number=96,
        code="USD",
        heading="US Dollar",
        added_version=1,
    ),
    "EUR": CodeListEntry(
        list_number=96,
        code="EUR",
        heading="Euro",
        added_version=1,
    ),
    "GBP": CodeListEntry(
        list_number=96,
        code="GBP",
        heading="Pound Sterling",
        added_version=1,
    ),
    "JPY": CodeListEntry(
        list_number=96,
        code="JPY",
        heading="Yen",
        added_version=1,
    ),
    "CHF": CodeListEntry(
        list_number=96,
        code="CHF",
        heading="Swiss Franc",
        added_version=1,
    ),
    "CAD": CodeListEntry(
        list_number=96,
        code="CAD",
        heading="Canadian Dollar",
        added_version=1,
    ),
    "AUD": CodeListEntry(
        list_number=96,
        code="AUD",
        heading="Australian Dollar",
        added_version=1,
    ),
    "CNY": CodeListEntry(
        list_number=96,
        code="CNY",
        heading="Yuan Renminbi",
        added_version=1,
    ),
    "MXN": CodeListEntry(
        list_number=96,
        code="MXN",
        heading="Mexican Peso",
        added_version=1,
    ),
    "BRL": CodeListEntry(
        list_number=96,
        code="BRL",
        heading="Brazilian Real",
        added_version=1,
    ),
}

List96 = CodeList(
    number=96,
    heading="Currency code – ISO 4217",
    scope_note="Used with <CurrencyCode>, <DefaultCurrencyCode>.",
    entries=_ENTRIES,
)

# Alias by name
CurrencyCode = List96
