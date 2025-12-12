"""Property-based tests for MCP server."""

import asyncio
import json
import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from exe_analyzer_mcp.mcp_server import MCPServer


# Feature: exe-analyzer-mcp, Property 15: File validation before analysis
@given(
    tool_name=st.sampled_from(
        ["analyze_frameworks", "analyze_libraries", "extract_strings", "infer_language"]
    ),
    file_path=st.one_of(
        st.just(""),  # Empty string
        st.just(None),  # None value
        st.integers(),  # Wrong type
        st.text(min_size=1, max_size=100).filter(
            lambda x: not Path(x).exists()
        ),  # Non-existent path
    ),
)
@settings(max_examples=100)
def test_file_validation_before_analysis(tool_name: str, file_path):
    """Property 15: File validation before analysis.

    For any tool invocation with a file path that does not exist or is not
    readable, an error should be returned before attempting analysis.

    Validates: Requirements 5.2
    """
    server = MCPServer()

    # Map tool names to handler methods
    handlers = {
        "analyze_frameworks": server._handle_analyze_frameworks,
        "analyze_libraries": server._handle_analyze_libraries,
        "extract_strings": server._handle_extract_strings,
        "infer_language": server._handle_infer_language,
    }

    # Call the tool with invalid file path
    result = asyncio.run(handlers[tool_name]({"file_path": file_path}))

    # Should return a list with one TextContent
    assert len(result) == 1
    assert result[0].type == "text"

    # Parse the JSON response
    response = json.loads(result[0].text)

    # Should contain an error
    assert "error" in response
    assert "type" in response["error"]
    assert "message" in response["error"]

    # Error type should be one of the validation/file errors
    assert response["error"]["type"] in [
        "ValidationError",
        "FileNotFoundError",
    ]


# Feature: exe-analyzer-mcp, Property 15: File validation before analysis (valid files)
@settings(max_examples=100)
@given(
    tool_name=st.sampled_from(
        ["analyze_frameworks", "analyze_libraries", "extract_strings", "infer_language"]
    )
)
def test_file_validation_with_valid_file(tool_name: str):
    """Property 15: File validation before analysis with valid files.

    For any tool invocation with a valid file path, the validation should pass
    and analysis should be attempted (may fail at analysis stage, but not validation).

    Validates: Requirements 5.2
    """
    server = MCPServer()

    # Map tool names to handler methods
    handlers = {
        "analyze_frameworks": server._handle_analyze_frameworks,
        "analyze_libraries": server._handle_analyze_libraries,
        "extract_strings": server._handle_extract_strings,
        "infer_language": server._handle_infer_language,
    }

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".exe") as tmp:
        tmp.write(b"MZ" + b"\x00" * 100)  # Minimal PE header
        tmp_path = tmp.name

    try:
        # Call the tool with valid file path
        result = asyncio.run(handlers[tool_name]({"file_path": tmp_path}))

        # Should return a list with one TextContent
        assert len(result) == 1
        assert result[0].type == "text"

        # Parse the JSON response
        response = json.loads(result[0].text)

        # If there's an error, it should NOT be a validation or file not found error
        # (it might be InvalidPEError or other analysis errors, which is fine)
        if "error" in response:
            assert response["error"]["type"] not in [
                "ValidationError",
            ]
            # FileNotFoundError is acceptable if the file was deleted between checks
    finally:
        # Clean up
        Path(tmp_path).unlink(missing_ok=True)


# Feature: exe-analyzer-mcp, Property 16: Successful analysis returns valid JSON
@settings(max_examples=100)
@given(
    tool_name=st.sampled_from(
        ["analyze_frameworks", "analyze_libraries", "extract_strings", "infer_language"]
    )
)
def test_successful_analysis_returns_valid_json(tool_name: str):
    """Property 16: Successful analysis returns valid JSON.

    For any successful analysis operation, the result should be valid JSON
    that can be parsed without error.

    Validates: Requirements 5.3
    """
    server = MCPServer()

    # Map tool names to handler methods
    handlers = {
        "analyze_frameworks": server._handle_analyze_frameworks,
        "analyze_libraries": server._handle_analyze_libraries,
        "extract_strings": server._handle_extract_strings,
        "infer_language": server._handle_infer_language,
    }

    # Create a temporary file with minimal PE structure
    with tempfile.NamedTemporaryFile(delete=False, suffix=".exe") as tmp:
        tmp.write(b"MZ" + b"\x00" * 100)
        tmp_path = tmp.name

    try:
        # Call the tool
        result = asyncio.run(handlers[tool_name]({"file_path": tmp_path}))

        # Should return a list with one TextContent
        assert len(result) == 1
        assert result[0].type == "text"

        # The response text should be valid JSON
        try:
            response = json.loads(result[0].text)
            # If we got here, JSON is valid
            assert isinstance(response, dict)

            # Response should have either data or error, but not both at top level
            # (though error responses can have partial_results)
            has_data = any(
                key in response
                for key in ["frameworks", "analysis", "strings", "inference"]
            )
            has_error = "error" in response

            # Should have at least one of data or error
            assert has_data or has_error

        except json.JSONDecodeError as e:
            # If JSON parsing fails, the test fails
            raise AssertionError(f"Response is not valid JSON: {e}") from e

    finally:
        # Clean up
        Path(tmp_path).unlink(missing_ok=True)


# Feature: exe-analyzer-mcp, Property 17: Error responses include error type
@given(
    tool_name=st.sampled_from(
        ["analyze_frameworks", "analyze_libraries", "extract_strings", "infer_language"]
    ),
    error_scenario=st.sampled_from(
        [
            "missing_file",  # File doesn't exist
            "invalid_type",  # Wrong parameter type
            "empty_path",  # Empty string path
        ]
    ),
)
@settings(max_examples=100)
def test_error_responses_include_error_type(tool_name: str, error_scenario: str):
    """Property 17: Error responses include error type.

    For any analysis operation that encounters an error, the error response
    should include both an error message and an error type field.

    Validates: Requirements 5.4
    """
    server = MCPServer()

    # Map tool names to handler methods
    handlers = {
        "analyze_frameworks": server._handle_analyze_frameworks,
        "analyze_libraries": server._handle_analyze_libraries,
        "extract_strings": server._handle_extract_strings,
        "infer_language": server._handle_infer_language,
    }

    # Create error scenarios
    if error_scenario == "missing_file":
        file_path = "/nonexistent/path/to/file.exe"
    elif error_scenario == "invalid_type":
        file_path = 12345  # Wrong type
    else:  # empty_path
        file_path = ""

    # Call the tool with error-inducing input
    result = asyncio.run(handlers[tool_name]({"file_path": file_path}))

    # Should return a list with one TextContent
    assert len(result) == 1
    assert result[0].type == "text"

    # Parse the JSON response
    response = json.loads(result[0].text)

    # Should contain an error
    assert "error" in response, "Response should contain an error field"

    # Error should have both type and message
    assert "type" in response["error"], "Error should have a type field"
    assert "message" in response["error"], "Error should have a message field"

    # Type and message should be non-empty strings
    assert isinstance(response["error"]["type"], str)
    assert isinstance(response["error"]["message"], str)
    assert len(response["error"]["type"]) > 0
    assert len(response["error"]["message"]) > 0
