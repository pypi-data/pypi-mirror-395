# Basic Usage Examples

This document provides practical examples of using exe-analyzer-mcp with AI assistants.

## Example 1: Analyzing a .NET Application

**Scenario:** You want to understand what frameworks a .NET application uses.

**Prompt to AI Assistant:**
```
Analyze the frameworks used in C:\Program Files\MyApp\MyApp.exe
```

**Expected Response:**
```json
{
  "frameworks": [
    {
      "name": ".NET Framework",
      "version": "4.8",
      "confidence": 0.95,
      "indicators": ["mscoree.dll", "mscorlib", "v4.0.30319"]
    }
  ]
}
```

**Interpretation:**
- The application uses .NET Framework 4.8
- High confidence (0.95) indicates strong evidence
- Multiple indicators confirm the detection

## Example 2: Checking Dependencies

**Scenario:** You need to identify all external libraries an application depends on.

**Prompt to AI Assistant:**
```
What libraries does C:\tools\utility.exe import? Show me both system and external libraries.
```

**Expected Response:**
```json
{
  "system_libraries": [
    {
      "name": "kernel32.dll",
      "category": "system",
      "functions": ["CreateFileW", "ReadFile", "WriteFile", "CloseHandle"]
    },
    {
      "name": "user32.dll",
      "category": "system",
      "functions": ["MessageBoxW", "CreateWindowExW"]
    }
  ],
  "external_libraries": [
    {
      "name": "sqlite3.dll",
      "category": "external",
      "functions": ["sqlite3_open", "sqlite3_exec", "sqlite3_close"]
    }
  ],
  "total_imports": 23
}
```

**Interpretation:**
- Uses standard Windows APIs (kernel32, user32)
- Depends on SQLite database library
- Total of 23 imported functions

## Example 3: Finding Hardcoded URLs

**Scenario:** Security analysis to find embedded URLs in an executable.

**Prompt to AI Assistant:**
```
Extract all strings from C:\downloads\suspicious.exe and show me any URLs or IP addresses
```

**Expected Response:**
```json
{
  "strings_by_category": {
    "URL": [
      {
        "value": "https://api.example.com/v1/data",
        "category": "URL",
        "offset": 45678,
        "encoding": "utf-8",
        "entropy": 3.4
      },
      {
        "value": "http://192.168.1.100:8080/callback",
        "category": "URL",
        "offset": 46234,
        "encoding": "ascii",
        "entropy": 3.6
      }
    ],
    "FilePath": [
      {
        "value": "C:\\ProgramData\\AppData\\config.dat",
        "category": "FilePath",
        "offset": 47890,
        "encoding": "utf-16",
        "entropy": 3.2
      }
    ]
  },
  "total_count": 342,
  "truncated": false
}
```

**Interpretation:**
- Found 2 URLs (one HTTPS, one HTTP with IP)
- Also found a suspicious file path in ProgramData
- Low entropy values indicate these are real strings, not random data

## Example 4: Identifying Programming Language

**Scenario:** You want to know what language was used to build an executable.

**Prompt to AI Assistant:**
```
What programming language was used to create C:\apps\game.exe?
```

**Expected Response:**
```json
{
  "primary_language": {
    "language": "C++",
    "confidence": 0.88,
    "indicators": ["MSVC", "vcruntime140.dll", "msvcp140.dll", "libstdc++"]
  },
  "alternative_languages": [
    {
      "language": "C",
      "confidence": 0.35,
      "indicators": ["msvcrt.dll"]
    }
  ]
}
```

**Interpretation:**
- Primarily C++ (88% confidence)
- Uses Microsoft Visual C++ runtime
- Some C code may be present (35% confidence)

## Example 5: Comprehensive Analysis

**Scenario:** Full analysis of an unknown executable.

**Prompt to AI Assistant:**
```
Perform a complete analysis of C:\unknown\app.exe - tell me the language, frameworks, libraries, and any interesting strings
```

**AI Assistant would invoke multiple tools:**

1. **infer_language** result:
```json
{
  "primary_language": {
    "language": "Go",
    "confidence": 0.92,
    "indicators": ["Go build ID:", "runtime.go", "runtime.main"]
  }
}
```

2. **analyze_frameworks** result:
```json
{
  "frameworks": []
}
```

3. **analyze_libraries** result:
```json
{
  "system_libraries": [
    {
      "name": "kernel32.dll",
      "category": "system",
      "functions": ["CreateFileW", "ReadFile"]
    },
    {
      "name": "ws2_32.dll",
      "category": "system",
      "functions": ["WSAStartup", "socket", "connect"]
    }
  ],
  "external_libraries": [],
  "total_imports": 15
}
```

4. **extract_strings** result:
```json
{
  "strings_by_category": {
    "URL": [
      {
        "value": "https://api.service.com/metrics",
        "category": "URL",
        "offset": 123456
      }
    ],
    "ErrorMessage": [
      {
        "value": "failed to connect to server",
        "category": "ErrorMessage",
        "offset": 234567
      }
    ]
  },
  "total_count": 89,
  "truncated": false
}
```

