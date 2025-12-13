"""
Base MCP Server

Responsibility: Provide base class for MCP-compliant FastAPI servers.
Follows Template Method Pattern for server structure.
"""

from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class ToolRequest(BaseModel):
    """Base request model for tool execution."""
    pass


class BaseMCPServer:
    """
    Base class for MCP-compliant servers.
    
    Follows Template Method Pattern - subclasses define tools,
    base class handles protocol compliance.
    """
    
    def __init__(self, server_name: str, port: int = 8000):
        """
        Initialize MCP server.
        
        Args:
            server_name: Name identifier for this server
            port: Port to run on (default: 8000)
        """
        self.server_name = server_name
        self.port = port
        self.app = FastAPI(title=f"MCP {server_name} Server")
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"]
        )
        self._tools: List[Dict[str, Any]] = []
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup MCP-compliant routes."""
        @self.app.get("/mcp/tools")
        async def list_tools():
            """MCP introspection endpoint."""
            return {"tools": self._tools}
        
        @self.app.get("/health")
        async def health():
            """Health check endpoint."""
            return {
                "status": "ok",
                "server": self.server_name,
                "tools": len(self._tools)
            }
        
        # Tool execution routes are added by register_tool
    
    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        handler: callable
    ):
        """
        Register a tool with the server.
        
        Args:
            name: Tool name
            description: Tool description
            input_schema: JSON Schema for tool inputs
            handler: Async function to handle tool execution
        """
        # Add to tools list
        self._tools.append({
            "name": name,
            "description": description,
            "inputSchema": input_schema
        })
        
        # Create route for tool execution
        @self.app.post(f"/mcp/tools/{name}")
        async def execute_tool(request: ToolRequest):
            """Execute tool."""
            try:
                result = await handler(request)
                if isinstance(result, dict) and "content" in result:
                    return result
                return {"content": str(result)}
            except Exception as e:
                return {"content": f"Error: {str(e)}"}
    
    def get_app(self) -> FastAPI:
        """Get FastAPI app instance."""
        return self.app
    
    def run(self, host: str = "0.0.0.0"):
        """
        Run the server.
        
        Args:
            host: Host to bind to
        """
        import uvicorn
        uvicorn.run(self.app, host=host, port=self.port)

