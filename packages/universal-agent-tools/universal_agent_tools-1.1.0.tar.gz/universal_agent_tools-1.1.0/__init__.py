"""
Universal Agent Tools

Reusable tools and utilities for Universal Agent stack.

This package provides:
- Pattern libraries for building agents
- Tool integration utilities
- Model configuration
- Observability helpers
- Code analysis and generation tools
"""

# Core utilities
from . import model_config
from . import observability

# Pattern libraries
from . import patterns

# Tool integrations
from . import ollama_tools

# Re-export commonly used items
from .model_config import ModelConfig, ModelProvider
from .observability import setup_observability, trace_runtime_execution
from .patterns import (
    RouteDefinition,
    build_decision_agent_manifest,
    OrganizationAgentFactory,
    build_organization_manifest,
    TenantIsolationHandler,
    create_tenant_agent,
    SelfModifyingAgent,
    deterministic_tool_from_error,
)
from .ollama_tools import (
    MCPTool,
    MCPToolLoader,
    create_llm_with_tools,
    parse_tool_calls_from_content,
)

__version__ = "1.1.0"

__all__ = [
    # Model config
    "ModelConfig",
    "ModelProvider",
    # Observability
    "setup_observability",
    "trace_runtime_execution",
    # Patterns
    "RouteDefinition",
    "build_decision_agent_manifest",
    "OrganizationAgentFactory",
    "build_organization_manifest",
    "TenantIsolationHandler",
    "create_tenant_agent",
    "SelfModifyingAgent",
    "deterministic_tool_from_error",
    # Ollama tools
    "MCPTool",
    "MCPToolLoader",
    "create_llm_with_tools",
    "parse_tool_calls_from_content",
]

