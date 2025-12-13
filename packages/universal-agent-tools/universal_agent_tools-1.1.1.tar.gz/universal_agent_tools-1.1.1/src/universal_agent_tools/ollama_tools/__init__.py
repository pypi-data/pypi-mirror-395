"""
Ollama Tools Integration

Provides working integration between Ollama LLMs and MCP tools via LangChain.
Uses ChatOpenAI with Ollama's OpenAI-compatible /v1 endpoint for proper tool calling.
"""

from .mcp_loader import MCPToolLoader
from .mcp_tool import MCPTool
from .ollama_llm import create_llm_with_tools
from .tool_parser import parse_tool_calls_from_content

__all__ = [
    "MCPToolLoader",
    "MCPTool",
    "create_llm_with_tools",
    "parse_tool_calls_from_content",
]

