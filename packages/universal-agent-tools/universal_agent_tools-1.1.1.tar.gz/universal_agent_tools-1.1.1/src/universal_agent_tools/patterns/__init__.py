"""
Advanced patterns for building Universal Agent architectures.

This module provides reusable patterns for:
- Router construction (single and multi-decision)
- Organization scaffolding (hierarchical agent graphs)
- Tenant-aware enrichment
- Self-modifying agents

All patterns follow SOLID principles and are production-ready.
"""

from .router import RouteDefinition, build_decision_agent_manifest
from .scaffolding import OrganizationAgentFactory, build_organization_manifest
from .enrichment import (
    TenantIsolationHandler,
    VectorDBIsolationHandler,
    create_tenant_agent,
)
from .self_modifying import (
    ExecutionLog,
    ToolGenerationVisitor,
    SelfModifyingAgent,
    deterministic_tool_from_error,
)

__all__ = [
    # Router patterns
    "RouteDefinition",
    "build_decision_agent_manifest",
    # Scaffolding
    "OrganizationAgentFactory",
    "build_organization_manifest",
    # Enrichment
    "TenantIsolationHandler",
    "VectorDBIsolationHandler",
    "create_tenant_agent",
    # Self-modifying
    "ExecutionLog",
    "ToolGenerationVisitor",
    "SelfModifyingAgent",
    "deterministic_tool_from_error",
]

__version__ = "1.1.0"

