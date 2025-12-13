"""
Generic Chunker

Responsibility: Fallback chunking strategy for any file type.
Chunks by lines with configurable size and overlap.
"""

from typing import List, Dict
from pathlib import Path


class GenericChunker:
    """
    Generic chunking strategy - chunks by lines with overlap.
    
    Used as fallback for unsupported file types or when
    format-specific chunking fails.
    """
    
    def __init__(self, chunk_size: int = 80, overlap: int = 10, small_file_threshold: int = 100):
        """
        Initialize generic chunker.
        
        Args:
            chunk_size: Number of lines per chunk
            overlap: Number of lines to overlap between chunks
            small_file_threshold: Files with fewer lines are kept as single chunk
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.small_file_threshold = small_file_threshold
    
    def chunk(self, content: str, file_path: str) -> List[Dict]:
        """
        Chunk content by lines with overlap.
        
        Args:
            content: File content
            file_path: Path to file
            
        Returns:
            List of chunk dictionaries
        """
        lines = content.split('\n')
        
        # For small files, keep as single chunk
        if len(lines) <= self.small_file_threshold:
            return [{
                "type": self._get_file_type(file_path),
                "name": Path(file_path).name,
                "content": content,
                "line_start": 1,
                "line_end": len(lines),
                "docstring": ""
            }]
        
        # For larger files, chunk with overlap
        chunks = []
        i = 0
        chunk_num = 1
        
        while i < len(lines):
            end = min(i + self.chunk_size, len(lines))
            chunk_content = '\n'.join(lines[i:end])
            
            chunks.append({
                "type": self._get_file_type(file_path),
                "name": f"{Path(file_path).stem}_part{chunk_num}",
                "content": chunk_content,
                "line_start": i + 1,
                "line_end": end,
                "docstring": ""
            })
            
            i += self.chunk_size - self.overlap
            chunk_num += 1
        
        return chunks
    
    def _get_file_type(self, file_path: str) -> str:
        """Get file type from path for chunk type."""
        from .file_type_detector import FileTypeDetector
        return FileTypeDetector.detect(file_path)

