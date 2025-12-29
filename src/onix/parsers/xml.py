"""XML parsing and serialization for ONIX messages.

Supports loading ONIXMessage from:
- Path-like string (file path)
- XML string
- ElementTree Element (stdlib xml.etree or lxml)
- Iterable of Element objects (combined into single message)

Supports dumping ONIXMessage to:
- ElementTree Element
- XML string
- File path

Prefers lxml if available for better performance and features;
falls back to stdlib xml.etree.ElementTree.
"""

from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable
from xml.etree import ElementTree as ET

from onix.header import (
    Addressee,
    AddresseeIdentifier,
    Header,
    Sender,
    SenderIdentifier,
)
from onix.message import ONIXMessage
from onix.parsers.fields import (
    field_name_to_tag,
    register_model,
    register_plural_mapping,
    tag_to_field_name,
)
from onix.parsers.tags import to_reference_tag, to_short_tag
from onix.product import Product

# Try to import lxml for better XML handling
try:
    from lxml import etree as lxml_etree

    HAS_LXML = True
except ImportError:
    lxml_etree = None  # type: ignore[assignment]
    HAS_LXML = False

if TYPE_CHECKING:
    from xml.etree.ElementTree import Element

    if HAS_LXML:
        from lxml.etree import _Element as LxmlElement

        ElementType = Element | LxmlElement
    else:
        ElementType = Element


# Register all models with the fields module for tag/field mapping
# This extracts aliases from model definitions
def _register_models() -> None:
    """Register all ONIX models with the field mapping module."""
    register_model(ONIXMessage)
    register_model(Header)
    register_model(Sender)
    register_model(SenderIdentifier)
    register_model(Addressee)
    register_model(AddresseeIdentifier)
    register_model(Product)

    # Register plural mappings for list fields that use singular XML tags
    register_plural_mapping("Product", "products")
    register_plural_mapping("Addressee", "addressees")
    register_plural_mapping("SenderIdentifier", "sender_identifiers")
    register_plural_mapping("AddresseeIdentifier", "addressee_identifiers")


# Register models at module load time
_register_models()


def xml_to_message(
    source: str | PathLike[str] | "ElementType" | Iterable["ElementType"],
    *,
    short_names: bool = False,
) -> ONIXMessage:
    """Parse an ONIX message from XML.

    Args:
        source: One of:
            - Path-like string pointing to an XML file
            - XML string (detected by starting with '<')
            - ElementTree Element (stdlib or lxml)
            - Iterable of Element objects (products combined)
        short_names: If True, expect short tag names in input;
            otherwise expect reference names (default). The parser
            will auto-detect and normalize to reference names.

    Returns:
        Parsed ONIXMessage instance.

    Raises:
        FileNotFoundError: If path doesn't exist
        ET.ParseError: If XML is invalid
        pydantic.ValidationError: If data doesn't match schema

    Example:
        >>> from onix.parsers import xml_to_message
        >>> msg = xml_to_message("/path/to/message.xml")
        >>> msg = xml_to_message("<ONIXMessage>...</ONIXMessage>")
    """
    root = _normalize_input(source)
    data = _element_to_dict(root, normalize_tags=not short_names)
    return ONIXMessage.model_validate(data)


def message_to_xml(
    message: ONIXMessage,
    *,
    short_names: bool = False,
    use_lxml: bool = True,
) -> "ElementType":
    """Convert an ONIX message to an XML Element.

    Args:
        message: The ONIXMessage to convert.
        short_names: If True, use short tag names;
            otherwise use reference names (default).
        use_lxml: If True and lxml is available, return lxml Element;
            otherwise return stdlib Element.

    Returns:
        XML Element representing the message.
    """
    data = message.model_dump(exclude_none=True, exclude_defaults=True)

    root_tag = "ONIXMessage" if not short_names else to_short_tag("ONIXMessage")

    if use_lxml and HAS_LXML:
        root = lxml_etree.Element(root_tag)
    else:
        root = ET.Element(root_tag)

    # Set release attribute
    root.set("release", data.get("release", "3.1"))

    # Add shared attributes if present
    for attr in ("datestamp", "sourcename", "sourcetype"):
        if attr in data:
            root.set(attr, str(data[attr]))

    # Build Header
    header_tag = "Header" if not short_names else to_short_tag("Header")
    header_data = data.get("header", {})
    header_elem = _dict_to_element(
        header_tag, header_data, short_names=short_names, use_lxml=use_lxml
    )
    root.append(header_elem)

    # Build Products or NoProduct
    if data.get("no_product"):
        no_product_tag = "NoProduct" if not short_names else to_short_tag("NoProduct")
        if use_lxml and HAS_LXML:
            root.append(lxml_etree.Element(no_product_tag))
        else:
            root.append(ET.Element(no_product_tag))
    else:
        product_tag = "Product" if not short_names else to_short_tag("Product")
        for product_data in data.get("products", []):
            product_elem = _dict_to_element(
                product_tag, product_data, short_names=short_names, use_lxml=use_lxml
            )
            root.append(product_elem)

    return root


