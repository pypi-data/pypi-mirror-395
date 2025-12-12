"""PE file parser wrapper with safe loading and error handling."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import pefile


@dataclass
class PESection:
    """Represents a PE file section."""

    name: str
    virtual_address: int
    virtual_size: int
    raw_size: int
    characteristics: int


@dataclass
class ImportedDLL:
    """Represents an imported DLL and its functions."""

    name: str
    functions: List[str]


class PEParserError(Exception):
    """Base exception for PE parser errors."""

    pass


class InvalidPEError(PEParserError):
    """Raised when file is not a valid PE format."""

    pass


class PEParser:
    """Wrapper for pefile library with safe loading and error handling."""

    def __init__(self, file_path: str):
        """Initialize PE parser with file path.

        Args:
            file_path: Path to the PE file to analyze

        Raises:
            FileNotFoundError: If file does not exist
            PermissionError: If file cannot be read
            InvalidPEError: If file is not a valid PE format
        """
        self.file_path = Path(file_path)
        self._pe: Optional[pefile.PE] = None
        self._load_pe_file()

    def _load_pe_file(self) -> None:
        """Load PE file with error handling."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        if not self.file_path.is_file():
            raise InvalidPEError(f"Path is not a file: {self.file_path}")

        try:
            self._pe = pefile.PE(str(self.file_path), fast_load=True)
        except PermissionError as e:
            raise PermissionError(f"Cannot read file: {self.file_path}") from e
        except pefile.PEFormatError as e:
            raise InvalidPEError(f"Invalid PE format: {self.file_path}") from e
        except Exception as e:
            raise PEParserError(f"Error loading PE file: {e}") from e

    def get_pe_header(self) -> dict:
        """Extract PE header information.

        Returns:
            Dictionary containing PE header metadata including:
            - machine: Target machine type
            - timestamp: Compilation timestamp
            - characteristics: PE characteristics flags
            - subsystem: Target subsystem
            - dll_characteristics: DLL characteristics flags

        Raises:
            PEParserError: If PE header cannot be read
        """
        if self._pe is None:
            raise PEParserError("PE file not loaded")

        try:
            header_info = {
                "machine": self._pe.FILE_HEADER.Machine,
                "timestamp": self._pe.FILE_HEADER.TimeDateStamp,
                "characteristics": self._pe.FILE_HEADER.Characteristics,
                "subsystem": self._pe.OPTIONAL_HEADER.Subsystem,
                "dll_characteristics": self._pe.OPTIONAL_HEADER.DllCharacteristics,
            }

            # Add entry point if available
            if hasattr(self._pe.OPTIONAL_HEADER, "AddressOfEntryPoint"):
                header_info["entry_point"] = self._pe.OPTIONAL_HEADER.AddressOfEntryPoint

            return header_info
        except AttributeError as e:
            raise PEParserError(f"Error reading PE header: {e}") from e

    def get_sections(self) -> List[PESection]:
        """Extract PE file sections.

        Returns:
            List of PESection objects containing section information

        Raises:
            PEParserError: If sections cannot be read
        """
        if self._pe is None:
            raise PEParserError("PE file not loaded")

        try:
            sections = []
            for section in self._pe.sections:
                sections.append(
                    PESection(
                        name=section.Name.decode("utf-8", errors="ignore").rstrip("\x00"),
                        virtual_address=section.VirtualAddress,
                        virtual_size=section.Misc_VirtualSize,
                        raw_size=section.SizeOfRawData,
                        characteristics=section.Characteristics,
                    )
                )
            return sections
        except Exception as e:
            raise PEParserError(f"Error reading sections: {e}") from e

    def get_import_table(self) -> List[ImportedDLL]:
        """Extract import table with DLL names and imported functions.

        Returns:
            List of ImportedDLL objects containing DLL names and their imported functions

        Raises:
            PEParserError: If import table cannot be read
        """
        if self._pe is None:
            raise PEParserError("PE file not loaded")

        try:
            # Parse import directory if not already done
            self._pe.parse_data_directories(
                directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]]
            )

            imports = []

            if hasattr(self._pe, "DIRECTORY_ENTRY_IMPORT"):
                for entry in self._pe.DIRECTORY_ENTRY_IMPORT:
                    dll_name = entry.dll.decode("utf-8", errors="ignore")
                    functions = []

                    for imp in entry.imports:
                        if imp.name:
                            func_name = imp.name.decode("utf-8", errors="ignore")
                            functions.append(func_name)
                        elif imp.ordinal:
                            # Import by ordinal
                            functions.append(f"Ordinal_{imp.ordinal}")

                    imports.append(ImportedDLL(name=dll_name, functions=functions))

            return imports
        except Exception as e:
            raise PEParserError(f"Error reading import table: {e}") from e

    def has_clr_header(self) -> bool:
        """Check if PE file has a CLR (.NET) header.

        Returns:
            True if CLR header is present, False otherwise
        """
        if self._pe is None:
            return False

        try:
            # Parse COM descriptor directory for .NET detection
            self._pe.parse_data_directories(
                directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_COM_DESCRIPTOR"]]
            )
            return hasattr(self._pe, "DIRECTORY_ENTRY_COM_DESCRIPTOR")
        except Exception:
            return False

    def close(self) -> None:
        """Close the PE file and release resources."""
        if self._pe is not None:
            self._pe.close()
            self._pe = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.close()
        return False
