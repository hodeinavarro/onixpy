"""ONIX tag name resolver.

Maps between reference tag names and short tag names.
Reference names are used by default; short names require explicit opt-in.

Minimal mapping for core message elements. Full mapping will be loaded
from the ONIX specification later.
"""

from __future__ import annotations

# Reference name -> Short tag mapping (minimal set for core message structure)
_REFERENCE_TO_SHORT: dict[str, str] = {
    "ONIXMessage": "ONIXmessage",
    "Header": "header",
    "Product": "product",
    "NoProduct": "x507",
}

# Reverse mapping: Short tag -> Reference name
_SHORT_TO_REFERENCE: dict[str, str] = {v: k for k, v in _REFERENCE_TO_SHORT.items()}


def to_short_tag(reference_name: str) -> str:
    """Convert a reference tag name to its short tag equivalent.

    Args:
        reference_name: The reference tag name (e.g., "ONIXMessage")

    Returns:
        The short tag name (e.g., "ONIXmessage"), or the original name
        if no mapping exists.

    Example:
        >>> to_short_tag("ONIXMessage")
        'ONIXmessage'
        >>> to_short_tag("Header")
        'header'
        >>> to_short_tag("UnknownTag")
        'UnknownTag'
    """
    return _REFERENCE_TO_SHORT.get(reference_name, reference_name)


def to_reference_tag(short_tag: str) -> str:
    """Convert a short tag name to its reference tag equivalent.

    Args:
        short_tag: The short tag name (e.g., "ONIXmessage")

    Returns:
        The reference tag name (e.g., "ONIXMessage"), or the original name
        if no mapping exists.

    Example:
        >>> to_reference_tag("ONIXmessage")
        'ONIXMessage'
        >>> to_reference_tag("x507")
        'NoProduct'
        >>> to_reference_tag("UnknownTag")
        'UnknownTag'
    """
    return _SHORT_TO_REFERENCE.get(short_tag, short_tag)


def is_short_tag(tag_name: str) -> bool:
    """Check if a tag name is a known short tag.

    Args:
        tag_name: The tag name to check

    Returns:
        True if the tag is a known short tag, False otherwise.
    """
    return tag_name in _SHORT_TO_REFERENCE


def is_reference_tag(tag_name: str) -> bool:
    """Check if a tag name is a known reference tag.

    Args:
        tag_name: The tag name to check

    Returns:
        True if the tag is a known reference tag, False otherwise.
    """
    return tag_name in _REFERENCE_TO_SHORT
