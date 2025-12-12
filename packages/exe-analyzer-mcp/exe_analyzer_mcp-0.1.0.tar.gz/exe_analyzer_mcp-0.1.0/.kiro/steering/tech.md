# Technology Stack

## Language & Runtime

- **Python**: 3.12+ (specified in pyproject.toml)
- **Package Manager**: uv (modern Python package manager)
- **Virtual Environment**: .venv (managed by uv)

## Key Dependencies

- **pefile**: PE (Portable Executable) format parsing library
- **mcp**: Model Context Protocol implementation
- **Hypothesis**: Property-based testing framework
- **pytest**: Unit testing framework
- **ruff**: Fast Python linter and formatter

## Build System

Project uses `pyproject.toml` for dependency management and configuration.

### Common Commands

```bash
# Install dependencies
uv sync

# Run the MCP server
uv run python main.py

# Run tests
uv run pytest

# Lint and format code
uv run ruff check .
uv run ruff format .
```

## Code Quality

- **Linting**: ruff for code quality and style enforcement
- **Testing**: pytest for unit tests, Hypothesis for property-based tests
- **Type Hints**: Use Python type annotations throughout

## MCP Protocol

The server implements MCP tools that can be invoked by AI assistants:
- `analyze_frameworks`: Detect frameworks in executables
- `analyze_libraries`: Extract and categorize imported libraries
- `extract_strings`: Find meaningful strings with categorization
- `infer_language`: Determine programming language used