**Interpretation:**
- Go application (92% confidence)
- No frameworks detected (typical for Go)
- Uses networking APIs (ws2_32.dll)
- Connects to an external API
- Contains error handling messages

## Example 6: Malware Analysis

**Scenario:** Initial triage of suspected malware.

**Prompt to AI Assistant:**
```
Analyze C:\quarantine\malware.exe for suspicious indicators - check for unusual strings, network-related libraries, and obfuscation
```

**Expected Analysis:**

1. **Language inference** might show low confidence:
```json
{
  "primary_language": {
    "language": "C++",
    "confidence": 0.45,
    "indicators": ["vcruntime140.dll"]
  },
  "alternative_languages": [
    {
      "language": "Delphi",
      "confidence": 0.40,
      "indicators": ["Borland"]
    }
  ]
}
```

2. **String extraction** might reveal:
```json
{
  "strings_by_category": {
    "URL": [
      {
        "value": "http://malicious-c2.com/gate.php",
        "category": "URL",
        "offset": 56789
      }
    ],
    "RegistryKey": [
      {
        "value": "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        "category": "RegistryKey",
        "offset": 67890
      }
    ]
  }
}
```

3. **Library analysis** might show:
```json
{
  "system_libraries": [
    {
      "name": "ws2_32.dll",
      "category": "system",
      "functions": ["socket", "connect", "send", "recv"]
    },
    {
      "name": "advapi32.dll",
      "category": "system",
      "functions": ["RegCreateKeyExW", "RegSetValueExW"]
    }
  ]
}
```

**Red Flags:**
- Low confidence in language detection (possible obfuscation)
- Suspicious URL in strings
- Registry persistence mechanism
- Network communication capabilities

## Example 7: Qt Application Analysis

**Scenario:** Verifying a Qt application's version and dependencies.

**Prompt to AI Assistant:**
```
Check what version of Qt is used in C:\QtApps\designer.exe
```

**Expected Response:**
```json
{
  "frameworks": [
    {
      "name": "Qt",
      "version": "5.15",
      "confidence": 0.90,
      "indicators": ["Qt5Core", "Qt5Gui", "Qt5Widgets", "Qt 5.15"]
    }
  ]
}
```

**Follow-up Analysis:**
```
What Qt libraries does it import?
```

**Expected Response:**
```json
{
  "external_libraries": [
    {
      "name": "Qt5Core.dll",
      "category": "external",
      "functions": ["QObject::connect", "QString::fromUtf8"]
    },
    {
      "name": "Qt5Gui.dll",
      "category": "external",
      "functions": ["QPixmap::load", "QPainter::drawText"]
    },
    {
      "name": "Qt5Widgets.dll",
      "category": "external",
      "functions": ["QApplication::exec", "QWidget::show"]
    }
  ]
}
```

## Example 8: Electron App Detection

**Scenario:** Identifying if an application is built with Electron.

**Prompt to AI Assistant:**
```
Is C:\Program Files\MyApp\MyApp.exe an Electron application?
```

**Expected Response:**
```json
{
  "frameworks": [
    {
      "name": "Electron",
      "version": null,
      "confidence": 0.85,
      "indicators": ["electron", "chrome_elf.dll", "node.dll", "libGLESv2.dll"]
    }
  ]
}
```

**Interpretation:**
- Yes, it's an Electron app (85% confidence)
- Uses Chrome rendering engine and Node.js
- Version not detected (common for Electron apps)

## Tips for Effective Analysis

### 1. Start Broad, Then Narrow

Begin with language and framework detection, then drill down into specific aspects:
```
1. What language is this executable written in?
2. What frameworks does it use?
3. Show me the imported libraries
4. Extract strings related to networking
```

### 2. Combine Multiple Analyses

Use multiple tools together for comprehensive understanding:
```
Analyze C:\app.exe and tell me:
- Programming language
- Any frameworks used
- Network-related libraries
- URLs and file paths in strings
```

### 3. Focus on Specific Categories

When extracting strings, ask for specific categories:
```
Extract only URLs and registry keys from C:\app.exe
```

### 4. Interpret Confidence Scores

- **>0.8**: High confidence, reliable result
- **0.5-0.8**: Moderate confidence, likely correct
- **<0.5**: Low confidence, consider alternatives

### 5. Look for Patterns

Multiple indicators strengthen conclusions:
```
If you see:
- Go language detected
- No frameworks
- Minimal imports
→ Likely a statically-linked Go binary
```

## Common Use Cases

### Security Analysis
- Identify suspicious URLs or IP addresses
- Check for persistence mechanisms (registry keys)
- Detect packing/obfuscation (low confidence scores)
- Find command-and-control indicators

### Dependency Management
- List all external libraries
- Identify runtime requirements
- Check for outdated components
- Verify licensing compliance

### Reverse Engineering
- Determine programming language
- Identify frameworks and toolkits
- Extract error messages for debugging
- Find configuration file paths

### Software Inventory
- Catalog technology stacks
- Track framework versions
- Document dependencies
- Assess technical debt
