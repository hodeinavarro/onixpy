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

from typing import Optional

from onix.lists.list44 import List44, NameIdentifierType
from onix.lists.models import CodeList, CodeListEntry

# Registry of all code lists (by number)
_CODE_LISTS: dict[int, CodeList] = {
    44: List44,
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


__all__ = [
    # Models
    "CodeList",
    "CodeListEntry",
    # Lists by number
    "List44",
    # Lists by name
    "NameIdentifierType",
    # Functions
    "get_list",
    "get_code",
    "list_available",
]
