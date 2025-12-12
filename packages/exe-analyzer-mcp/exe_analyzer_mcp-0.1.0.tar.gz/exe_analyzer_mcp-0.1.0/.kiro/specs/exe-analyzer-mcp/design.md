# Design Document

## Overview

The exe-analyzer-mcp is a Model Context Protocol (MCP) server implemented in Python that provides automated analysis capabilities for Windows executable files. The system leverages the pefile library for PE format parsing and implements custom algorithms for framework detection, library identification, string analysis, and language inference. The server exposes four primary MCP tools that can be invoked by AI assistants to analyze executables and extract meaningful information.

## Architecture

The system follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    MCP Server Layer                      │
│  (Tool Registration, Request Handling, Response Format)  │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────┴────────────────────────────────────────┐
│                  Analysis Orchestrator                   │
│         (Coordinates analysis workflows)                 │
└────┬──────────┬──────────┬──────────┬──────────────────┘
     │          │          │          │
┌────┴───┐ ┌───┴────┐ ┌───┴────┐ ┌──┴─────────┐
│Framework│ │Library │ │ String │ │  Language  │
│Detector │ │Analyzer│ │Extractor│ │  Inferrer  │
└────┬───┘ └───┬────┘ └───┬────┘ └──┬─────────┘
     │          │          │          │
     └──────────┴──────────┴──────────┘
                 │
        ┌────────┴────────┐
        │   PE Parser     │
        │   (pefile)      │
        └─────────────────┘
```

### Component Responsibilities

- **MCP Server Layer**: Handles MCP protocol communication, tool registration, and request/response formatting
- **Analysis Orchestrator**: Coordinates analysis workflows and manages data flow between components
- **Framework Detector**: Identifies known frameworks by analyzing strings and PE metadata
- **Library Analyzer**: Parses import tables and categorizes external dependencies
- **String Extractor**: Extracts and filters meaningful strings using entropy analysis
- **Language Inferrer**: Determines programming language based on compiler signatures and metadata
- **PE Parser**: Low-level PE file parsing using the pefile library

## Components and Interfaces

### MCP Server Component

**Interface:**
```python
class MCPServer:
    def register_tools(self) -> None
    def handle_analyze_frameworks(self, file_path: str) -> FrameworkResult
    def handle_analyze_libraries(self, file_path: str) -> LibraryResult
    def handle_extract_strings(self, file_path: str) -> StringResult
    def handle_infer_language(self, file_path: str) -> LanguageResult
```

### Framework Detector Component

**Interface:**
```python
class FrameworkDetector:
    def detect_frameworks(self, pe: pefile.PE, strings: List[str]) -> List[Framework]
    def _check_dotnet(self, pe: pefile.PE) -> Optional[Framework]
    def _check_qt(self, strings: List[str]) -> Optional[Framework]
    def _check_electron(self, strings: List[str]) -> Optional[Framework]
    def _check_other_frameworks(self, strings: List[str]) -> List[Framework]
```

**Framework Signatures:**
- .NET: CLR header presence, mscoree.dll import, .NET assembly metadata
- Qt: Qt library strings (e.g., "Qt5Core", "QApplication")
- Electron: "electron", "chrome", "node.js" strings
- wxWidgets: "wxWidgets", "wxMSW" strings
- MFC: "MFC", "MFCXX.DLL" patterns
- GTK: "gtk-", "glib-" library references

### Library Analyzer Component

**Interface:**
```python
class LibraryAnalyzer:
    def analyze_libraries(self, pe: pefile.PE) -> LibraryAnalysis
    def _parse_import_table(self, pe: pefile.PE) -> List[str]
    def _categorize_library(self, dll_name: str) -> LibraryCategory
    def _is_system_library(self, dll_name: str) -> bool
```

**Library Categories:**
- System: Windows system DLLs (kernel32.dll, user32.dll, etc.)
- Runtime: Language runtime libraries (msvcrt.dll, vcruntime140.dll)
- External: Third-party libraries (not in system/runtime categories)

### String Extractor Component

**Interface:**
```python
class StringExtractor:
    def extract_strings(self, file_path: str, min_length: int = 4) -> List[ExtractedString]
    def _calculate_entropy(self, text: str) -> float
    def _is_meaningful(self, text: str, entropy: float) -> bool
    def _categorize_string(self, text: str) -> StringCategory
    def _extract_with_encoding(self, data: bytes, encoding: str) -> List[str]
```

**String Categories:**
- URL: Matches http://, https://, ftp:// patterns
- FilePath: Matches C:\, \\, / path patterns
- RegistryKey: Matches HKEY_, Software\ patterns
- ErrorMessage: Contains "error", "exception", "failed" keywords
- General: Other meaningful text

**Entropy Threshold:** Strings with entropy > 4.5 are considered random/binary data

### Language Inferrer Component

**Interface:**
```python
class LanguageInferrer:
    def infer_language(self, pe: pefile.PE, strings: List[str]) -> LanguageInference
    def _check_dotnet_language(self, pe: pefile.PE) -> Optional[LanguageResult]
    def _check_compiler_signature(self, pe: pefile.PE) -> Optional[LanguageResult]
    def _check_runtime_indicators(self, pe: pefile.PE) -> List[LanguageResult]
    def _calculate_confidence(self, indicators: List[str]) -> float
