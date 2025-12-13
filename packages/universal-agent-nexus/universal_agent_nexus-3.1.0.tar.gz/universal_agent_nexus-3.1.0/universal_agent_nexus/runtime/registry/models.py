"""
Tool Definition Models

Responsibility: Define data models for tool definitions.
Follows Single Responsibility Principle - only data structures.
"""

from pydantic import BaseModel
from typing import Dict, Any


class ToolDefinition(BaseModel):
    """
    Standardized tool definition.
    
    Follows Data Transfer Object pattern and provides a clean abstraction
    for tool metadata discovered from MCP servers.
    
    Attributes:
        name: Tool name/identifier
        description: Human-readable tool description
        server_url: URL of the MCP server hosting this tool
        server_name: Name/identifier of the server
        input_schema: JSON schema for tool inputs
        protocol: Communication protocol (default: "mcp")
    """
    name: str
    description: str
    server_url: str
    server_name: str
    input_schema: Dict[str, Any]
    protocol: str = "mcp"

