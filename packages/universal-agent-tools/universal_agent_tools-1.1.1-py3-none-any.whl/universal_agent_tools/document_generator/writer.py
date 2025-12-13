"""
Document Writer

Responsibility: Write sections and compile final documents.
Single Responsibility - only writing/compilation.
"""

from pathlib import Path
from typing import Dict, Optional
from .planner import DocumentPlan


class DocumentWriter:
    """
    Writes document sections and compiles final documents.
    
    Follows Single Responsibility Principle - only writing/compilation.
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize document writer.
        
        Args:
            output_dir: Output directory for documents (default: current_dir/generated_docs)
        """
        if output_dir is None:
            output_dir = Path.cwd() / "generated_docs"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._active_plan: Optional[DocumentPlan] = None
    
    def set_plan(self, plan: DocumentPlan):
        """Set the active document plan."""
        self._active_plan = plan
    
    def write_section(self, section_id: str, content: str) -> Dict:
        """
        Write content for a specific section.
        
        Args:
            section_id: ID of section from the plan
            content: Markdown content for this section
            
        Returns:
            Dictionary with progress and next step
        """
        if self._active_plan is None:
            return {"error": "No active plan. Set a plan first."}
        
        # Validate section exists
        section = next(
            (s for s in self._active_plan.sections if s["id"] == section_id),
            None
        )
        if not section:
            valid_ids = [s["id"] for s in self._active_plan.sections]
            return {
                "error": f"Section '{section_id}' not in plan. Valid: {valid_ids}"
            }
        
        # Store content
        self._active_plan.content[section_id] = content
        
        # Determine next step
        completed = len(self._active_plan.content)
        total = len(self._active_plan.sections)
        
        if completed >= total:
            return {
                "status": "all_sections_complete",
                "completed": completed,
                "total": total,
                "next_step": "Call compile_document to save the final document"
            }
        
        # Find next incomplete section
        for s in self._active_plan.sections:
            if s["id"] not in self._active_plan.content:
                return {
                    "status": "section_written",
                    "completed": completed,
                    "total": total,
                    "next_step": f"Call write_section with section_id='{s['id']}'"
                }
        
        return {"status": "ready_to_compile", "next_step": "Call compile_document"}
    
    def compile_document(self, filename: str) -> Dict:
        """
        Compile all sections and save the document.
        
        Args:
            filename: Output filename (will be saved to output_dir)
            
        Returns:
            Dictionary with save status and path
        """
        if self._active_plan is None:
            return {"error": "No active plan. Set a plan first."}
        
        # Check all sections are written
        missing = self._active_plan.get_missing_sections()
        if missing:
            return {
                "error": f"Missing sections: {missing}. Write them first.",
                "completed": len(self._active_plan.content),
                "total": len(self._active_plan.sections)
            }
        
        # Compile document
        lines = [f"# {self._active_plan.title}", ""]
        lines.append(f"*Generated: {self._active_plan.created_at}*")
        lines.append("")
        
        for section in self._active_plan.sections:
            heading = section["heading"]
            content = self._active_plan.content[section["id"]]
            
            lines.append(f"## {heading}")
            lines.append("")
            lines.append(content)
            lines.append("")
        
        document = "\n".join(lines)
        
        # Save
        if not filename.endswith(".md"):
            filename += ".md"
        
        output_path = self.output_dir / filename
        output_path.write_text(document, encoding="utf-8")
        
        # Clear plan
        saved_plan = self._active_plan.to_dict()
        self._active_plan = None
        
        return {
            "status": "document_saved",
            "path": str(output_path),
            "filename": filename,
            "sections_compiled": len(saved_plan["sections"]),
            "total_chars": len(document)
        }
    
    def get_plan_status(self) -> Dict:
        """Get current plan status."""
        if self._active_plan is None:
            return {"status": "no_active_plan"}
        
        return self._active_plan.to_dict()

