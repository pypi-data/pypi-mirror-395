"""
Codebase Analyzer

Responsibility: Coordinate codebase analysis using AST parsing, clustering, and PageRank.
Follows Facade Pattern - provides simple interface to complex analysis.
"""

from typing import Dict, List, Optional
from collections import defaultdict

from .ast_parser import ASTParser
from .clustering import SemanticClustering
from .pagerank import PageRankScorer


class CodebaseAnalyzer:
    """
    Analyzes codebase structure for intelligent documentation generation.
    
    Coordinates:
    - AST parsing for structure
    - Dependency graph building
    - Semantic clustering
    - PageRank scoring
    """
    
    def __init__(self):
        """Initialize analyzer with empty state."""
        self.file_metadata: Dict[str, Dict] = {}
        self.dependency_graph = defaultdict(set)  # file -> {imported_files}
        self.reverse_deps = defaultdict(set)  # file -> {files_that_import_this}
        self._ast_parser = ASTParser()
        self._clustering = SemanticClustering()
        self._pagerank = PageRankScorer()
    
    def analyze_structure(
        self,
        files: List[Dict[str, any]],
        file_content_provider: Optional[callable] = None
    ) -> Dict:
        """
        Stage 1: Structural Analysis
        
        Parse AST for all files, extract classes, methods, signatures, dependencies.
        
        Args:
            files: List of file info dicts with keys: path, repo (optional), content (optional)
            file_content_provider: Optional function(file_path) -> content string
            
        Returns:
            Dictionary with analysis results
        """
        for file_info in files:
            file_path = file_info.get("path", "")
            file_type = self._get_file_type(file_path)
            
            if file_type == "python":
                # Get content
                content = file_info.get("content")
                if not content and file_content_provider:
                    content = file_content_provider(file_path)
                
                if content:
                    metadata = self._ast_parser.parse_file(content)
                    if metadata:
                        self.file_metadata[file_path] = metadata
                        # Build dependency graph
                        for imp in metadata.get("imports", []):
                            self.dependency_graph[file_path].add(imp)
                            self.reverse_deps[imp].add(file_path)
        
        # Calculate complexity scores
        for file_path in self.file_metadata:
            self.file_metadata[file_path]["complexity"] = self._calculate_complexity(
                self.file_metadata[file_path]
            )
        
        return {
            "files_analyzed": len(self.file_metadata),
            "total_files": len(files),
            "dependency_graph_size": len(self.dependency_graph),
            "metadata": self.file_metadata
        }
    
    def create_semantic_clusters(self, max_clusters: int = 10) -> Dict:
        """
        Stage 2: Semantic Clustering
        
        Group related components (adapters, runtime, tools, etc.).
        
        Args:
            max_clusters: Maximum number of clusters
            
        Returns:
            Dictionary with cluster information
        """
        if not self.file_metadata:
            return {"error": "Run analyze_structure first"}
        
        return self._clustering.cluster(self.file_metadata, max_clusters)
    
    def build_dependency_graph(self) -> Dict:
        """
        Build dependency graph showing what imports what.
        
        Returns:
            Dictionary with dependency graph structure
        """
        graph = {}
        for file_path in self.file_metadata.keys():
            graph[file_path] = {
                "imports": list(self.dependency_graph.get(file_path, set())),
                "imported_by": list(self.reverse_deps.get(file_path, set())),
                "in_degree": len(self.reverse_deps.get(file_path, set())),
                "out_degree": len(self.dependency_graph.get(file_path, set()))
            }
        
        return {
            "nodes": len(graph),
            "edges": sum(len(v["imports"]) for v in graph.values()),
            "graph": graph
        }
    
    def calculate_pagerank_scores(self, iterations: int = 10) -> Dict:
        """
        Stage 3: PageRank-style Importance Scoring
        
        Identify "hub" modules that many others depend on.
        
        Args:
            iterations: Number of PageRank iterations
            
        Returns:
            Dictionary with PageRank scores
        """
        if not self.dependency_graph:
            return {"error": "Build dependency graph first"}
        
        return self._pagerank.calculate(
            self.dependency_graph,
            self.reverse_deps,
            self.file_metadata,
            iterations
        )
    
    def _calculate_complexity(self, metadata: Dict) -> int:
        """Calculate complexity score (simple heuristic)."""
        score = 0
        score += len(metadata.get("classes", [])) * 5
        score += len(metadata.get("functions", [])) * 2
        score += metadata.get("line_count", 0) // 50
        return score
    
    def _get_file_type(self, file_path: str) -> str:
        """Get file type from path."""
        from universal_agent_tools.code_chunking import FileTypeDetector
        return FileTypeDetector.detect(file_path)


# Global analyzer instance (Singleton Pattern)
_analyzer = None


def get_analyzer() -> CodebaseAnalyzer:
    """Get or create global analyzer instance."""
    global _analyzer
    if _analyzer is None:
        _analyzer = CodebaseAnalyzer()
    return _analyzer

