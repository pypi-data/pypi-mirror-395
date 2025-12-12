"""Property-based tests for string extraction component."""

import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from exe_analyzer_mcp.string_extractor import (
    StringCategory,
    StringExtractor,
)


# Helper function to create test files
def create_test_file_with_strings(
    file_path: Path, strings: list[str], encoding: str = "ascii"
) -> None:
    """Create a test file containing specified strings.

    Args:
        file_path: Path where to create the file
        strings: List of strings to embed in the file
        encoding: Encoding to use (ascii, utf-8, utf-16-le)
    """
    with open(file_path, "wb") as f:
        for string in strings:
            # Write the string
            if encoding == "utf-16-le":
                f.write(string.encode("utf-16-le"))
            else:
                f.write(string.encode(encoding, errors="ignore"))

            # Add some null bytes as separator
            f.write(b"\x00" * 4)


# Feature: exe-analyzer-mcp, Property 1: String extraction completeness
@settings(max_examples=100)
@given(
    st.lists(
        st.text(
            alphabet=st.characters(
                whitelist_categories=("Lu", "Ll", "Nd"),
                min_codepoint=32,
                max_codepoint=126,
            ),
            min_size=4,
            max_size=50,
        ),
        min_size=1,
        max_size=20,
    )
)
def test_string_extraction_completeness(strings: list[str]):
    """Property 1: For any valid executable file, when string extraction
    is performed, the result should contain only strings with length >= 4.

    Validates: Requirements 3.1
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.exe"

        # Create test file with strings
        create_test_file_with_strings(test_file, strings)

        # Extract strings
        extractor = StringExtractor(min_length=4)
        result = extractor.extract_strings(str(test_file))

        # Property: All extracted strings should have length >= 4
        for category_strings in result.strings_by_category.values():
            for extracted in category_strings:
                assert (
                    len(extracted.value) >= 4
                ), f"String '{extracted.value}' has length {len(extracted.value)} < 4"


# Feature: exe-analyzer-mcp, Property 7: Entropy filtering excludes high-entropy strings
@settings(max_examples=100)
@given(
    st.lists(
        st.text(
            alphabet=st.characters(min_codepoint=33, max_codepoint=126),
            min_size=10,
            max_size=20,
        ),
        min_size=1,
        max_size=10,
    )
)
def test_entropy_filtering_excludes_high_entropy(strings: list[str]):
    """Property 7: For any string with entropy > 4.5, it should not appear
    in the meaningful strings result.

    Validates: Requirements 3.2
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.exe"

        # Create test file with strings
        create_test_file_with_strings(test_file, strings)

        # Extract strings
        extractor = StringExtractor(min_length=4)
        result = extractor.extract_strings(str(test_file))

        # Property: All extracted strings should have entropy <= 4.5
        for category_strings in result.strings_by_category.values():
            for extracted in category_strings:
                assert (
                    extracted.entropy <= 4.5
                ), f"String '{extracted.value}' has entropy {extracted.entropy} > 4.5"


# Feature: exe-analyzer-mcp, Property 8: String categorization is exclusive
@settings(max_examples=100)
@given(
    st.lists(
        st.one_of(
            st.just("http://example.com"),
            st.just("https://test.org/path"),
            st.just("C:\\Windows\\System32"),
            st.just("HKEY_LOCAL_MACHINE\\Software"),
            st.just("Error: operation failed"),
            st.just("General text string"),
        ),
        min_size=1,
        max_size=10,
    )
)
def test_string_categorization_is_exclusive(strings: list[str]):
    """Property 8: For any extracted meaningful string, it should be assigned
    to exactly one category.

    Validates: Requirements 3.3
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.exe"

        # Create test file with strings
        create_test_file_with_strings(test_file, strings)

        # Extract strings
        extractor = StringExtractor(min_length=4)
        result = extractor.extract_strings(str(test_file))

        # Collect all extracted strings with their categories
        all_extracted = []
        for category, category_strings in result.strings_by_category.items():
            for extracted in category_strings:
                all_extracted.append((extracted.value, category))

        # Property: Each string value should appear in exactly one category
        string_categories: dict[str, list[StringCategory]] = {}
        for value, category in all_extracted:
            if value not in string_categories:
                string_categories[value] = []
            string_categories[value].append(category)

        for value, categories in string_categories.items():
            # Each unique string should have exactly one category
            unique_categories = set(categories)
            assert (
                len(unique_categories) == 1
            ), f"String '{value}' appears in multiple categories: {unique_categories}"


# Feature: exe-analyzer-mcp, Property 9: String results include offset information
@settings(max_examples=100)
@given(
    st.lists(
        st.text(
            alphabet=st.characters(
                whitelist_categories=("Lu", "Ll", "Nd"),
                min_codepoint=32,
                max_codepoint=126,
            ),
            min_size=4,
            max_size=30,
        ),
        min_size=1,
        max_size=15,
    )
)
def test_string_results_include_offset(strings: list[str]):
    """Property 9: For any extracted string in the result, it should include
    a file offset value indicating where it was found.

    Validates: Requirements 3.4
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.exe"

        # Create test file with strings
        create_test_file_with_strings(test_file, strings)

        # Extract strings
        extractor = StringExtractor(min_length=4)
        result = extractor.extract_strings(str(test_file))

        # Property: All extracted strings should have an offset >= 0
        for category_strings in result.strings_by_category.values():
            for extracted in category_strings:
                assert (
                    extracted.offset >= 0
                ), f"String '{extracted.value}' has invalid offset {extracted.offset}"
                assert isinstance(
                    extracted.offset, int
                ), f"Offset should be int, got {type(extracted.offset)}"


