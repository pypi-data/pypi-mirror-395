"""
Self-modifying agent helpers for runtime-driven tool generation.

This module provides utilities for creating agents that can evolve themselves
by generating new tools based on execution failures.

Example:
    ```python
    from universal_agent_tools.patterns import SelfModifyingAgent, ExecutionLog, deterministic_tool_from_error

    agent = SelfModifyingAgent("manifest.yaml")
    log = ExecutionLog(failed_queries=["query1", "query2", "query3"])

    tool = agent.analyze_and_generate_tool(
        log,
        deterministic_tool_from_error,
        failure_threshold=3
    )

    if tool:
        agent.register_generated_tool(tool, "contains(output, 'error')")
        agent.compile("evolved_agent.py")
    ```
"""

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

from universal_agent_nexus.compiler import generate, parse
from universal_agent_nexus.ir import EdgeIR, ManifestIR, NodeIR, NodeKind, ToolIR
from universal_agent_nexus.ir.visitor import DefaultIRVisitor


@dataclass
class ExecutionLog:
    """Lightweight execution log used to decide whether to evolve the agent.

    Attributes:
        failed_queries: List of queries that failed during execution
        decision_hint: Optional hint about what decision led to the failure
    """

    failed_queries: List[str]
    decision_hint: Optional[str] = None


class ToolGenerationVisitor(DefaultIRVisitor):
    """Tracks tool usage in a manifest IR for analysis or reporting.

    This visitor implements the Visitor Pattern to traverse the IR and collect
    statistics about tool usage.

    Example:
        ```python
        visitor = ToolGenerationVisitor()
        visitor.visit(manifest_ir)
        print(visitor.tool_call_counts)
        ```
    """

    def __init__(self) -> None:
        """Initialize visitor with empty tool call counts."""
        self.tool_call_counts: Dict[str, int] = {}

    def visit_tool(self, tool: ToolIR) -> None:  # type: ignore[override]
        """Visit a tool node and increment its call count.

        Args:
            tool: The ToolIR node being visited
        """
        self.tool_call_counts[tool.name] = self.tool_call_counts.get(tool.name, 0) + 1


class SelfModifyingAgent:
    """Utility for evolving manifests with newly generated tools.

    This class follows the Single Responsibility Principle by focusing solely
    on agent evolution through tool generation and registration.

    Example:
        ```python
        agent = SelfModifyingAgent("manifest.yaml")
        tool = ToolIR(name="new_tool", protocol="mcp", config={})
        agent.register_generated_tool(tool, "condition")
        agent.compile("evolved.py")
        ```
    """

    def __init__(self, manifest_path: str):
        """Initialize self-modifying agent with a manifest.

        Args:
            manifest_path: Path to the manifest YAML file
        """
        self.manifest_path = manifest_path
        self.ir: ManifestIR = parse(manifest_path)

    def analyze_and_generate_tool(
        self,
        execution_log: ExecutionLog,
        tool_generator: Callable[[str], ToolIR],
        failure_threshold: int = 3,
    ) -> Optional[ToolIR]:
        """Generate a tool from the most common failure if threshold is met.

        This method implements the Open/Closed Principle by accepting a tool_generator
        function, allowing different generation strategies without modifying the class.

        Args:
            execution_log: Log of failed queries
            tool_generator: Function that generates a ToolIR from an error message
            failure_threshold: Minimum number of failures required to generate a tool

        Returns:
            Generated ToolIR if threshold is met, None otherwise
        """
        if len(execution_log.failed_queries) < failure_threshold:
            return None

        common_failure = execution_log.failed_queries[-1]
        return tool_generator(common_failure)

    def register_generated_tool(
        self,
        tool: ToolIR,
        condition_expression: str,
        label: Optional[str] = None,
    ) -> None:
        """Inject the tool into the manifest and wire it to the router and formatter.

        This method follows the Dependency Inversion Principle by working with
        the IR abstraction rather than concrete implementations.

        Args:
            tool: The tool to register
            condition_expression: Expression for routing to this tool
            label: Optional label for the execution node
        """
        self.ir.tools.append(tool)

        for graph in self.ir.graphs:
            router = next((node for node in graph.nodes if node.kind == NodeKind.ROUTER), None)
            formatter = next((node for node in graph.nodes if node.kind == NodeKind.TASK), None)

            if not router:
                continue

            exec_node = NodeIR(
                id=f"{tool.name}_exec",
                kind=NodeKind.TOOL,
                tool_ref=tool.name,
                label=label or f"Execute {tool.name}",
            )
            graph.nodes.append(exec_node)

            graph.edges.append(
                EdgeIR(
                    from_node=router.id,
                    to_node=exec_node.id,
                    condition={"expression": condition_expression},
                )
            )

            if formatter:
                graph.edges.append(
                    EdgeIR(
                        from_node=exec_node.id,
                        to_node=formatter.id,
                    )
                )

    def compile(self, output_path: str, target: str = "langgraph") -> str:
        """Compile the evolved manifest to code for the requested runtime.

        Args:
            output_path: Path where compiled code should be written
            target: Target runtime (e.g., "langgraph", "aws", "mcp")

        Returns:
            Path to the compiled code file
        """
        compiled_code = generate(self.ir, target=target)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(compiled_code)
        return output_path


def deterministic_tool_from_error(error_msg: str, name_prefix: str = "repair") -> ToolIR:
    """Create a deterministic MCP tool definition from an error message.

    This function implements a deterministic naming strategy to ensure that
    the same error message always generates the same tool name.

    Args:
        error_msg: The error message to base the tool on
        name_prefix: Prefix for the tool name (default: "repair")

    Returns:
        A ToolIR configured to handle the specified error pattern

    Example:
        ```python
        tool = deterministic_tool_from_error("Connection timeout", name_prefix="fix")
        # Creates tool: fix_connection-timeout
        ```
    """
    safe_suffix = error_msg.lower().replace(" ", "-").replace("'", "")[:32]
    return ToolIR(
        name=f"{name_prefix}_{safe_suffix}",
        protocol="mcp",
        description="Auto-generated repair tool derived from execution failures.",
        config={
            "command": "python",
            "args": ["-m", "mcp_toolkit.repair"],
            "env": {"ERROR_PATTERN": error_msg},
        },
    )


__all__ = [
    "ExecutionLog",
    "ToolGenerationVisitor",
    "SelfModifyingAgent",
    "deterministic_tool_from_error",
]

