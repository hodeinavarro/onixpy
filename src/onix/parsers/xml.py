"""XML parsing and serialization for ONIX messages.

Supports loading ONIXMessage from:
- Path-like string (file path)
- XML string
- lxml Element
- Iterable of Element objects (combined into single message)

Supports dumping ONIXMessage to:
- lxml Element
- XML string
- File path

Requires lxml for XML handling.
"""

from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable

from lxml import etree

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
    is_list_field,
    register_model,
    register_plural_mapping,
    tag_to_field_name,
)
from onix.parsers.tags import to_reference_tag, to_short_tag
from onix.product import Product, ProductIdentifier

if TYPE_CHECKING:
    from lxml.etree import _Element as Element

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
    register_model(ProductIdentifier)

    # Register plural mappings for list fields that use singular XML tags
    register_plural_mapping("Product", "products")
    register_plural_mapping("Addressee", "addressees")
    register_plural_mapping("SenderIdentifier", "sender_identifiers")
    register_plural_mapping("AddresseeIdentifier", "addressee_identifiers")
    register_plural_mapping("ProductIdentifier", "product_identifiers")


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
            - lxml Element
            - Iterable of lxml Element objects (products combined)
        short_names: If True, expect short tag names in input;
            otherwise expect reference names (default). The parser
            will auto-detect and normalize to reference names.

    Returns:
        Parsed ONIXMessage instance.

    Raises:
        FileNotFoundError: If path doesn't exist
        etree.ParseError: If XML is invalid
        pydantic.ValidationError: If data doesn't match schema

    Example:
        >>> from onix.parsers import xml_to_message
        >>> msg = xml_to_message("/path/to/message.xml")
        >>> msg = xml_to_message("<ONIXMessage>...</ONIXMessage>")
    """
    root = _normalize_input(source)
    data = _element_to_dict(root, normalize_tags=not short_names)

    # Ensure products is always a list if present and not already
    # This handles single <Product> elements that get flattened
    if "products" in data and not isinstance(data["products"], list):
        data["products"] = [data["products"]]

    return ONIXMessage.model_validate(data)


def message_to_xml(
    message: ONIXMessage,
    *,
    short_names: bool = False,
) -> "ElementType":
    """Convert an ONIX message to an XML Element.

    Args:
        message: The ONIXMessage to convert.
        short_names: If True, use short tag names;
            otherwise use reference names (default).

    Returns:
        lxml Element representing the message.
    """
    data = message.model_dump(exclude_none=True, exclude_defaults=True)

    root_tag = "ONIXMessage" if not short_names else to_short_tag("ONIXMessage")

    # Define namespace based on tag format
    namespace = (
        "http://ns.editeur.org/onix/3.1/reference"
        if not short_names
        else "http://ns.editeur.org/onix/3.1/short"
    )
    nsmap: dict[str | None, str] = {None: namespace}  # Default namespace

    # Use Clark notation for the root element tag to ensure namespace is properly set
    # type: ignore because lxml accepts None key but stubs type it as Mapping[str, str]
    root = etree.Element(f"{{{namespace}}}{root_tag}", nsmap=nsmap)  # type: ignore[arg-type]

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
        header_tag, header_data, short_names=short_names, namespace=namespace
    )
    root.append(header_elem)

    # Build Products or NoProduct
    if data.get("no_product"):
        no_product_tag = "NoProduct" if not short_names else to_short_tag("NoProduct")
        root.append(etree.Element(f"{{{namespace}}}{no_product_tag}"))
    else:
        product_tag = "Product" if not short_names else to_short_tag("Product")
        for product_data in data.get("products", []):
            product_elem = _dict_to_element(
                product_tag, product_data, short_names=short_names, namespace=namespace
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
        pretty_print: If True, format with indentation.

    Returns:
        XML string representation of the message.
    """
    root = message_to_xml(message, short_names=short_names)

    # lxml doesn't support xml_declaration with unicode encoding
    # so we build it manually
    xml_str = etree.tostring(
        root,
        encoding="unicode",
        pretty_print=pretty_print,
    )
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
    """Normalize various input types to a single lxml Element."""
    # Check if it's an lxml Element
    if _is_element(source):
        return source  # type: ignore[return-value]

    # Handle string input (XML string or file path)
    if isinstance(source, str):
        # Heuristic: XML strings start with '<'
        if source.strip().startswith("<"):
            return _parse_xml_string(source)
        # Otherwise treat as path
        path = Path(source)
        if path.exists():
            return _parse_xml_file(path)
        raise FileNotFoundError(f"XML file not found: {path}")

    # Handle PathLike input (file path)
    if isinstance(source, PathLike):
        path = Path(source)  # type: ignore[arg-type]  # ty can't narrow PathLike from Iterable
        if path.exists():
            return _parse_xml_file(path)
        raise FileNotFoundError(f"XML file not found: {path}")

    # Iterable of elements - combine products from multiple messages
    elements = list(source)  # type: ignore[arg-type]
    if not elements:
        # Return empty message structure
        nsmap: dict[str | None, str] = {
            None: "http://ns.editeur.org/onix/3.1/reference"
        }
        root = etree.Element("ONIXMessage", nsmap=nsmap)  # type: ignore[arg-type]
        root.set("release", "3.1")
        root.append(etree.Element("Header"))
        return root

    # Use first element as base, append products from others
    from copy import deepcopy

    root = deepcopy(elements[0])

    for elem in elements[1:]:
        # Find Product elements and append them
        products = _find_products(elem)
        for prod in products:
            root.append(prod)

    return root


