"""
Document Planner

Responsibility: Create and manage document plans.
Single Responsibility - only planning logic.
"""

from datetime import datetime
from typing import List, Dict, Optional


class DocumentPlan:
    """
    Structured document plan - prevents unbounded generation.
    
    Follows Data Transfer Object pattern.
    """
    
    def __init__(
        self,
        title: str,
        sections: List[Dict],
        generation_mode: str = "standard"
    ):
        """
        Initialize document plan.
        
        Args:
            title: Document title
            sections: List of {id, heading, description} for each section
            generation_mode: "standard" or "multi_pass"
        """
        self.title = title
        self.sections = sections
        self.content: Dict[str, str] = {}  # section_id -> content
        self.created_at = datetime.utcnow().isoformat()
        self.generation_mode = generation_mode
        self.preprocessing_data: Dict = {}  # Store clustering, dependency graph, etc.
        self.pass_status = {
            "architecture": False,
            "modules": False,
            "examples": False
        }
    
    def to_dict(self) -> Dict:
        """Convert plan to dictionary."""
        return {
            "title": self.title,
            "sections": self.sections,
            "content": self.content,
            "created_at": self.created_at,
            "completed_sections": len(self.content),
            "total_sections": len(self.sections),
            "generation_mode": self.generation_mode,
            "pass_status": self.pass_status
        }
    
    def is_complete(self) -> bool:
        """Check if all sections are written."""
        return len(self.content) >= len(self.sections)
    
    def get_missing_sections(self) -> List[str]:
        """Get list of section IDs that haven't been written."""
        written = set(self.content.keys())
        return [s["id"] for s in self.sections if s["id"] not in written]


class DocumentPlanner:
    """
    Creates and manages document plans.
    
    Follows Single Responsibility Principle - only planning.
    """
    
    MAX_SECTIONS = 10
    
    def create_plan(
        self,
        title: str,
        sections: List[Dict]
    ) -> Dict:
        """
        Create a structured document plan.
        
        Args:
            title: Document title
            sections: List of {id, heading, description} for each section
            
        Returns:
            Dictionary with plan status or error
        """
        # Validate sections
        if not sections or len(sections) == 0:
            return {"error": "Must provide at least one section"}
        
        if len(sections) > self.MAX_SECTIONS:
            return {"error": f"Maximum {self.MAX_SECTIONS} sections to prevent churning"}
        
        # Create plan
        plan = DocumentPlan(title, sections)
        
        return {
            "status": "plan_created",
            "title": title,
            "sections": [{"id": s["id"], "heading": s["heading"]} for s in sections],
            "next_step": f"Call write_section with section_id='{sections[0]['id']}' and content"
        }
    
    def create_multi_pass_plan(self, title: str, topic: str) -> Dict:
        """
        Create a multi-pass document plan.
        
        Passes:
        1. Architecture overview
        2. Module-by-module detailed docs
        3. Code examples and tutorials
        
        Args:
            title: Document title
            topic: Document topic/theme
            
        Returns:
            Dictionary with plan status
        """
        sections = [
            {
                "id": "architecture",
                "heading": "Architecture Overview",
                "description": "High-level system architecture, components, and design patterns",
                "pass": "architecture"
            },
            {
                "id": "core_modules",
                "heading": "Core Modules",
                "description": "Detailed documentation of core modules and their APIs",
                "pass": "modules"
            },
            {
                "id": "adapters",
                "heading": "Adapters and Integrations",
                "description": "Integration layer and adapter modules",
                "pass": "modules"
            },
            {
                "id": "tools",
                "heading": "Tools and Utilities",
                "description": "Tool definitions, MCP servers, and utility functions",
                "pass": "modules"
            },
            {
                "id": "examples",
                "heading": "Code Examples and Tutorials",
                "description": "Practical examples and usage patterns",
                "pass": "examples"
            }
        ]
        
        return {
            "status": "multi_pass_plan_created",
            "title": title,
            "topic": topic,
            "sections": [{"id": s["id"], "heading": s["heading"], "pass": s["pass"]} for s in sections],
            "next_step": "Call set_preprocessing_data with analysis results, then start with architecture pass"
        }

