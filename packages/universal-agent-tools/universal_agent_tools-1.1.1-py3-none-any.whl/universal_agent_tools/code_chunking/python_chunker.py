"""
Python Chunker

Responsibility: Chunk Python code using AST parsing.
Preserves semantic structure (classes, functions, imports).
"""

import ast
from typing import List, Dict
from pathlib import Path

from .generic_chunker import GenericChunker


class PythonChunker:
    """
    Chunks Python content using AST parsing.
    
    Extracts:
    - Classes (with methods)
    - Standalone functions
    - Module-level code
    - Imports (preserved with first chunk)
    """
    
    def chunk(self, content: str, file_path: str) -> List[Dict]:
        """
        Chunk Python content using AST.
        
        Args:
            content: Python source code
            file_path: Path to Python file
            
        Returns:
            List of chunk dictionaries
        """
        try:
            tree = ast.parse(content)
        except SyntaxError:
            # Fallback to generic chunking for invalid Python
            return GenericChunker().chunk(content, file_path)
        
        chunks = []
        lines = content.split('\n')
        
        # Extract imports
        import_block = self._extract_imports(tree, lines)
        
        # Extract classes
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                chunk = self._create_class_chunk(node, lines, import_block, chunks)
                chunks.append(chunk)
        
        # Extract standalone functions
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not self._is_in_class(node, tree):
                    chunk = self._create_function_chunk(node, lines, import_block, chunks)
                    chunks.append(chunk)
        
        # If no classes/functions, chunk as module
        if not chunks:
            chunks.append(self._create_module_chunk(tree, content, lines, file_path, import_block))
        
        return chunks
    
    def _extract_imports(self, tree: ast.AST, lines: List[str]) -> str:
        """Extract all import statements."""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                start = node.lineno - 1
                end = getattr(node, 'end_lineno', node.lineno)
                imports.append('\n'.join(lines[start:end]))
        return '\n'.join(imports) if imports else ""
    
    def _is_in_class(self, func_node: ast.FunctionDef, tree: ast.AST) -> bool:
        """Check if function is inside a class."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if item == func_node:
                        return True
        return False
    
    def _create_class_chunk(
        self,
        node: ast.ClassDef,
        lines: List[str],
        import_block: str,
        existing_chunks: List[Dict]
    ) -> Dict:
        """Create chunk dictionary for a class."""
        start = node.lineno - 1
        end = getattr(node, 'end_lineno', node.lineno)
        class_code = '\n'.join(lines[start:end])
        
        # Add imports to first chunk
        if not existing_chunks and import_block:
            class_code = import_block + '\n\n' + class_code
        
        return {
            "type": "class",
            "name": node.name,
            "content": class_code,
            "line_start": node.lineno,
            "line_end": end,
            "docstring": ast.get_docstring(node) or ""
        }
    
    def _create_function_chunk(
        self,
        node: ast.FunctionDef,
        lines: List[str],
        import_block: str,
        existing_chunks: List[Dict]
    ) -> Dict:
        """Create chunk dictionary for a function."""
        start = node.lineno - 1
        end = getattr(node, 'end_lineno', node.lineno)
        func_code = '\n'.join(lines[start:end])
        
        # Add imports to first standalone function
        if not any(c.get('type') == 'function' for c in existing_chunks) and import_block:
            func_code = import_block + '\n\n' + func_code
        
        return {
            "type": "function",
            "name": node.name,
            "content": func_code,
            "line_start": node.lineno,
            "line_end": end,
            "docstring": ast.get_docstring(node) or ""
        }
    
    def _create_module_chunk(
        self,
        tree: ast.AST,
        content: str,
        lines: List[str],
        file_path: str,
        import_block: str
    ) -> Dict:
        """Create chunk dictionary for module-level code."""
        return {
            "type": "module",
            "name": Path(file_path).stem,
            "content": content,
            "line_start": 1,
            "line_end": len(lines),
            "docstring": ast.get_docstring(tree) or ""
        }

