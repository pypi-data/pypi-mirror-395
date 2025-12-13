"""
Prompt Generator

Responsibility: Generate LLM-optimized prompts for document generation.
Single Responsibility - only prompt generation.
"""

import json
from typing import Dict


class PromptGenerator:
    """
    Generates LLM-optimized prompts for document generation.
    
    Follows Single Responsibility Principle - only prompt generation.
    """
    
    def __init__(self, model: str = "qwen"):
        """
        Initialize prompt generator.
        
        Args:
            model: LLM model name (for model-specific optimizations)
        """
        self.model = model.lower()
    
    def get_prompt(
        self,
        pass_type: str,
        context: Dict
    ) -> str:
        """
        Generate prompt for a specific documentation pass.
        
        Args:
            pass_type: "architecture", "module_detail", or "code_examples"
            context: Context data for the prompt
            
        Returns:
            Formatted prompt string
        """
        if pass_type == "architecture":
            return self._architecture_prompt(context)
        elif pass_type == "module_detail":
            return self._module_detail_prompt(context)
        elif pass_type == "code_examples":
            return self._code_examples_prompt(context)
        else:
            return self._generic_prompt(context)
    
    def _architecture_prompt(self, context: Dict) -> str:
        """Generate architecture overview prompt."""
        base_system = self._get_base_system()
        clusters = context.get("clusters", {})
        dependency_graph = context.get("dependency_graph", {})
        top_files = context.get("top_files", [])
        
        return f"""{base_system}

Analyze this codebase structure and generate a comprehensive architecture overview.

CODEBASE STRUCTURE:
{json.dumps(clusters, indent=2)[:2000]}...

DEPENDENCY GRAPH:
{json.dumps(dependency_graph, indent=2)[:2000]}...

TOP IMPORTANT FILES (by PageRank):
{json.dumps(top_files[:10], indent=2)[:1000]}...

Generate a comprehensive architecture overview covering:
1. System purpose and key capabilities
2. Major components and their responsibilities
3. Data flow and integration points
4. Technology stack and frameworks
5. Key design patterns used

Use clear markdown with diagrams (mermaid syntax where appropriate).
Be specific and reference actual module names and relationships.
"""
    
    def _module_detail_prompt(self, context: Dict) -> str:
        """Generate module detail prompt."""
        base_system = self._get_base_system()
        module_info = context.get("module_info", {})
        related_modules = context.get("related_modules", [])
        architecture_context = context.get("architecture_context", "")
        
        return f"""{base_system}

Context from Architecture: {architecture_context[:500]}...

MODULE TO DOCUMENT:
{json.dumps(module_info, indent=2)[:3000]}...

RELATED MODULES:
{json.dumps(related_modules, indent=2)[:1000]}...

Generate detailed API documentation for this module:
1. Module purpose and use cases
2. Public API surface (classes, methods, endpoints)
3. Parameters, return types, exceptions
4. Code examples for each major function
5. Integration patterns

Format as professional API reference (like Swagger/OpenAPI style).
Be thorough but concise. Include actual code signatures.
"""
    
    def _code_examples_prompt(self, context: Dict) -> str:
        """Generate code examples prompt."""
        base_system = self._get_base_system()
        api_docs = context.get("api_docs", [])
        use_case = context.get("use_case", "common usage")
        
        return f"""{base_system}

Based on this API documentation:
{json.dumps(api_docs, indent=2)[:2000]}...

Create practical code examples showing:
1. Authentication/initialization
2. Common use case: {use_case}
3. Error handling patterns
4. End-to-end workflow

Provide runnable Python code with explanations.
Make examples realistic and production-ready.
"""
    
    def _generic_prompt(self, context: Dict) -> str:
        """Generate generic prompt."""
        base_system = self._get_base_system()
        return f"""{base_system}

Generate documentation based on: {json.dumps(context, indent=2)[:1000]}...
"""
    
    def _get_base_system(self) -> str:
        """Get base system prompt based on model."""
        if "qwen" in self.model:
            return "You are Qwen, created by Alibaba Cloud. You are a technical documentation expert who generates comprehensive, accurate API documentation with code examples."
        else:
            return "You are a technical documentation expert who generates comprehensive, accurate API documentation with code examples."

