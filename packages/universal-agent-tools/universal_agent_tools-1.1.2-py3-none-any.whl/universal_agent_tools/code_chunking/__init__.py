"""
Code Chunking System

Multi-format intelligent chunking with AST parsing and semantic preservation.
Supports Python, YAML, Markdown, JSON, and generic file types.
"""

from .chunker import Chunker
from .file_type_detector import FileTypeDetector, get_file_type
from .python_chunker import PythonChunker
from .yaml_chunker import YamlChunker
from .markdown_chunker import MarkdownChunker
from .json_chunker import JsonChunker
from .generic_chunker import GenericChunker

__all__ = [
    "Chunker",
    "FileTypeDetector",
    "get_file_type",
    "PythonChunker",
    "YamlChunker",
    "MarkdownChunker",
    "JsonChunker",
    "GenericChunker",
    "chunk_content",
]

# Convenience function
def chunk_content(content: str, file_path: str) -> list:
    """
    Chunk content based on file type.
    
    Args:
        content: File content as string
        file_path: Path to file (used for type detection)
        
    Returns:
        List of chunk dictionaries with type, name, content, line_start, line_end, docstring
    """
    chunker = Chunker()
    return chunker.chunk(content, file_path)

