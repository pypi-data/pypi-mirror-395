"""
Markdown Chunker

Responsibility: Chunk Markdown content by headers.
Preserves document structure and hierarchy.
"""

from typing import List, Dict
from pathlib import Path
from .generic_chunker import GenericChunker


class MarkdownChunker:
    """
    Chunks Markdown content by headers (h1, h2, h3).
    
    Each header section becomes a separate chunk.
    """
    
    def chunk(self, content: str, file_path: str) -> List[Dict]:
        """
        Chunk Markdown content by headers.
        
        Args:
            content: Markdown content
            file_path: Path to Markdown file
            
        Returns:
            List of chunk dictionaries
        """
        chunks = []
        lines = content.split('\n')
        
        current_header = Path(file_path).stem
        current_start = 0
        current_level = 0
        
        for i, line in enumerate(lines):
            # Check for markdown headers
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                header_text = line.lstrip('#').strip()
                
                # Save previous chunk (only for h1, h2, h3)
                if level <= 3 and current_start < i:
                    chunk = self._create_header_chunk(
                        lines, current_start, i, current_header, current_level
                    )
                    if chunk:
                        chunks.append(chunk)
                
                if level <= 3:
                    current_header = header_text
                    current_start = i
                    current_level = level
        
        # Don't forget the last chunk
        chunk = self._create_header_chunk(
            lines, current_start, len(lines), current_header, current_level
        )
        if chunk:
            chunks.append(chunk)
        
        return chunks if chunks else GenericChunker().chunk(content, file_path)
    
    def _create_header_chunk(
        self,
        lines: List[str],
        start: int,
        end: int,
        header: str,
        level: int
    ) -> Dict:
        """Create chunk dictionary for a header section."""
        chunk_content = '\n'.join(lines[start:end])
        if not chunk_content.strip():
            return {}
        
        chunk_type = f"markdown_h{level}" if level else "markdown_intro"
        if start == 0 and level == 0:
            chunk_type = "markdown_content"
        
        return {
            "type": chunk_type,
            "name": header,
            "content": chunk_content,
            "line_start": start + 1,
            "line_end": end,
            "docstring": ""
        }

