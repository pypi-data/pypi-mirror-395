"""
File Type Detector

Responsibility: Detect file type from path.
Single Responsibility Principle - only handles type detection.
"""

from pathlib import Path
from typing import Protocol


class FileTypeDetector:
    """
    Detects file type from file path.
    
    Follows Open/Closed Principle - extensible for new file types.
    """
    
    # File type mappings
    EXTENSION_MAP = {
        ".py": "python",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".md": "markdown",
        ".json": "json",
        ".toml": "toml",
        ".sh": "shell",
        ".bash": "shell",
        ".ps1": "powershell",
        ".dockerfile": "dockerfile",
    }
    
    # Special file names (case-insensitive)
    SPECIAL_NAMES = {
        "dockerfile": "dockerfile",
    }
    
    @classmethod
    def detect(cls, file_path: str) -> str:
        """
        Detect file type from path.
        
        Args:
            file_path: Path to file
            
        Returns:
            File type string (python, yaml, markdown, json, etc.)
        """
        path = Path(file_path)
        ext = path.suffix.lower()
        name = path.name.lower()
        
        # Check special names first
        if name in cls.SPECIAL_NAMES:
            return cls.SPECIAL_NAMES[name]
        
        # Check extension
        if ext in cls.EXTENSION_MAP:
            return cls.EXTENSION_MAP[ext]
        
        # Default to text
        return "text"
    
    @classmethod
    def register_extension(cls, extension: str, file_type: str):
        """
        Register a new file extension mapping.
        
        Follows Open/Closed Principle - can extend without modification.
        
        Args:
            extension: File extension (e.g., ".ts")
            file_type: File type identifier (e.g., "typescript")
        """
        cls.EXTENSION_MAP[extension.lower()] = file_type
    
    @classmethod
    def register_special_name(cls, name: str, file_type: str):
        """
        Register a special file name mapping.
        
        Args:
            name: File name (case-insensitive, e.g., "Dockerfile")
            file_type: File type identifier
        """
        cls.SPECIAL_NAMES[name.lower()] = file_type


# Convenience function
def get_file_type(file_path: str) -> str:
    """
    Get file type from path.
    
    Args:
        file_path: Path to file
        
    Returns:
        File type string
    """
    return FileTypeDetector.detect(file_path)

