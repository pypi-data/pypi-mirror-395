"""
MCP Tool Decorator

Responsibility: Provide decorator for easy tool registration.
Simplifies tool definition syntax.
"""

from typing import Callable, Dict, Any
from functools import wraps


def mcp_tool(
    name: str,
    description: str,
    input_schema: Dict[str, Any]
):
    """
    Decorator for MCP tool registration.
    
    Usage:
        @mcp_tool(
            name="my_tool",
            description="Does something",
            input_schema={"type": "object", "properties": {...}}
        )
        async def my_tool_handler(request: ToolRequest):
            return {"content": "result"}
    
    Args:
        name: Tool name
        description: Tool description
        input_schema: JSON Schema for inputs
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        
        # Attach metadata for registration
        wrapper._mcp_tool_name = name
        wrapper._mcp_tool_description = description
        wrapper._mcp_tool_schema = input_schema
        
        return wrapper
    return decorator

