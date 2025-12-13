"""
Tool Call Parser

Responsibility: Parse tool calls from Ollama responses when returned in content field.
Handles edge cases where Ollama returns tool calls as JSON in content instead of tool_calls array.
"""

import json
import re
from typing import List, Dict, Any
from langchain_core.tools import BaseTool


def parse_tool_calls_from_content(
    content: str,
    tools: List[BaseTool]
) -> List[Dict[str, Any]]:
    """
    Parse tool calls from JSON content when Ollama returns them in content field.
    
    Ollama's /v1 API sometimes returns tool calls as JSON in content instead of
    the standard tool_calls array. This function extracts and converts them.
    
    Args:
        content: Response content that may contain tool calls
        tools: List of available tools for validation
        
    Returns:
        List of tool call dictionaries with 'name', 'args', and 'id' keys
        Empty list if no tool calls found
    """
    if not content or not isinstance(content, str):
        return []
    
    # Try to parse as JSON directly
    tool_call = _parse_json_tool_call(content, tools)
    if tool_call:
        return [tool_call]
    
    # Try to find JSON in content (might be mixed with text)
    tool_call = _parse_embedded_json_tool_call(content, tools)
    if tool_call:
        return [tool_call]
    
    return []


def _parse_json_tool_call(
    content: str,
    tools: List[BaseTool]
) -> Dict[str, Any]:
    """
    Parse tool call from direct JSON content.
    
    Single Responsibility: Only handles direct JSON parsing.
    """
    try:
        tool_call_data = json.loads(content.strip())
        if isinstance(tool_call_data, dict) and "name" in tool_call_data:
            return _create_tool_call_dict(tool_call_data, tools)
    except (json.JSONDecodeError, AttributeError):
        pass
    
    return {}


def _parse_embedded_json_tool_call(
    content: str,
    tools: List[BaseTool]
) -> Dict[str, Any]:
    """
    Parse tool call from JSON embedded in text content.
    
    Single Responsibility: Only handles embedded JSON extraction.
    """
    # Try to find JSON object with "name" field (handles nested objects)
    # Match from { to matching } accounting for nested braces
    brace_count = 0
    start_idx = -1
    
    for i, char in enumerate(content):
        if char == '{':
            if start_idx == -1:
                start_idx = i
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0 and start_idx != -1:
                # Found complete JSON object
                json_str = content[start_idx:i+1]
                try:
                    tool_call_data = json.loads(json_str)
                    if isinstance(tool_call_data, dict) and "name" in tool_call_data:
                        result = _create_tool_call_dict(tool_call_data, tools)
                        if result:
                            return result
                except (json.JSONDecodeError, AttributeError):
                    pass
                start_idx = -1
    
    return {}


def _create_tool_call_dict(
    tool_call_data: Dict[str, Any],
    tools: List[BaseTool]
) -> Dict[str, Any]:
    """
    Create standardized tool call dictionary.
    
    Single Responsibility: Only creates tool call structure.
    """
    tool_name = tool_call_data.get("name")
    tool_args = tool_call_data.get("arguments", {})
    
    # Validate tool exists
    # Handle both BaseTool objects and Mock objects
    tool = None
    for t in tools:
        tool_name_attr = getattr(t, 'name', None)
        if tool_name_attr == tool_name:
            tool = t
            break
    
    if not tool:
        return {}
    
    return {
        "name": tool_name,
        "args": tool_args,
        "id": f"call_{tool_name}_{hash(str(tool_args))}"
    }

