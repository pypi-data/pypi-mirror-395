"""
GitHub Repository Operations

Responsibility: Repository-level operations (commits, files, content).
Single Responsibility - only repository operations.
"""

import json
import base64
from datetime import datetime
from typing import Optional, List, Dict, Set

from .cli import GitHubCLI, run_gh_command


class GitHubRepository:
    """
    GitHub repository operations using CLI.
    
    Follows Single Responsibility Principle - only repository operations.
    """
    
    # File types relevant to code development
    SUPPORTED_EXTENSIONS = [
        ".py", ".yaml", ".yml", ".md", ".json", ".toml",
        ".sh", ".ps1", ".dockerfile"
    ]
    
    def __init__(self, repo: str):
        """
        Initialize repository client.
        
        Args:
            repo: Repository in owner/name format
        """
        self.repo = repo
        self._default_branch = None
    
    def get_default_branch(self) -> str:
        """Get and cache default branch."""
        if self._default_branch is None:
            self._default_branch = GitHubCLI.get_default_branch(self.repo)
        return self._default_branch
    
    def get_commits(
        self,
        since: Optional[str] = None,
        limit: int = 10
    ) -> Dict:
        """
        Get recent commits for the repository.
        
        Args:
            since: ISO date string to get commits since (e.g., "2025-12-01")
            limit: Maximum number of commits to return
            
        Returns:
            Dictionary with commits list or error
        """
        args = [
            "api", f"/repos/{self.repo}/commits",
            "--jq", f".[:{limit}] | .[] | {{sha: .sha, message: .commit.message, date: .commit.author.date, author: .commit.author.name}}"
        ]
        
        if since:
            args.extend(["--method", "GET", "-f", f"since={since}"])
        
        result = run_gh_command(args)
        
        if "error" in result:
            return result
        
        # Parse JSONL output
        commits = []
        output = result["data"]
        if isinstance(output, str):
            for line in output.strip().split("\n"):
                if line:
                    try:
                        commits.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        elif isinstance(output, list):
            commits = output
        
        return {"repo": self.repo, "commits": commits}
    
    def list_code_files(self, path: str = "") -> Dict:
        """
        List all relevant code/config files in the repository.
        
        Args:
            path: Path prefix to filter (empty for root)
            
        Returns:
            Dictionary with code_files list or error
        """
        branch = self.get_default_branch()
        
        # Build jq filter for all supported extensions
        ext_filters = " or ".join([f'endswith("{ext}")' for ext in self.SUPPORTED_EXTENSIONS])
        jq_filter = f'.tree[] | select((.path | ({ext_filters})) or (.path | endswith("Dockerfile"))) | {{path: .path, sha: .sha, size: .size}}'
        
        # Get tree recursively
        args = [
            "api", f"/repos/{self.repo}/git/trees/{branch}?recursive=1",
            "--jq", jq_filter
        ]
        
        result = run_gh_command(args)
        
        if "error" in result:
            return result
        
        # Parse JSONL output
        files = []
        output = result["data"]
        if isinstance(output, str):
            for line in output.strip().split("\n"):
                if line:
                    try:
                        file_info = json.loads(line)
                        # Filter by path prefix if specified
                        if not path or file_info["path"].startswith(path):
                            files.append(file_info)
                    except json.JSONDecodeError:
                        pass
        elif isinstance(output, list):
            files = [f for f in output if not path or f.get("path", "").startswith(path)]
        
        return {
            "repo": self.repo,
            "path": path,
            "code_files": files,
            "count": len(files)
        }
    
    def get_file_with_metadata(self, path: str) -> Dict:
        """
        Get file content along with its metadata (last commit, sha).
        
        Args:
            path: File path within repository
            
        Returns:
            Dictionary with file content and metadata or error
        """
        branch = self.get_default_branch()
        
        # Get file content
        content_result = run_gh_command([
            "api", f"/repos/{self.repo}/contents/{path}?ref={branch}",
            "--jq", '{sha: .sha, size: .size, content: .content, encoding: .encoding}'
        ])
        
        if "error" in content_result:
            return content_result
        
        # Get last commit for this file
        commit_result = run_gh_command([
            "api", f"/repos/{self.repo}/commits?path={path}&per_page=1",
            "--jq", '.[0] | {commit_sha: .sha, commit_date: .commit.author.date, commit_message: .commit.message}'
        ])
        
        try:
            content_data = (
                json.loads(content_result["data"])
                if isinstance(content_result["data"], str)
                else content_result["data"]
            )
            commit_data = (
                json.loads(commit_result["data"])
                if isinstance(commit_result["data"], str)
                else commit_result.get("data", {})
            )
            
            # Decode content
            decoded_content = ""
            if content_data.get("encoding") == "base64" and content_data.get("content"):
                try:
                    decoded_content = base64.b64decode(content_data["content"]).decode("utf-8")
                except Exception:
                    decoded_content = "[Binary or encoding error]"
            
            return {
                "repo": self.repo,
                "path": path,
                "sha": content_data.get("sha"),
                "size": content_data.get("size"),
                "content": decoded_content,
                "last_commit": commit_data if commit_data else None,
                "retrieved_at": datetime.utcnow().isoformat() + "Z"
            }
            
        except Exception as e:
            return {"error": f"Failed to parse response: {str(e)}"}
    
    def get_changed_files(self, since: str, file_extension: Optional[str] = None) -> Dict:
        """
        Get list of files that changed since a given date.
        
        Args:
            since: ISO date string (e.g., "2025-12-01T00:00:00Z")
            file_extension: Optional file extension filter (e.g., ".py")
            
        Returns:
            Dictionary with changed files list or error
        """
        # Get commits since date
        commits_result = self.get_commits(since=since, limit=50)
        
        if "error" in commits_result:
            return commits_result
        
        # For each commit, get changed files
        changed_files: Set[str] = set()
        
        for commit in commits_result.get("commits", []):
            sha = commit.get("sha")
            if sha:
                files_result = run_gh_command([
                    "api", f"/repos/{self.repo}/commits/{sha}",
                    "--jq", '.files[].filename'
                ])
                
                if "data" in files_result:
                    output = files_result["data"]
                    filenames = output.strip().split("\n") if isinstance(output, str) else output
                    for filename in filenames:
                        if filename and (not file_extension or filename.endswith(file_extension)):
                            changed_files.add(filename)
        
        return {
            "repo": self.repo,
            "since": since,
            "changed_files": sorted(list(changed_files)),
            "count": len(changed_files)
        }

