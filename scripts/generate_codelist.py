#!/usr/bin/env python3
"""Generate ONIX code list Python files from EDItEUR's official source.

Usage:
    uv run generate-list 44
    uv run generate-list 44 58 74 96
    uv run generate-list --all

The script fetches the code list from EDItEUR's website, parses the HTML table,
generates Python code, and runs ruff to lint and format.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

# EDItEUR code list base URL
CODELIST_URL = "https://ns.editeur.org/onix/en/{list_number}"

# Output directory for generated lists
OUTPUT_DIR = Path(__file__).parent.parent / "src" / "onix" / "lists"


def fetch_codelist_html(list_number: int) -> str:
    """Fetch the HTML page for a code list from EDItEUR."""
    url = CODELIST_URL.format(list_number=list_number)
    print(f"Fetching List {list_number} from {url}...")

    response = httpx.get(url, follow_redirects=True, timeout=30)
    response.raise_for_status()
    return response.text


def parse_codelist(html: str, list_number: int) -> dict:
    """Parse the HTML table and extract code list data."""
    soup = BeautifulSoup(html, "lxml")

    # Get the list title
    title_elem = soup.select_one("h1, .page-title, title")
    title = title_elem.get_text(strip=True) if title_elem else f"List {list_number}"
    # Clean up title
    title = re.sub(r"^List\s+\d+[:\s]*", "", title).strip()
    if not title:
        title = f"Code list {list_number}"

    # Find the main table with code values
    table = soup.select_one("table.table, table")
    if not table:
        raise ValueError(f"Could not find code table for List {list_number}")

    entries = []
    list_heading = None  # The main heading for the list (from first row)
    rows = table.select("tr")

    # The EDItEUR table structure has columns:
    # | List# | Code | Description (with heading in <a> and notes in <span class="scopenote">) | Added | ? | Deprecated | ✽ |
    for row in rows:
        cells = row.select("td")
        if not cells or len(cells) < 3:
            continue

        # Get cell values
        list_num_cell = cells[0].get_text(strip=True)
        code_cell = cells[1].get_text(strip=True) if len(cells) > 1 else ""
        desc_cell = cells[2] if len(cells) > 2 else None

        # Skip if this isn't a row for our list
        if list_num_cell != str(list_number):
            continue

        # Skip if no code (this is the list header row)
        if not code_cell:
            # This is the list title row - extract the list heading
            if desc_cell:
                heading_link = desc_cell.select_one("a")
                if heading_link:
                    list_heading = heading_link.get_text(strip=True)
            continue

        # Extract heading from <a> tag in description cell
        heading = ""
        notes = None
        if desc_cell:
            # Heading is in the <a> tag
            heading_link = desc_cell.select_one("a")
            if heading_link:
                heading = heading_link.get_text(strip=True)

            # Notes are in <span class="scopenote">
            notes_span = desc_cell.select_one("span.scopenote")
            if notes_span:
                notes = notes_span.get_text(strip=True)

        # Clean up heading - remove trailing ellipsis or symbols
        heading = heading.rstrip("…✽? ").strip()

        # Get version info from remaining cells
        added_version = None
        deprecated_version = None

        if len(cells) > 3:
            added_text = cells[3].get_text(strip=True)
            if added_text and added_text.isdigit():
                added_version = int(added_text)

        if len(cells) > 5:
            deprecated_text = cells[5].get_text(strip=True)
            if deprecated_text and deprecated_text.isdigit():
                deprecated_version = int(deprecated_text)

        # Check for deprecated marker in row class
        row_class = row.get("class", [])
        row_class_str = " ".join(row_class) if row_class else ""
        if "deprecated" in row_class_str.lower():
            deprecated_version = deprecated_version or True

        entry = {
            "code": code_cell,
            "heading": heading,
            "notes": notes,
            "added_version": added_version,
            "deprecated_version": deprecated_version,
        }
        entries.append(entry)

    # Use the list heading if we found it
    if list_heading:
        title = list_heading

    return {
        "number": list_number,
        "heading": title,
        "entries": entries,
    }


def generate_python_code(data: dict) -> str:
    """Generate Python code for a code list."""
    list_number = data["number"]
    heading = data["heading"]
    entries = data["entries"]

    # Escape strings for Python
    def escape(s: str | None) -> str:
        if s is None:
            return "None"
        escaped = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return f'"{escaped}"'

    def normalize(s: str | None) -> str | None:
        """Replace special Unicode characters with ASCII equivalents."""
        if s is None:
            return None
        # Curly quotes and apostrophes
        s = s.replace("'", "'").replace("'", "'")
        s = s.replace(""", '"').replace(""", '"')
        # Dashes
        s = s.replace("–", "-").replace("—", "-")
        # Ellipsis
        s = s.replace("…", "...")
        # Non-breaking space
        s = s.replace("\u00a0", " ")
        # Other common replacements
        s = s.replace("©", "(c)").replace("®", "(R)").replace("™", "(TM)")
        return s

    lines = [
        f'"""ONIX Code List {list_number}: {normalize(heading)}."""',
        "",
        "from onix.lists.models import CodeList, CodeListEntry",
        "",
        "_ENTRIES = {",
    ]

    for entry in entries:
        code = entry["code"]
        heading_val = normalize(entry["heading"])
        notes = normalize(entry["notes"])
        added = entry.get("added_version")
        deprecated = entry.get("deprecated_version")

        lines.append(f'    "{code}": CodeListEntry(')
        lines.append(f"        list_number={list_number},")
        lines.append(f'        code="{code}",')
        lines.append(f"        heading={escape(heading_val)},")
        if notes:
            lines.append(f"        notes={escape(notes)},")
        if added:
            lines.append(f"        added_version={added},")
        if deprecated:
            lines.append(f"        deprecated_version={deprecated},")
        lines.append("    ),")

    lines.append("}")
    lines.append("")
    lines.append(f"List{list_number} = CodeList(")
    lines.append(f"    number={list_number},")
    lines.append(f"    heading={escape(normalize(data['heading']))},")
    lines.append('    scope_note="",')
    lines.append("    entries=_ENTRIES,")
    lines.append(")")
    lines.append("")

    # Generate name alias based on heading
    alias_name = _heading_to_alias(list_number, data["heading"])
    if alias_name:
        lines.append("# Alias by name")
        lines.append(f"{alias_name} = List{list_number}")
        lines.append("")

    return "\n".join(lines)


# Well-known alias names for common lists
_KNOWN_ALIASES: dict[int, str] = {
    44: "NameIdentifierType",
    58: "PriceType",
    74: "LanguageCode",
    96: "CurrencyCode",
    5: "ProductIdentifierType",
    15: "TitleType",
    17: "ContributorRole",
    78: "ProductFormDetail",
    153: "TextType",
}


def _heading_to_alias(list_number: int, heading: str) -> str | None:
    """Convert a list heading to a Python identifier alias."""
    # Check if we have a known alias for this list
    if list_number in _KNOWN_ALIASES:
        return _KNOWN_ALIASES[list_number]

    # Otherwise generate from heading
    # Remove common prefixes/suffixes and convert to PascalCase
    cleaned = heading.strip()

    # Remove "code" suffix if present
    cleaned = re.sub(r"\s*code$", "", cleaned, flags=re.IGNORECASE)

    # Replace special characters with space (en-dash, em-dash, etc.)
    cleaned = re.sub(r"[–—/\\()]", " ", cleaned)

    # Keep only alphanumeric and spaces
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", cleaned)

    # Split into words and capitalize
    words = re.split(r"\s+", cleaned)
    words = [w.capitalize() for w in words if w]

    if not words:
        return None

    alias = "".join(words)

    # Ensure it's a valid Python identifier
    if not alias or not alias[0].isalpha():
        return None

    return alias


def save_and_format(list_number: int, code: str) -> Path:
    """Save the generated code and run ruff to format it."""
    output_path = OUTPUT_DIR / f"list{list_number}.py"

    print(f"Writing to {output_path}...")
    output_path.write_text(code, encoding="utf-8")

    # Run ruff check --fix
    print("Running ruff check --fix...")
    subprocess.run(
        ["ruff", "check", "--fix", str(output_path)],
        capture_output=True,
    )

    # Run ruff format
    print("Running ruff format...")
    subprocess.run(
        ["ruff", "format", str(output_path)],
        capture_output=True,
    )

    return output_path


def generate_list(list_number: int) -> None:
    """Generate a single code list file."""
    try:
        html = fetch_codelist_html(list_number)
        data = parse_codelist(html, list_number)
        code = generate_python_code(data)
        output_path = save_and_format(list_number, code)
        print(f"✓ Generated List {list_number}: {output_path}")
        print(f"  {len(data['entries'])} entries")
    except Exception as e:
        print(f"✗ Failed to generate List {list_number}: {e}", file=sys.stderr)
        raise


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate ONIX code list Python files from EDItEUR"
    )
    parser.add_argument(
        "lists",
        nargs="*",
        type=int,
        help="List numbers to generate (e.g., 44 58 74)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate all commonly used lists",
    )

    args = parser.parse_args()

    if args.all:
        # Common lists used in ONIX
        lists = [
            1,
            2,
            3,
            5,
            9,
            12,
            13,
            15,
            17,
            18,
            19,
            44,
            58,
            74,
            79,
            81,
            91,
            96,
            150,
            175,
        ]
    elif args.lists:
        lists = args.lists
    else:
        parser.print_help()
        sys.exit(1)

    for list_num in lists:
        generate_list(list_num)

    print(f"\n✓ Generated {len(lists)} code list(s)")


if __name__ == "__main__":
    main()