```

**Language Detection Strategies:**
- .NET: Check CLR header, analyze assembly metadata for C# vs VB.NET
- C/C++: Check for MSVC, GCC, or Clang compiler strings
- Go: Look for "Go build ID", "runtime.go" strings
- Rust: Check for "rustc", ".rust" section names
- Delphi: Look for Borland/Embarcadero signatures
- Visual Basic: Check for VB runtime DLLs (msvbvm60.dll)

## Data Models

### Framework Model
```python
@dataclass
class Framework:
    name: str                    # Framework name (e.g., ".NET Framework")
    version: Optional[str]       # Version if detected (e.g., "4.8")
    confidence: float            # Confidence score 0.0-1.0
    indicators: List[str]        # Evidence strings that led to detection
```

### Library Model
```python
@dataclass
class Library:
    name: str                    # DLL name (e.g., "kernel32.dll")
    category: LibraryCategory    # System, Runtime, or External
    functions: List[str]         # Imported function names (optional)

@dataclass
class LibraryAnalysis:
    system_libraries: List[Library]
    external_libraries: List[Library]
    total_imports: int
```

### String Model
```python
@dataclass
class ExtractedString:
    value: str                   # The actual string content
    category: StringCategory     # URL, FilePath, RegistryKey, ErrorMessage, General
    offset: int                  # File offset where string was found
    encoding: str                # Encoding used (ascii, utf-8, utf-16)
    entropy: float               # Calculated entropy value

@dataclass
class StringResult:
    strings_by_category: Dict[StringCategory, List[ExtractedString]]
    total_count: int
    truncated: bool              # True if limited to 10,000 entries
```

### Language Model
```python
@dataclass
class LanguageResult:
    language: str                # Programming language name
    confidence: float            # Confidence score 0.0-1.0
    indicators: List[str]        # Evidence that led to inference

@dataclass
class LanguageInference:
    primary_language: LanguageResult
    alternative_languages: List[LanguageResult]  # Other possibilities
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property Reflection

After reviewing all testable properties from the prework, several redundancies were identified:

- Properties 2.2 and 2.3 both test library categorization and can be combined into a single comprehensive property
- Properties 1.3 and 1.4 both test the structure of framework detection results and can be combined
- Properties 4.4 and 4.5 both test language inference output structure and can be combined

The following properties represent the unique, non-redundant set of correctness guarantees:

### Property 1: String extraction completeness
*For any* valid executable file, when string extraction is performed, the result should contain only strings with length >= 4 characters
**Validates: Requirements 3.1**

### Property 2: Framework detection returns structured results
*For any* executable file where frameworks are detected, each detected framework in the result should include a name field and optionally a version field
**Validates: Requirements 1.3, 1.4**

### Property 3: Multiple framework detection completeness
*For any* executable containing signatures for multiple frameworks, all frameworks with valid signatures should appear in the detection result
**Validates: Requirements 1.4**

### Property 4: Import table parsing extracts DLL names
*For any* valid PE file with a non-empty import table, parsing should extract at least one DLL name
**Validates: Requirements 2.1**

### Property 5: Library categorization is complete and exclusive
*For any* extracted library name, it should be categorized as exactly one of: system, runtime, or external
**Validates: Requirements 2.2, 2.3**

### Property 6: Library results include required fields
*For any* library in the analysis result, it should have both a name field and a category field populated
**Validates: Requirements 2.4**

### Property 7: Entropy filtering excludes high-entropy strings
*For any* string with entropy > 4.5, it should not appear in the meaningful strings result
**Validates: Requirements 3.2**

### Property 8: String categorization is exclusive
*For any* extracted meaningful string, it should be assigned to exactly one category (URL, FilePath, RegistryKey, ErrorMessage, or General)
**Validates: Requirements 3.3**

### Property 9: String results include offset information
*For any* extracted string in the result, it should include a file offset value indicating where it was found
**Validates: Requirements 3.4**

### Property 10: Multi-encoding extraction attempts
*For any* executable file, string extraction should attempt extraction using ASCII, UTF-8, and UTF-16 encodings
**Validates: Requirements 3.5**

### Property 11: PE header examination for language inference
*For any* valid PE file, language inference should successfully read and examine the PE header without error
**Validates: Requirements 4.1**

### Property 12: Compiler signature to language mapping
*For any* known compiler signature found in a PE file, the inferred language should match the expected language for that compiler
**Validates: Requirements 4.2**

### Property 13: .NET CLR detection
*For any* executable with a CLR header, the language inference should identify it as either C# or VB.NET
**Validates: Requirements 4.3**

