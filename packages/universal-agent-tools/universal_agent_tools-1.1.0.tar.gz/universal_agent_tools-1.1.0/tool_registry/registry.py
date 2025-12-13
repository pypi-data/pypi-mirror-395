"""
Tool Registry

Responsibility: Centralized tool discovery and management.
Follows Singleton Pattern for global registry.
"""

from typing import List, Dict, Optional
import httpx
from .models import ToolDefinition


class ToolRegistry:
    """
    Centralized tool registry for discovering and managing MCP tools.
    
    Follows Single Responsibility Principle - only handles tool discovery/management.
    """
    
    def __init__(self):
        """Initialize empty registry."""
        self._tools: Dict[str, ToolDefinition] = {}
        self._servers: Dict[str, str] = {}
    
    def register_server(self, name: str, url: str):
        """
        Register an MCP server for tool discovery.
        
        Args:
            name: Server identifier
            url: Server URL (e.g., "http://localhost:8000/mcp")
        """
        self._servers[name] = url
    
    def discover_tools(self, server_name: Optional[str] = None) -> List[ToolDefinition]:
        """
        Discover tools from registered MCP servers.
        
        Args:
            server_name: If provided, only discover from this server.
                        If None, discover from all registered servers.
        
        Returns:
            List of discovered tool definitions
        """
        tools = []
        
        servers_to_check = (
            {server_name: self._servers[server_name]} 
            if server_name and server_name in self._servers
            else self._servers
        )
        
        for name, url in servers_to_check.items():
            try:
                # MCP introspection endpoint
                response = httpx.get(f"{url}/tools", timeout=5)
                response.raise_for_status()
                
                tools_data = response.json()
                
                for tool_def in tools_data.get("tools", []):
                    tool = ToolDefinition(
                        name=tool_def["name"],
                        description=tool_def.get("description", ""),
                        server_url=url,
                        server_name=name,
                        input_schema=tool_def.get("inputSchema", {}),
                        protocol="mcp"
                    )
                    tools.append(tool)
                    self._tools[tool.name] = tool
                    
            except Exception as e:
                print(f"Warning: Could not discover tools from {name} ({url}): {e}")
        
        return tools
    
    def get_tool(self, tool_name: str) -> Optional[ToolDefinition]:
        """
        Get a specific tool by name.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            ToolDefinition if found, None otherwise
        """
        return self._tools.get(tool_name)
    
    def list_tools(self) -> List[ToolDefinition]:
        """
        List all discovered tools.
        
        Returns:
            List of all tool definitions
        """
        return list(self._tools.values())
    
    def list_servers(self) -> Dict[str, str]:
        """
        List all registered servers.
        
        Returns:
            Dictionary mapping server names to URLs
        """
        return self._servers.copy()


# Global registry instance (Singleton Pattern)
_registry = ToolRegistry()


def get_registry() -> ToolRegistry:
    """
    Get the global tool registry instance.
    
    Returns:
        Singleton ToolRegistry instance
    """
    return _registry

