"""
MCP Tool Wrapper

Responsibility: Wrap MCP tools as LangChain BaseTool instances.
Handles schema conversion and HTTP execution.
"""

from typing import Dict, Any, Optional
import httpx
from langchain_core.tools import BaseTool
from pydantic import create_model


class MCPTool(BaseTool):
    """
    LangChain tool wrapper for MCP tools.
    
    Converts MCP tool definitions (with JSON Schema) into LangChain tools
    that can be used with Ollama and other LLMs via function calling.
    """
    
    def __init__(
        self,
        server_url: str,
        tool_name: str,
        input_schema: Dict[str, Any],
        name: Optional[str] = None,
        description: str = ""
    ):
        """
        Initialize MCP tool wrapper.
        
        Args:
            server_url: Base URL of MCP server
            tool_name: Name of the tool on the server
            input_schema: JSON Schema for tool inputs
            name: LangChain tool name (defaults to tool_name)
            description: Tool description
        """
        # CRITICAL: BaseTool needs args_schema for Ollama tool calling
        # Convert MCP inputSchema to Pydantic model for LangChain
        args_schema = self._create_args_schema(tool_name, input_schema)
        
        # Call parent first (Pydantic models need this)
        super().__init__(
            name=name or tool_name,
            description=description,
            args_schema=args_schema
        )
        
        # Store MCP-specific attributes AFTER super().__init__()
        # Use object.__setattr__ to bypass Pydantic's attribute handling
        object.__setattr__(self, '_server_url', server_url)
        object.__setattr__(self, '_tool_name', tool_name)
        object.__setattr__(self, '_input_schema', input_schema)
    
    @staticmethod
    def _create_args_schema(tool_name: str, input_schema: Dict[str, Any]):
        """
        Create Pydantic model from JSON Schema.
        
        Follows Open/Closed Principle - extensible for new schema types.
        """
        if not input_schema or not input_schema.get("properties"):
            return None
        
        fields = {}
        for prop_name, prop_def in input_schema.get("properties", {}).items():
            prop_type = str  # Default to str
            prop_schema = prop_def.get("type", "string")
            
            if prop_schema == "integer":
                prop_type = int
            elif prop_schema == "boolean":
                prop_type = bool
            elif prop_schema == "number":
                prop_type = float
            elif prop_schema == "array":
                prop_type = list
            
            # Check if required
            required = prop_name in input_schema.get("required", [])
            if required:
                fields[prop_name] = (prop_type, ...)
            else:
                fields[prop_name] = (Optional[prop_type], None)
        
        if fields:
            ArgsModel = create_model(f"{tool_name}_Args", **fields)
            return ArgsModel
        
        return None
    
    def _run(self, **kwargs) -> str:
        """
        Execute MCP tool via HTTP (synchronous).
        
        Args:
            **kwargs: Tool arguments from JSON schema
            
        Returns:
            Tool execution result as string
        """
        try:
            response = httpx.post(
                f"{self._server_url}/tools/{self._tool_name}",
                json=kwargs,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            return result.get("content", str(result))
        except httpx.HTTPError as e:
            return f"HTTP error executing tool: {str(e)}"
        except Exception as e:
            return f"Error executing tool: {str(e)}"
    
    async def _arun(self, **kwargs) -> str:
        """
        Execute MCP tool via HTTP (asynchronous).
        
        Args:
            **kwargs: Tool arguments from JSON schema
            
        Returns:
            Tool execution result as string
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self._server_url}/tools/{self._tool_name}",
                    json=kwargs,
                    timeout=10
                )
                response.raise_for_status()
                result = response.json()
                return result.get("content", str(result))
            except httpx.HTTPError as e:
                return f"HTTP error executing tool: {str(e)}"
            except Exception as e:
                return f"Error executing tool: {str(e)}"

