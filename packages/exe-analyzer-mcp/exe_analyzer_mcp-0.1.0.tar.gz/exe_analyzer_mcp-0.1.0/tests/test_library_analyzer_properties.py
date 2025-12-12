"""Property-based tests for library analyzer."""

from hypothesis import given, settings
from hypothesis import strategies as st

from exe_analyzer_mcp.library_analyzer import (
    Library,
    LibraryAnalyzer,
    LibraryCategory,
)


# Custom strategies for generating test data
@st.composite
def pe_with_imports(draw):
    """Generate a mock PE object with import table."""
    num_dlls = draw(st.integers(min_value=1, max_value=10))

    # Mix of system, runtime, and external libraries
    system_dlls = [
        "kernel32.dll",
        "user32.dll",
        "gdi32.dll",
        "advapi32.dll",
        "shell32.dll",
    ]
    runtime_dlls = [
        "msvcrt.dll",
        "vcruntime140.dll",
        "msvcp140.dll",
        "ucrtbase.dll",
    ]
    external_dlls = [
        "custom.dll",
        "thirdparty.dll",
        "mylib.dll",
        "external.dll",
    ]

    class MockImport:
        def __init__(self, name, ordinal=None):
            self.name = name.encode("utf-8") if name else None
            self.ordinal = ordinal

    class MockEntry:
        def __init__(self, dll_name, functions):
            self.dll = dll_name.encode("utf-8")
            self.imports = [MockImport(func) for func in functions]

    class MockPE:
        def __init__(self, entries):
            self.DIRECTORY_ENTRY_IMPORT = entries

        def parse_data_directories(self, directories):
            pass

    # Generate random mix of DLLs
    entries = []
    for _ in range(num_dlls):
        dll_type = draw(st.sampled_from(["system", "runtime", "external"]))
        if dll_type == "system":
            dll_name = draw(st.sampled_from(system_dlls))
        elif dll_type == "runtime":
            dll_name = draw(st.sampled_from(runtime_dlls))
        else:
            dll_name = draw(st.sampled_from(external_dlls))

        # Generate some function names
        num_functions = draw(st.integers(min_value=1, max_value=5))
        functions = [f"Function{i}" for i in range(num_functions)]

        entries.append(MockEntry(dll_name, functions))

    return MockPE(entries)


# Feature: exe-analyzer-mcp, Property 4: Import table parsing extracts
# DLL names
@settings(max_examples=100)
@given(pe=pe_with_imports())
def test_import_table_parsing_extracts_dll_names(pe):
    """Property: For any valid PE file with a non-empty import table,
    parsing should extract at least one DLL name.

    Validates: Requirements 2.1
    """
    analyzer = LibraryAnalyzer()

    # Analyze libraries
    result = analyzer.analyze_libraries(pe)

    # Property: At least one DLL should be extracted
    total_libraries = len(result.system_libraries) + len(result.external_libraries)
    assert total_libraries > 0, "Should extract at least one DLL"

    # Property: total_imports should match the number of unique DLLs
    assert result.total_imports > 0, "total_imports should be positive"
    assert (
        result.total_imports == total_libraries
    ), "total_imports should match library count"


# Feature: exe-analyzer-mcp, Property 5: Library categorization is
# complete and exclusive
@settings(max_examples=100)
@given(pe=pe_with_imports())
def test_library_categorization_complete_and_exclusive(pe):
    """Property: For any extracted library name, it should be categorized
    as exactly one of: system, runtime, or external.

    Validates: Requirements 2.2, 2.3
    """
    analyzer = LibraryAnalyzer()

    # Analyze libraries
    result = analyzer.analyze_libraries(pe)

    # Collect all libraries
    all_libraries = result.system_libraries + result.external_libraries

    # Property: Every library must have exactly one category
    for library in all_libraries:
        assert isinstance(library, Library)
        assert isinstance(library.category, LibraryCategory)

        # Category must be one of the valid enum values
        assert library.category in [
            LibraryCategory.SYSTEM,
            LibraryCategory.RUNTIME,
            LibraryCategory.EXTERNAL,
        ]

    # Property: No library should appear in multiple categories
    # (this is enforced by the data structure, but we verify)
    system_names = {lib.name for lib in result.system_libraries}
    external_names = {lib.name for lib in result.external_libraries}

    # No overlap between system and external
    overlap = system_names & external_names
    assert len(overlap) == 0, f"Libraries in multiple categories: {overlap}"


# Feature: exe-analyzer-mcp, Property 6: Library results include
# required fields
@settings(max_examples=100)
@given(pe=pe_with_imports())
def test_library_results_include_required_fields(pe):
    """Property: For any library in the analysis result, it should have
    both a name field and a category field populated.

    Validates: Requirements 2.4
    """
    analyzer = LibraryAnalyzer()

    # Analyze libraries
    result = analyzer.analyze_libraries(pe)

    # Collect all libraries
    all_libraries = result.system_libraries + result.external_libraries

    # Property: Every library must have required fields
    for library in all_libraries:
        # Must have a name field that is a non-empty string
        assert isinstance(library.name, str)
        assert len(library.name) > 0, "Library name must not be empty"

        # Must have a category field
        assert isinstance(library.category, LibraryCategory)

        # Must have a functions list (can be empty)
        assert isinstance(library.functions, list)

        # All function names must be strings
        for func in library.functions:
            assert isinstance(func, str)
            assert len(func) > 0, "Function name must not be empty"
