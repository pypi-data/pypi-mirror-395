# Project Structure

## Root Directory

```
exe-analyzer-mcp/
├── .git/                 # Git version control
├── .kiro/                # Kiro IDE configuration
│   ├── specs/            # Feature specifications
│   └── steering/         # AI assistant guidance (this file)
├── .venv/                # Python virtual environment (uv managed)
├── main.py               # MCP server entry point
├── pyproject.toml        # Project metadata and dependencies
├── uv.lock               # Locked dependency versions
├── .python-version       # Python version specification
├── .gitignore            # Git ignore patterns
└── README.md             # Project documentation
```

## Architecture

The codebase follows a modular architecture with clear separation:

- **MCP Server Layer**: Tool registration, request handling, response formatting
- **Analysis Orchestrator**: Coordinates analysis workflows between components
- **Framework Detector**: Identifies frameworks via string and metadata analysis
- **Library Analyzer**: Parses PE import tables and categorizes dependencies
- **String Extractor**: Extracts meaningful strings using entropy filtering
- **Language Inferrer**: Determines programming language from compiler signatures
- **PE Parser**: Low-level PE file parsing (pefile library)

## Specifications

The `.kiro/specs/exe-analyzer-mcp/` directory contains:
- `requirements.md`: User stories and acceptance criteria
- `design.md`: Architecture, components, data models, correctness properties
- `tasks.md`: Implementation tasks and tracking

## Code Organization Principles

- Each analysis component should be in its own module
- Use dataclasses for structured data models
- Implement clear interfaces between components
- Keep MCP protocol handling separate from analysis logic
- Store configuration (framework signatures, compiler patterns) in external files
