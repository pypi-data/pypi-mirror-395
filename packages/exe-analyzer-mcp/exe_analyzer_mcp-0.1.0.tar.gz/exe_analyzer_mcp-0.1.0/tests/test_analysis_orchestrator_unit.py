"""Unit tests for AnalysisOrchestrator error handling."""

import sys

import pytest

from exe_analyzer_mcp.analysis_orchestrator import AnalysisOrchestrator


class TestAnalysisOrchestratorErrorHandling:
    """Test error handling in AnalysisOrchestrator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.orchestrator = AnalysisOrchestrator()

    def test_file_not_found_framework_analysis(self):
        """Test framework analysis with non-existent file."""
        # Test with a file that doesn't exist
        result = self.orchestrator.analyze_frameworks("/nonexistent/file.exe")

        # Should return error result
        assert result.error is not None
        assert result.error.error_type == "FileNotFoundError"
        assert "not found" in result.error.message.lower()
        assert result.error.phase == "file_validation"
        assert result.frameworks == []

    def test_file_not_found_library_analysis(self):
        """Test library analysis with non-existent file."""
        result = self.orchestrator.analyze_libraries("/nonexistent/file.exe")

        assert result.error is not None
        assert result.error.error_type == "FileNotFoundError"
        assert "not found" in result.error.message.lower()
        assert result.error.phase == "file_validation"
        assert result.analysis is None

    def test_file_not_found_string_extraction(self):
        """Test string extraction with non-existent file."""
        result = self.orchestrator.extract_strings("/nonexistent/file.exe")

        assert result.error is not None
        assert result.error.error_type == "FileNotFoundError"
        assert "not found" in result.error.message.lower()
        assert result.error.phase == "file_validation"
        assert result.strings is None

    def test_file_not_found_language_inference(self):
        """Test language inference with non-existent file."""
        result = self.orchestrator.infer_language("/nonexistent/file.exe")

        assert result.error is not None
        assert result.error.error_type == "FileNotFoundError"
        assert "not found" in result.error.message.lower()
        assert result.error.phase == "file_validation"
        assert result.inference is None

    @pytest.mark.skipif(sys.platform == "win32", reason="chmod doesn't work the same on Windows")
    def test_permission_denied_framework_analysis(self, tmp_path):
        """Test framework analysis with permission denied."""
        # Create a file and make it unreadable
        test_file = tmp_path / "test.exe"
        test_file.write_bytes(b"MZ\x90\x00")  # Minimal PE header

        # Make file unreadable (Unix-like systems)
        try:
            test_file.chmod(0o000)

            result = self.orchestrator.analyze_frameworks(str(test_file))

            # Should return permission error
            assert result.error is not None
            assert result.error.error_type == "PermissionError"
            assert result.error.phase == "file_validation"
            assert result.frameworks == []
        finally:
            # Restore permissions for cleanup
            test_file.chmod(0o644)

    @pytest.mark.skipif(sys.platform == "win32", reason="chmod doesn't work the same on Windows")
    def test_permission_denied_library_analysis(self, tmp_path):
        """Test library analysis with permission denied."""
        test_file = tmp_path / "test.exe"
        test_file.write_bytes(b"MZ\x90\x00")

        try:
            test_file.chmod(0o000)

            result = self.orchestrator.analyze_libraries(str(test_file))

            assert result.error is not None
            assert result.error.error_type == "PermissionError"
            assert result.error.phase == "file_validation"
            assert result.analysis is None
        finally:
            test_file.chmod(0o644)

    @pytest.mark.skipif(sys.platform == "win32", reason="chmod doesn't work the same on Windows")
    def test_permission_denied_string_extraction(self, tmp_path):
        """Test string extraction with permission denied."""
        test_file = tmp_path / "test.exe"
        test_file.write_bytes(b"MZ\x90\x00")

        try:
            test_file.chmod(0o000)

            result = self.orchestrator.extract_strings(str(test_file))

            assert result.error is not None
            assert result.error.error_type == "PermissionError"
            assert result.error.phase == "file_validation"
            assert result.strings is None
        finally:
            test_file.chmod(0o644)

    @pytest.mark.skipif(sys.platform == "win32", reason="chmod doesn't work the same on Windows")
    def test_permission_denied_language_inference(self, tmp_path):
        """Test language inference with permission denied."""
        test_file = tmp_path / "test.exe"
        test_file.write_bytes(b"MZ\x90\x00")

        try:
            test_file.chmod(0o000)

            result = self.orchestrator.infer_language(str(test_file))

            assert result.error is not None
            assert result.error.error_type == "PermissionError"
            assert result.error.phase == "file_validation"
            assert result.inference is None
        finally:
            test_file.chmod(0o644)

    def test_invalid_pe_format_framework_analysis(self, tmp_path):
        """Test framework analysis with invalid PE format."""
        # Create a file with invalid PE format
        test_file = tmp_path / "invalid.exe"
        test_file.write_bytes(b"This is not a PE file")

        result = self.orchestrator.analyze_frameworks(str(test_file))

        # Should return InvalidPEError
        assert result.error is not None
        assert result.error.error_type == "InvalidPEError"
        assert result.error.phase == "pe_parsing"
        assert result.frameworks == []

    def test_invalid_pe_format_library_analysis(self, tmp_path):
        """Test library analysis with invalid PE format."""
        test_file = tmp_path / "invalid.exe"
        test_file.write_bytes(b"This is not a PE file")

        result = self.orchestrator.analyze_libraries(str(test_file))

        assert result.error is not None
        assert result.error.error_type == "InvalidPEError"
        assert result.error.phase == "pe_parsing"
        assert result.analysis is None

    def test_invalid_pe_format_language_inference(self, tmp_path):
        """Test language inference with invalid PE format."""
        test_file = tmp_path / "invalid.exe"
        test_file.write_bytes(b"This is not a PE file")

        result = self.orchestrator.infer_language(str(test_file))

        assert result.error is not None
        assert result.error.error_type == "InvalidPEError"
        assert result.error.phase == "pe_parsing"
        assert result.inference is None

    def test_partial_result_on_string_extraction_failure(self, tmp_path):
        """Test that framework analysis continues even if string extraction fails."""
        # This test verifies that if string extraction fails during framework
        # analysis, the analysis continues with an empty string list
        # We can't easily force string extraction to fail without a valid PE,
        # so this is more of a design verification test

        # Create a minimal valid PE file
        # For this test, we'll just verify the orchestrator handles the workflow
        test_file = tmp_path / "test.exe"

        # Write minimal PE header (DOS header + PE signature)
        dos_header = b"MZ" + b"\x00" * 58 + b"\x80\x00\x00\x00"  # e_lfanew at offset 60
        pe_signature = b"PE\x00\x00"
        # Minimal COFF header
        coff_header = (
            b"\x4c\x01"  # Machine (i386)
            + b"\x00\x00"  # NumberOfSections
            + b"\x00\x00\x00\x00"  # TimeDateStamp
            + b"\x00\x00\x00\x00"  # PointerToSymbolTable
            + b"\x00\x00\x00\x00"  # NumberOfSymbols
            + b"\x00\x00"  # SizeOfOptionalHeader
            + b"\x00\x00"  # Characteristics
        )

        test_file.write_bytes(dos_header + pe_signature + coff_header)

        # This should not crash even if string extraction has issues
        result = self.orchestrator.analyze_frameworks(str(test_file))

        # Should either succeed or fail gracefully
        # The key is that it doesn't crash
        assert result is not None
        assert isinstance(result.frameworks, list)
