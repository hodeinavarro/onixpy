"""ONIX Code List 141: Barcode indicator."""

from onix.lists.models import CodeList, CodeListEntry

_ENTRIES = {
    "00": CodeListEntry(
        list_number=141,
        code="00",
        heading="Not barcoded",
        added_version=9,
    ),
    "01": CodeListEntry(
        list_number=141,
        code="01",
        heading="Barcoded, scheme unspecified",
        added_version=9,
    ),
    "02": CodeListEntry(
        list_number=141,
        code="02",
        heading="GTIN-13",
        notes="Barcode uses 13-digit EAN symbology (version NR without 5-digit extension). See (eg) https://bic.org.uk/wp-content/uploads/2022/11/2019.05.31-Bar-Coding-for-Books-rev-09.pdf or https://www.bisg.org/barcoding-guidelines-for-the-us-book-industry",
        added_version=9,
    ),
    "03": CodeListEntry(
        list_number=141,
        code="03",
        heading="GTIN-13+5 (US dollar price encoded)",
        notes="EAN symbology (version NK, first digit of 5-digit extension is 1-5)",
        added_version=9,
    ),
    "04": CodeListEntry(
        list_number=141,
        code="04",
        heading="GTIN-13+5 (CAN dollar price encoded)",
        notes="EAN symbology (version NK, first digit of 5-digit extension is 6)",
        added_version=9,
    ),
    "05": CodeListEntry(
        list_number=141,
        code="05",
        heading="GTIN-13+5 (no price encoded)",
        notes="EAN symbology (version NF, 5-digit extension is 90000-98999 for proprietary use - extension does not indicate a price)",
        added_version=9,
    ),
    "06": CodeListEntry(
        list_number=141,
        code="06",
        heading="UPC-12 (item-specific)",
        notes="AKA item/price",
        added_version=9,
    ),
    "07": CodeListEntry(
        list_number=141,
        code="07",
        heading="UPC-12+5 (item-specific)",
        notes="AKA item/price",
        added_version=9,
    ),
    "08": CodeListEntry(
        list_number=141,
        code="08",
        heading="UPC-12 (price-point)",
        notes="AKA price/item",
        added_version=9,
    ),
    "09": CodeListEntry(
        list_number=141,
        code="09",
        heading="UPC-12+5 (price-point)",
        notes="AKA price/item",
        added_version=9,
    ),
    "10": CodeListEntry(
        list_number=141,
        code="10",
        heading="GTIN-13+5 (UK Pound Sterling price encoded)",
        notes="EAN symbology (version NK, first digit of 5-digit extension is 0)",
        added_version=57,
    ),
    "11": CodeListEntry(
        list_number=141,
        code="11",
        heading="GTIN-13+5 (other price encoded)",
        notes="EAN symbology (version NK, price currency by local agreement)",
        added_version=62,
    ),
    "12": CodeListEntry(
        list_number=141,
        code="12",
        heading="GTIN-13+2",
        notes="EAN symbology (two-digit extension, normally indicating periodical issue number)",
        added_version=62,
    ),
    "13": CodeListEntry(
        list_number=141,
        code="13",
        heading="GTIN-13+5",
        notes="EAN symbology (five-digit extension, normally indicating periodical issue number)",
        added_version=67,
    ),
}

List141 = CodeList(
    number=141,
    heading="Barcode indicator",
    scope_note="",
    entries=_ENTRIES,
)

# Alias by name
BarcodeIndicator = List141
