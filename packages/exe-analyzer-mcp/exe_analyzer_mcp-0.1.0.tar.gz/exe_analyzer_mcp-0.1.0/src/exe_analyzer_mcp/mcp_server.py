"""MCP server implementation for exe-analyzer-mcp."""

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from exe_analyzer_mcp.analysis_orchestrator import AnalysisOrchestrator


class MCPServer:
    """MCP server that provides executable analysis tools."""

    def __init__(self):
        """Initialize the MCP server with analysis orchestrator."""
        self.server = Server("exe-analyzer-mcp")
        self.orchestrator = AnalysisOrchestrator()
        self._register_tools()

    def _register_tools(self) -> None:
        """Register all analysis tools with the MCP server."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List all available analysis tools."""
            return [
                Tool(
                    name="analyze_frameworks",
                    description=(
                        "Detect frameworks used in a Windows executable "
                        "(e.g., .NET, Qt, Electron, wxWidgets, MFC, GTK)"
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the executable file",
                            }
                        },
                        "required": ["file_path"],
                    },
                ),
                Tool(
                    name="analyze_libraries",
                    description=(
                        "Extract and categorize imported libraries from a Windows executable"
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the executable file",
                            }
                        },
                        "required": ["file_path"],
                    },
                ),
                Tool(
                    name="extract_strings",
                    description=(
                        "Extract meaningful strings from a Windows executable "
                        "(URLs, file paths, registry keys, error messages)"
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the executable file",
                            }
                        },
                        "required": ["file_path"],
                    },
                ),
                Tool(
                    name="infer_language",
                    description=(
                        "Infer the programming language used to create a Windows executable"
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the executable file",
                            }
                        },
                        "required": ["file_path"],
                    },
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Handle tool invocation."""
            if name == "analyze_frameworks":
                return await self._handle_analyze_frameworks(arguments)
            elif name == "analyze_libraries":
                return await self._handle_analyze_libraries(arguments)
            elif name == "extract_strings":
                return await self._handle_extract_strings(arguments)
            elif name == "infer_language":
                return await self._handle_infer_language(arguments)
            else:
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(
                            {
                                "error": {
                                    "type": "ToolNotFoundError",
                                    "message": f"Unknown tool: {name}",
                                }
                            }
                        ),
                    )
                ]

    async def _handle_analyze_frameworks(self, arguments: dict) -> list[TextContent]:
        """Handle analyze_frameworks tool invocation."""
        file_path = self._validate_file_path(arguments.get("file_path"))
        if isinstance(file_path, dict):  # Error response
            return [TextContent(type="text", text=json.dumps(file_path))]

        result = self.orchestrator.analyze_frameworks(file_path)

        if result.error:
            return [
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "error": {
                                "type": result.error.error_type,
                                "message": result.error.message,
                                "phase": result.error.phase,
                            }
                        }
                    ),
                )
            ]

        # Convert frameworks to dict
        frameworks_data = [asdict(f) for f in result.frameworks]
        return [
            TextContent(
                type="text",
                text=json.dumps({"frameworks": frameworks_data}, indent=2),
            )
        ]

    async def _handle_analyze_libraries(self, arguments: dict) -> list[TextContent]:
        """Handle analyze_libraries tool invocation."""
        file_path = self._validate_file_path(arguments.get("file_path"))
        if isinstance(file_path, dict):  # Error response
            return [TextContent(type="text", text=json.dumps(file_path))]

        result = self.orchestrator.analyze_libraries(file_path)

        if result.error:
            return [
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "error": {
                                "type": result.error.error_type,
                                "message": result.error.message,
                                "phase": result.error.phase,
                            }
                        }
                    ),
                )
            ]

        # Convert analysis to dict, handling enum categories
        system_libs = []
        for lib in result.analysis.system_libraries:
            lib_dict = asdict(lib)
            lib_dict["category"] = lib.category.value
            system_libs.append(lib_dict)

        external_libs = []
        for lib in result.analysis.external_libraries:
            lib_dict = asdict(lib)
            lib_dict["category"] = lib.category.value
            external_libs.append(lib_dict)

        analysis_data = {
            "system_libraries": system_libs,
            "external_libraries": external_libs,
            "total_imports": result.analysis.total_imports,
        }

        return [
            TextContent(
                type="text",
                text=json.dumps({"analysis": analysis_data}, indent=2),
            )
        ]

    async def _handle_extract_strings(self, arguments: dict) -> list[TextContent]:
        """Handle extract_strings tool invocation."""
        file_path = self._validate_file_path(arguments.get("file_path"))
        if isinstance(file_path, dict):  # Error response
            return [TextContent(type="text", text=json.dumps(file_path))]

        result = self.orchestrator.extract_strings(file_path)

        if result.error:
            return [
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "error": {
                                "type": result.error.error_type,
                                "message": result.error.message,
                                "phase": result.error.phase,
                            }
                        }
                    ),
                )
            ]

        # Convert strings to dict, handling enum keys and values
        strings_by_category = {}
        for category, strings_list in result.strings.strings_by_category.items():
            # Convert enum to string for JSON serialization
            category_key = category.value if hasattr(category, "value") else str(category)
            # Convert each string, replacing category enum with its value
            serialized_strings = []
            for s in strings_list:
                s_dict = asdict(s)
                s_dict["category"] = s.category.value
                serialized_strings.append(s_dict)
            strings_by_category[category_key] = serialized_strings

        strings_data = {
            "strings_by_category": strings_by_category,
            "total_count": result.strings.total_count,
            "truncated": result.strings.truncated,
        }

        return [
            TextContent(
                type="text",
                text=json.dumps({"strings": strings_data}, indent=2),
            )
        ]

    async def _handle_infer_language(self, arguments: dict) -> list[TextContent]:
        """Handle infer_language tool invocation."""
        file_path = self._validate_file_path(arguments.get("file_path"))
        if isinstance(file_path, dict):  # Error response
            return [TextContent(type="text", text=json.dumps(file_path))]

        result = self.orchestrator.infer_language(file_path)

        if result.error:
            return [
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "error": {
                                "type": result.error.error_type,
                                "message": result.error.message,
                                "phase": result.error.phase,
                            }
                        }
                    ),
                )
            ]

        # Convert inference to dict
        inference_data = asdict(result.inference)
        return [
            TextContent(
                type="text",
                text=json.dumps({"inference": inference_data}, indent=2),
            )
        ]

    def _validate_file_path(self, file_path: Any) -> str | Dict[str, Any]:
        """Validate file path parameter.

        Args:
            file_path: The file path to validate

        Returns:
            The validated file path string, or an error dict
        """
        if not file_path:
            return {
                "error": {
                    "type": "ValidationError",
                    "message": "file_path parameter is required",
                }
            }

        if not isinstance(file_path, str):
            return {
                "error": {
                    "type": "ValidationError",
                    "message": "file_path must be a string",
                }
            }

        # Check if file exists and is readable
        path = Path(file_path)
        if not path.exists():
            return {
                "error": {
                    "type": "FileNotFoundError",
                    "message": f"File not found: {file_path}",
                }
            }

        if not path.is_file():
            return {
                "error": {
                    "type": "ValidationError",
                    "message": f"Path is not a file: {file_path}",
                }
            }

        return file_path

    async def run(self) -> None:
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options(),
            )
