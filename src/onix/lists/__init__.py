"""ONIX code lists.

Provides access to ONIX code lists used throughout the specification.
Code lists define allowed values for various fields (e.g., List 44 for
Name Identifier Type).

This is a placeholder implementation with minimal data. The full code lists
will be imported from the ONIX specification later.

Example usage:
    >>> from onix.lists import get_list, get_code
    >>> list_44 = get_list(44)
    >>> code = get_code(44, "16")
    >>> code.heading
    'ISNI'
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class CodeListEntry:
    """A single entry in an ONIX code list.

    Attributes:
        list_number: The code list number (e.g., 44)
        code: The code value (e.g., "16")
        heading: Human-readable description (e.g., "ISNI")
        notes: Additional usage notes (optional)
        added_version: ONIX version when code was added (optional)
        modified_version: ONIX version when code was modified (optional)
        deprecated_version: ONIX version when code was deprecated (optional)
    """

    list_number: int
    code: str
    heading: str
    notes: Optional[str] = None
    added_version: Optional[int] = None
    modified_version: Optional[int] = None
    deprecated_version: Optional[int] = None

    @property
    def is_deprecated(self) -> bool:
        """Check if this code is deprecated."""
        return self.deprecated_version is not None


@dataclass
class CodeList:
    """An ONIX code list.

    Attributes:
        number: The list number (e.g., 44)
        heading: Human-readable name (e.g., "Name identifier type")
        scope_note: Usage information about which elements use this list
        entries: Dict mapping code values to CodeListEntry objects
    """

    number: int
    heading: str
    scope_note: str
    entries: dict[str, CodeListEntry]

    def get(self, code: str) -> Optional[CodeListEntry]:
        """Get an entry by code value."""
        return self.entries.get(code)

    def __iter__(self):
        """Iterate over entries."""
        return iter(self.entries.values())

    def __len__(self) -> int:
        """Number of entries in the list."""
        return len(self.entries)


# Placeholder data: List 44 (Name identifier type) - minimal subset for testing
_LIST_44_ENTRIES = {
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

_LIST_44 = CodeList(
    number=44,
    heading="Name identifier type",
    scope_note=(
        "Used with <NameIDType>, <SenderIDType>, <AddresseeIDType>, "
        "<ImprintIDType>, <PublisherIDType>, and others."
    ),
    entries=_LIST_44_ENTRIES,
)

# Registry of all code lists
_CODE_LISTS: dict[int, CodeList] = {
    44: _LIST_44,
}


def get_list(list_number: int) -> Optional[CodeList]:
    """Get a code list by number.

    Args:
        list_number: The ONIX code list number (e.g., 44)

    Returns:
        The CodeList if found, None otherwise.

    Example:
        >>> list_44 = get_list(44)
        >>> list_44.heading
        'Name identifier type'
    """
    return _CODE_LISTS.get(list_number)


def get_code(list_number: int, code: str) -> Optional[CodeListEntry]:
    """Get a specific code entry from a list.

    Args:
        list_number: The ONIX code list number (e.g., 44)
        code: The code value (e.g., "16")

    Returns:
        The CodeListEntry if found, None otherwise.

    Example:
        >>> entry = get_code(44, "16")
        >>> entry.heading
        'ISNI'
    """
    code_list = get_list(list_number)
    if code_list is None:
        return None
    return code_list.get(code)


def list_available() -> list[int]:
    """Get list of available code list numbers.

    Returns:
        Sorted list of available code list numbers.
    """
    return sorted(_CODE_LISTS.keys())
