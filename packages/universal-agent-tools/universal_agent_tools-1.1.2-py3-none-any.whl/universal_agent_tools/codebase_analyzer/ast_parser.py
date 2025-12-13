"""
AST Parser

Responsibility: Parse Python AST and extract structural information.
Single Responsibility - only handles AST parsing.
"""

import ast
from typing import Dict, List, Optional


class ASTParser:
    """
    Parses Python code using AST to extract structural information.
    
    Follows Single Responsibility Principle - only AST parsing.
    """
    
    @staticmethod
    def parse_file(content: str) -> Dict:
        """
        Parse Python file content and extract structure.
        
        Args:
            content: Python source code
            
        Returns:
            Dictionary with:
            - classes: List of class definitions
            - functions: List of function definitions
            - imports: List of imports
            - line_count: Total lines
        """
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return {
                "classes": [],
                "functions": [],
                "imports": [],
                "line_count": len(content.split('\n'))
            }
        
        classes = []
        functions = []
        imports = []
        lines = content.split('\n')
        
        # Extract imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}" if module else alias.name)
        
        # Extract classes
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                classes.append({
                    "name": node.name,
                    "line": node.lineno,
                    "methods": methods,
                    "docstring": ast.get_docstring(node) or ""
                })
        
        # Extract standalone functions
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not ASTParser._is_in_class(node, tree):
                    functions.append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": [arg.arg for arg in node.args.args],
                        "docstring": ast.get_docstring(node) or ""
                    })
        
        return {
            "classes": classes,
            "functions": functions,
            "imports": imports,
            "line_count": len(lines)
        }
    
    @staticmethod
    def _is_in_class(func_node: ast.FunctionDef, tree: ast.AST) -> bool:
        """Check if function is inside a class."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if item == func_node:
                        return True
        return False

