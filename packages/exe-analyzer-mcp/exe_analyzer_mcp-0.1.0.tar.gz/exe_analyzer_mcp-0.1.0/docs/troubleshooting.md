# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with exe-analyzer-mcp.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Server Startup Issues](#server-startup-issues)
3. [Analysis Errors](#analysis-errors)
4. [Detection Issues](#detection-issues)
5. [Performance Issues](#performance-issues)
6. [MCP Integration Issues](#mcp-integration-issues)
7. [Configuration Issues](#configuration-issues)
8. [Testing Issues](#testing-issues)

## Installation Issues

### Issue: uv command not found

**Symptoms:**
```
'uv' is not recognized as an internal or external command
```

**Cause:** uv package manager is not installed.

**Solution:**
1. Install uv following the official guide: https://docs.astral.sh/uv/
2. On Windows, you can use:
   ```bash
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
3. Verify installation:
   ```bash
   uv --version
   ```

### Issue: Python version mismatch

**Symptoms:**
```
Python 3.12 or higher is required
```

**Cause:** Installed Python version is too old.

**Solution:**
1. Check your Python version:
   ```bash
   python --version
   ```
2. Install Python 3.12 or higher from https://www.python.org/
3. Update .python-version file if needed:
   ```
   3.12
   ```

### Issue: Dependency installation fails

**Symptoms:**
```
error: Failed to download distributions
```

**Cause:** Network issues or package conflicts.

**Solution:**
1. Clear uv cache:
   ```bash
   uv cache clean
   ```
2. Try installing again:
   ```bash
   uv sync
   ```
3. If still failing, check your internet connection
4. Try with verbose output:
   ```bash
   uv sync -v
   ```

## Server Startup Issues

### Issue: Server fails to start

**Symptoms:**
```
Error: Failed to initialize MCP server
```

**Cause:** Configuration files missing or invalid.

**Solution:**
1. Verify configuration files exist:
   ```bash
   dir src\exe_analyzer_mcp\config\*.json
   ```
2. Validate JSON syntax:
   ```bash
   python -m json.tool src/exe_analyzer_mcp/config/framework_signatures.json
   ```
3. Check file permissions (must be readable)
4. Review error message for specific file causing issue

### Issue: Import errors on startup

**Symptoms:**
```
ModuleNotFoundError: No module named 'pefile'
```

**Cause:** Dependencies not installed.

**Solution:**
1. Ensure you're in the project directory
2. Install dependencies:
   ```bash
   uv sync
   ```
3. Verify installation:
   ```bash
   uv run python -c "import pefile; print('OK')"
   ```

### Issue: Server starts but doesn't respond

**Symptoms:**
- Server process runs but no output
- MCP client can't connect

**Cause:** Server waiting for stdio input.

**Solution:**
1. The server uses stdio for MCP communication
2. Don't run it directly in terminal for testing
3. Use the CLI tool instead:
   ```bash
   uv run python -m exe_analyzer_mcp.cli analyze-frameworks test.exe
   ```
4. Or configure it with an MCP client (Claude Desktop)

## Analysis Errors

### Issue: File not found

**Symptoms:**
```json
{
  "error": {
    "type": "FileNotFoundError",
    "message": "File not found: C:\\path\\to\\file.exe"
  }
}
```

**Cause:** File path is incorrect or file doesn't exist.

**Solution:**
1. Verify file exists:
   ```bash
   dir "C:\path\to\file.exe"
   ```
2. Use absolute paths, not relative
3. On Windows, use double backslashes or raw strings:
   - Good: `C:\\path\\to\\file.exe`
   - Good: `C:/path/to/file.exe`
   - Bad: `C:\path\to\file.exe` (in JSON)
4. Check for typos in filename

### Issue: Permission denied

**Symptoms:**
```json
{
  "error": {
    "type": "PermissionError",
    "message": "Permission denied: C:\\Windows\\System32\\cmd.exe"
  }
}
```

**Cause:** Insufficient permissions to read the file.

**Solution:**
1. Run as administrator if analyzing system files
2. Check file permissions:
   ```bash
   icacls "C:\path\to\file.exe"
   ```
3. Copy file to a location you have access to
4. Avoid analyzing files in protected directories

### Issue: Invalid PE format

**Symptoms:**
```json
{
  "error": {
    "type": "InvalidPEError",
    "message": "Not a valid PE file"
  }
}
```

**Cause:** File is not a Windows PE executable.

**Solution:**
1. Verify file is actually an .exe:
   ```bash
   file file.exe  # On Linux/WSL
   ```
2. Check file signature (should start with "MZ"):
   ```bash
   xxd -l 2 file.exe  # Should show "4d 5a"
   ```
3. File may be:
   - Corrupted
   - Compressed/packed
   - Not a PE file (e.g., script, document)
   - Encrypted

### Issue: Corrupted import table

**Symptoms:**
```json
{
  "error": {
    "type": "PEFormatError",
    "message": "Failed to parse import table"
  }
}
```

**Cause:** PE file has corrupted or obfuscated import table.

**Solution:**
1. This is common with packed/protected executables
2. Try other analysis tools (frameworks, strings, language)
3. The file may be intentionally obfuscated
4. Consider unpacking the executable first
5. Check if partial results are available in error response

## Detection Issues

### Issue: No frameworks detected

**Symptoms:**
```json
{
  "frameworks": []
}
```

**Cause:** Executable doesn't use recognized frameworks or signatures are missing.

**Solution:**
1. Extract strings to see what's in the file:
   ```bash
   uv run python -m exe_analyzer_mcp.cli extract-strings file.exe
   ```
2. Look for framework-related strings manually
3. Add custom signatures to framework_signatures.json
4. The executable may:
   - Use a custom/proprietary framework
   - Be statically linked (no framework DLLs)
   - Be packed/obfuscated

### Issue: Wrong framework detected

**Symptoms:**
- Framework detected with low confidence
- Multiple conflicting frameworks

**Cause:** False positive from generic signatures.

**Solution:**
1. Check confidence scores (>0.8 is reliable)
2. Review indicators in the result
3. Refine signatures in framework_signatures.json
4. Make signatures more specific
5. The executable may genuinely use multiple frameworks

### Issue: Language detection returns low confidence

**Symptoms:**
```json
{
  "primary_language": {
    "language": "C++",
    "confidence": 0.35
  }
}
```

**Cause:** Insufficient compiler signatures or obfuscated executable.

**Solution:**
1. Check alternative_languages for other possibilities
2. Examine the indicators to understand why confidence is low
3. Add more compiler signatures to compiler_signatures.json
4. The executable may be:
   - Packed/obfuscated
   - Built with uncommon compiler
   - Mixed-language project
5. Try analyzing libraries for additional clues

### Issue: No strings extracted

**Symptoms:**
```json
{
  "strings_by_category": {},
  "total_count": 0,
  "truncated": false
}
```

**Cause:** Executable has no readable strings or they're encrypted.

**Solution:**
1. Verify file is not empty:
   ```bash
   dir file.exe
   ```
2. The executable may be:
   - Packed/compressed
   - String-encrypted
   - Very small/minimal
3. Try lowering minimum string length (requires code modification)
4. Check if file is actually a PE executable

### Issue: Too many random strings

**Symptoms:**
- Thousands of meaningless strings
- High entropy strings in results

**Cause:** Entropy threshold too low or data sections included.

**Solution:**
1. The analyzer filters strings with entropy >4.5
2. Remaining strings should be meaningful
3. If still seeing random data:
   - File may be partially encrypted
   - Data sections may contain binary data
   - Consider the strings may actually be encoded data

## Performance Issues

### Issue: Analysis is very slow

**Symptoms:**
- Takes minutes to analyze a file
- High CPU usage

**Cause:** Large executable or inefficient processing.

**Solution:**
1. Check file size:
   ```bash
   dir file.exe
   ```
2. For files >100MB:
   - Analysis uses chunked processing
   - This is expected behavior
3. For smaller files:
   - Check if file is corrupted
   - Try analyzing specific aspects only
   - Restart the server

### Issue: Out of memory error

**Symptoms:**
```
MemoryError: Unable to allocate memory
```

**Cause:** File too large or memory leak.

**Solution:**
1. Check available memory:
   ```bash
   wmic OS get FreePhysicalMemory
   ```
2. Close other applications
3. The analyzer limits:
   - String extraction to 10,000 entries
   - Maximum file size to 500MB
4. For very large files:
   - Analyze in parts
   - Use CLI for specific operations only

### Issue: String extraction truncated

**Symptoms:**
```json
{
  "total_count": 10000,
  "truncated": true
}
```

**Cause:** Hit the 10,000 string limit (by design).

**Solution:**
1. This is expected for executables with many strings
2. The most meaningful strings are included
3. To get more strings:
   - Modify MAX_STRINGS constant in string_extractor.py
   - Be aware of memory implications
4. Consider filtering by category:
   - Focus on URLs, file paths, or error messages

## MCP Integration Issues

### Issue: Claude Desktop doesn't see the server

**Symptoms:**
- Server not listed in Claude Desktop
- Tools not available

**Cause:** Configuration file incorrect or server not starting.

**Solution:**
1. Check Claude Desktop config file location:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Verify configuration syntax:
   ```json
   {
     "mcpServers": {
       "exe-analyzer": {
         "command": "uv",
         "args": [
           "--directory",
           "C:\\path\\to\\exe-analyzer-mcp",
           "run",
           "python",
           "main.py"
         ]
       }
     }
   }
   ```
3. Use absolute paths
4. Restart Claude Desktop after config changes

### Issue: Tools fail when invoked

**Symptoms:**
- Error message in Claude Desktop
- "Tool execution failed"

**Cause:** Server error or invalid input.

**Solution:**
1. Check server logs (if available)
2. Test with CLI first:
   ```bash
   uv run python -m exe_analyzer_mcp.cli analyze-frameworks test.exe
   ```
3. Verify file path is accessible from server
4. Check error message for specific issue
5. Restart Claude Desktop

### Issue: Slow response from MCP tools

**Symptoms:**
- Long wait times for results
- Timeout errors

**Cause:** Large file or complex analysis.

**Solution:**
1. This is expected for large executables
2. Try analyzing smaller files first
3. Use specific tools instead of asking for "everything"
4. Consider the file may be packed/obfuscated (slower)

## Configuration Issues

### Issue: Configuration changes not applied

**Symptoms:**
- Added framework not detected
- New signatures ignored

**Cause:** Server not restarted or configuration not loaded.

**Solution:**
1. Restart the MCP server:
   ```bash
   # Stop server (Ctrl+C)
   uv run python main.py
   ```
2. If using Claude Desktop, restart it too
3. Verify configuration file was saved
4. Check for JSON syntax errors:
   ```bash
   python -m json.tool config_file.json
   ```

### Issue: Invalid JSON in configuration

**Symptoms:**
```
JSONDecodeError: Expecting property name enclosed in double quotes
```

**Cause:** Syntax error in configuration file.

**Solution:**
1. Validate JSON:
   ```bash
   python -m json.tool src/exe_analyzer_mcp/config/framework_signatures.json
   ```
2. Common issues:
   - Missing commas between items
   - Trailing commas (not allowed in JSON)
   - Single quotes instead of double quotes
   - Missing closing brackets
3. Use a JSON validator or editor with syntax highlighting

### Issue: Configuration file not found

**Symptoms:**
```
FileNotFoundError: config/framework_signatures.json not found
```

**Cause:** Configuration file missing or wrong directory.

**Solution:**
1. Verify files exist:
   ```bash
   dir src\exe_analyzer_mcp\config\*.json
   ```
2. Ensure you're running from project root
3. Check file names are correct (case-sensitive on some systems)
4. Restore from git if deleted:
   ```bash
   git checkout src/exe_analyzer_mcp/config/
   ```

## Testing Issues

### Issue: Tests fail to run

**Symptoms:**
```
ERROR: file not found: tests/
```

**Cause:** Running from wrong directory or tests not installed.

**Solution:**
1. Ensure you're in project root:
   ```bash
   cd path\to\exe-analyzer-mcp
   ```
2. Install test dependencies:
   ```bash
   uv sync
   ```
3. Run tests:
   ```bash
   uv run pytest
   ```

### Issue: Property tests fail

**Symptoms:**
```
Falsifying example: test_property(...)
```

**Cause:** Property test found a counterexample (possible bug).

**Solution:**
1. This is expected behavior for property-based testing
2. Review the counterexample in the output
3. Determine if it's:
   - A real bug (fix the code)
   - Invalid input (fix the test generator)
   - Edge case (document or handle specially)
4. Run the specific test to reproduce:
   ```bash
   uv run pytest tests/test_framework_detector_properties.py -v
   ```

### Issue: Import errors in tests

**Symptoms:**
```
ModuleNotFoundError: No module named 'exe_analyzer_mcp'
```

**Cause:** Package not installed in development mode.

**Solution:**
1. Install in development mode:
   ```bash
   uv sync
   ```
2. Verify installation:
   ```bash
   uv run python -c "import exe_analyzer_mcp; print('OK')"
   ```

## Getting Help

If your issue isn't covered here:

### 1. Check Documentation

- README.md - Installation and basic usage
- docs/configuration_guide.md - Configuration details
- examples/basic_usage.md - Usage examples
- .kiro/specs/exe-analyzer-mcp/ - Design and requirements

### 2. Enable Verbose Logging

Use the CLI with verbose flag:
```bash
uv run python -m exe_analyzer_mcp.cli analyze-frameworks file.exe --verbose
```

### 3. Collect Diagnostic Information

When reporting issues, include:
- Error message (full text)
- File type being analyzed (language, framework if known)
- File size
- Steps to reproduce
- Expected vs actual behavior
- Python version: `python --version`
- uv version: `uv --version`
- Operating system

### 4. Test with Known Files

Try analyzing a known executable:
```bash
# Windows Calculator
uv run python -m exe_analyzer_mcp.cli analyze-frameworks C:\Windows\System32\calc.exe

# Notepad
uv run python -m exe_analyzer_mcp.cli infer-language C:\Windows\System32\notepad.exe
```

If these work, the issue is likely with your specific file.

### 5. Check for Updates

Ensure you have the latest version:
```bash
git pull
uv sync
```

### 6. Review Test Suite

The tests demonstrate expected behavior:
```bash
# Run all tests
uv run pytest -v

# Run specific component tests
uv run pytest tests/test_framework_detector_unit.py -v
```

## Common Error Messages

### "PE file has no import table"

**Meaning:** The executable doesn't import any DLLs (statically linked).

**Action:** This is normal for some executables (e.g., Go binaries). Try other analysis methods.

### "String extraction returned no results"

**Meaning:** No readable strings found in the executable.

**Action:** File may be packed, encrypted, or very minimal. Try framework or language detection.

### "Confidence score too low to determine language"

**Meaning:** Not enough evidence to identify the programming language.

**Action:** Check alternative_languages, examine libraries, or add custom signatures.

### "File size exceeds maximum limit"

**Meaning:** File is larger than 500MB.

**Action:** This is a safety limit. Consider analyzing a smaller file or modifying the limit in code.

### "Failed to parse PE header"

**Meaning:** File is corrupted or not a valid PE file.

**Action:** Verify file integrity, check if it's actually an executable.

## Debug Checklist

When troubleshooting, work through this checklist:

- [ ] File exists and path is correct
- [ ] File is readable (permissions)
- [ ] File is a valid PE executable
- [ ] Server is running and configured correctly
- [ ] Configuration files are valid JSON
- [ ] Dependencies are installed (`uv sync`)
- [ ] Using correct Python version (3.12+)
- [ ] Tried with a known working file
- [ ] Checked error message carefully
- [ ] Restarted server after config changes
- [ ] Reviewed relevant documentation

## Prevention Tips

1. **Always use absolute paths** for file analysis
2. **Validate JSON** before editing configuration files
3. **Test changes** with known files before production use
4. **Keep backups** of working configurations
5. **Update regularly** to get bug fixes
6. **Run tests** after making changes
7. **Use version control** to track configuration changes
8. **Document custom additions** to configurations
9. **Monitor confidence scores** to catch false positives
10. **Start simple** - test one tool at a time

## Still Having Issues?

If you've tried everything and still have problems:

1. Create a minimal reproduction case
2. Document exact steps to reproduce
3. Include all diagnostic information
4. Check if it's a known limitation
5. Consider if the file is intentionally obfuscated
6. Open an issue with complete details

Remember: Some executables are designed to resist analysis (packers, protectors, obfuscators). This is expected behavior, not a bug in the analyzer.
