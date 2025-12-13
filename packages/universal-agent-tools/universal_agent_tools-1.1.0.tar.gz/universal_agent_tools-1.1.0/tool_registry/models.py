"""
Tool Definition Models

Responsibility: Define data models for tool definitions.
Single Responsibility - only data structures.
"""

from pydantic import BaseModel
from typing import Dict, Any


class ToolDefinition(BaseModel):
    """
    Standardized tool definition.
    
    Follows Data Transfer Object pattern.
    """
    name: str
    description: str
    server_url: str
    server_name: str
    input_schema: Dict[str, Any]
    protocol: str = "mcp"

