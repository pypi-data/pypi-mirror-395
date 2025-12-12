"""Property-based tests for language inferrer."""

from hypothesis import given, settings
from hypothesis import strategies as st

from exe_analyzer_mcp.language_inferrer import (
    LanguageInference,
    LanguageInferrer,
    LanguageResult,
)


# Custom strategies for generating test data
@st.composite
def compiler_signature_strings(draw):
    """Generate strings that contain compiler signatures."""
    compiler_signatures = {
        "C++": ["MSVC", "vcruntime140.dll", "msvcp140.dll", "libstdc++"],
        "C": ["msvcrt.dll", "Microsoft (R) C Compiler"],
        "Go": ["Go build ID:", "runtime.go", "runtime.main"],
        "Rust": ["rustc", "rust_panic", "rust_begin_unwind"],
        "Delphi": ["Borland", "Embarcadero", "@System@@"],
        "Visual Basic 6": ["msvbvm60.dll", "VB6"],
        "Python": ["python3", "python310.dll", "PyInstaller"],
    }

    language = draw(st.sampled_from(list(compiler_signatures.keys())))
    signature = draw(st.sampled_from(compiler_signatures[language]))

    # Generate a list of strings that includes the signature
    num_strings = draw(st.integers(min_value=1, max_value=20))
    strings = [signature]

    for _ in range(num_strings - 1):
        strings.append(draw(st.text(min_size=4, max_size=50)))

    return language, strings


@st.composite
def pe_with_clr(draw):
    """Generate a mock PE object with or without CLR header."""

    class MockPE:
        def __init__(self, has_clr):
            self._has_clr = has_clr
            if has_clr:
                self.DIRECTORY_ENTRY_COM_DESCRIPTOR = True

        def parse_data_directories(self, directories):
            pass

    has_clr = draw(st.booleans())
    return MockPE(has_clr), has_clr


# Feature: exe-analyzer-mcp, Property 12: Compiler signature to language
# mapping
@settings(max_examples=100)
@given(data=compiler_signature_strings())
def test_compiler_signature_to_language_mapping(data):
    """Property: For any known compiler signature found in a PE file,
    the inferred language should match the expected language for that
    compiler.

    Validates: Requirements 4.2
    """
    expected_language, strings = data
    inferrer = LanguageInferrer()

    # Create a mock PE object without CLR (for non-.NET languages)
    class MockPE:
        def parse_data_directories(self, directories):
            pass

    mock_pe = MockPE()

    # Infer language
    result = inferrer.infer_language(mock_pe, strings)

    # Property: The inferred language should match the expected language
    # Either as primary or alternative
    all_languages = [result.primary_language.language]
    all_languages.extend([lang.language for lang in result.alternative_languages])

    assert expected_language in all_languages, (
        f"Expected {expected_language} to be detected, " f"but got {all_languages}"
    )

    # Property: Result should be a valid LanguageInference object
    assert isinstance(result, LanguageInference)
    assert isinstance(result.primary_language, LanguageResult)


# Feature: exe-analyzer-mcp, Property 13: .NET CLR detection
@settings(max_examples=100)
@given(
    clr_strings=st.lists(
        st.sampled_from(
            [
                "csc.exe",
                "Microsoft (R) Visual C# Compiler",
                "vbc.exe",
                "Microsoft.VisualBasic",
                "System.Runtime.CompilerServices",
            ]
        ),
        min_size=1,
        max_size=5,
    )
)
def test_dotnet_clr_detection(clr_strings):
    """Property: For any executable with a CLR header, the language
    inference should identify it as either C# or VB.NET.

    Validates: Requirements 4.3
    """
    inferrer = LanguageInferrer()

    # Create a mock PE object WITH CLR header
    class MockPE:
        def __init__(self):
            self.DIRECTORY_ENTRY_COM_DESCRIPTOR = True

        def parse_data_directories(self, directories):
            pass

    mock_pe = MockPE()

    # Infer language
    result = inferrer.infer_language(mock_pe, clr_strings)

    # Property: Primary language should be C# or VB.NET
    assert result.primary_language.language in ["C#", "VB.NET"], (
        f"Expected C# or VB.NET for CLR executable, "
        f"got {result.primary_language.language}"
    )

    # Property: Confidence should be high for CLR-based detection
    assert result.primary_language.confidence >= 0.7, (
        f"Expected high confidence for CLR detection, "
        f"got {result.primary_language.confidence}"
    )


# Feature: exe-analyzer-mcp, Property 14: Language inference includes
# confidence scores
@settings(max_examples=100)
@given(
    strings=st.lists(
        st.text(min_size=4, max_size=50),
        min_size=1,
        max_size=30,
    )
)
def test_language_inference_includes_confidence_scores(strings):
    """Property: For any language inference result, each language candidate
    should include a confidence score between 0.0 and 1.0.

    Validates: Requirements 4.4, 4.5
    """
    inferrer = LanguageInferrer()

    # Create a mock PE object
    class MockPE:
        def parse_data_directories(self, directories):
            pass

    mock_pe = MockPE()

    # Infer language
    result = inferrer.infer_language(mock_pe, strings)

    # Property: Primary language must have confidence score
    assert isinstance(result.primary_language.confidence, float)
    assert 0.0 <= result.primary_language.confidence <= 1.0, (
        f"Primary language confidence "
        f"{result.primary_language.confidence} not in [0.0, 1.0]"
    )

    # Property: All alternative languages must have confidence scores
    for alt_lang in result.alternative_languages:
        assert isinstance(alt_lang.confidence, float)
        assert 0.0 <= alt_lang.confidence <= 1.0, (
            f"Alternative language confidence "
            f"{alt_lang.confidence} not in [0.0, 1.0]"
        )

    # Property: Primary language should have highest confidence
    for alt_lang in result.alternative_languages:
        assert (
            result.primary_language.confidence >= alt_lang.confidence
        ), "Primary language should have highest confidence"

    # Property: All language results must have indicators list
    assert isinstance(result.primary_language.indicators, list)
    for alt_lang in result.alternative_languages:
        assert isinstance(alt_lang.indicators, list)