def message_to_xml_string(
    message: ONIXMessage,
    *,
    short_names: bool = False,
    xml_declaration: bool = True,
    encoding: str = "utf-8",
    pretty_print: bool = True,
) -> str:
    """Serialize an ONIX message to an XML string.

    Args:
        message: The ONIXMessage to serialize.
        short_names: If True, use short tag names;
            otherwise use reference names (default).
        xml_declaration: If True, include XML declaration.
        encoding: Character encoding for the declaration.
        pretty_print: If True, format with indentation (lxml only).

    Returns:
        XML string representation of the message.
    """
    root = message_to_xml(message, short_names=short_names, use_lxml=HAS_LXML)

    if HAS_LXML:
        return lxml_etree.tostring(
            root,
            encoding="unicode",
            xml_declaration=xml_declaration,
            pretty_print=pretty_print,
        )
    else:
        # Stdlib doesn't support pretty_print directly
        if pretty_print:
            _indent_element(root)
        xml_str = ET.tostring(root, encoding="unicode")
        if xml_declaration:
            xml_str = f'<?xml version="1.0" encoding="{encoding}"?>\n{xml_str}'
        return xml_str


def save_xml(
    message: ONIXMessage,
    path: str | PathLike[str],
    *,
    short_names: bool = False,
    xml_declaration: bool = True,
    encoding: str = "utf-8",
    pretty_print: bool = True,
) -> None:
    """Save an ONIX message to an XML file.

    Args:
        message: The ONIXMessage to save.
        path: File path to write to.
        short_names: If True, use short tag names;
            otherwise use reference names (default).
        xml_declaration: If True, include XML declaration.
        encoding: Character encoding.
        pretty_print: If True, format with indentation.
    """
    xml_str = message_to_xml_string(
        message,
        short_names=short_names,
        xml_declaration=xml_declaration,
        encoding=encoding,
        pretty_print=pretty_print,
    )
    Path(path).write_text(xml_str, encoding=encoding)


def _normalize_input(
    source: str | PathLike[str] | "ElementType" | Iterable["ElementType"],
) -> "ElementType":
    """Normalize various input types to a single Element."""
    # Check if it's an Element type (stdlib or lxml)
    if _is_element(source):
        return source  # type: ignore[return-value]

    # Path-like or XML string
    if isinstance(source, (str, PathLike)):
        path = Path(source) if not isinstance(source, str) else None

        # Check if it's a file path
        if path is None:
            str_source = source
            # Heuristic: XML strings start with '<'
            if str_source.strip().startswith("<"):
                return _parse_xml_string(str_source)
            # Otherwise treat as path
            path = Path(str_source)

        if path.exists():
            return _parse_xml_file(path)
        raise FileNotFoundError(f"XML file not found: {path}")

    # Iterable of elements - combine products from multiple messages
    elements = list(source)  # type: ignore[arg-type]
    if not elements:
        # Return empty message structure
        root = ET.Element("ONIXMessage")
        root.set("release", "3.1")
        root.append(ET.Element("Header"))
        return root

    # Use first element as base, append products from others
    if HAS_LXML:
        from copy import deepcopy

        root = deepcopy(elements[0])
    else:
        from copy import deepcopy

        root = deepcopy(elements[0])

    for elem in elements[1:]:
        # Find Product elements and append them
        products = _find_products(elem)
        for prod in products:
            root.append(prod)

    return root


