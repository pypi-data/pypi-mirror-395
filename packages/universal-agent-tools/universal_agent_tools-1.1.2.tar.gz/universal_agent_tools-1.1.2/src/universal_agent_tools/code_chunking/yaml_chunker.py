"""
YAML Chunker

Responsibility: Chunk YAML content by top-level keys.
Preserves YAML structure and hierarchy.
"""

from typing import List, Dict
from .generic_chunker import GenericChunker


class YamlChunker:
    """
    Chunks YAML content by top-level keys.
    
    Each top-level key becomes a separate chunk.
    """
    
    def chunk(self, content: str, file_path: str) -> List[Dict]:
        """
        Chunk YAML content by top-level keys.
        
        Args:
            content: YAML content
            file_path: Path to YAML file
            
        Returns:
            List of chunk dictionaries
        """
        chunks = []
        lines = content.split('\n')
        
        current_chunk_start = 0
        current_key = None
        
        for i, line in enumerate(lines):
            # Skip empty lines and comments at start
            if not line.strip() or line.strip().startswith('#'):
                continue
            
            # Check if this is a top-level key (no leading whitespace, has colon)
            if line and not line[0].isspace() and ':' in line:
                # Save previous chunk
                if current_key is not None:
                    chunk = self._create_section_chunk(
                        lines, current_chunk_start, i, current_key
                    )
                    if chunk:
                        chunks.append(chunk)
                
                current_key = line.split(':')[0].strip()
                current_chunk_start = i
        
        # Don't forget the last chunk
        if current_key is not None:
            chunk = self._create_section_chunk(
                lines, current_chunk_start, len(lines), current_key
            )
            if chunk:
                chunks.append(chunk)
        
        # If no sections found, fallback to generic
        if not chunks:
            return GenericChunker().chunk(content, file_path)
        
        return chunks
    
    def _create_section_chunk(
        self,
        lines: List[str],
        start: int,
        end: int,
        key: str
    ) -> Dict:
        """Create chunk dictionary for a YAML section."""
        chunk_content = '\n'.join(lines[start:end])
        if not chunk_content.strip():
            return {}
        
        return {
            "type": "yaml_section",
            "name": key,
            "content": chunk_content,
            "line_start": start + 1,
            "line_end": end,
            "docstring": ""
        }

