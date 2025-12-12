"""Library analysis component for import table parsing and categorization."""

from dataclasses import dataclass
from enum import Enum
from typing import List

import pefile

from exe_analyzer_mcp.config import load_system_libraries


class LibraryCategory(Enum):
    """Categories for imported libraries."""

    SYSTEM = "system"
    RUNTIME = "runtime"
    EXTERNAL = "external"


@dataclass
class Library:
    """Represents an imported library."""

    name: str
    category: LibraryCategory
    functions: List[str]


@dataclass
class LibraryAnalysis:
    """Results of library analysis."""

    system_libraries: List[Library]
    external_libraries: List[Library]
    total_imports: int


class LibraryAnalyzer:
    """Analyzes imported libraries in PE files."""

    def __init__(self):
        """Initialize library analyzer with system library database."""
        config = load_system_libraries()
        self.system_libs = set(
            lib.lower() for lib in config.get("system_libraries", [])
        )
        self.runtime_libs = set(
            lib.lower() for lib in config.get("runtime_libraries", [])
        )

    def analyze_libraries(self, pe: pefile.PE) -> LibraryAnalysis:
        """Analyze libraries imported by a PE file.

        Args:
            pe: Parsed PE file object

        Returns:
            LibraryAnalysis object containing categorized libraries
        """
        # Parse import table
        dll_imports = self._parse_import_table(pe)

        # Categorize libraries
        system_libraries = []
        external_libraries = []

        for dll_name, functions in dll_imports.items():
            category = self._categorize_library(dll_name)
            library = Library(name=dll_name, category=category, functions=functions)

            if category == LibraryCategory.EXTERNAL:
                external_libraries.append(library)
            else:
                system_libraries.append(library)

        return LibraryAnalysis(
            system_libraries=system_libraries,
            external_libraries=external_libraries,
            total_imports=len(dll_imports),
        )

    def _parse_import_table(self, pe: pefile.PE) -> dict[str, List[str]]:
        """Parse import table and extract DLL names with functions.

        Args:
            pe: Parsed PE file object

        Returns:
            Dictionary mapping DLL names to lists of imported functions
        """
        imports = {}

        try:
            # Parse import directory if not already done
            pe.parse_data_directories(
                directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]]
            )

            if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    dll_name = entry.dll.decode("utf-8", errors="ignore")
                    functions = []

                    for imp in entry.imports:
                        if imp.name:
                            func_name = imp.name.decode("utf-8", errors="ignore")
                            functions.append(func_name)
                        elif imp.ordinal:
                            # Import by ordinal
                            functions.append(f"Ordinal_{imp.ordinal}")

                    imports[dll_name] = functions

        except Exception:
            # Return empty dict if import table is corrupted or missing
            pass

        return imports

    def _categorize_library(self, dll_name: str) -> LibraryCategory:
        """Categorize a library as system, runtime, or external.

        Args:
            dll_name: Name of the DLL

        Returns:
            LibraryCategory enum value
        """
        dll_lower = dll_name.lower()

        if self._is_system_library(dll_lower):
            return LibraryCategory.SYSTEM
        elif self._is_runtime_library(dll_lower):
            return LibraryCategory.RUNTIME
        else:
            return LibraryCategory.EXTERNAL

    def _is_system_library(self, dll_name: str) -> bool:
        """Check if a library is a Windows system library.

        Args:
            dll_name: Name of the DLL (lowercase)

        Returns:
            True if system library, False otherwise
        """
        return dll_name in self.system_libs

    def _is_runtime_library(self, dll_name: str) -> bool:
        """Check if a library is a language runtime library.

        Args:
            dll_name: Name of the DLL (lowercase)

        Returns:
            True if runtime library, False otherwise
        """
        return dll_name in self.runtime_libs
