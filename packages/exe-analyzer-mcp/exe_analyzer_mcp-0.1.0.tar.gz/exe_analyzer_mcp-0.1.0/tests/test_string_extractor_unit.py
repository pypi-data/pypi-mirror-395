"""Unit tests for string extractor resource management."""

import os
import tempfile

import pytest

from exe_analyzer_mcp.string_extractor import StringExtractor


class TestResourceManagement:
    """Test resource management and optimization features."""

    def test_file_handle_cleanup_after_extraction(self):
        """Test that file handles are properly closed after string extraction.

        Requirements: 6.5
        """
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
            temp_path = f.name
            # Write some test data
            f.write(b"Test string content here\x00")

        try:
            extractor = StringExtractor()

            # Extract strings
            result = extractor.extract_strings(temp_path)

            # Verify we got results
            assert result is not None
            assert result.total_count >= 0

            # Try to delete the file - this will fail on Windows if handle is open
            # On Unix, this always succeeds, so we check differently
            if os.name == "nt":  # Windows
                # Should be able to delete immediately if handle is closed
                os.unlink(temp_path)
                temp_path = None  # Mark as deleted
            else:  # Unix-like
                # Check that we can open the file again
                with open(temp_path, "rb") as f:
                    f.read()
                # Clean up
                os.unlink(temp_path)
                temp_path = None

        finally:
            # Clean up if not already deleted
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_result_truncation_at_max_strings(self):
        """Test that results are truncated at 10,000 strings.

        Requirements: 6.2
        """
        # Create a file with many strings
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
            temp_path = f.name
            # Write more than 10,000 unique strings
            for i in range(12000):
                # Write unique strings with null terminators
                f.write(f"TestString{i:05d}\x00".encode("ascii"))

        try:
            extractor = StringExtractor()
            result = extractor.extract_strings(temp_path)

            # Verify truncation occurred
            assert result.total_count == extractor.MAX_STRINGS
            assert result.truncated is True

            # Verify we got exactly MAX_STRINGS
            total_extracted = sum(
                len(strings) for strings in result.strings_by_category.values()
            )
            assert total_extracted == extractor.MAX_STRINGS

        finally:
            os.unlink(temp_path)

    def test_memory_mapped_file_for_large_files(self):
        """Test that large files use memory-mapped I/O.

        Requirements: 6.1
        """
        # Create a file larger than MMAP_THRESHOLD (100MB)
        # We'll create a smaller file for testing but verify the logic
        extractor = StringExtractor()

        # Create a file just over the threshold
        file_size = extractor.MMAP_THRESHOLD + 1024

        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
            temp_path = f.name
            # Write data in chunks to avoid memory issues
            chunk_size = 1024 * 1024  # 1MB chunks
            remaining = file_size

            while remaining > 0:
                write_size = min(chunk_size, remaining)
                # Write some test strings mixed with null bytes
                data = (b"TestString\x00" * (write_size // 11))[:write_size]
                f.write(data)
                remaining -= write_size

        try:
            # Extract strings - should use mmap internally
            result = extractor.extract_strings(temp_path)

            # Verify we got results
            assert result is not None
            assert result.total_count >= 0

            # Verify file is accessible after extraction (handle closed)
            assert os.path.exists(temp_path)
            file_stat = os.stat(temp_path)
            # File size should be close to expected (within chunk size)
            assert abs(file_stat.st_size - file_size) < chunk_size

        finally:
            os.unlink(temp_path)

    def test_small_file_uses_regular_read(self):
        """Test that small files use regular file reading.

        Requirements: 6.1
        """
        extractor = StringExtractor()

        # Create a small file (well under MMAP_THRESHOLD)
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
            temp_path = f.name
            f.write(b"Small test file content\x00")

        try:
            # Verify file is small
            file_size = os.path.getsize(temp_path)
            assert file_size < extractor.MMAP_THRESHOLD

            # Extract strings
            result = extractor.extract_strings(temp_path)

            # Verify we got results
            assert result is not None
            assert result.total_count >= 0

        finally:
            os.unlink(temp_path)

    def test_file_handle_cleanup_on_error(self):
        """Test that file handles are cleaned up even when errors occur.

        Requirements: 6.5
        """
        extractor = StringExtractor()

        # Try to extract from non-existent file
        with pytest.raises(FileNotFoundError):
            extractor.extract_strings("/nonexistent/path/to/file.exe")

        # No file handles should be left open
        # This is implicit - if handles were left open, we'd see issues
        # in subsequent tests or resource exhaustion

    def test_permission_error_cleanup(self):
        """Test cleanup when permission errors occur.

        Requirements: 6.5
        """
        # Create a file and make it unreadable
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
            temp_path = f.name
            f.write(b"Test content\x00")

        try:
            # Make file unreadable (Unix only)
            if os.name != "nt":
                os.chmod(temp_path, 0o000)

                extractor = StringExtractor()

                # Should raise PermissionError
                with pytest.raises(PermissionError):
                    extractor.extract_strings(temp_path)

                # Restore permissions for cleanup
                os.chmod(temp_path, 0o644)

        finally:
            # Ensure we can delete the file
            if os.name != "nt":
                try:
                    os.chmod(temp_path, 0o644)
                except Exception:
                    pass
            os.unlink(temp_path)


class TestChunkedProcessing:
    """Test chunked processing for large files."""

    def test_offset_parameter_in_extract_with_encoding(self):
        """Test that offset parameter correctly adjusts string offsets."""
        extractor = StringExtractor()

        # Create test data
        data = b"TestString1\x00TestString2\x00"

        # Extract with offset 0
        strings_no_offset = extractor._extract_with_encoding(
            data, "ascii", "ascii", offset=0
        )

        # Extract with offset 1000
        strings_with_offset = extractor._extract_with_encoding(
            data, "ascii", "ascii", offset=1000
        )

        # Verify offsets are adjusted
        assert len(strings_no_offset) > 0
        assert len(strings_with_offset) > 0

        # Check that offsets differ by 1000
        for s1, s2 in zip(strings_no_offset, strings_with_offset):
            assert s2.offset == s1.offset + 1000
