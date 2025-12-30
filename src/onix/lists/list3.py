"""ONIX Code List 3: Record source type."""

from onix.lists.models import CodeList, CodeListEntry

_ENTRIES = {
    "00": CodeListEntry(
        list_number=3,
        code="00",
        heading="Unspecified",
    ),
    "01": CodeListEntry(
        list_number=3,
        code="01",
        heading="Publisher",
    ),
    "02": CodeListEntry(
        list_number=3,
        code="02",
        heading="Publisher’s distributor",
        notes="Use to designate a distributor providing primary warehousing and fulfillment for a publisher or for a publisher’s sales agent, as distinct from a wholesaler",
    ),
    "03": CodeListEntry(
        list_number=3,
        code="03",
        heading="Wholesaler",
    ),
    "04": CodeListEntry(
        list_number=3,
        code="04",
        heading="Bibliographic agency",
        notes="Bibliographic data aggregator",
    ),
    "05": CodeListEntry(
        list_number=3,
        code="05",
        heading="Library bookseller",
        notes="Library supplier. Bookseller selling to libraries (including academic libraries)",
    ),
    "06": CodeListEntry(
        list_number=3,
        code="06",
        heading="Publisher’s sales agent",
        notes="Use for a publisher’s sales agent responsible for marketing the publisher’s products within a territory, as opposed to a publisher’s distributor who fulfills orders but does not market",
        added_version=4,
    ),
    "07": CodeListEntry(
        list_number=3,
        code="07",
        heading="Publisher’s conversion service provider",
        notes="Downstream provider of e-publication format conversion services (who might also be a distributor or retailer of the converted e-publication), supplying metadata on behalf of the publisher. The assigned ISBN is taken from the publisher’s ISBN prefix",
        added_version=15,
    ),
    "08": CodeListEntry(
        list_number=3,
        code="08",
        heading="Conversion service provider",
        notes="Downstream provider of e-publication format conversion services (who might also be a distributor or retailer of the converted e-publication), supplying metadata on behalf of the publisher. The assigned ISBN is taken from the service provider’s prefix (whether or not the service provider dedicates that prefix to a particular publisher)",
        added_version=15,
    ),
    "09": CodeListEntry(
        list_number=3,
        code="09",
        heading="ISBN Registration Agency",
        added_version=18,
    ),
    "10": CodeListEntry(
        list_number=3,
        code="10",
        heading="ISTC Registration Agency",
        notes="Deprecated: the ISTC was withdrawn as a standard in 2021",
        added_version=18,
        deprecated_version=71,
    ),
    "11": CodeListEntry(
        list_number=3,
        code="11",
        heading="Retail bookseller",
        notes="Bookseller selling primarily to consumers",
        added_version=28,
    ),
    "12": CodeListEntry(
        list_number=3,
        code="12",
        heading="Education bookseller",
        notes="Bookseller selling primarily to educational institutions",
        added_version=28,
    ),
    "13": CodeListEntry(
        list_number=3,
        code="13",
        heading="Library",
        notes="Library service providing enhanced metadata to publishers or other parties",
        added_version=36,
    ),
}

List3 = CodeList(
    number=3,
    heading="Record source type",
    scope_note="",
    entries=_ENTRIES,
)

# Alias by name
RecordSourceType = List3
