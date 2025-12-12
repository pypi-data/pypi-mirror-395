"""Analysis orchestrator that coordinates all analysis components."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from exe_analyzer_mcp.framework_detector import Framework, FrameworkDetector
from exe_analyzer_mcp.language_inferrer import LanguageInference, LanguageInferrer
from exe_analyzer_mcp.library_analyzer import LibraryAnalysis, LibraryAnalyzer
from exe_analyzer_mcp.pe_parser import InvalidPEError, PEParser
from exe_analyzer_mcp.string_extractor import StringExtractor, StringResult


@dataclass
class AnalysisError:
    """Represents an error that occurred during analysis."""

    error_type: str
    message: str
    phase: str
    partial_results: Optional[Dict[str, Any]] = None


@dataclass
class FrameworkAnalysisResult:
    """Result of framework analysis."""

    frameworks: List[Framework]
    error: Optional[AnalysisError] = None


@dataclass
class LibraryAnalysisResult:
    """Result of library analysis."""

    analysis: Optional[LibraryAnalysis]
    error: Optional[AnalysisError] = None


@dataclass
class StringAnalysisResult:
    """Result of string extraction analysis."""

    strings: Optional[StringResult]
    error: Optional[AnalysisError] = None


@dataclass
class LanguageAnalysisResult:
    """Result of language inference analysis."""

    inference: Optional[LanguageInference]
    error: Optional[AnalysisError] = None


class AnalysisOrchestrator:
    """Coordinates analysis workflows across all components."""

    def __init__(self):
        """Initialize orchestrator with all analysis components."""
        self.framework_detector = FrameworkDetector()
        self.library_analyzer = LibraryAnalyzer()
        self.string_extractor = StringExtractor()
        self.language_inferrer = LanguageInferrer()

    def analyze_frameworks(self, file_path: str) -> FrameworkAnalysisResult:
        """Analyze frameworks used in an executable.

        Args:
            file_path: Path to the executable file

        Returns:
            FrameworkAnalysisResult with detected frameworks or error
        """
        try:
            # Validate file exists and is readable
            self._validate_file(file_path)

            # Parse PE file
            with PEParser(file_path) as parser:
                pe = parser._pe

                # Extract strings for framework detection
                try:
                    string_result = self.string_extractor.extract_strings(file_path)
                    all_strings = []
                    for strings_list in string_result.strings_by_category.values():
                        all_strings.extend([s.value for s in strings_list])
                except Exception:
                    # If string extraction fails, continue with empty list
                    all_strings = []

                # Detect frameworks
                frameworks = self.framework_detector.detect_frameworks(pe, all_strings)

                return FrameworkAnalysisResult(frameworks=frameworks)

        except FileNotFoundError as e:
            return FrameworkAnalysisResult(
                frameworks=[],
                error=AnalysisError(
                    error_type="FileNotFoundError",
                    message=str(e),
                    phase="file_validation",
                ),
            )
        except PermissionError as e:
            return FrameworkAnalysisResult(
                frameworks=[],
                error=AnalysisError(
                    error_type="PermissionError",
                    message=str(e),
                    phase="file_validation",
                ),
            )
        except InvalidPEError as e:
            return FrameworkAnalysisResult(
                frameworks=[],
                error=AnalysisError(
                    error_type="InvalidPEError",
                    message=str(e),
                    phase="pe_parsing",
                ),
            )
        except Exception as exc:
            return FrameworkAnalysisResult(
                frameworks=[],
                error=AnalysisError(
                    error_type="UnknownError",
                    message=(f"Unexpected error during framework analysis: {str(exc)}"),
                    phase="framework_detection",
                ),
            )

    def analyze_libraries(self, file_path: str) -> LibraryAnalysisResult:
        """Analyze libraries imported by an executable.

        Args:
            file_path: Path to the executable file

        Returns:
            LibraryAnalysisResult with library analysis or error
        """
        try:
            # Validate file exists and is readable
            self._validate_file(file_path)

            # Parse PE file
            with PEParser(file_path) as parser:
                pe = parser._pe

                # Analyze libraries
                analysis = self.library_analyzer.analyze_libraries(pe)

                return LibraryAnalysisResult(analysis=analysis)

        except FileNotFoundError as e:
            return LibraryAnalysisResult(
                analysis=None,
                error=AnalysisError(
                    error_type="FileNotFoundError",
                    message=str(e),
                    phase="file_validation",
                ),
            )
        except PermissionError as e:
            return LibraryAnalysisResult(
                analysis=None,
                error=AnalysisError(
                    error_type="PermissionError",
                    message=str(e),
                    phase="file_validation",
                ),
            )
        except InvalidPEError as e:
            return LibraryAnalysisResult(
                analysis=None,
                error=AnalysisError(
                    error_type="InvalidPEError",
                    message=str(e),
                    phase="pe_parsing",
                ),
            )
        except Exception as exc:
            return LibraryAnalysisResult(
                analysis=None,
                error=AnalysisError(
                    error_type="UnknownError",
                    message=(f"Unexpected error during library analysis: {str(exc)}"),
                    phase="library_analysis",
                ),
            )

    def extract_strings(self, file_path: str) -> StringAnalysisResult:
        """Extract meaningful strings from an executable.

        Args:
            file_path: Path to the executable file

        Returns:
            StringAnalysisResult with extracted strings or error
        """
        try:
            # Validate file exists and is readable
            self._validate_file(file_path)

            # Extract strings
            strings = self.string_extractor.extract_strings(file_path)

            return StringAnalysisResult(strings=strings)

        except FileNotFoundError as e:
            return StringAnalysisResult(
                strings=None,
                error=AnalysisError(
                    error_type="FileNotFoundError",
                    message=str(e),
                    phase="file_validation",
                ),
            )
        except PermissionError as e:
            return StringAnalysisResult(
                strings=None,
                error=AnalysisError(
                    error_type="PermissionError",
                    message=str(e),
                    phase="file_validation",
                ),
            )
        except Exception as exc:
            return StringAnalysisResult(
                strings=None,
                error=AnalysisError(
                    error_type="UnknownError",
                    message=(f"Unexpected error during string extraction: {str(exc)}"),
                    phase="string_extraction",
                ),
            )

    def infer_language(self, file_path: str) -> LanguageAnalysisResult:
        """Infer programming language used to create an executable.

        Args:
            file_path: Path to the executable file

        Returns:
            LanguageAnalysisResult with language inference or error
        """
        try:
            # Validate file exists and is readable
            self._validate_file(file_path)

            # Parse PE file
            with PEParser(file_path) as parser:
                pe = parser._pe

                # Extract strings for language inference
                try:
                    string_result = self.string_extractor.extract_strings(file_path)
                    all_strings = []
                    for strings_list in string_result.strings_by_category.values():
                        all_strings.extend([s.value for s in strings_list])
                except Exception:
                    # If string extraction fails, continue with empty list
                    all_strings = []

                # Infer language
                inference = self.language_inferrer.infer_language(pe, all_strings)

                return LanguageAnalysisResult(inference=inference)

        except FileNotFoundError as e:
            return LanguageAnalysisResult(
                inference=None,
                error=AnalysisError(
                    error_type="FileNotFoundError",
                    message=str(e),
                    phase="file_validation",
                ),
            )
        except PermissionError as e:
            return LanguageAnalysisResult(
                inference=None,
                error=AnalysisError(
                    error_type="PermissionError",
                    message=str(e),
                    phase="file_validation",
                ),
            )
        except InvalidPEError as e:
            return LanguageAnalysisResult(
                inference=None,
                error=AnalysisError(
                    error_type="InvalidPEError",
                    message=str(e),
                    phase="pe_parsing",
                ),
            )
        except Exception as exc:
            return LanguageAnalysisResult(
                inference=None,
                error=AnalysisError(
                    error_type="UnknownError",
                    message=(f"Unexpected error during language inference: {str(exc)}"),
                    phase="language_inference",
                ),
            )

    def _validate_file(self, file_path: str) -> None:
        """Validate that file exists and is readable.

        Args:
            file_path: Path to the file

        Raises:
            FileNotFoundError: If file does not exist
            PermissionError: If file is not readable
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not path.is_file():
            raise FileNotFoundError(f"Path is not a file: {file_path}")

        # Try to check if file is readable
        try:
            with open(path, "rb") as f:
                # Just try to read one byte to check permissions
                f.read(1)
        except PermissionError as e:
            raise PermissionError(f"Cannot read file: {file_path}") from e
