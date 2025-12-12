#!/usr/bin/env python3
"""
MCP Server for jupyter-switch functionality
Provides a switch_file tool that converts between .md and .ipynb formats
"""

import asyncio
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .switch_between_md_and_ipynb import convert_file

# Create the MCP server
server = Server("jupyter-switch")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available tools for the MCP server
    """
    return [
        Tool(
            name="switch_file",
            description="Convert between Markdown (.md) and Jupyter Notebook (.ipynb) formats. Recommended workflow for editing .ipynb files: 1) First use this tool to convert .ipynb to .md for easier editing, 2) Edit the .md file with your preferred editor, 3) Use this tool again to convert .md back to .ipynb when done.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the input file (.md or .ipynb). The tool automatically detects file type and converts accordingly. For .ipynb editing: first convert to .md, edit, then convert back."
                    }
                },
                "required": ["file_path"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """
    Handle tool calls
    """
    if name != "switch_file":
        raise ValueError(f"Unknown tool: {name}")
    
    if "file_path" not in arguments:
        raise ValueError("Missing required argument: file_path")
    
    file_path = arguments["file_path"]
    
    try:
        result = convert_file(file_path)
        return [TextContent(type="text", text=result)]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def async_main():
    """
    Async main function to run the MCP server
    """
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

def main():
    """
    Synchronous entry point for the MCP server
    """
    asyncio.run(async_main())

if __name__ == "__main__":
    main()