"""Configuration management via environment variables."""

import os
from pathlib import Path


def get_repos_path() -> Path:
    """Get the path where cloned repositories are stored."""
    default = Path.home() / ".mcp-git-analyzer" / "repos"
    path = Path(os.environ.get("GIT_ANALYZER_REPOS_PATH", str(default)))
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_db_path() -> Path:
    """Get the path to the SQLite database file."""
    default = Path.home() / ".mcp-git-analyzer" / "analysis.db"
    path = Path(os.environ.get("GIT_ANALYZER_DB_PATH", str(default)))
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