### Property 14: Language inference includes confidence scores
*For any* language inference result, each language candidate should include a confidence score between 0.0 and 1.0
**Validates: Requirements 4.4, 4.5**

### Property 15: File validation before analysis
*For any* tool invocation with a file path that does not exist or is not readable, an error should be returned before attempting analysis
**Validates: Requirements 5.2**

### Property 16: Successful analysis returns valid JSON
*For any* successful analysis operation, the result should be valid JSON that can be parsed without error
**Validates: Requirements 5.3**

### Property 17: Error responses include error type
*For any* analysis operation that encounters an error, the error response should include both an error message and an error type field
**Validates: Requirements 5.4**

### Property 18: String extraction result size limit
*For any* string extraction operation, the total number of strings returned should not exceed 10,000 entries
**Validates: Requirements 6.2**

## Error Handling

The system implements comprehensive error handling at multiple levels:

### File Access Errors
- **File Not Found**: Return error with type "FileNotFoundError" and descriptive message
- **Permission Denied**: Return error with type "PermissionError" and guidance
- **File Locked**: Return error with type "FileLockError" without crashing the server

### PE Parsing Errors
- **Invalid PE Format**: Return error with type "InvalidPEError" when file is not a valid PE
- **Corrupted Headers**: Attempt partial analysis and return available data with warning
- **Missing Sections**: Continue analysis with available sections, note missing data in result

### Analysis Errors
- **Encoding Errors**: Try multiple encodings, log failures, return successfully decoded strings
- **Memory Errors**: Implement chunked processing for large files, limit result sizes
- **Timeout Errors**: Set reasonable timeouts for each analysis phase, return partial results if timeout occurs

### MCP Protocol Errors
- **Invalid Parameters**: Validate all parameters before analysis, return clear validation errors
- **Serialization Errors**: Catch JSON serialization errors, return simplified error response
- **Tool Not Found**: Return standard MCP error for unregistered tools

### Error Response Format
```python
{
    "error": {
        "type": "ErrorTypeName",
        "message": "Human-readable error description",
        "details": {
            "file_path": "path/to/file.exe",
            "phase": "string_extraction",
            "partial_results": {}  # If any analysis completed
        }
    }
}
```

## Testing Strategy

The testing strategy employs both unit testing and property-based testing to ensure correctness and robustness.

### Unit Testing Approach

Unit tests will cover:
- Specific examples of framework detection (e.g., test with known .NET executable)
- Known compiler signatures mapping to correct languages
- String categorization with example URLs, file paths, registry keys
- Library categorization with known system and external DLLs
- Error handling with specific error conditions (missing file, corrupted PE)
- MCP tool registration and invocation with sample requests

### Property-Based Testing Approach

Property-based testing will use the **Hypothesis** library for Python to verify universal properties across many randomly generated inputs.

**Configuration:**
- Each property test should run a minimum of 100 iterations
- Use custom generators for PE file structures, string data, and library names
- Implement shrinking to find minimal failing examples

**Test Generators:**
- `generate_valid_pe_file()`: Creates valid PE structures with random sections
- `generate_string_with_entropy(min_entropy, max_entropy)`: Creates strings with controlled entropy
- `generate_library_name(category)`: Creates library names for testing categorization
- `generate_framework_signature(framework_name)`: Embeds framework signatures in test data

**Property Test Tagging:**
Each property-based test must include a comment tag in this format:
```python
# Feature: exe-analyzer-mcp, Property 1: String extraction completeness
```

This links the test implementation to the correctness property in this design document.

### Integration Testing

Integration tests will verify:
- End-to-end MCP tool invocation with real executable files
- Multiple analysis operations in sequence
- Resource cleanup after analysis completion

### Test Data

The test suite will include:
- Sample executables compiled from different languages (C++, C#, Go, Rust)
- Executables using different frameworks (.NET, Qt, Electron)
- Malformed PE files for error handling tests
- Large executables (>100MB) for performance testing

## Implementation Notes

### Technology Stack
- **Language**: Python 3.9+
- **PE Parsing**: pefile library (version 2023.2.7 or later)
- **MCP Protocol**: mcp Python package
- **Property Testing**: Hypothesis library
- **Unit Testing**: pytest framework

### Performance Considerations
- Implement lazy loading for large executables
- Cache parsed PE structures for multiple analysis operations
- Use memory-mapped files for string extraction from large files
- Limit string extraction to first 100MB of file for very large executables

### Security Considerations
- Never execute or load analyzed executables
- Validate file paths to prevent directory traversal attacks
- Limit file size to prevent DoS attacks (max 500MB)
- Run analysis in isolated process if possible
- Sanitize all strings before returning to prevent injection attacks

### Extensibility
- Framework signatures stored in external JSON configuration file
- Compiler signature database can be updated without code changes
- Plugin architecture for adding new analysis capabilities
- Configurable thresholds for entropy, string length, confidence scores
