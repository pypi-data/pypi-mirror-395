"""
PageRank Scorer

Responsibility: Calculate PageRank-style importance scores for code modules.
Single Responsibility - only PageRank algorithm.
"""

from typing import Dict, Set
from collections import defaultdict


class PageRankScorer:
    """
    Calculates PageRank-style importance scores.
    
    Identifies "hub" modules that many others depend on.
    """
    
    def calculate(
        self,
        dependency_graph: Dict[str, Set[str]],
        reverse_deps: Dict[str, Set[str]],
        file_metadata: Dict[str, Dict],
        iterations: int = 10
    ) -> Dict:
        """
        Calculate PageRank scores for files.
        
        Args:
            dependency_graph: file -> {imported_files}
            reverse_deps: file -> {files_that_import_this}
            file_metadata: File metadata with complexity scores
            iterations: Number of PageRank iterations
            
        Returns:
            Dictionary with PageRank scores and top files
        """
        # Initialize scores
        nodes = set(file_metadata.keys())
        scores = {node: 1.0 for node in nodes}
        
        # PageRank algorithm (simplified)
        damping = 0.85
        
        for _ in range(iterations):
            new_scores = {}
            for node in nodes:
                score = (1 - damping) / len(nodes)
                
                # Sum contributions from nodes that link to this one
                for incoming in reverse_deps.get(node, set()):
                    if incoming in nodes:
                        out_degree = len(dependency_graph.get(incoming, set()))
                        if out_degree > 0:
                            score += damping * scores[incoming] / out_degree
                
                new_scores[node] = score
            
            scores = new_scores
        
        # Normalize and combine with complexity
        max_score = max(scores.values()) if scores.values() else 1.0
        final_scores = {}
        
        for node in nodes:
            pagerank = scores[node] / max_score if max_score > 0 else 0
            complexity = file_metadata.get(node, {}).get("complexity", 0)
            # Combined score (weighted)
            final_scores[node] = {
                "pagerank": pagerank,
                "complexity": complexity,
                "combined": pagerank * 0.6 + (complexity / 100) * 0.4,
                "in_degree": len(reverse_deps.get(node, set())),
                "out_degree": len(dependency_graph.get(node, set()))
            }
        
        # Sort by combined score
        top_files = sorted(
            final_scores.items(),
            key=lambda x: x[1]["combined"],
            reverse=True
        )[:20]  # Top 20
        
        return {
            "scores": final_scores,
            "top_files": [{"file": f, "score": s} for f, s in top_files],
            "total_files": len(final_scores)
        }

