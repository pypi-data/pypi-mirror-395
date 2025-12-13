"""
Semantic Clustering

Responsibility: Group related code components into semantic clusters.
Single Responsibility - only handles clustering logic.
"""

from typing import Dict, List
from collections import defaultdict


class SemanticClustering:
    """
    Groups related components into semantic clusters.
    
    Follows Single Responsibility Principle - only clustering logic.
    """
    
    def cluster(self, file_metadata: Dict[str, Dict], max_clusters: int = 10) -> Dict:
        """
        Create semantic clusters from file metadata.
        
        Args:
            file_metadata: Dictionary mapping file paths to metadata
            max_clusters: Maximum number of clusters
            
        Returns:
            Dictionary with cluster information
        """
        clusters = defaultdict(list)
        
        for file_path, metadata in file_metadata.items():
            cluster_name = self._infer_cluster(file_path, metadata)
            clusters[cluster_name].append({
                "file": file_path,
                "metadata": metadata
            })
        
        # If too many clusters, merge small ones
        if len(clusters) > max_clusters:
            clusters = self._merge_small_clusters(clusters, max_clusters)
        
        # Generate cluster summaries
        cluster_summaries = {}
        for cluster_name, files in clusters.items():
            cluster_summaries[cluster_name] = {
                "name": cluster_name,
                "files": [f["file"] for f in files],
                "file_count": len(files),
                "total_classes": sum(len(f["metadata"].get("classes", [])) for f in files),
                "total_functions": sum(len(f["metadata"].get("functions", [])) for f in files),
                "description": self._generate_cluster_description(cluster_name, files)
            }
        
        return {
            "clusters": cluster_summaries,
            "total_clusters": len(cluster_summaries)
        }
    
    def _infer_cluster(self, file_path: str, metadata: Dict) -> str:
        """Infer cluster name from file path and content."""
        path_lower = file_path.lower()
        
        # Pattern matching
        if "adapter" in path_lower or "adapters" in path_lower:
            return "adapters"
        elif "runtime" in path_lower or "agent" in path_lower:
            return "runtime"
        elif "compiler" in path_lower or "compile" in path_lower:
            return "compiler"
        elif "tool" in path_lower or "mcp" in path_lower:
            return "tools"
        elif "test" in path_lower:
            return "tests"
        elif "config" in path_lower or "yaml" in path_lower:
            return "configuration"
        elif "doc" in path_lower or "readme" in path_lower:
            return "documentation"
        elif "server" in path_lower or "api" in path_lower:
            return "api"
        else:
            # Check imports for hints
            imports = metadata.get("imports", [])
            if any("fastapi" in imp.lower() or "flask" in imp.lower() for imp in imports):
                return "api"
            elif any("pytest" in imp.lower() or "unittest" in imp.lower() for imp in imports):
                return "tests"
            else:
                return "core"
    
    def _merge_small_clusters(self, clusters: Dict, max_clusters: int) -> Dict:
        """Merge small clusters into 'other' category."""
        sorted_clusters = sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)
        result = {}
        
        # Keep top N-1 clusters
        for i, (name, files) in enumerate(sorted_clusters[:max_clusters - 1]):
            result[name] = files
        
        # Merge rest into "other"
        other_files = []
        for name, files in sorted_clusters[max_clusters - 1:]:
            other_files.extend(files)
        
        if other_files:
            result["other"] = other_files
        
        return result
    
    def _generate_cluster_description(self, cluster_name: str, files: List[Dict]) -> str:
        """Generate a natural language description of a cluster."""
        file_count = len(files)
        total_classes = sum(len(f["metadata"].get("classes", [])) for f in files)
        total_functions = sum(len(f["metadata"].get("functions", [])) for f in files)
        
        descriptions = {
            "adapters": f"Integration layer with {file_count} adapter modules",
            "runtime": f"Agent runtime and execution engine ({file_count} files)",
            "compiler": f"Code generation and compilation logic",
            "tools": f"Tool definitions and MCP servers ({file_count} files)",
            "tests": f"Test suite with {file_count} test files",
            "configuration": f"Configuration and manifest files",
            "documentation": f"Documentation and README files",
            "api": f"API endpoints and server definitions",
            "core": f"Core functionality ({file_count} files, {total_classes} classes, {total_functions} functions)",
            "other": f"Miscellaneous files ({file_count} files)"
        }
        
        return descriptions.get(cluster_name, f"{cluster_name} cluster with {file_count} files")

