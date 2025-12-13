"""
MCP Tool Loader

Responsibility: Discover and load tools from MCP servers via introspection.
Follows Single Responsibility Principle - only handles tool discovery.
"""

from typing import List
import httpx
from langchain_core.tools import BaseTool

from .mcp_tool import MCPTool


class MCPToolLoader:
    """
    Load tools from MCP servers using standardized introspection.
    
    MCP Spec (November 2025):
    - SEP-986: Standardized tool naming
    - Auto-discovery via introspection
    - Standardized schema format
    """
    
    @staticmethod
    def load_from_server(server_url: str, timeout: int = 5) -> List[BaseTool]:
        """
        Load tools from an MCP server via introspection.
        
        Args:
            server_url: MCP server URL (e.g., "http://localhost:8000/mcp")
            timeout: Request timeout in seconds
            
        Returns:
            List of LangChain tools wrapped as MCPTool instances
            
        Raises:
            httpx.HTTPError: If server is unreachable or returns error
        """
        try:
            # MCP introspection endpoint (standardized)
            response = httpx.get(f"{server_url}/tools", timeout=timeout)
            response.raise_for_status()
            
            tools_data = response.json()
            tools = []
            
            for tool_def in tools_data.get("tools", []):
                # Create LangChain tool from MCP tool definition
                tool = MCPTool(
                    server_url=server_url,
                    tool_name=tool_def["name"],
                    input_schema=tool_def.get("inputSchema", {}),
                    name=tool_def["name"],
                    description=tool_def.get("description", "")
                )
                tools.append(tool)
            
            return tools
            
        except httpx.HTTPError as e:
            raise httpx.HTTPError(
                f"Failed to load tools from {server_url}: {e}"
            ) from e
        except Exception as e:
            # Log warning but don't fail completely
            print(f"Warning: Could not load tools from {server_url}: {e}")
            return []