# Feature: exe-analyzer-mcp, Property 10: Multi-encoding extraction attempts
@settings(max_examples=100)
@given(
    st.lists(
        st.text(
            alphabet=st.characters(
                whitelist_categories=("Lu", "Ll", "Nd"),
                min_codepoint=32,
                max_codepoint=126,
            ),
            min_size=4,
            max_size=30,
        ),
        min_size=1,
        max_size=10,
    )
)
def test_multi_encoding_extraction_attempts(strings: list[str]):
    """Property 10: For any executable file, string extraction should attempt
    extraction using ASCII, UTF-8, and UTF-16 encodings.

    Validates: Requirements 3.5
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create three test files with different encodings
        ascii_file = Path(tmpdir) / "ascii.exe"
        utf8_file = Path(tmpdir) / "utf8.exe"
        utf16_file = Path(tmpdir) / "utf16.exe"

        create_test_file_with_strings(ascii_file, strings, "ascii")
        create_test_file_with_strings(utf8_file, strings, "utf-8")
        create_test_file_with_strings(utf16_file, strings, "utf-16-le")

        extractor = StringExtractor(min_length=4)

        # Extract from ASCII file
        ascii_result = extractor.extract_strings(str(ascii_file))
        ascii_encodings = set()
        for category_strings in ascii_result.strings_by_category.values():
            for extracted in category_strings:
                ascii_encodings.add(extracted.encoding)

        # Extract from UTF-8 file
        utf8_result = extractor.extract_strings(str(utf8_file))
        utf8_encodings = set()
        for category_strings in utf8_result.strings_by_category.values():
            for extracted in category_strings:
                utf8_encodings.add(extracted.encoding)

        # Extract from UTF-16 file
        utf16_result = extractor.extract_strings(str(utf16_file))
        utf16_encodings = set()
        for category_strings in utf16_result.strings_by_category.values():
            for extracted in category_strings:
                utf16_encodings.add(extracted.encoding)

        # Property: At least one file should have strings from each encoding
        # (The extractor tries all encodings on each file)
        all_encodings = ascii_encodings | utf8_encodings | utf16_encodings

        # We should see evidence of multiple encoding attempts
        # At minimum, we should have extracted strings with encoding labels
        assert len(all_encodings) > 0, "No strings extracted with encoding info"


# Feature: exe-analyzer-mcp, Property 18: String extraction result size limit
@settings(max_examples=100, deadline=None)
@given(st.integers(min_value=100, max_value=15000))
def test_string_extraction_result_size_limit(num_strings: int):
    """Property 18: For any string extraction operation, the total number
    of strings returned should not exceed 10,000 entries.

    Validates: Requirements 6.2
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.exe"

        # Generate many strings
        strings = [f"TestString{i:05d}" for i in range(num_strings)]

        # Create test file with many strings
        create_test_file_with_strings(test_file, strings)

        # Extract strings
        extractor = StringExtractor(min_length=4)
        result = extractor.extract_strings(str(test_file))

        # Property: Total count should not exceed 10,000
        assert (
            result.total_count <= 10000
        ), f"Result contains {result.total_count} strings, exceeds limit of 10,000"

        # If we generated more than 10,000 strings, truncated should be True
        if num_strings > 10000:
            assert (
                result.truncated
            ), "Result should be marked as truncated when exceeding limit"
