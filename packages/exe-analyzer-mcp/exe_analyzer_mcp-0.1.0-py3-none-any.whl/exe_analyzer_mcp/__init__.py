"""exe-analyzer-mcp: MCP server for Windows executable analysis."""

from exe_analyzer_mcp.analysis_orchestrator import (
    AnalysisError,
    AnalysisOrchestrator,
    FrameworkAnalysisResult,
    LanguageAnalysisResult,
    LibraryAnalysisResult,
    StringAnalysisResult,
)
from exe_analyzer_mcp.framework_detector import Framework, FrameworkDetector
from exe_analyzer_mcp.language_inferrer import (
    LanguageInference,
    LanguageInferrer,
    LanguageResult,
)
from exe_analyzer_mcp.library_analyzer import (
    Library,
    LibraryAnalysis,
    LibraryAnalyzer,
    LibraryCategory,
)
from exe_analyzer_mcp.pe_parser import (
    ImportedDLL,
    InvalidPEError,
    PEParser,
    PEParserError,
    PESection,
)
from exe_analyzer_mcp.string_extractor import (
    ExtractedString,
    StringCategory,
    StringExtractor,
    StringResult,
)

__version__ = "0.1.0"

__all__ = [
    # Orchestrator
    "AnalysisOrchestrator",
    "AnalysisError",
    "FrameworkAnalysisResult",
    "LibraryAnalysisResult",
    "StringAnalysisResult",
    "LanguageAnalysisResult",
    # Framework Detection
    "FrameworkDetector",
    "Framework",
    # Library Analysis
    "LibraryAnalyzer",
    "LibraryAnalysis",
    "Library",
    "LibraryCategory",
    # String Extraction
    "StringExtractor",
    "StringResult",
    "ExtractedString",
    "StringCategory",
    # Language Inference
    "LanguageInferrer",
    "LanguageInference",
    "LanguageResult",
    # PE Parser
    "PEParser",
    "PEParserError",
    "InvalidPEError",
    "PESection",
    "ImportedDLL",
]