def _is_element(obj: Any) -> bool:
    """Check if object is an lxml Element."""
    return isinstance(obj, etree._Element)


def _parse_xml_string(xml_str: str) -> "ElementType":
    """Parse XML from string."""
    return etree.fromstring(xml_str.encode("utf-8"))


def _parse_xml_file(path: Path) -> "ElementType":
    """Parse XML from file."""
    tree = etree.parse(str(path))
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
        # Strip namespace from tag using lxml's QName or localname
        child_tag = child.tag
        if isinstance(child_tag, str) and "{" in child_tag:
            # Clark notation: {namespace}localname
            child_tag = child_tag.split("}")[-1]

        if normalize_tags:
            child_tag = to_reference_tag(child_tag)

        child_key = tag_to_field_name(child_tag)

        # Determine if element has complex content
        has_children = len(child) > 0
        has_attributes = bool(child.attrib)
        has_text = bool(child.text and child.text.strip())

        # If element has children or attributes, it's complex
        # If it has no children, no attributes, but also no text, treat as empty complex (e.g., <Product/>)
        is_complex = has_children or has_attributes or not has_text

        if not is_complex:
            # Leaf element with text content only
            value = child.text or ""
        else:
            # Complex element (including empty ones like <Product/>)
            value = _element_to_dict(child, normalize_tags=normalize_tags)

        if child_key not in children:
            children[child_key] = []
        children[child_key].append(value)

    # Add children to result
    # Keep as list if multiple values or if field is a list field, otherwise flatten to single value
    for key, values in children.items():
        if len(values) > 1 or is_list_field(key):
            result[key] = values
        else:
            result[key] = values[0]

    return result


def _dict_to_element(
    tag: str,
    data: dict[str, Any],
    *,
    short_names: bool = False,
    namespace: str | None = None,
) -> "ElementType":
    """Convert a dictionary to an XML Element."""
    if namespace:
        full_tag = f"{{{namespace}}}{tag}"
    else:
        full_tag = tag

    elem = etree.Element(full_tag)

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
                child_tag, value, short_names=short_names, namespace=namespace
            )
            elem.append(child)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    child = _dict_to_element(
                        child_tag, item, short_names=short_names, namespace=namespace
                    )
                else:
                    if namespace:
                        child_full_tag = f"{{{namespace}}}{child_tag}"
                    else:
                        child_full_tag = child_tag

                    child = etree.Element(child_full_tag)
                    child.text = str(item)
                elem.append(child)
        else:
            if namespace:
                child_full_tag = f"{{{namespace}}}{child_tag}"
            else:
                child_full_tag = child_tag

            child = etree.Element(child_full_tag)
            child.text = str(value)
            elem.append(child)

    return elem
