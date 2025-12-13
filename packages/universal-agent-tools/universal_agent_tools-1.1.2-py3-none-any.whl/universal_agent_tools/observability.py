"""
Observability Helper - Reusable setup for all examples.

Provides consistent observability setup across all Universal Agent examples,
following the Single Responsibility Principle by focusing solely on observability configuration.

This module implements the Dependency Inversion Principle by depending on
abstractions (OpenTelemetry) rather than concrete implementations.
"""

import os
from typing import Optional
from contextlib import asynccontextmanager


def setup_observability(
    service_name: str,
    environment: str = "development",
    otlp_endpoint: Optional[str] = None
) -> bool:
    """
    Setup OpenTelemetry observability for an example.

    This function follows the Open/Closed Principle by being extensible
    through environment variables without modification.

    Args:
        service_name: Name of the service (e.g., "hello-world", "support-chatbot")
        environment: Deployment environment (default: "development")
        otlp_endpoint: OTLP endpoint (default: from env or http://localhost:4317)

    Returns:
        True if observability is available and enabled, False otherwise

    Example:
        ```python
        if setup_observability("my-service"):
            print("Tracing enabled")
        ```
    """
    try:
        from universal_agent_nexus.observability import setup_tracing

        # Get endpoint from env or use default
        if otlp_endpoint is None:
            otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")

        # Set service name in environment for consistency
        os.environ.setdefault("OTEL_SERVICE_NAME", service_name)

        # Setup tracing
        setup_tracing(
            service_name=service_name,
            otlp_endpoint=otlp_endpoint,
            environment=environment
        )

        print(f"[OK] Observability enabled - View traces at http://localhost:16686")
        print(f"   Service: {service_name}, Endpoint: {otlp_endpoint}")
        return True

    except ImportError:
        print("[WARN] Observability module not available - using basic logging")
        return False


@asynccontextmanager
async def trace_runtime_execution(
    execution_id: str,
    graph_name: Optional[str] = None,
    attributes: Optional[dict] = None
):
    """
    Context manager for tracing runtime execution.

    This implements the Strategy Pattern by allowing different tracing strategies
    without modifying the execution code.

    Usage:
        ```python
        async with trace_runtime_execution("exec-001", graph_name="main"):
            result = await runtime.execute(...)
        ```

    Args:
        execution_id: Unique execution identifier
        graph_name: Name of the graph being executed
        attributes: Additional span attributes

    Yields:
        Control to the execution block
    """
    try:
        from universal_agent_nexus.observability import trace_execution

        async with trace_execution(
            span_name="execute_graph",
            execution_id=execution_id,
            graph_name=graph_name,
            attributes=attributes
        ):
            yield

        # Force flush spans to ensure they're sent
        _flush_spans()

    except ImportError:
        # If observability not available, just pass through
        yield


def _flush_spans():
    """Force flush all pending spans."""
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider

        provider = trace.get_tracer_provider()
        if isinstance(provider, TracerProvider):
            # Force flush all span processors
            if hasattr(provider, '_active_span_processor'):
                processor = provider._active_span_processor
                if hasattr(processor, '_span_processors'):
                    for span_processor in processor._span_processors:
                        if hasattr(span_processor, 'force_flush'):
                            span_processor.force_flush()
    except Exception:
        # Silently fail if flush doesn't work
        pass


__all__ = [
    "setup_observability",
    "trace_runtime_execution",
]

