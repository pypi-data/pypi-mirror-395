"""Git repository management tools."""

import hashlib
import os
from pathlib import Path
from urllib.parse import urlparse

from git import Repo
from git.exc import GitCommandError

from mcp_git_analyzer.config import get_repos_path
from mcp_git_analyzer.db import Database


def url_to_repo_name(url: str) -> str:
    """Extract repository name from Git URL."""
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    if path.endswith(".git"):
        path = path[:-4]
    return path.split("/")[-1]


def url_to_unique_path(url: str) -> str:
    """Generate a unique directory name from Git URL."""
    # Use hash to avoid conflicts with same repo name from different sources
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    name = url_to_repo_name(url)
    return f"{name}_{url_hash}"


class GitTools:
    """Git repository operations."""
    
    def __init__(self, db: Database):
        self.db = db
        self.repos_path = get_repos_path()
    
    def clone_repo(self, url: str, branch: str | None = None) -> dict:
        """
        Clone a Git repository.
        
        Args:
            url: Git repository URL (HTTPS or SSH)
            branch: Optional branch name to checkout (default: repository's default branch)
        
        Returns:
            Repository info as JSON with id, name, url, local_path, branch
        """
        # Check if already cloned
        existing = self.db.execute(
            "SELECT * FROM repositories WHERE url = ?", (url,)
        )
        if existing:
            repo_info = self.db.row_to_dict(existing[0])
            return {
                "status": "already_exists",
                "message": f"Repository already cloned at {repo_info['local_path']}",
                "repository": repo_info
            }
        
        # Prepare local path
        dir_name = url_to_unique_path(url)
        local_path = self.repos_path / dir_name
        
        try:
            # Clone repository
            clone_kwargs = {"depth": None}  # Full clone for analysis
            if branch:
                clone_kwargs["branch"] = branch
            
            repo = Repo.clone_from(url, local_path, **clone_kwargs)
            
            # Get default branch
            default_branch = branch or repo.active_branch.name
            
            # Extract description from README if exists
            description = self._extract_description(local_path)
            
            # Insert into database
            repo_id = self.db.insert(
                """INSERT INTO repositories (url, name, local_path, default_branch, description)
                   VALUES (?, ?, ?, ?, ?)""",
                (url, url_to_repo_name(url), str(local_path), default_branch, description)
            )
            
            return {
                "status": "cloned",
                "message": "Successfully cloned repository",
                "repository": {
                    "id": repo_id,
                    "name": url_to_repo_name(url),
                    "url": url,
                    "local_path": str(local_path),
                    "branch": default_branch,
                    "description": description
                }
            }
        except GitCommandError as e:
            return {
                "status": "error",
                "message": f"Git clone failed: {str(e)}",
                "repository": None
            }
    
    def list_repos(self) -> dict:
        """
        List all registered repositories.
        
        Returns:
            List of repositories with their analysis status
        """
        rows = self.db.execute(
            """SELECT id, url, name, local_path, default_branch, 
                      cloned_at, last_analyzed, description
               FROM repositories ORDER BY cloned_at DESC"""
        )
        
        repos = []
        for row in rows:
            repo_dict = self.db.row_to_dict(row)
            
            # Check if local path still exists
            repo_dict["exists_locally"] = Path(repo_dict["local_path"]).exists()
            
            # Get file count if analyzed
            if repo_dict["last_analyzed"]:
                file_count = self.db.execute(
                    "SELECT COUNT(*) as count FROM files WHERE repo_id = ?",
                    (repo_dict["id"],)
                )
                symbol_count = self.db.execute(
                    """SELECT COUNT(*) as count FROM symbols s 
                       JOIN files f ON s.file_id = f.id 
                       WHERE f.repo_id = ?""",
                    (repo_dict["id"],)
                )
                repo_dict["file_count"] = file_count[0]["count"] if file_count else 0
                repo_dict["symbol_count"] = symbol_count[0]["count"] if symbol_count else 0
            
            repos.append(repo_dict)
        
        return {
            "total": len(repos),
            "repositories": repos
        }
    
    def get_repo_tree(self, repo_id: int, max_depth: int = 3) -> dict:
        """
        Get the file structure of a repository.
        
        Args:
            repo_id: Repository ID
            max_depth: Maximum directory depth to traverse (default: 3)
        
        Returns:
            Tree structure with files and directories
        """
        rows = self.db.execute(
            "SELECT * FROM repositories WHERE id = ?", (repo_id,)
        )
        if not rows:
            return {"status": "error", "message": f"Repository {repo_id} not found"}
        
        repo = self.db.row_to_dict(rows[0])
        local_path = Path(repo["local_path"])
        
        if not local_path.exists():
            return {"status": "error", "message": f"Local path no longer exists: {local_path}"}
        
        def build_tree(path: Path, depth: int = 0) -> dict:
            """Recursively build directory tree."""
            if depth > max_depth:
                return {"type": "directory", "name": path.name, "truncated": True}
            
            result = {
                "type": "directory",
                "name": path.name,
                "children": []
            }
            
            try:
                entries = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
                for entry in entries:
                    # Skip hidden files and common non-essential directories
                    if entry.name.startswith(".") or entry.name in ["node_modules", "__pycache__", "venv", ".venv", "dist", "build"]:
                        continue
                    
                    if entry.is_dir():
                        result["children"].append(build_tree(entry, depth + 1))
                    else:
                        file_info = {
                            "type": "file",
                            "name": entry.name,
                            "extension": entry.suffix,
                            "size": entry.stat().st_size
                        }
                        # Detect language
                        file_info["language"] = self._detect_language(entry.suffix)
                        result["children"].append(file_info)
            except PermissionError:
                result["error"] = "Permission denied"
            
            return result
        
        tree = build_tree(local_path)
        tree["name"] = repo["name"]
        
        return {
            "status": "success",
            "repository": {
                "id": repo["id"],
                "name": repo["name"],
                "url": repo["url"]
            },
            "tree": tree
        }
    
    def get_repo_by_id(self, repo_id: int) -> dict | None:
        """Get repository info by ID."""
        rows = self.db.execute(
            "SELECT * FROM repositories WHERE id = ?", (repo_id,)
        )
        if rows:
            return self.db.row_to_dict(rows[0])
        return None
    
    def delete_repo(self, repo_id: int, delete_files: bool = False) -> dict:
        """
        Delete a repository from the database.
        
        Args:
            repo_id: Repository ID
            delete_files: Also delete cloned files from disk
        
        Returns:
            Deletion status
        """
        repo = self.get_repo_by_id(repo_id)
        if not repo:
            return {"status": "error", "message": f"Repository {repo_id} not found"}
        
        if delete_files:
            local_path = Path(repo["local_path"])
            if local_path.exists():
                import shutil
                import stat
                
                def remove_readonly(func, path, excinfo):
                    """Handle read-only files on Windows (e.g., .git folder)."""
                    os.chmod(path, stat.S_IWRITE)
                    func(path)
                
                shutil.rmtree(local_path, onerror=remove_readonly)
        
        # Cascade delete will remove files, symbols, etc.
        with self.db.connection() as conn:
            conn.execute("DELETE FROM repositories WHERE id = ?", (repo_id,))
            conn.commit()
        
        return {
            "status": "deleted",
            "message": f"Repository '{repo['name']}' deleted",
            "files_deleted": delete_files
        }
    
    def _extract_description(self, repo_path: Path) -> str | None:
        """Extract description from README file."""
        readme_names = ["README.md", "README.rst", "README.txt", "README"]
        for name in readme_names:
            readme_path = repo_path / name
            if readme_path.exists():
                try:
                    content = readme_path.read_text(encoding="utf-8", errors="ignore")
                    # Get first paragraph (non-header, non-empty)
                    lines = content.split("\n")
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith("#") and not line.startswith("="):
                            return line[:500]  # Limit length
                except Exception:
                    pass
        return None
    
    def _detect_language(self, extension: str) -> str | None:
        """Detect programming language from file extension."""
        lang_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".jsx": "javascript",
            ".java": "java",
            ".c": "c",
            ".cpp": "cpp",
            ".h": "c",
            ".hpp": "cpp",
            ".go": "go",
            ".rs": "rust",
            ".rb": "ruby",
            ".php": "php",
            ".cs": "csharp",
            ".swift": "swift",
            ".kt": "kotlin",
            ".scala": "scala",
            ".r": "r",
            ".R": "r",
            ".sql": "sql",
            ".sh": "shell",
            ".bash": "shell",
            ".zsh": "shell",
            ".ps1": "powershell",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".json": "json",
            ".xml": "xml",
            ".html": "html",
            ".css": "css",
            ".scss": "scss",
            ".md": "markdown",
        }
        return lang_map.get(extension.lower())
