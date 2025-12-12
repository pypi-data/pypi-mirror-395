"""Unit tests for language inferrer."""

from exe_analyzer_mcp.language_inferrer import LanguageInferrer


class MockPE:
    """Mock PE object for testing."""

    def __init__(self, has_clr=False):
        self.has_clr = has_clr
        if has_clr:
            self.DIRECTORY_ENTRY_COM_DESCRIPTOR = True

    def parse_data_directories(self, directories):
        """Mock parse_data_directories method."""
        return None


def test_csharp_executable_detection():
    """Test C# executable detection with CLR header and C# signatures.

    Requirements: 4.2, 4.3, 4.4
    """  # noqa: D401
    inferrer = LanguageInferrer()

    # Create mock PE with CLR header
    mock_pe = MockPE(has_clr=True)

    # Provide C# specific strings
    strings = [
        "csc.exe",
        "Microsoft (R) Visual C# Compiler",
        "System.Runtime.CompilerServices",
        "Roslyn",
    ]

    result = inferrer.infer_language(mock_pe, strings)

    # Should detect C# as primary language
    assert result.primary_language.language == "C#"
    # High confidence with CLR
    assert result.primary_language.confidence >= 0.7
    assert len(result.primary_language.indicators) > 0


def test_vbnet_executable_detection():
    """Test VB.NET executable detection.

    Requirements: 4.2, 4.3, 4.4
    """
    inferrer = LanguageInferrer()

    # Create mock PE with CLR header
    mock_pe = MockPE(has_clr=True)

    # Provide VB.NET specific strings
    strings = [
        "vbc.exe",
        "Microsoft (R) Visual Basic Compiler",
        "Microsoft.VisualBasic",
    ]

    result = inferrer.infer_language(mock_pe, strings)

    # Should detect VB.NET as primary language
    assert result.primary_language.language == "VB.NET"
    assert result.primary_language.confidence >= 0.7


def test_cpp_executable_detection():
    """Test C++ executable detection with MSVC signatures.

    Requirements: 4.2, 4.3, 4.4
    """
    inferrer = LanguageInferrer()

    # Create mock PE without CLR header
    mock_pe = MockPE(has_clr=False)

    # Provide C++ specific strings
    strings = [
        "Microsoft (R) C/C++ Optimizing Compiler",
        "vcruntime140.dll",
        "msvcp140.dll",
        "MSVC",
    ]

    result = inferrer.infer_language(mock_pe, strings)

    # Should detect C++ as primary language
    assert result.primary_language.language == "C++"
    assert result.primary_language.confidence > 0.0
    assert len(result.primary_language.indicators) > 0


def test_cpp_with_gcc_detection():
    """Test C++ executable detection with GCC signatures.

    Requirements: 4.2
    """
    inferrer = LanguageInferrer()
    mock_pe = MockPE(has_clr=False)

    strings = [
        "GCC: (GNU) 11.2.0",
        "libstdc++",
        "g++ compiler",
    ]

    result = inferrer.infer_language(mock_pe, strings)

    # Should detect C++ or C
    assert result.primary_language.language in ["C++", "C"]
    assert result.primary_language.confidence > 0.0


def test_go_executable_detection():
    """Test Go executable detection.

    Requirements: 4.2, 4.3, 4.4
    """
    inferrer = LanguageInferrer()
    mock_pe = MockPE(has_clr=False)

    # Provide Go specific strings
    strings = [
        "Go build ID: abc123",
        "runtime.go",
        "runtime.main",
        "type..runtime.g",
    ]

    result = inferrer.infer_language(mock_pe, strings)

    # Should detect Go as primary language
    assert result.primary_language.language == "Go"
    assert result.primary_language.confidence > 0.0
    assert len(result.primary_language.indicators) > 0


def test_rust_executable_detection():
    """Test Rust executable detection.

    Requirements: 4.2
    """
    inferrer = LanguageInferrer()
    mock_pe = MockPE(has_clr=False)

    strings = [
        "rustc 1.70.0",
        "rust_panic",
        "rust_begin_unwind",
        "cargo",
    ]

    result = inferrer.infer_language(mock_pe, strings)

    # Should detect Rust as primary language
    assert result.primary_language.language == "Rust"
    assert result.primary_language.confidence > 0.0


