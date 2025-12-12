"""Property-based tests for PE parser component.

Feature: exe-analyzer-mcp, Property 11: PE header examination for language inference
Validates: Requirements 4.1
"""

import struct
import tempfile
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from exe_analyzer_mcp.pe_parser import InvalidPEError, PEParser, PEParserError


def create_minimal_pe_file(file_path: Path) -> None:
    """Create a minimal valid PE file for testing.

    This creates a bare-minimum PE file with proper DOS and PE headers.
    """
    with open(file_path, "wb") as f:
        # DOS Header (64 bytes)
        dos_header = bytearray(64)
        dos_header[0:2] = b"MZ"  # DOS signature
        dos_header[60:64] = struct.pack("<I", 64)  # PE header offset

        # PE Signature (4 bytes)
        pe_signature = b"PE\x00\x00"

        # COFF File Header (20 bytes)
        coff_header = struct.pack(
            "<HHIIIHH",
            0x014C,  # Machine (IMAGE_FILE_MACHINE_I386)
            0,  # NumberOfSections
            0,  # TimeDateStamp
            0,  # PointerToSymbolTable
            0,  # NumberOfSymbols
            224,  # SizeOfOptionalHeader (PE32)
            0x0002,  # Characteristics (IMAGE_FILE_EXECUTABLE_IMAGE)
        )

        # Optional Header (224 bytes for PE32)
        optional_header = struct.pack(
            "<HBB",
            0x010B,  # Magic (PE32)
            0,  # MajorLinkerVersion
            0,  # MinorLinkerVersion
        )
        optional_header += b"\x00" * (224 - len(optional_header))

        # Write all parts
        f.write(dos_header)
        f.write(pe_signature)
        f.write(coff_header)
        f.write(optional_header)


# Feature: exe-analyzer-mcp, Property 11: PE header examination for language inference
@given(st.integers(min_value=0, max_value=0xFFFF))
def test_pe_header_examination_succeeds_for_valid_pe(machine_type: int):
    """Property 11: For any valid PE file, language inference should successfully
    read and examine the PE header without error.

    This test verifies that the PE parser can successfully extract header information
    from any valid PE file, which is a prerequisite for language inference.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.exe"

        # Create a minimal valid PE file
        with open(test_file, "wb") as f:
            # DOS Header
            dos_header = bytearray(64)
            dos_header[0:2] = b"MZ"
            dos_header[60:64] = struct.pack("<I", 64)

            # PE Signature
            pe_signature = b"PE\x00\x00"

            # COFF File Header with the generated machine type
            coff_header = struct.pack(
                "<HHIIIHH",
                machine_type & 0xFFFF,  # Machine type
                0,  # NumberOfSections
                0,  # TimeDateStamp
                0,  # PointerToSymbolTable
                0,  # NumberOfSymbols
                224,  # SizeOfOptionalHeader
                0x0002,  # Characteristics
            )

            # Optional Header
            optional_header = struct.pack("<HBB", 0x010B, 0, 0)
            optional_header += b"\x00" * (224 - len(optional_header))

            f.write(dos_header)
            f.write(pe_signature)
            f.write(coff_header)
            f.write(optional_header)

        # Property: PE header examination should succeed without error
        with PEParser(str(test_file)) as parser:
            header = parser.get_pe_header()

            # Verify that header information was successfully extracted
            assert isinstance(header, dict)
            assert "machine" in header
            assert "timestamp" in header
            assert "characteristics" in header
            assert "subsystem" in header
            assert "dll_characteristics" in header


def test_pe_header_examination_fails_for_invalid_file():
    """Verify that invalid PE files raise appropriate errors."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "invalid.exe"

        # Create an invalid file (not PE format)
        with open(test_file, "wb") as f:
            f.write(b"This is not a PE file")

        # Should raise InvalidPEError for non-PE files
        with pytest.raises(InvalidPEError):
            PEParser(str(test_file))


def test_pe_header_examination_fails_for_nonexistent_file():
    """Verify that nonexistent files raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        PEParser("/nonexistent/path/to/file.exe")


def test_pe_parser_extracts_sections():
    """Verify that PE parser can extract section information."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.exe"
        create_minimal_pe_file(test_file)

        with PEParser(str(test_file)) as parser:
            sections = parser.get_sections()
            # Minimal PE has no sections, but should return empty list without error
            assert isinstance(sections, list)


def test_pe_parser_extracts_import_table():
    """Verify that PE parser can extract import table."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.exe"
        create_minimal_pe_file(test_file)

        with PEParser(str(test_file)) as parser:
            imports = parser.get_import_table()
            # Minimal PE has no imports, but should return empty list without error
            assert isinstance(imports, list)


def test_pe_parser_checks_clr_header():
    """Verify that PE parser can check for CLR header."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.exe"
        create_minimal_pe_file(test_file)

        with PEParser(str(test_file)) as parser:
            has_clr = parser.has_clr_header()
            # Minimal PE has no CLR header
            assert isinstance(has_clr, bool)
            assert has_clr is False


def test_pe_parser_context_manager():
    """Verify that PE parser works as context manager and cleans up resources."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.exe"
        create_minimal_pe_file(test_file)

        with PEParser(str(test_file)) as parser:
            header = parser.get_pe_header()
            assert isinstance(header, dict)

        # After context exit, PE should be closed
        # Accessing after close should raise error
        with pytest.raises(PEParserError):
            parser.get_pe_header()
