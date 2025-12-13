"""
Main Chunker

Responsibility: Coordinate chunking using appropriate strategy per file type.
Follows Strategy Pattern for different chunking algorithms.
"""

from typing import List, Dict, Protocol
from pathlib import Path

from .file_type_detector import FileTypeDetector
from .python_chunker import PythonChunker
from .yaml_chunker import YamlChunker
from .markdown_chunker import MarkdownChunker
from .json_chunker import JsonChunker
from .generic_chunker import GenericChunker


class ChunkingStrategy(Protocol):
    """Protocol for chunking strategies - follows Dependency Inversion Principle."""
    
    def chunk(self, content: str, file_path: str) -> List[Dict]:
        """Chunk content and return list of chunk dictionaries."""
        ...


class Chunker:
    """
    Main chunker that dispatches to appropriate strategy.
    
    Follows Strategy Pattern and Open/Closed Principle.
    """
    
    def __init__(self):
        """Initialize chunker with default strategies."""
        self._strategies = {
            "python": PythonChunker(),
            "yaml": YamlChunker(),
            "markdown": MarkdownChunker(),
            "json": JsonChunker(),
        }
        self._default_strategy = GenericChunker()
    
    def chunk(self, content: str, file_path: str) -> List[Dict]:
        """
        Chunk content based on file type.
        
        Args:
            content: File content as string
            file_path: Path to file (used for type detection)
            
        Returns:
            List of chunk dictionaries with:
            - type: Chunk type (class, function, yaml_section, etc.)
            - name: Chunk name
            - content: Chunk content
            - line_start: Starting line number
            - line_end: Ending line number
            - docstring: Optional docstring/description
        """
        file_type = FileTypeDetector.detect(file_path)
        strategy = self._strategies.get(file_type, self._default_strategy)
        return strategy.chunk(content, file_path)
    
    def register_strategy(self, file_type: str, strategy: ChunkingStrategy):
        """
        Register a custom chunking strategy.
        
        Follows Open/Closed Principle - can extend without modifying core.
        
        Args:
            file_type: File type identifier
            strategy: ChunkingStrategy instance
        """
        self._strategies[file_type] = strategy

