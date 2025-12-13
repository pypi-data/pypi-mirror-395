"""
Sync State Manager

Responsibility: Manage sync state for file synchronization.
Tracks file versions, SHA hashes, and sync status.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime

from .models import FileState, RepoState


class SyncStateManager:
    """
    Manages sync state for file synchronization.
    
    Tracks:
    - File SHA hashes for change detection
    - Chunk counts per file
    - Last sync timestamps
    - Repository-level aggregation
    """
    
    def __init__(self, state_file: Optional[Path] = None):
        """
        Initialize sync state manager.
        
        Args:
            state_file: Path to state file (default: sync_state.json in current dir)
        """
        if state_file is None:
            state_file = Path.cwd() / "sync_state.json"
        self.state_file = Path(state_file)
        self._state: Dict = {}
        self._load_state()
    
    def _load_state(self):
        """Load state from file."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    self._state = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._state = {"repos": {}, "last_full_sync": None}
        else:
            self._state = {"repos": {}, "last_full_sync": None}
    
    def _save_state(self):
        """Save state to file."""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self._state, f, indent=2, default=str)
        except IOError as e:
            print(f"Warning: Could not save sync state: {e}")
    
    @staticmethod
    def get_content_hash(content: str) -> str:
        """
        Generate hash of content for change detection.
        
        Args:
            content: File content as string
            
        Returns:
            SHA256 hash (first 16 characters)
        """
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def get_sync_status(self, repo: Optional[str] = None) -> Dict:
        """
        Get sync status for all or one repository.
        
        Args:
            repo: Optional repository name to filter
            
        Returns:
            Dictionary with sync status
        """
        if repo:
            repo_state = self._state.get("repos", {}).get(repo, {})
            return {
                "repo": repo,
                "last_sync": repo_state.get("last_sync"),
                "last_github_sha": repo_state.get("last_github_sha"),
                "files_synced": repo_state.get("files_synced", 0),
                "total_chunks": repo_state.get("total_chunks", 0),
                "needs_sync": repo_state.get("needs_sync", True)
            }
        
        # Return all repos
        statuses = []
        for r, data in self._state.get("repos", {}).items():
            statuses.append({
                "repo": r,
                "last_sync": data.get("last_sync"),
                "files_synced": data.get("files_synced", 0),
                "total_chunks": data.get("total_chunks", 0)
            })
        
        return {
            "repos": statuses,
            "last_full_sync": self._state.get("last_full_sync")
        }
    
    def update_file_state(
        self,
        repo: str,
        file_path: str,
        sha: str,
        chunks_count: int,
        content_hash: Optional[str] = None
    ) -> Dict:
        """
        Update sync state after syncing a file.
        
        Args:
            repo: Repository name
            file_path: Path to file
            sha: File SHA (e.g., GitHub SHA)
            chunks_count: Number of chunks created
            content_hash: Optional content hash
            
        Returns:
            Dictionary with update status
        """
        if repo not in self._state.get("repos", {}):
            self._state["repos"][repo] = {
                "files": {},
                "files_synced": 0,
                "total_chunks": 0
            }
        
        repo_state = self._state["repos"][repo]
        
        # Update file info
        repo_state["files"][file_path] = {
            "sha": sha,
            "chunks": chunks_count,
            "synced_at": datetime.utcnow().isoformat() + "Z",
            "content_hash": content_hash
        }
        
        # Recalculate totals
        repo_state["files_synced"] = len(repo_state["files"])
        repo_state["total_chunks"] = sum(f["chunks"] for f in repo_state["files"].values())
        repo_state["last_sync"] = datetime.utcnow().isoformat() + "Z"
        
        self._save_state()
        
        return {
            "repo": repo,
            "file": file_path,
            "status": "synced",
            "chunks_stored": chunks_count
        }
    
    def check_file_needs_sync(
        self,
        repo: str,
        file_path: str,
        sha: str
    ) -> Dict:
        """
        Check if a file needs to be re-synced based on SHA.
        
        Args:
            repo: Repository name
            file_path: Path to file
            sha: Current file SHA
            
        Returns:
            Dictionary with sync status
        """
        repo_state = self._state.get("repos", {}).get(repo, {})
        file_state = repo_state.get("files", {}).get(file_path, {})
        
        stored_sha = file_state.get("sha")
        needs_sync = stored_sha != sha
        
        return {
            "repo": repo,
            "file": file_path,
            "needs_sync": needs_sync,
            "stored_sha": stored_sha,
            "github_sha": sha,
            "last_synced": file_state.get("synced_at")
        }
    
    def delete_file_state(self, repo: str, file_path: str) -> Dict:
        """
        Delete sync state for a file (when file is deleted/renamed).
        
        Args:
            repo: Repository name
            file_path: Path to file
            
        Returns:
            Dictionary with deletion status
        """
        if repo in self._state.get("repos", {}) and file_path in self._state["repos"][repo].get("files", {}):
            del self._state["repos"][repo]["files"][file_path]
            
            # Recalculate totals
            repo_state = self._state["repos"][repo]
            repo_state["files_synced"] = len(repo_state["files"])
            repo_state["total_chunks"] = sum(f["chunks"] for f in repo_state["files"].values())
            
            self._save_state()
            
            return {
                "repo": repo,
                "file_path": file_path,
                "status": "deleted"
            }
        
        return {
            "repo": repo,
            "file_path": file_path,
            "status": "not_found"
        }
    
    def get_storage_stats(self) -> Dict:
        """
        Get storage statistics.
        
        Returns:
            Dictionary with storage statistics
        """
        total_files = 0
        total_chunks = 0
        
        for repo_state in self._state.get("repos", {}).values():
            total_files += repo_state.get("files_synced", 0)
            total_chunks += repo_state.get("total_chunks", 0)
        
        return {
            "repos_tracked": len(self._state.get("repos", {})),
            "total_files": total_files,
            "total_chunks": total_chunks,
            "last_full_sync": self._state.get("last_full_sync"),
            "state_file": str(self.state_file)
        }


# Global state manager instance (Singleton Pattern)
_state_manager: Optional[SyncStateManager] = None


def get_sync_state_manager(state_file: Optional[Path] = None) -> SyncStateManager:
    """
    Get or create global sync state manager instance.
    
    Args:
        state_file: Optional path to state file
        
    Returns:
        SyncStateManager instance
    """
    global _state_manager
    if _state_manager is None:
        _state_manager = SyncStateManager(state_file)
    return _state_manager