def _is_element(obj: Any) -> bool:
    """Check if object is an XML Element (stdlib or lxml)."""
    if isinstance(obj, ET.Element):
        return True
    if HAS_LXML and isinstance(obj, lxml_etree._Element):
        return True
    return False


def _parse_xml_string(xml_str: str) -> "ElementType":
    """Parse XML from string."""
    if HAS_LXML:
        return lxml_etree.fromstring(xml_str.encode("utf-8"))
    return ET.fromstring(xml_str)


def _parse_xml_file(path: Path) -> "ElementType":
    """Parse XML from file."""
    if HAS_LXML:
        tree = lxml_etree.parse(str(path))
        return tree.getroot()
    tree = ET.parse(path)
    return tree.getroot()


def _find_products(root: "ElementType") -> list["ElementType"]:
    """Find all Product elements in a message."""
    products = []
    for tag in ("Product", "product"):  # Reference and short names
        products.extend(root.findall(f".//{tag}"))
    return products


def _element_to_dict(
    element: "ElementType",
    *,
    normalize_tags: bool = True,
) -> dict[str, Any]:
    """Convert an XML Element to a dictionary.

    Args:
        element: The XML Element to convert.
        normalize_tags: If True, convert short tags to reference names.
    """
    result: dict[str, Any] = {}

    # Handle attributes
    for attr, value in element.attrib.items():
        if attr == "release":
            result["release"] = value
        elif attr in ("datestamp", "sourcename", "sourcetype"):
            result[attr] = value

    # Handle child elements
    children: dict[str, list[Any]] = {}
    for child in element:
        child_tag = child.tag if not normalize_tags else to_reference_tag(child.tag)
        child_key = tag_to_field_name(child_tag)

        # Check if this is a known complex element
        is_complex_element = child_key in (
            "header",
            "products",
            "no_product",
            "sender",
            "sender_identifiers",
            "addressees",
            "addressee_identifiers",
        )

        if len(child) == 0 and not child.attrib and not is_complex_element:
            # Leaf element with text content
            value = child.text or ""
        else:
            # Complex element - recurse to get dict
            value = _element_to_dict(child, normalize_tags=normalize_tags)

        if child_key not in children:
            children[child_key] = []
        children[child_key].append(value)

    # Flatten single-value lists, except for known list fields
    list_fields = (
        "products",
        "sender_identifiers",
        "addressees",
        "addressee_identifiers",
    )
    for key, values in children.items():
        if key in list_fields or len(values) > 1:
            result[key] = values
        else:
            result[key] = values[0]

    return result


def _dict_to_element(
    tag: str,
    data: dict[str, Any],
    *,
    short_names: bool = False,
    use_lxml: bool = True,
) -> "ElementType":
    """Convert a dictionary to an XML Element."""
    if use_lxml and HAS_LXML:
        elem = lxml_etree.Element(tag)
    else:
        elem = ET.Element(tag)

    # Set attributes
    for attr in ("datestamp", "sourcename", "sourcetype"):
        if attr in data:
            elem.set(attr, str(data[attr]))

    # Set child elements
    for key, value in data.items():
        if key in ("datestamp", "sourcename", "sourcetype"):
            continue

        # Convert field name to XML tag
        ref_tag = field_name_to_tag(key)
        child_tag = ref_tag if not short_names else to_short_tag(ref_tag)

        if isinstance(value, dict):
            child = _dict_to_element(
                child_tag, value, short_names=short_names, use_lxml=use_lxml
            )
            elem.append(child)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    child = _dict_to_element(
                        child_tag, item, short_names=short_names, use_lxml=use_lxml
                    )
                else:
                    if use_lxml and HAS_LXML:
                        child = lxml_etree.Element(child_tag)
                    else:
                        child = ET.Element(child_tag)
                    child.text = str(item)
                elem.append(child)
        else:
            if use_lxml and HAS_LXML:
                child = lxml_etree.Element(child_tag)
            else:
                child = ET.Element(child_tag)
            child.text = str(value)
            elem.append(child)

    return elem


def _indent_element(elem: "Element", level: int = 0) -> None:
    """Add indentation to XML Element (for stdlib pretty-printing)."""
    indent = "\n" + "  " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
        for child in elem:
            _indent_element(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = indent
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent
