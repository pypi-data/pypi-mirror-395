# Configuration Guide

This guide explains how to customize exe-analyzer-mcp's detection capabilities through configuration files.

## Overview

The analyzer uses three JSON configuration files located in `src/exe_analyzer_mcp/config/`:

1. **framework_signatures.json** - Framework detection patterns
2. **compiler_signatures.json** - Language inference mappings
3. **system_libraries.json** - Known Windows libraries

## Framework Signatures Configuration

### File Location
`src/exe_analyzer_mcp/config/framework_signatures.json`

### Purpose
Defines patterns for detecting frameworks and runtime environments in executables.

### Structure

```json
{
  "frameworks": [
    {
      "name": "Framework Name",
      "signatures": ["pattern1", "pattern2", "pattern3"],
      "version_patterns": ["version_pattern1", "version_pattern2"]
    }
  ]
}
```

### Fields

- **name** (string, required): Display name of the framework
- **signatures** (array of strings, required): Strings that indicate the framework's presence
- **version_patterns** (array of strings, optional): Patterns to extract version information

### How Detection Works

1. The analyzer extracts all strings from the executable
2. For each framework, it checks if any signatures match extracted strings
3. If matches are found, it searches for version patterns
4. Results include the framework name, version (if found), and confidence score

### Example: Adding a New Framework

To add support for detecting Flutter applications:

```json
{
  "frameworks": [
    {
      "name": "Flutter",
      "signatures": [
        "flutter",
        "libflutter.so",
        "flutter_engine",
        "io.flutter"
      ],
      "version_patterns": [
        "Flutter ",
        "flutter_version"
      ]
    }
  ]
}
```

### Best Practices

1. **Use Specific Signatures**: Choose unique strings that are unlikely to appear in other contexts
   - Good: `"Qt5Core.dll"`, `"QApplication"`
   - Bad: `"core"`, `"app"`

2. **Include Multiple Signatures**: More signatures increase detection confidence
   - Minimum: 2-3 signatures per framework
   - Recommended: 4-6 signatures

3. **Version Patterns**: Include common version string formats
   - Example: `"v4.0.30319"`, `"Qt 5."`, `"Electron/"`

4. **Case Sensitivity**: Signatures are case-sensitive
   - Include variations if needed: `"electron"`, `"Electron"`

### Existing Frameworks

The default configuration includes:
- .NET Framework
- .NET Core
- Qt (versions 5 and 6)
- Electron
- wxWidgets
- MFC (Microsoft Foundation Classes)
- GTK

## Compiler Signatures Configuration

### File Location
`src/exe_analyzer_mcp/config/compiler_signatures.json`

### Purpose
Maps compiler signatures to programming languages for language inference.

### Structure

```json
{
  "compilers": [
    {
      "language": "Language Name",
      "signatures": ["signature1", "signature2"],
      "clr_required": false
    }
  ]
}
```

### Fields

- **language** (string, required): Name of the programming language
- **signatures** (array of strings, required): Compiler-specific strings or patterns
- **clr_required** (boolean, required): Whether .NET CLR header must be present

### How Detection Works

1. The analyzer examines PE headers and extracted strings
2. For .NET languages (clr_required: true), it first checks for CLR header
3. It searches for compiler signatures in the executable
4. Confidence scores are calculated based on number of matching signatures
5. Multiple languages may be detected with different confidence levels

### Example: Adding a New Language

To add support for detecting Nim-compiled executables:

```json
{
  "compilers": [
    {
      "language": "Nim",
      "signatures": [
        "nim_",
        "NimMain",
        "nimGC",
        "@nim@"
      ],
      "clr_required": false
    }
  ]
}
```

### Best Practices

1. **Compiler-Specific Strings**: Use strings unique to the compiler
   - Good: `"rustc"`, `"Go build ID:"`, `"NimMain"`
   - Bad: `"main"`, `"init"`, `"start"`

2. **Runtime Indicators**: Include runtime library names
   - C++: `"vcruntime140.dll"`, `"libstdc++"`
   - Go: `"runtime.go"`, `"runtime.main"`
   - Rust: `"rust_panic"`, `"rust_begin_unwind"`

3. **CLR Requirement**: Set to true only for .NET languages
   - C#, VB.NET: `"clr_required": true`
   - All others: `"clr_required": false`

4. **Multiple Indicators**: Include 4-6 signatures for reliable detection

### Existing Languages

The default configuration includes:
- C#
- VB.NET
- C++
- C
- Go
- Rust
- Delphi
- Visual Basic 6
- Python (PyInstaller)

## System Libraries Configuration

### File Location
`src/exe_analyzer_mcp/config/system_libraries.json`

### Purpose
Lists known Windows system and runtime libraries for categorization.

### Structure

```json
{
  "system_libraries": [
    "library1.dll",
    "library2.dll"
  ],
  "runtime_libraries": [
    "runtime1.dll",
    "runtime2.dll"
  ]
}
```

### Fields

- **system_libraries** (array of strings): Windows system DLLs
- **runtime_libraries** (array of strings): Language runtime DLLs

### How Categorization Works

1. The analyzer extracts imported DLL names from the PE import table
2. Each DLL is checked against system_libraries and runtime_libraries
3. Libraries are categorized as:
   - **system**: Found in system_libraries list
   - **runtime**: Found in runtime_libraries list
   - **external**: Not found in either list (third-party)

### Example: Adding New Libraries

To add support for newer Windows APIs:

```json
{
  "system_libraries": [
    "kernel32.dll",
    "user32.dll",
    "api-ms-win-core-synch-l1-2-0.dll",
    "api-ms-win-core-processthreads-l1-1-3.dll"
  ],
  "runtime_libraries": [
    "msvcrt.dll",
    "vcruntime140.dll",
    "vcruntime140_1.dll",
    "msvcp140.dll"
  ]
}
```

### Best Practices

1. **Use Lowercase**: All library names should be lowercase
   - Good: `"kernel32.dll"`
   - Bad: `"KERNEL32.DLL"`

2. **Include Versions**: Add all common versions of runtime libraries
   - Example: `"vcruntime140.dll"`, `"vcruntime140_1.dll"`

3. **API Sets**: Include Windows API set DLLs
   - Pattern: `"api-ms-win-*"`

4. **Complete Names**: Always include the `.dll` extension

### Existing Libraries

**System Libraries** (partial list):
- Core: kernel32.dll, user32.dll, ntdll.dll
- Graphics: gdi32.dll
- Security: advapi32.dll, crypt32.dll
- Networking: ws2_32.dll, wininet.dll, winhttp.dll
- Shell: shell32.dll, shlwapi.dll

**Runtime Libraries** (partial list):
- MSVC: msvcrt.dll, vcruntime140.dll, msvcp140.dll
- Universal CRT: ucrtbase.dll, api-ms-win-crt-*.dll
- .NET: mscoree.dll, mscorlib.dll, clr.dll

## Configuration Reload

### When Changes Take Effect

Configuration files are loaded when the MCP server starts. To apply changes:

1. Edit the configuration file
2. Save the file
3. Restart the MCP server:
   ```bash
   # Stop the server (Ctrl+C)
   # Start it again
   uv run python main.py
   ```

### Validation

The server validates configuration files on startup. Invalid JSON will cause startup failure with an error message.

## Advanced Configuration

### Custom Configuration Directory

To use a custom configuration directory, modify `src/exe_analyzer_mcp/config/__init__.py`:

```python
import os
from pathlib import Path

# Default: use config directory in package
CONFIG_DIR = Path(__file__).parent

# Custom: use environment variable
if "EXE_ANALYZER_CONFIG_DIR" in os.environ:
    CONFIG_DIR = Path(os.environ["EXE_ANALYZER_CONFIG_DIR"])
```

Then set the environment variable:
```bash
set EXE_ANALYZER_CONFIG_DIR=C:\custom\config
uv run python main.py
```

### Configuration Merging

To extend default configurations without modifying them:

1. Create a custom configuration file
2. Load both default and custom configurations
3. Merge the lists

Example implementation:

```python
import json
from pathlib import Path

def load_frameworks():
    # Load default
    default_path = Path(__file__).parent / "framework_signatures.json"
    with open(default_path) as f:
        default_config = json.load(f)

    # Load custom if exists
    custom_path = Path("custom_frameworks.json")
    if custom_path.exists():
        with open(custom_path) as f:
            custom_config = json.load(f)
        # Merge
        default_config["frameworks"].extend(custom_config["frameworks"])

    return default_config
```

## Testing Configuration Changes

### Verify Framework Detection

After adding a new framework signature:

```bash
# Create a test file with the signature
echo "Qt5Core.dll" > test_strings.txt

# Test with CLI (requires implementation)
uv run python -m exe_analyzer_mcp.cli analyze-frameworks test.exe --verbose
```

### Verify Language Detection

After adding a new compiler signature:

```bash
# Test with a known executable
uv run python -m exe_analyzer_mcp.cli infer-language known_go_app.exe --verbose
```

### Run Tests

The test suite includes configuration validation:

```bash
# Run all tests
uv run pytest

# Run configuration-specific tests
uv run pytest tests/test_framework_detector_unit.py
uv run pytest tests/test_language_inferrer_unit.py
```

## Troubleshooting

### Framework Not Detected

**Problem**: Added a framework but it's not being detected.

**Solutions**:
1. Verify JSON syntax is valid
2. Check that signatures are present in the executable:
   ```bash
   uv run python -m exe_analyzer_mcp.cli extract-strings app.exe | grep "signature"
   ```
3. Ensure signatures are case-sensitive matches
4. Add more signatures to increase confidence
5. Check server logs for errors

### Language Detection Incorrect

**Problem**: Wrong language is detected or confidence is low.

**Solutions**:
1. Add more compiler-specific signatures
2. Check if multiple languages are present (mixed-language project)
3. Verify clr_required setting is correct
4. Review alternative_languages in the result
5. Consider the executable may be obfuscated

### Library Miscategorized

**Problem**: A library is categorized incorrectly.

**Solutions**:
1. Check spelling in system_libraries.json (must be lowercase)
2. Verify the library name includes .dll extension
3. Add the library to the appropriate list
4. Restart the server after changes

### Configuration Not Loading

**Problem**: Changes to configuration files don't take effect.

**Solutions**:
1. Verify JSON syntax with a validator
2. Check file permissions (must be readable)
3. Ensure you restarted the MCP server
4. Check for typos in file names
5. Review server startup logs for errors

## Examples

### Example 1: Adding Unity Engine Detection

```json
{
  "frameworks": [
    {
      "name": "Unity",
      "signatures": [
        "UnityEngine.dll",
        "UnityPlayer.dll",
        "Unity Technologies",
        "mono.dll"
      ],
      "version_patterns": [
        "Unity ",
        "UnityEngine "
      ]
    }
  ]
}
```

### Example 2: Adding Zig Language Detection

```json
{
  "compilers": [
    {
      "language": "Zig",
      "signatures": [
        "zig_",
        "@zig@",
        "zig.exe",
        "std.zig"
      ],
      "clr_required": false
    }
  ]
}
```

### Example 3: Adding DirectX Libraries

```json
{
  "system_libraries": [
    "d3d11.dll",
    "d3d12.dll",
    "dxgi.dll",
    "d3dcompiler_47.dll",
    "xinput1_4.dll"
  ]
}
```

## Best Practices Summary

1. **Backup Before Editing**: Keep a copy of original configurations
2. **Test Changes**: Verify detection works with known executables
3. **Use Specific Patterns**: Avoid generic strings that may cause false positives
4. **Document Custom Additions**: Comment why custom signatures were added
5. **Version Control**: Track configuration changes in git
6. **Validate JSON**: Use a JSON validator before saving
7. **Restart Server**: Always restart after configuration changes
8. **Monitor Confidence**: Low confidence may indicate need for more signatures

## Reference

### JSON Validation

Validate your configuration files:
```bash
# Using Python
python -m json.tool framework_signatures.json

# Using jq (if installed)
jq . framework_signatures.json
```

### Configuration Schema

All configuration files must be valid JSON. Use these schemas as reference:

**framework_signatures.json**:
- Root: object with "frameworks" array
- Each framework: object with "name", "signatures", "version_patterns"

**compiler_signatures.json**:
- Root: object with "compilers" array
- Each compiler: object with "language", "signatures", "clr_required"

**system_libraries.json**:
- Root: object with "system_libraries" and "runtime_libraries" arrays
- Each array: list of lowercase DLL names with .dll extension
