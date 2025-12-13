"""
Sync State Models

Responsibility: Define data models for sync state.
Single Responsibility - only data structures.
"""

from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime


class FileState(BaseModel):
    """
    State for a single file.
    
    Follows Data Transfer Object pattern.
    """
    file_path: str
    sha: Optional[str] = None
    chunks: int = 0
    synced_at: Optional[str] = None
    content_hash: Optional[str] = None


class RepoState(BaseModel):
    """
    State for a repository.
    
    Follows Data Transfer Object pattern.
    """
    repo: str
    files: Dict[str, FileState] = {}
    files_synced: int = 0
    total_chunks: int = 0
    last_sync: Optional[str] = None
    last_github_sha: Optional[str] = None

