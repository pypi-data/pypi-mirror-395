"""Tests for exe2txt.core module."""

from __future__ import annotations

import pytest

from exe2txt.core import PEInfo, SectionInfo, ImportInfo, ExportInfo


class TestPEInfo:
    """Tests for PEInfo dataclass."""

    def test_to_text_basic(self) -> None:
        """Test basic text output."""
        info = PEInfo(
            filename="test.exe",
            machine_type="AMD64",
            timestamp=1234567890,
            entry_point=0x1000,
            image_base=0x140000000,
        )
        text = info.to_text()

        assert "test.exe" in text
        assert "AMD64" in text
        assert "0x00001000" in text
        assert "0x140000000" in text

    def test_to_text_with_sections(self) -> None:
        """Test text output with sections."""
        info = PEInfo(
            filename="test.exe",
            machine_type="AMD64",
            timestamp=1234567890,
            entry_point=0x1000,
            image_base=0x140000000,
            sections=[
                SectionInfo(
                    name=".text",
                    virtual_address=0x1000,
                    virtual_size=0x5000,
                    raw_size=0x5000,
                    characteristics=0x60000020,
                ),
            ],
        )
        text = info.to_text()

        assert ".text" in text
        assert "Sections" in text

    def test_to_text_with_imports(self) -> None:
        """Test text output with imports."""
        info = PEInfo(
            filename="test.exe",
            machine_type="AMD64",
            timestamp=1234567890,
            entry_point=0x1000,
            image_base=0x140000000,
            imports=[
                ImportInfo(
                    dll_name="kernel32.dll",
                    functions=["GetProcAddress", "LoadLibraryA"],
                ),
            ],
        )
        text = info.to_text()

        assert "kernel32.dll" in text
        assert "GetProcAddress" in text
        assert "Imports" in text


class TestAnalyzePE:
    """Tests for analyze_pe function."""

    def test_file_not_found(self) -> None:
        """Test that FileNotFoundError is raised for missing files."""
        from exe2txt.core import analyze_pe

        with pytest.raises(FileNotFoundError):
            analyze_pe("/nonexistent/path/to/file.exe")
