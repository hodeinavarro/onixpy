"""ONIX code lists.

Provides access to ONIX code lists used throughout the specification.
Code lists define allowed values for various fields (e.g., List 44 for
Name Identifier Type).

Import lists by number or name:
    >>> from onix.lists import List44
    >>> from onix.lists import NameIdentifierType  # Alias for List44

Access list data:
    >>> from onix.lists import get_list, get_code
    >>> list_44 = get_list(44)
    >>> code = get_code(44, "16")
    >>> code.heading
    'ISNI'

This is a placeholder implementation with minimal data. The full code lists
will be imported from the ONIX specification later.
"""

from __future__ import annotations

from onix.lists.list1 import List1, NotificationOrUpdateType
from onix.lists.list5 import List5, ProductIdentifierType
from onix.lists.list17 import ContributorRole, List17
from onix.lists.list18 import List18, NameType
from onix.lists.list19 import List19, UnnamedPersons
from onix.lists.list44 import List44, NameIdentifierType
from onix.lists.list45 import List45, PublishingRole
from onix.lists.list48 import List48, MeasureType
from onix.lists.list49 import List49, RegionCode
from onix.lists.list50 import List50, MeasureUnit
from onix.lists.list58 import List58, PriceType
from onix.lists.list73 import List73, WebsiteRole
from onix.lists.list74 import LanguageCode, List74
from onix.lists.list75 import ContributorDateRole, List75
from onix.lists.list96 import CurrencyCode, List96
from onix.lists.list148 import CollectionType, List148
from onix.lists.list151 import ContributorPlaceRelator, List151
from onix.lists.models import CodeList, CodeListEntry

# Registry of all code lists (by number)
_CODE_LISTS: dict[int, CodeList] = {
    1: List1,
    5: List5,
    17: List17,
    18: List18,
    19: List19,
    44: List44,
    45: List45,
    48: List48,
    49: List49,
    50: List50,
    58: List58,
    73: List73,
    74: List74,
    75: List75,
    96: List96,
    148: List148,
    151: List151,
}


def get_list(list_number: int) -> CodeList | None:
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


def get_code(list_number: int, code: str) -> CodeListEntry | None:
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


__all__ = [
    # Models
    "CodeList",
    "CodeListEntry",
    # Lists by number
    "List1",
    "List5",
    "List17",
    "List18",
    "List19",
    "List44",
    "List45",
    "List48",
    "List49",
    "List50",
    "List58",
    "List73",
    "List74",
    "List75",
    "List96",
    "List148",
    "List151",
    # Lists by name
    "NotificationOrUpdateType",
    "ProductIdentifierType",
    "ContributorRole",
    "NameType",
    "UnnamedPersons",
    "NameIdentifierType",
    "PublishingRole",
    "MeasureType",
    "RegionCode",
    "MeasureUnit",
    "PriceType",
    "WebsiteRole",
    "LanguageCode",
    "ContributorDateRole",
    "CurrencyCode",
    "CollectionType",
    "ContributorPlaceRelator",
    # Functions
    "get_list",
    "get_code",
    "list_available",
]
