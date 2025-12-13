"""
Tests for tool registry.
"""

import pytest
from unittest.mock import Mock, patch
from universal_agent_tools.tool_registry import (
    ToolRegistry,
    ToolDefinition,
    get_registry
)


class TestToolRegistry:
    """Tests for tool registry."""
    
    def test_register_server(self):
        """Test server registration."""
        registry = ToolRegistry()
        registry.register_server("test", "http://localhost:8000/mcp")
        assert "test" in registry.list_servers()
    
    @patch("httpx.get")
    def test_discover_tools(self, mock_get):
        """Test tool discovery."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "tools": [
                {
                    "name": "test_tool",
                    "description": "A test",
                    "inputSchema": {}
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        registry = ToolRegistry()
        registry.register_server("test", "http://localhost:8000/mcp")
        tools = registry.discover_tools()
        
        assert len(tools) == 1
        assert tools[0].name == "test_tool"
    
    def test_get_tool(self):
        """Test getting tool by name."""
        registry = ToolRegistry()
        tool = ToolDefinition(
            name="test_tool",
            description="Test",
            server_url="http://localhost:8000/mcp",
            server_name="test",
            input_schema={}
        )
        registry._tools["test_tool"] = tool
        
        retrieved = registry.get_tool("test_tool")
        assert retrieved == tool
        assert registry.get_tool("nonexistent") is None


class TestToolDefinition:
    """Tests for tool definition model."""
    
    def test_tool_definition_creation(self):
        """Test creating tool definition."""
        tool = ToolDefinition(
            name="test_tool",
            description="A test tool",
            server_url="http://localhost:8000/mcp",
            server_name="test",
            input_schema={"type": "object"}
        )
        assert tool.name == "test_tool"
        assert tool.protocol == "mcp"


class TestGetRegistry:
    """Tests for global registry singleton."""
    
    def test_singleton_pattern(self):
        """Test that get_registry returns same instance."""
        registry1 = get_registry()
        registry2 = get_registry()
        assert registry1 is registry2

