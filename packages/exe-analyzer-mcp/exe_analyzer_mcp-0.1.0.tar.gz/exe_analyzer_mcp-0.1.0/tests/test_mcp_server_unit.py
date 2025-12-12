"""Unit tests for MCP server."""

import asyncio
import json
import tempfile
from pathlib import Path

import pytest

from exe_analyzer_mcp.mcp_server import MCPServer


class TestMCPServerToolRegistration:
    """Test tool registration on server start."""

    def test_server_initializes_with_tools(self):
        """Test that server registers all tools on initialization."""
        server = MCPServer()

        # Server should have the MCP server instance
        assert server.server is not None
        assert server.orchestrator is not None

    def test_server_has_all_handler_methods(self):
        """Test that server has all four tool handler methods."""
        server = MCPServer()

        # Check that all handler methods exist
        assert hasattr(server, "_handle_analyze_frameworks")
        assert hasattr(server, "_handle_analyze_libraries")
        assert hasattr(server, "_handle_extract_strings")
        assert hasattr(server, "_handle_infer_language")

        # Check that they are callable
        assert callable(server._handle_analyze_frameworks)
        assert callable(server._handle_analyze_libraries)
        assert callable(server._handle_extract_strings)
        assert callable(server._handle_infer_language)


class TestMCPServerToolHandlers:
    """Test each tool handler with valid inputs."""

    @pytest.fixture
    def temp_exe_file(self):
        """Create a temporary executable file for testing."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".exe") as tmp:
            # Write minimal PE header
            tmp.write(b"MZ" + b"\x00" * 100)
            tmp_path = tmp.name

        yield tmp_path

        # Cleanup
        Path(tmp_path).unlink(missing_ok=True)

    def test_analyze_frameworks_with_valid_file(self, temp_exe_file):
        """Test analyze_frameworks handler with valid file."""
        server = MCPServer()

        result = asyncio.run(
            server._handle_analyze_frameworks({"file_path": temp_exe_file})
        )

        # Should return a list with one TextContent
        assert len(result) == 1
        assert result[0].type == "text"

        # Parse response
        response = json.loads(result[0].text)

        # Should have frameworks key (even if empty) or error
        assert "frameworks" in response or "error" in response

    def test_analyze_libraries_with_valid_file(self, temp_exe_file):
        """Test analyze_libraries handler with valid file."""
        server = MCPServer()

        result = asyncio.run(
            server._handle_analyze_libraries({"file_path": temp_exe_file})
        )

        # Should return a list with one TextContent
        assert len(result) == 1
        assert result[0].type == "text"

        # Parse response
        response = json.loads(result[0].text)

        # Should have analysis key or error
        assert "analysis" in response or "error" in response

    def test_extract_strings_with_valid_file(self, temp_exe_file):
        """Test extract_strings handler with valid file."""
        server = MCPServer()

        result = asyncio.run(
            server._handle_extract_strings({"file_path": temp_exe_file})
        )

        # Should return a list with one TextContent
        assert len(result) == 1
        assert result[0].type == "text"

        # Parse response
        response = json.loads(result[0].text)

        # Should have strings key or error
        assert "strings" in response or "error" in response

    def test_infer_language_with_valid_file(self, temp_exe_file):
        """Test infer_language handler with valid file."""
        server = MCPServer()

        result = asyncio.run(
            server._handle_infer_language({"file_path": temp_exe_file})
        )

        # Should return a list with one TextContent
        assert len(result) == 1
        assert result[0].type == "text"

        # Parse response
        response = json.loads(result[0].text)

        # Should have inference key or error
        assert "inference" in response or "error" in response


class TestMCPServerErrorHandling:
    """Test tool handlers with invalid file paths."""

    def test_analyze_frameworks_with_missing_file(self):
        """Test analyze_frameworks with non-existent file."""
        server = MCPServer()

        result = asyncio.run(
            server._handle_analyze_frameworks({"file_path": "/nonexistent/file.exe"})
        )

        # Should return error
        response = json.loads(result[0].text)
        assert "error" in response
        assert response["error"]["type"] == "FileNotFoundError"

    def test_analyze_libraries_with_missing_file(self):
        """Test analyze_libraries with non-existent file."""
        server = MCPServer()

        result = asyncio.run(
            server._handle_analyze_libraries({"file_path": "/nonexistent/file.exe"})
        )

        # Should return error
        response = json.loads(result[0].text)
        assert "error" in response
        assert response["error"]["type"] == "FileNotFoundError"

    def test_extract_strings_with_missing_file(self):
        """Test extract_strings with non-existent file."""
        server = MCPServer()

        result = asyncio.run(
            server._handle_extract_strings({"file_path": "/nonexistent/file.exe"})
        )

        # Should return error
        response = json.loads(result[0].text)
        assert "error" in response
        assert response["error"]["type"] == "FileNotFoundError"

    def test_infer_language_with_missing_file(self):
        """Test infer_language with non-existent file."""
        server = MCPServer()

        result = asyncio.run(
            server._handle_infer_language({"file_path": "/nonexistent/file.exe"})
        )

        # Should return error
        response = json.loads(result[0].text)
        assert "error" in response
        assert response["error"]["type"] == "FileNotFoundError"

    def test_handler_with_invalid_path_type(self):
        """Test handler with invalid path type."""
        server = MCPServer()

        result = asyncio.run(server._handle_analyze_frameworks({"file_path": 12345}))

        # Should return validation error
        response = json.loads(result[0].text)
        assert "error" in response
        assert response["error"]["type"] == "ValidationError"

    def test_handler_with_empty_path(self):
        """Test handler with empty path."""
        server = MCPServer()

        result = asyncio.run(server._handle_analyze_frameworks({"file_path": ""}))

        # Should return validation error
        response = json.loads(result[0].text)
        assert "error" in response
        assert response["error"]["type"] == "ValidationError"


class TestJSONSerialization:
    """Test JSON serialization of results."""

    @pytest.fixture
    def temp_exe_file(self):
        """Create a temporary executable file for testing."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".exe") as tmp:
            # Write minimal PE header
            tmp.write(b"MZ" + b"\x00" * 100)
            tmp_path = tmp.name

        yield tmp_path

        # Cleanup
        Path(tmp_path).unlink(missing_ok=True)

    def test_all_responses_are_valid_json(self, temp_exe_file):
        """Test that all tool responses produce valid JSON."""
        server = MCPServer()

        handlers = [
            server._handle_analyze_frameworks,
            server._handle_analyze_libraries,
            server._handle_extract_strings,
            server._handle_infer_language,
        ]

        for handler in handlers:
            result = asyncio.run(handler({"file_path": temp_exe_file}))

            # Should be able to parse as JSON
            response = json.loads(result[0].text)
            assert isinstance(response, dict)

    def test_error_responses_are_valid_json(self):
        """Test that error responses produce valid JSON."""
        server = MCPServer()

        handlers = [
            server._handle_analyze_frameworks,
            server._handle_analyze_libraries,
            server._handle_extract_strings,
            server._handle_infer_language,
        ]

        for handler in handlers:
            result = asyncio.run(handler({"file_path": "/nonexistent/file.exe"}))

            # Should be able to parse as JSON
            response = json.loads(result[0].text)
            assert isinstance(response, dict)
            assert "error" in response
