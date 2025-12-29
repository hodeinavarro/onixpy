"""Tests for ONIX code lists."""

from __future__ import annotations


from onix.lists import CodeList, CodeListEntry, get_code, get_list, list_available


class TestCodeListEntry:
    """Tests for CodeListEntry dataclass."""

    def test_entry_attributes(self):
        """Entry has expected attributes."""
        entry = CodeListEntry(
            list_number=44,
            code="16",
            heading="ISNI",
            notes="International Standard Name Identifier",
            added_version=10,
        )

        assert entry.list_number == 44
        assert entry.code == "16"
        assert entry.heading == "ISNI"
        assert entry.notes is not None
        assert entry.added_version == 10
        assert entry.is_deprecated is False

    def test_deprecated_entry(self):
        """Deprecated entry is correctly identified."""
        entry = CodeListEntry(
            list_number=44,
            code="02",
            heading="Deprecated code",
            deprecated_version=10,
        )

        assert entry.is_deprecated is True


class TestCodeList:
    """Tests for CodeList dataclass."""

    def test_list_attributes(self):
        """CodeList has expected attributes."""
        entry = CodeListEntry(list_number=44, code="01", heading="Test")
        code_list = CodeList(
            number=44,
            heading="Test list",
            scope_note="Used with test elements",
            entries={"01": entry},
        )

        assert code_list.number == 44
        assert code_list.heading == "Test list"
        assert len(code_list) == 1

    def test_list_get(self):
        """Get entry by code."""
        entry = CodeListEntry(list_number=44, code="16", heading="ISNI")
        code_list = CodeList(
            number=44,
            heading="Name identifier type",
            scope_note="",
            entries={"16": entry},
        )

        result = code_list.get("16")
        assert result is not None
        assert result.heading == "ISNI"

        assert code_list.get("99") is None

    def test_list_iteration(self):
        """Iterate over entries."""
        entries = {
            "01": CodeListEntry(list_number=44, code="01", heading="A"),
            "02": CodeListEntry(list_number=44, code="02", heading="B"),
        }
        code_list = CodeList(number=44, heading="Test", scope_note="", entries=entries)

        headings = [e.heading for e in code_list]
        assert "A" in headings
        assert "B" in headings


class TestGetList:
    """Tests for get_list function."""

    def test_get_list_44(self):
        """List 44 (Name identifier type) is available."""
        code_list = get_list(44)

        assert code_list is not None
        assert code_list.number == 44
        assert code_list.heading == "Name identifier type"

    def test_get_list_44_has_isni(self):
        """List 44 includes ISNI code."""
        code_list = get_list(44)
        assert code_list is not None

        isni = code_list.get("16")
        assert isni is not None
        assert isni.heading == "ISNI"

    def test_get_list_nonexistent(self):
        """Non-existent list returns None."""
        result = get_list(9999)
        assert result is None


class TestGetCode:
    """Tests for get_code function."""

    def test_get_code_exists(self):
        """Get existing code from list."""
        entry = get_code(44, "16")

        assert entry is not None
        assert entry.code == "16"
        assert entry.heading == "ISNI"

    def test_get_code_not_in_list(self):
        """Code not in list returns None."""
        entry = get_code(44, "99")
        assert entry is None

    def test_get_code_list_not_exists(self):
        """Code from non-existent list returns None."""
        entry = get_code(9999, "01")
        assert entry is None


class TestListAvailable:
    """Tests for list_available function."""

    def test_list_44_available(self):
        """List 44 is in available lists."""
        available = list_available()

        assert 44 in available

    def test_returns_sorted(self):
        """Available lists are sorted."""
        available = list_available()

        assert available == sorted(available)
