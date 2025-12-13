"""
Tests for Ollama tools integration.
"""

import pytest
from unittest.mock import Mock, patch
from universal_agent_tools.ollama_tools import (
    MCPToolLoader,
    MCPTool,
    parse_tool_calls_from_content
)


class TestMCPToolLoader:
    """Tests for MCP tool loader."""
    
    @patch("httpx.get")
    def test_load_from_server_success(self, mock_get):
        """Test successful tool loading."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "tools": [
                {
                    "name": "test_tool",
                    "description": "A test tool",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "param": {"type": "string"}
                        }
                    }
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        tools = MCPToolLoader.load_from_server("http://localhost:8000/mcp")
        assert len(tools) == 1
        assert tools[0].name == "test_tool"
    
    @patch("httpx.get")
    def test_load_from_server_failure(self, mock_get):
        """Test handling of server errors."""
        import httpx
        mock_get.side_effect = httpx.HTTPError("Connection failed")
        
        with pytest.raises(httpx.HTTPError):
            MCPToolLoader.load_from_server("http://localhost:8000/mcp")


class TestMCPTool:
    """Tests for MCP tool wrapper."""
    
    def test_tool_creation(self):
        """Test MCP tool creation."""
        tool = MCPTool(
            server_url="http://localhost:8000/mcp",
            tool_name="test_tool",
            input_schema={
                "type": "object",
                "properties": {
                    "param": {"type": "string"}
                }
            },
            name="test_tool",
            description="A test tool"
        )
        assert tool.name == "test_tool"
        assert tool.description == "A test tool"
    
    @patch("httpx.post")
    def test_tool_execution(self, mock_post):
        """Test tool execution."""
        mock_response = Mock()
        mock_response.json.return_value = {"content": "result"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        tool = MCPTool(
            server_url="http://localhost:8000/mcp",
            tool_name="test_tool",
            input_schema={},
            name="test_tool"
        )
        
        result = tool._run(param="value")
        assert result == "result"


class TestToolParser:
    """Tests for tool call parsing."""
    
    def test_parse_json_tool_call(self):
        """Test parsing tool call from JSON."""
        content = '{"name": "test_tool", "arguments": {"param": "value"}}'
        tool = Mock()
        tool.name = "test_tool"
        tools = [tool]
        
        tool_calls = parse_tool_calls_from_content(content, tools)
        assert len(tool_calls) == 1
        assert tool_calls[0]["name"] == "test_tool"
    
    def test_parse_embedded_json(self):
        """Test parsing tool call embedded in text."""
        content = 'Some text {"name": "test_tool", "arguments": {}} more text'
        tool = Mock()
        tool.name = "test_tool"
        tools = [tool]
        
        tool_calls = parse_tool_calls_from_content(content, tools)
        assert len(tool_calls) == 1
    
    def test_parse_no_tool_call(self):
        """Test parsing content with no tool calls."""
        content = "Just regular text"
        tools = []
        
        tool_calls = parse_tool_calls_from_content(content, tools)
        assert len(tool_calls) == 0

