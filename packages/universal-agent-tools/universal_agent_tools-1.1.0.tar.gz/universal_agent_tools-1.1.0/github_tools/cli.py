"""
GitHub CLI Wrapper

Responsibility: Execute GitHub CLI commands and parse output.
Single Responsibility - only CLI execution.
"""

import subprocess
import json
from typing import List, Dict, Optional


def run_gh_command(args: List[str], timeout: int = 30) -> Dict:
    """
    Run a gh CLI command and return parsed output.
    
    Args:
        args: List of command arguments (without 'gh')
        timeout: Command timeout in seconds
        
    Returns:
        Dictionary with 'data' key on success, 'error' key on failure
    """
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode != 0:
            return {
                "error": result.stderr.strip() or f"Command failed with code {result.returncode}"
            }
        
        # Try to parse as JSON
        try:
            return {"data": json.loads(result.stdout)}
        except json.JSONDecodeError:
            return {"data": result.stdout.strip()}
            
    except subprocess.TimeoutExpired:
        return {"error": "Command timed out"}
    except FileNotFoundError:
        return {"error": "gh CLI not found. Install from https://cli.github.com"}


class GitHubCLI:
    """
    GitHub CLI wrapper for repository operations.
    
    Follows Single Responsibility Principle - only GitHub CLI operations.
    """
    
    @staticmethod
    def get_default_branch(repo: str) -> str:
        """
        Get the default branch for a repository.
        
        Args:
            repo: Repository in owner/name format
            
        Returns:
            Default branch name (defaults to "main")
        """
        result = run_gh_command(["api", f"/repos/{repo}", "--jq", ".default_branch"])
        if "data" in result and isinstance(result["data"], str):
            return result["data"].strip()
        return "main"  # fallback
    
    @staticmethod
    def get_repo_info(repo: str) -> Dict:
        """
        Get repository information.
        
        Args:
            repo: Repository in owner/name format
            
        Returns:
            Dictionary with repo info or error
        """
        result = run_gh_command([
            "repo", "view", repo, "--json",
            "name,description,pushedAt,defaultBranchRef"
        ])
        
        if "error" in result:
            return result
        
        data = result["data"]
        return {
            "repo": repo,
            "name": data.get("name"),
            "description": data.get("description"),
            "last_pushed": data.get("pushedAt"),
            "default_branch": data.get("defaultBranchRef", {}).get("name", "main")
        }

