"""Database package."""

from mcp_git_analyzer.db.schema import Database, init_db, get_connection

__all__ = ["Database", "init_db", "get_connection"]
