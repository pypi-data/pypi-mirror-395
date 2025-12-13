"""
Composable enrichment handlers for tenant-aware compilation.

This module provides enrichment handlers that can be composed to create
tenant-specific agent configurations with isolated storage and policies.

Example:
    ```python
    from universal_agent_tools.patterns import create_tenant_agent

    compiled_path = create_tenant_agent(
        tenant_id="acme-corp",
        tenant_config={"name": "ACME", "retention": 30, "tools": ["research"]},
        base_manifest_path="manifest.yaml",
    )
    ```
"""

from typing import Any, Dict, List, Optional

from universal_agent_nexus.enrichment import (
    ComposableEnrichmentStrategy,
    EnrichmentHandler,
    create_custom_enrichment_strategy,
)


class TenantIsolationHandler(EnrichmentHandler):
    """Inject tenant-specific metadata and policies.

    This handler implements the Strategy Pattern and follows the Open/Closed Principle,
    allowing extension through composition without modification.

    Example:
        ```python
        handler = TenantIsolationHandler(
            tenant_id="acme",
            tenant_config={"name": "ACME Corp", "retention": 30}
        )
        enriched_manifest = handler.handle(manifest, role, domains, policies, mixins)
        ```
    """

    def __init__(self, tenant_id: str, tenant_config: Dict[str, Any]):
        """Initialize tenant isolation handler.

        Args:
            tenant_id: Unique identifier for the tenant
            tenant_config: Configuration dictionary with tenant-specific settings
        """
        self.tenant_id = tenant_id
        self.tenant_config = tenant_config

    def handle(
        self,
        manifest: Dict[str, Any],
        role: Optional[Dict[str, Any]],
        domains: List[Dict[str, Any]],
        policies: List[Dict[str, Any]],
        mixins: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Enrich manifest with tenant isolation metadata and policies.

        Args:
            manifest: The base manifest dictionary
            role: Optional role definition
            domains: List of domain definitions
            policies: List of policy definitions
            mixins: List of mixin definitions

        Returns:
            Enriched manifest with tenant-specific metadata and policies
        """
        manifest.setdefault("metadata", {})
        manifest["metadata"].update(
            {
                "tenant_id": self.tenant_id,
                "tenant_name": self.tenant_config.get("name"),
                "data_retention_days": self.tenant_config.get("retention"),
                "allowed_tools": self.tenant_config.get("tools", []),
            }
        )

        manifest.setdefault("policies", [])
        manifest["policies"].append(
            {
                "name": f"tenant_{self.tenant_id}_isolation",
                "target_pattern": "execute_*",
                "action": "add_tenant_context",
                "context": {
                    "tenant_id": self.tenant_id,
                    "isolated_db": f"tenant_{self.tenant_id}",
                },
            }
        )

        return manifest


class VectorDBIsolationHandler(EnrichmentHandler):
    """Map tools to tenant-specific vector stores.

    This handler ensures that each tenant's vector database operations are isolated
    by mapping tool configurations to tenant-specific vector store paths.

    Example:
        ```python
        handler = VectorDBIsolationHandler({
            "acme": "/vectorstores/acme/embeddings.sqlite",
            "beta": "/vectorstores/beta/embeddings.sqlite"
        })
        enriched_manifest = handler.handle(manifest, role, domains, policies, mixins)
        ```
    """

    def __init__(self, vector_store_mapping: Dict[str, str]):
        """Initialize vector DB isolation handler.

        Args:
            vector_store_mapping: Dictionary mapping tenant_id to vector store path
        """
        self.vector_store_mapping = vector_store_mapping

    def handle(
        self,
        manifest: Dict[str, Any],
        role: Optional[Dict[str, Any]],
        domains: List[Dict[str, Any]],
        policies: List[Dict[str, Any]],
        mixins: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Enrich manifest with tenant-specific vector store mappings.

        Args:
            manifest: The base manifest dictionary
            role: Optional role definition
            domains: List of domain definitions
            policies: List of policy definitions
            mixins: List of mixin definitions

        Returns:
            Enriched manifest with tenant-specific vector store configurations
        """
        if "tools" in manifest:
            for tool in manifest["tools"]:
                tenant_id = manifest.get("metadata", {}).get("tenant_id")
                if tenant_id and "vector_store" in tool.get("config", {}):
                    tool["config"]["vector_store"] = self.vector_store_mapping.get(
                        tenant_id, f"/vectorstores/{tenant_id}"
                    )

        return manifest


def create_tenant_agent(
    tenant_id: str,
    tenant_config: Dict[str, Any],
    base_manifest_path: str,
) -> str:
    """Compile a tenant-specific agent with isolated storage and policies.

    This function composes multiple enrichment handlers to create a complete
    tenant-isolated agent configuration.

    Args:
        tenant_id: Unique identifier for the tenant
        tenant_config: Configuration dictionary with tenant-specific settings
        base_manifest_path: Path to the base manifest YAML file

    Returns:
        Path to the compiled agent code

    Example:
        ```python
        compiled_path = create_tenant_agent(
            tenant_id="acme-corp",
            tenant_config={"name": "ACME", "retention": 30, "tools": ["research"]},
            base_manifest_path="manifest.yaml",
        )
        ```
    """
    from universal_agent_fabric import NexusEnricher
    from universal_agent_nexus.compiler import compile

    strategy: ComposableEnrichmentStrategy = create_custom_enrichment_strategy(
        handlers=[
            TenantIsolationHandler(tenant_id, tenant_config),
            VectorDBIsolationHandler({tenant_id: f"/vectorstores/{tenant_id}/embeddings.sqlite"}),
        ]
    )

    enricher = NexusEnricher(strategy=strategy)
    enriched_manifest_path = enricher.enrich(
        baseline_path=base_manifest_path,
        output_path=f"/tmp/enriched_{tenant_id}.yaml",
    )

    compiled_path = compile(
        enriched_manifest_path,
        target="langgraph",
        output=f"/agents/tenant_{tenant_id}_agent.py",
    )
    return compiled_path


__all__ = [
    "TenantIsolationHandler",
    "VectorDBIsolationHandler",
    "create_tenant_agent",
]

