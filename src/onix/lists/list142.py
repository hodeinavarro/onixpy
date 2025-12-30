"""ONIX Code List 142: Position on product."""

from onix.lists.models import CodeList, CodeListEntry

_ENTRIES = {
    "00": CodeListEntry(
        list_number=142,
        code="00",
        heading="Unknown / unspecified",
        notes="Position unknown or unspecified",
        added_version=9,
    ),
    "01": CodeListEntry(
        list_number=142,
        code="01",
        heading="Cover 4",
        notes="The back cover of a book (or book jacket) - the recommended position",
        added_version=9,
    ),
    "02": CodeListEntry(
        list_number=142,
        code="02",
        heading="Cover 3",
        notes="The inside back cover of a book",
        added_version=9,
    ),
    "03": CodeListEntry(
        list_number=142,
        code="03",
        heading="Cover 2",
        notes="The inside front cover of a book",
        added_version=9,
    ),
    "04": CodeListEntry(
        list_number=142,
        code="04",
        heading="Cover 1",
        notes="The front cover of a book",
        added_version=9,
    ),
    "05": CodeListEntry(
        list_number=142,
        code="05",
        heading="On spine",
        notes="The spine of a book",
        added_version=9,
    ),
    "06": CodeListEntry(
        list_number=142,
        code="06",
        heading="On box",
        notes="Used only for boxed products",
        added_version=9,
    ),
    "07": CodeListEntry(
        list_number=142,
        code="07",
        heading="On tag",
        notes="Used only for products fitted with hanging tags",
        added_version=9,
    ),
    "08": CodeListEntry(
        list_number=142,
        code="08",
        heading="On bottom",
        notes="Not be used for books unless they are contained within outer packaging",
        added_version=9,
    ),
    "09": CodeListEntry(
        list_number=142,
        code="09",
        heading="On back",
        notes="Not be used for books unless they are contained within outer packaging",
        added_version=9,
    ),
    "10": CodeListEntry(
        list_number=142,
        code="10",
        heading="On outer sleeve / back",
        notes="Used only for products packaged in outer sleeves",
        added_version=9,
    ),
    "11": CodeListEntry(
        list_number=142,
        code="11",
        heading="On removable wrapping",
        notes="Used only for products packaged in shrink-wrap or other removable wrapping",
        added_version=9,
    ),
}

List142 = CodeList(
    number=142,
    heading="Position on product",
    scope_note="",
    entries=_ENTRIES,
)

# Alias by name
PositionOnProduct = List142
