"""
Reusable router construction patterns for single- and multi-decision agents.

This module provides utilities for building decision router agents that can
route queries to multiple tools based on LLM decisions.

Example:
    ```python
    from universal_agent_tools.patterns import RouteDefinition, build_decision_agent_manifest

    routes = [
        RouteDefinition(
            name="financial",
            tool_ref="financial_analyzer",
            condition_expression="contains(output, 'financial')"
        ),
        RouteDefinition(
            name="technical",
            tool_ref="technical_researcher",
            condition_expression="contains(output, 'technical')"
        ),
    ]

    manifest = build_decision_agent_manifest(
        agent_name="research-director",
        system_message="Classify query intent and route appropriately.",
        llm="local://qwen3",
        routes=routes,
    )
    ```
"""

from dataclasses import dataclass
from typing import List, Optional

from universal_agent_nexus.ir import EdgeIR, GraphIR, ManifestIR, NodeIR, NodeKind, ToolIR


@dataclass
class RouteDefinition:
    """Defines a routing target for a decision node.

    Attributes:
        name: Unique identifier for this route (used in node IDs)
        tool_ref: Reference to the tool to execute for this route
        condition_expression: Expression to evaluate router output (e.g., "contains(output, 'keyword')")
        label: Optional human-readable label for the execution node
    """

    name: str
    tool_ref: str
    condition_expression: str
    label: Optional[str] = None


def build_decision_agent_manifest(
    agent_name: str,
    system_message: str,
    llm: str,
    routes: List[RouteDefinition],
    formatter_prompt: str = "Format the tool result for the user: {result}",
    tools: Optional[List[ToolIR]] = None,
    version: str = "1.0.0",
) -> ManifestIR:
    """Create a manifest with a single decision node that can route to N tools.

    This function implements the Single Responsibility Principle by focusing
    solely on manifest construction. It creates a complete agent structure with:
    - One router node (makes the decision)
    - N tool execution nodes (one per route)
    - One formatter node (formats the final response)

    Args:
        agent_name: Display and manifest name.
        system_message: System prompt for the router node.
        llm: LLM reference (e.g., ``local://qwen3``).
        routes: A list of RouteDefinition objects describing each decision path.
        formatter_prompt: Prompt used by the final formatting task.
        tools: Optional tool definitions to include with the manifest.
        version: Manifest version string.

    Returns:
        A ManifestIR ready for compilation to LangGraph, AWS, or MCP runtimes.

    Example:
        ```python
        routes = [
            RouteDefinition(
                name="search",
                tool_ref="search_tool",
                condition_expression="contains(output, 'search')"
            )
        ]
        manifest = build_decision_agent_manifest(
            agent_name="search_agent",
            system_message="Route queries appropriately.",
            llm="local://qwen3",
            routes=routes
        )
        ```
    """

    router_node = NodeIR(
        id="analyze_query",
        kind=NodeKind.ROUTER,
        label="Decision Router",
        config={"system_message": system_message, "llm": llm},
    )

    format_node = NodeIR(
        id="format_response",
        kind=NodeKind.TASK,
        label="Format Response",
        config={"prompt": formatter_prompt},
    )

    tool_nodes: List[NodeIR] = []
    edges: List[EdgeIR] = []

    for route in routes:
        node_id = f"{route.name}_exec"
        tool_nodes.append(
            NodeIR(
                id=node_id,
                kind=NodeKind.TOOL,
                tool_ref=route.tool_ref,
                label=route.label or f"Execute {route.name}",
            )
        )

        edges.append(
            EdgeIR(
                from_node=router_node.id,
                to_node=node_id,
                condition={"expression": route.condition_expression},
            )
        )

        edges.append(EdgeIR(from_node=node_id, to_node=format_node.id))

    graph = GraphIR(
        name="main",
        entry_node=router_node.id,
        nodes=[router_node, *tool_nodes, format_node],
        edges=edges,
    )

    return ManifestIR(
        name=agent_name,
        version=version,
        description=f"Decision router agent with {len(routes)} routing paths",
        graphs=[graph],
        tools=tools or [],
    )


__all__ = ["RouteDefinition", "build_decision_agent_manifest"]

