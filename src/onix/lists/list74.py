"""ONIX Code List 74: Language code – ISO 639-2/B.

Based on ISO 639-2/B three-letter language codes.
"""

from onix.lists.models import CodeList, CodeListEntry

# Placeholder entries - will be expanded from ONIX spec
_ENTRIES = {
    "eng": CodeListEntry(
        list_number=74,
        code="eng",
        heading="English",
        added_version=1,
    ),
    "spa": CodeListEntry(
        list_number=74,
        code="spa",
        heading="Spanish",
        added_version=1,
    ),
    "fra": CodeListEntry(
        list_number=74,
        code="fra",
        heading="French",
        added_version=1,
    ),
    "deu": CodeListEntry(
        list_number=74,
        code="deu",
        heading="German",
        added_version=1,
    ),
    "ita": CodeListEntry(
        list_number=74,
        code="ita",
        heading="Italian",
        added_version=1,
    ),
    "por": CodeListEntry(
        list_number=74,
        code="por",
        heading="Portuguese",
        added_version=1,
    ),
    "jpn": CodeListEntry(
        list_number=74,
        code="jpn",
        heading="Japanese",
        added_version=1,
    ),
    "zho": CodeListEntry(
        list_number=74,
        code="zho",
        heading="Chinese",
        added_version=1,
    ),
    "ara": CodeListEntry(
        list_number=74,
        code="ara",
        heading="Arabic",
        added_version=1,
    ),
    "rus": CodeListEntry(
        list_number=74,
        code="rus",
        heading="Russian",
        added_version=1,
    ),
}

List74 = CodeList(
    number=74,
    heading="Language code – ISO 639-2/B",
    scope_note="Used with <DefaultLanguageOfText>, <Language>, <LanguageOfText>, etc.",
    entries=_ENTRIES,
)

# Alias by name
LanguageCode = List74
