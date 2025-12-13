"""
JSON Chunker

Responsibility: Chunk JSON content with structure awareness.
Usually keeps as single chunk but extracts metadata.
"""

import json
from typing import List, Dict
from pathlib import Path
from .generic_chunker import GenericChunker


class JsonChunker:
    """
    Chunks JSON content - usually keeps as single chunk.
    Extracts metadata about structure (keys, array length, etc.).
    """
    
    def chunk(self, content: str, file_path: str) -> List[Dict]:
        """
        Chunk JSON content.
        
        Args:
            content: JSON content
            file_path: Path to JSON file
            
        Returns:
            List with single chunk dictionary (or fallback to generic)
        """
        try:
            data = json.loads(content)
            
            # Generate description based on structure
            description = self._generate_description(data)
            
            return [{
                "type": "json_document",
                "name": Path(file_path).stem,
                "content": content,
                "line_start": 1,
                "line_end": len(content.split('\n')),
                "docstring": description
            }]
        except json.JSONDecodeError:
            # Fallback to generic chunking for invalid JSON
            return GenericChunker().chunk(content, file_path)
    
    def _generate_description(self, data: object) -> str:
        """Generate description of JSON structure."""
        if isinstance(data, dict):
            top_keys = list(data.keys())[:10]
            return f"JSON with keys: {', '.join(top_keys)}"
        elif isinstance(data, list):
            return f"JSON array with {len(data)} items"
        else:
            return "JSON value"