def test_delphi_executable_detection():
    """Test Delphi executable detection.

    Requirements: 4.2
    """
    inferrer = LanguageInferrer()
    mock_pe = MockPE(has_clr=False)

    strings = [
        "Borland Delphi",
        "Embarcadero",
        "@System@@",
        "TObject",
    ]

    result = inferrer.infer_language(mock_pe, strings)

    # Should detect Delphi as primary language
    assert result.primary_language.language == "Delphi"
    assert result.primary_language.confidence > 0.0


def test_visual_basic_6_detection():
    """Test Visual Basic 6 executable detection.

    Requirements: 4.2
    """
    inferrer = LanguageInferrer()
    mock_pe = MockPE(has_clr=False)

    strings = [
        "msvbvm60.dll",
        "VB6",
        "ThunRTMain",
    ]

    result = inferrer.infer_language(mock_pe, strings)

    # Should detect Visual Basic 6 as primary language
    assert result.primary_language.language == "Visual Basic 6"
    assert result.primary_language.confidence > 0.0


def test_python_executable_detection():
    """Test Python executable detection (e.g., PyInstaller).

    Requirements: 4.2
    """
    inferrer = LanguageInferrer()
    mock_pe = MockPE(has_clr=False)

    strings = [
        "python310.dll",
        "PyInstaller",
        "python3",
    ]

    result = inferrer.infer_language(mock_pe, strings)

    # Should detect Python as primary language
    assert result.primary_language.language == "Python"
    assert result.primary_language.confidence > 0.0


def test_multi_language_indicator_handling():
    """Test handling of executables with multiple language indicators.

    Requirements: 4.2, 4.3, 4.4
    """
    inferrer = LanguageInferrer()
    mock_pe = MockPE(has_clr=False)

    # Provide signatures for multiple languages
    strings = [
        "vcruntime140.dll",  # C++
        "python310.dll",  # Python
        "Go build ID:",  # Go
    ]

    result = inferrer.infer_language(mock_pe, strings)

    # Should detect a primary language
    assert result.primary_language.language in ["C++", "Python", "Go"]
    assert result.primary_language.confidence > 0.0

    # May have alternative languages
    all_languages = [result.primary_language.language]
    all_languages.extend([lang.language for lang in result.alternative_languages])

    # At least one of the languages should be detected
    assert len(set(all_languages) & {"C++", "Python", "Go"}) >= 1


def test_unknown_language_when_no_signatures():
    """Test that Unknown is returned when no language signatures are found.

    Requirements: 4.4
    """
    inferrer = LanguageInferrer()
    mock_pe = MockPE(has_clr=False)

    # Provide strings with no language signatures
    strings = [
        "Hello World",
        "Some random text",
        "C:\\Windows\\System32\\kernel32.dll",
    ]

    result = inferrer.infer_language(mock_pe, strings)

    # Should return Unknown
    assert result.primary_language.language == "Unknown"
    assert result.primary_language.confidence == 0.0
    assert len(result.alternative_languages) == 0


def test_confidence_scores_are_valid():
    """Test that confidence scores are always between 0.0 and 1.0.

    Requirements: 4.4, 4.5
    """
    inferrer = LanguageInferrer()
    mock_pe = MockPE(has_clr=False)

    strings = [
        "vcruntime140.dll",
        "msvcp140.dll",
    ]

    result = inferrer.infer_language(mock_pe, strings)

    # Primary language confidence should be valid
    assert 0.0 <= result.primary_language.confidence <= 1.0

    # All alternative language confidences should be valid
    for alt_lang in result.alternative_languages:
        assert 0.0 <= alt_lang.confidence <= 1.0


def test_clr_without_dotnet_signatures():
    """Test CLR header detection without specific .NET signatures.

    Requirements: 4.3
    """
    inferrer = LanguageInferrer()

    # Create mock PE with CLR header but minimal strings
    mock_pe = MockPE(has_clr=True)

    strings = [
        "System.Runtime.CompilerServices",  # Generic .NET string
    ]

    result = inferrer.infer_language(mock_pe, strings)

    # Should still detect a .NET language
    assert result.primary_language.language in ["C#", "VB.NET"]
    assert result.primary_language.confidence >= 0.7
