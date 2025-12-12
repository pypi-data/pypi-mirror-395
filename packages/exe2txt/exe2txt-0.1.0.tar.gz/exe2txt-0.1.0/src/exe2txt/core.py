"""Core functionality for analyzing PE files."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

import pefile


@dataclass
class SectionInfo:
    """Information about a PE section."""

    name: str
    virtual_address: int
    virtual_size: int
    raw_size: int
    characteristics: int


@dataclass
class ImportInfo:
    """Information about an imported DLL and its functions."""

    dll_name: str
    functions: list[str] = field(default_factory=list)


@dataclass
class ExportInfo:
    """Information about an exported function."""

    name: str
    ordinal: int
    address: int


@dataclass
class PEInfo:
    """Parsed PE file information."""

    filename: str
    machine_type: str
    timestamp: int
    entry_point: int
    image_base: int
    sections: list[SectionInfo] = field(default_factory=list)
    imports: list[ImportInfo] = field(default_factory=list)
    exports: list[ExportInfo] = field(default_factory=list)

    def to_text(self) -> str:
        """Convert PE information to human-readable text format."""
        lines = [
            f"=== PE File Analysis: {self.filename} ===",
            "",
            "## Basic Information",
            f"Machine Type: {self.machine_type}",
            f"Timestamp: {self.timestamp}",
            f"Entry Point: 0x{self.entry_point:08X}",
            f"Image Base: 0x{self.image_base:08X}",
            "",
        ]

        if self.sections:
            lines.append("## Sections")
            for section in self.sections:
                lines.append(
                    f"  {section.name}: VA=0x{section.virtual_address:08X}, "
                    f"VSize=0x{section.virtual_size:08X}, "
                    f"RawSize=0x{section.raw_size:08X}"
                )
            lines.append("")

        if self.imports:
            lines.append("## Imports")
            for imp in self.imports:
                lines.append(f"  {imp.dll_name}:")
                for func in imp.functions[:10]:  # Limit to first 10 functions
                    lines.append(f"    - {func}")
                if len(imp.functions) > 10:
                    lines.append(f"    ... and {len(imp.functions) - 10} more")
            lines.append("")

        if self.exports:
            lines.append("## Exports")
            for exp in self.exports[:20]:  # Limit to first 20 exports
                lines.append(f"  {exp.name} (ordinal={exp.ordinal})")
            if len(self.exports) > 20:
                lines.append(f"  ... and {len(self.exports) - 20} more")

        return "\n".join(lines)


def _get_machine_type(machine: int) -> str:
    """Convert machine type constant to human-readable string."""
    machine_types = {
        0x014C: "i386",
        0x0200: "IA64",
        0x8664: "AMD64",
        0xAA64: "ARM64",
    }
    return machine_types.get(machine, f"Unknown (0x{machine:04X})")


def analyze_pe(filepath: str | Path) -> PEInfo:
    """
    Analyze a PE file and return structured information.

    Args:
        filepath: Path to the PE file (EXE or DLL).

    Returns:
        PEInfo object containing parsed PE information.

    Raises:
        FileNotFoundError: If the file does not exist.
        pefile.PEFormatError: If the file is not a valid PE file.
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    pe = pefile.PE(str(filepath))

    # Basic information
    info = PEInfo(
        filename=filepath.name,
        machine_type=_get_machine_type(pe.FILE_HEADER.Machine),
        timestamp=pe.FILE_HEADER.TimeDateStamp,
        entry_point=pe.OPTIONAL_HEADER.AddressOfEntryPoint,
        image_base=pe.OPTIONAL_HEADER.ImageBase,
    )

    # Sections
    for section in pe.sections:
        section_name = section.Name.decode("utf-8", errors="ignore").rstrip("\x00")
        info.sections.append(
            SectionInfo(
                name=section_name,
                virtual_address=section.VirtualAddress,
                virtual_size=section.Misc_VirtualSize,
                raw_size=section.SizeOfRawData,
                characteristics=section.Characteristics,
            )
        )

    # Imports
    if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            dll_name = entry.dll.decode("utf-8", errors="ignore")
            functions = []
            for imp in entry.imports:
                if imp.name:
                    functions.append(imp.name.decode("utf-8", errors="ignore"))
                else:
                    functions.append(f"ordinal_{imp.ordinal}")
            info.imports.append(ImportInfo(dll_name=dll_name, functions=functions))

    # Exports
    if hasattr(pe, "DIRECTORY_ENTRY_EXPORT"):
        for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            name = exp.name.decode("utf-8", errors="ignore") if exp.name else f"ordinal_{exp.ordinal}"
            info.exports.append(
                ExportInfo(
                    name=name,
                    ordinal=exp.ordinal,
                    address=exp.address,
                )
            )

    pe.close()
    return info
