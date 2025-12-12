"""Unit tests for library analyzer."""

from exe_analyzer_mcp.library_analyzer import (
    LibraryAnalyzer,
    LibraryCategory,
)


class MockImport:
    """Mock import entry."""

    def __init__(self, name, ordinal=None):
        self.name = name.encode("utf-8") if name else None
        self.ordinal = ordinal


class MockEntry:
    """Mock import directory entry."""

    def __init__(self, dll_name, functions):
        self.dll = dll_name.encode("utf-8")
        self.imports = [MockImport(func) for func in functions]


class MockPE:
    """Mock PE object with import table."""

    def __init__(self, entries):
        if entries:
            self.DIRECTORY_ENTRY_IMPORT = entries
        self._has_import = bool(entries)

    def parse_data_directories(self, directories):
        """Mock parse_data_directories."""
        return None


def test_system_library_identification():
    """Test system library identification (kernel32.dll, user32.dll).

    Requirements: 2.2, 2.3
    """
    analyzer = LibraryAnalyzer()

    # Create PE with system libraries
    entries = [
        MockEntry("kernel32.dll", ["CreateFileA", "ReadFile", "WriteFile"]),
        MockEntry("user32.dll", ["MessageBoxA", "CreateWindowExA"]),
    ]
    pe = MockPE(entries)

    # Analyze libraries
    result = analyzer.analyze_libraries(pe)

    # All should be categorized as system libraries
    assert len(result.system_libraries) == 2
    assert len(result.external_libraries) == 0

    # Check specific libraries
    system_names = {lib.name for lib in result.system_libraries}
    assert "kernel32.dll" in system_names
    assert "user32.dll" in system_names

    # Check categories
    for lib in result.system_libraries:
        assert lib.category == LibraryCategory.SYSTEM


def test_runtime_library_identification():
    """Test runtime library identification (msvcrt.dll, vcruntime140.dll).

    Requirements: 2.2, 2.3
    """
    analyzer = LibraryAnalyzer()

    # Create PE with runtime libraries
    entries = [
        MockEntry("msvcrt.dll", ["malloc", "free", "printf"]),
        MockEntry("vcruntime140.dll", ["memcpy", "memset"]),
        MockEntry("msvcp140.dll", ["std::cout"]),
    ]
    pe = MockPE(entries)

    # Analyze libraries
    result = analyzer.analyze_libraries(pe)

    # All should be categorized as system libraries (runtime is a subcategory)
    assert len(result.system_libraries) == 3
    assert len(result.external_libraries) == 0

    # Check categories - runtime libraries should have RUNTIME category
    for lib in result.system_libraries:
        assert lib.category == LibraryCategory.RUNTIME


def test_external_library_identification():
    """Test external library identification.

    Requirements: 2.2, 2.3
    """
    analyzer = LibraryAnalyzer()

    # Create PE with external libraries
    entries = [
        MockEntry("custom.dll", ["CustomFunction1", "CustomFunction2"]),
        MockEntry("thirdparty.dll", ["ThirdPartyAPI"]),
        MockEntry("mylib.dll", ["MyFunction"]),
    ]
    pe = MockPE(entries)

    # Analyze libraries
    result = analyzer.analyze_libraries(pe)

    # All should be categorized as external libraries
    assert len(result.system_libraries) == 0
    assert len(result.external_libraries) == 3

    # Check specific libraries
    external_names = {lib.name for lib in result.external_libraries}
    assert "custom.dll" in external_names
    assert "thirdparty.dll" in external_names
    assert "mylib.dll" in external_names

    # Check categories
    for lib in result.external_libraries:
        assert lib.category == LibraryCategory.EXTERNAL


def test_mixed_library_categorization():
    """Test mixed system, runtime, and external libraries.

    Requirements: 2.2, 2.3
    """
    analyzer = LibraryAnalyzer()

    # Create PE with mixed libraries
    entries = [
        MockEntry("kernel32.dll", ["CreateFileA"]),
        MockEntry("msvcrt.dll", ["malloc"]),
        MockEntry("custom.dll", ["CustomFunction"]),
    ]
    pe = MockPE(entries)

    # Analyze libraries
    result = analyzer.analyze_libraries(pe)

    # Should have both system and external libraries
    assert len(result.system_libraries) == 2  # kernel32 + msvcrt
    assert len(result.external_libraries) == 1  # custom

    # Check system libraries
    system_names = {lib.name for lib in result.system_libraries}
    assert "kernel32.dll" in system_names
    assert "msvcrt.dll" in system_names

    # Check external libraries
    external_names = {lib.name for lib in result.external_libraries}
    assert "custom.dll" in external_names


def test_error_handling_with_corrupted_import_table():
    """Test error handling with corrupted import table.

    Requirements: 2.5
    """
    analyzer = LibraryAnalyzer()

    # Create PE without import table
    pe = MockPE([])

    # Should handle gracefully and return empty results
    result = analyzer.analyze_libraries(pe)

    assert len(result.system_libraries) == 0
    assert len(result.external_libraries) == 0
    assert result.total_imports == 0


def test_function_name_extraction():
    """Test that function names are extracted from import table.

    Requirements: 2.4
    """
    analyzer = LibraryAnalyzer()

    # Create PE with specific functions
    entries = [
        MockEntry(
            "kernel32.dll",
            ["CreateFileA", "ReadFile", "WriteFile", "CloseHandle"],
        ),
    ]
    pe = MockPE(entries)

    # Analyze libraries
    result = analyzer.analyze_libraries(pe)

    # Find kernel32.dll
    kernel32 = None
    for lib in result.system_libraries:
        if lib.name == "kernel32.dll":
            kernel32 = lib
            break

    assert kernel32 is not None
    assert len(kernel32.functions) == 4
    assert "CreateFileA" in kernel32.functions
    assert "ReadFile" in kernel32.functions
    assert "WriteFile" in kernel32.functions
    assert "CloseHandle" in kernel32.functions


def test_ordinal_imports():
    """Test handling of imports by ordinal.

    Requirements: 2.4
    """
    analyzer = LibraryAnalyzer()

    # Create PE with ordinal imports
    class MockOrdinalEntry:
        def __init__(self, dll_name):
            self.dll = dll_name.encode("utf-8")
            self.imports = [
                MockImport(None, ordinal=1),
                MockImport(None, ordinal=42),
                MockImport("NamedFunction", ordinal=None),
            ]

    entries = [MockOrdinalEntry("custom.dll")]
    pe = MockPE(entries)

    # Analyze libraries
    result = analyzer.analyze_libraries(pe)

    # Find custom.dll
    custom = result.external_libraries[0]
    assert custom.name == "custom.dll"

    # Should have ordinal imports formatted as "Ordinal_N"
    assert "Ordinal_1" in custom.functions
    assert "Ordinal_42" in custom.functions
    assert "NamedFunction" in custom.functions


def test_case_insensitive_categorization():
    """Test that library categorization is case-insensitive.

    Requirements: 2.2, 2.3
    """
    analyzer = LibraryAnalyzer()

    # Create PE with different case variations
    entries = [
        MockEntry("KERNEL32.DLL", ["CreateFileA"]),
        MockEntry("Kernel32.dll", ["ReadFile"]),
        MockEntry("kernel32.DLL", ["WriteFile"]),
    ]
    pe = MockPE(entries)

    # Analyze libraries
    result = analyzer.analyze_libraries(pe)

    # All should be recognized as system libraries despite case differences
    assert len(result.system_libraries) == 3
    assert len(result.external_libraries) == 0

    for lib in result.system_libraries:
        assert lib.category == LibraryCategory.SYSTEM
