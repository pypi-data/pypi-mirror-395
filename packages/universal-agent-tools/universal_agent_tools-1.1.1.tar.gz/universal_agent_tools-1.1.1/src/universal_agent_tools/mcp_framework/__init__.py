"""
MCP Server Framework

Provides base classes and utilities for creating MCP-compliant servers.
Follows MCP spec (November 2025).
"""

from .base_server import BaseMCPServer
from .tool_decorator import mcp_tool

__all__ = [
    "BaseMCPServer",
    "mcp_tool",
]

