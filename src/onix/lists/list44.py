"""ONIX Code List 44: Name identifier type."""

from onix.lists.models import CodeList, CodeListEntry

_ENTRIES = {
    "01": CodeListEntry(
        list_number=44,
        code="01",
        heading="Proprietary name ID scheme",
        notes="For example, a publisher's own name, contributor or imprint ID scheme.",
        added_version=10,
        modified_version=70,
    ),
    "06": CodeListEntry(
        list_number=44,
        code="06",
        heading="GLN",
        notes="GS1 global location number (formerly EAN location number)",
        added_version=1,
        modified_version=9,
    ),
    "07": CodeListEntry(
        list_number=44,
        code="07",
        heading="SAN",
        notes="Book trade Standard Address Number – US, UK etc",
        added_version=1,
        modified_version=6,
    ),
    "16": CodeListEntry(
        list_number=44,
        code="16",
        heading="ISNI",
        notes="International Standard Name Identifier. A sixteen digit number.",
        added_version=10,
    ),
    "21": CodeListEntry(
        list_number=44,
        code="21",
        heading="ORCID",
        notes="Open Researcher and Contributor ID. A sixteen digit number.",
        added_version=13,
    ),
}

List44 = CodeList(
    number=44,
    heading="Name identifier type",
    scope_note=(
        "Used with <NameIDType>, <SenderIDType>, <AddresseeIDType>, "
        "<ImprintIDType>, <PublisherIDType>, and others."
    ),
    entries=_ENTRIES,
)

# Alias for import by name
NameIdentifierType = List44
