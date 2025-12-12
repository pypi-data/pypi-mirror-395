"""Search tools using FTS5 full-text search."""

import json
from typing import Literal

from mcp_git_analyzer.db import Database


class SearchTools:
    """Code search operations."""
    
    def __init__(self, db: Database):
        self.db = db
    
    def search_code(
        self, 
        query: str, 
        search_type: Literal["all", "function", "class", "method"] | None = None,
        repo_id: int | None = None,
        limit: int = 20
    ) -> dict:
        """
        Search symbols using full-text search.
        
        Args:
            query: Search query (supports FTS5 syntax: AND, OR, NOT, "phrase", prefix*)
            search_type: Filter by symbol type (function, class, method)
            repo_id: Optional repository ID to limit search
            limit: Maximum results to return
        
        Returns:
            Search results with matching symbols and snippets
        """
        # Build FTS5 query
        # Escape special characters and handle user input
        fts_query = self._prepare_fts_query(query)
        
        # Build SQL query
        sql = """
            SELECT s.*, f.path as file_path, f.repo_id, r.name as repo_name,
                   snippet(symbols_fts, 0, '<match>', '</match>', '...', 32) as name_snippet,
                   snippet(symbols_fts, 2, '<match>', '</match>', '...', 64) as docstring_snippet,
                   rank
            FROM symbols_fts
            JOIN symbols s ON symbols_fts.rowid = s.id
            JOIN files f ON s.file_id = f.id
            JOIN repositories r ON f.repo_id = r.id
            WHERE symbols_fts MATCH ?
        """
        params = [fts_query]
        
        if search_type and search_type != "all":
            sql += " AND s.type = ?"
            params.append(search_type)
        
        if repo_id:
            sql += " AND f.repo_id = ?"
            params.append(repo_id)
        
        sql += " ORDER BY rank LIMIT ?"
        params.append(limit)
        
        try:
            rows = self.db.execute(sql, tuple(params))
        except Exception:
            # Fallback to LIKE search if FTS fails
            return self._fallback_search(query, search_type, repo_id, limit)
        
        results = []
        for row in rows:
            result = self.db.row_to_dict(row)
            
            # Parse metadata
            metadata = {}
            if result.get("metadata"):
                try:
                    metadata = json.loads(result["metadata"])
                except json.JSONDecodeError:
                    pass
            
            results.append({
                "name": result["name"],
                "type": result["type"],
                "signature": result["signature"],
                "docstring": result.get("docstring"),
                "file": result["file_path"],
                "repository": {
                    "id": result["repo_id"],
                    "name": result["repo_name"]
                },
                "line_range": [result["start_line"], result["end_line"]],
                "snippets": {
                    "name": result.get("name_snippet"),
                    "docstring": result.get("docstring_snippet")
                },
                "parameters": metadata.get("parameters", []),
                "decorators": metadata.get("decorators", [])
            })
        
        return {
            "status": "success",
            "query": query,
            "total": len(results),
            "results": results
        }
    
    def search_docs(self, query: str, repo_id: int | None = None, limit: int = 20) -> dict:
        """
        Search documentation using full-text search.
        
        Args:
            query: Search query
            repo_id: Optional repository ID to limit search
            limit: Maximum results to return
        
        Returns:
            Search results with matching documentation
        """
        fts_query = self._prepare_fts_query(query)
        
        sql = """
            SELECT d.*, f.path as file_path, r.name as repo_name,
                   snippet(docs_fts, 0, '<match>', '</match>', '...', 64) as content_snippet
            FROM docs_fts
            JOIN documentation d ON docs_fts.rowid = d.id
            LEFT JOIN files f ON d.file_id = f.id
            LEFT JOIN repositories r ON d.repo_id = r.id OR f.repo_id = r.id
            WHERE docs_fts MATCH ?
        """
        params = [fts_query]
        
        if repo_id:
            sql += " AND (d.repo_id = ? OR f.repo_id = ?)"
            params.extend([repo_id, repo_id])
        
        sql += " ORDER BY rank LIMIT ?"
        params.append(limit)
        
        try:
            rows = self.db.execute(sql, tuple(params))
        except Exception:
            return {"status": "success", "query": query, "total": 0, "results": []}
        
        results = []
        for row in rows:
            result = self.db.row_to_dict(row)
            results.append({
                "doc_type": result["doc_type"],
                "content_snippet": result.get("content_snippet"),
                "file": result.get("file_path"),
                "repository": result.get("repo_name"),
                "line_range": [result.get("start_line"), result.get("end_line")]
            })
        
        return {
            "status": "success",
            "query": query,
            "total": len(results),
            "results": results
        }
    
    def find_patterns(
        self, 
        pattern_type: Literal["algorithm", "design_pattern", "all"] | None = None,
        pattern_name: str | None = None,
        repo_id: int | None = None,
        min_confidence: float = 0.5,
        limit: int = 50
    ) -> dict:
        """
        Find detected patterns in the codebase.
        
        Args:
            pattern_type: Filter by pattern type
            pattern_name: Filter by specific pattern name
            repo_id: Optional repository ID to limit search
            min_confidence: Minimum confidence threshold (0.0-1.0)
            limit: Maximum results to return
        
        Returns:
            Patterns found with evidence and locations
        """
        sql = """
            SELECT p.*, s.name as symbol_name, s.signature, s.type as symbol_type,
                   f.path as file_path, r.name as repo_name, r.id as repo_id
            FROM patterns p
            LEFT JOIN symbols s ON p.symbol_id = s.id
            JOIN files f ON p.file_id = f.id
            JOIN repositories r ON f.repo_id = r.id
            WHERE p.confidence >= ?
        """
        params = [min_confidence]
        
        if pattern_type and pattern_type != "all":
            sql += " AND p.pattern_type = ?"
            params.append(pattern_type)
        
        if pattern_name:
            sql += " AND p.pattern_name = ?"
            params.append(pattern_name)
        
        if repo_id:
            sql += " AND f.repo_id = ?"
            params.append(repo_id)
        
        sql += " ORDER BY p.confidence DESC, p.pattern_name LIMIT ?"
        params.append(limit)
        
        rows = self.db.execute(sql, tuple(params))
        
        results = []
        for row in rows:
            result = self.db.row_to_dict(row)
            results.append({
                "pattern_type": result["pattern_type"],
                "pattern_name": result["pattern_name"],
                "confidence": result["confidence"],
                "evidence": result.get("evidence"),
                "symbol": {
                    "name": result.get("symbol_name"),
                    "type": result.get("symbol_type"),
                    "signature": result.get("signature")
                } if result.get("symbol_name") else None,
                "file": result["file_path"],
                "repository": {
                    "id": result["repo_id"],
                    "name": result["repo_name"]
                }
            })
        
        # Group by pattern for summary
        pattern_groups = {}
        for r in results:
            key = f"{r['pattern_type']}:{r['pattern_name']}"
            if key not in pattern_groups:
                pattern_groups[key] = {
                    "type": r["pattern_type"],
                    "name": r["pattern_name"],
                    "count": 0,
                    "avg_confidence": 0.0
                }
            pattern_groups[key]["count"] += 1
            pattern_groups[key]["avg_confidence"] += r["confidence"]
        
        for group in pattern_groups.values():
            group["avg_confidence"] = round(group["avg_confidence"] / group["count"], 2)
        
        return {
            "status": "success",
            "total": len(results),
            "summary": list(pattern_groups.values()),
            "results": results
        }
    
    def find_imports(
        self, 
        module: str | None = None,
        repo_id: int | None = None,
        include_relative: bool = False,
        limit: int = 50
    ) -> dict:
        """
        Find import statements across the codebase.
        
        Args:
            module: Filter by module name (partial match)
            repo_id: Optional repository ID to limit search
            include_relative: Include relative imports
            limit: Maximum results to return
        
        Returns:
            Import statements with usage counts
        """
        sql = """
            SELECT i.module, i.imported_names, i.is_relative, i.line_number,
                   f.path as file_path, r.name as repo_name, r.id as repo_id
            FROM imports i
            JOIN files f ON i.file_id = f.id
            JOIN repositories r ON f.repo_id = r.id
            WHERE 1=1
        """
        params = []
        
        if not include_relative:
            sql += " AND i.is_relative = 0"
        
        if module:
            sql += " AND i.module LIKE ?"
            params.append(f"%{module}%")
        
        if repo_id:
            sql += " AND f.repo_id = ?"
            params.append(repo_id)
        
        sql += " ORDER BY i.module LIMIT ?"
        params.append(limit)
        
        rows = self.db.execute(sql, tuple(params))
        
        results = []
        module_counts = {}
        
        for row in rows:
            result = self.db.row_to_dict(row)
            
            # Parse imported names
            imported_names = []
            if result.get("imported_names"):
                try:
                    imported_names = json.loads(result["imported_names"])
                except json.JSONDecodeError:
                    pass
            
            results.append({
                "module": result["module"],
                "imported_names": imported_names,
                "is_relative": bool(result["is_relative"]),
                "line_number": result["line_number"],
                "file": result["file_path"],
                "repository": {
                    "id": result["repo_id"],
                    "name": result["repo_name"]
                }
            })
            
            # Count module usage
            mod = result["module"]
            if mod:
                base_module = mod.split(".")[0]
                module_counts[base_module] = module_counts.get(base_module, 0) + 1
        
        # Sort module counts
        top_modules = sorted(module_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "status": "success",
            "total": len(results),
            "top_modules": [{"module": m, "count": c} for m, c in top_modules],
            "results": results
        }
    
    def list_symbols(
        self,
        repo_id: int,
        symbol_type: Literal["function", "class", "method", "all"] | None = None,
        file_path: str | None = None,
        limit: int = 100
    ) -> dict:
        """
        List all symbols in a repository.
        
        Args:
            repo_id: Repository ID
            symbol_type: Filter by symbol type
            file_path: Filter by file path
            limit: Maximum results to return
        
        Returns:
            List of symbols with their details
        """
        sql = """
            SELECT s.*, f.path as file_path
            FROM symbols s
            JOIN files f ON s.file_id = f.id
            WHERE f.repo_id = ?
        """
        params = [repo_id]
        
        if symbol_type and symbol_type != "all":
            sql += " AND s.type = ?"
            params.append(symbol_type)
        
        if file_path:
            sql += " AND f.path = ?"
            params.append(file_path)
        
        sql += " ORDER BY f.path, s.start_line LIMIT ?"
        params.append(limit)
        
        rows = self.db.execute(sql, tuple(params))
        
        results = []
        for row in rows:
            result = self.db.row_to_dict(row)
            
            metadata = {}
            if result.get("metadata"):
                try:
                    metadata = json.loads(result["metadata"])
                except json.JSONDecodeError:
                    pass
            
            results.append({
                "id": result["id"],
                "name": result["name"],
                "type": result["type"],
                "signature": result["signature"],
                "docstring": result.get("docstring"),
                "file": result["file_path"],
                "line_range": [result["start_line"], result["end_line"]],
                "parameters": metadata.get("parameters", []),
                "decorators": metadata.get("decorators", [])
            })
        
        return {
            "status": "success",
            "total": len(results),
            "results": results
        }
    
    def _prepare_fts_query(self, query: str) -> str:
        """Prepare user query for FTS5 search."""
        # Remove or escape FTS5 special characters for safety
        # Keep basic operators: AND, OR, NOT
        query = query.strip()
        
        # If it looks like a simple search, wrap in quotes for phrase matching
        # or add wildcards for prefix matching
        if not any(op in query.upper() for op in [" AND ", " OR ", " NOT ", '"', "*"]):
            # Split into words and add prefix matching
            words = query.split()
            if len(words) == 1:
                return f'"{query}" OR {query}*'
            else:
                return f'"{query}" OR ({" ".join(w + "*" for w in words)})'
        
        return query
    
    def _fallback_search(
        self, 
        query: str, 
        search_type: str | None,
        repo_id: int | None,
        limit: int
    ) -> dict:
        """Fallback to LIKE search when FTS fails."""
        sql = """
            SELECT s.*, f.path as file_path, f.repo_id, r.name as repo_name
            FROM symbols s
            JOIN files f ON s.file_id = f.id
            JOIN repositories r ON f.repo_id = r.id
            WHERE (s.name LIKE ? OR s.signature LIKE ? OR s.docstring LIKE ?)
        """
        like_pattern = f"%{query}%"
        params = [like_pattern, like_pattern, like_pattern]
        
        if search_type and search_type != "all":
            sql += " AND s.type = ?"
            params.append(search_type)
        
        if repo_id:
            sql += " AND f.repo_id = ?"
            params.append(repo_id)
        
        sql += " LIMIT ?"
        params.append(limit)
        
        rows = self.db.execute(sql, tuple(params))
        
        results = []
        for row in rows:
            result = self.db.row_to_dict(row)
            results.append({
                "name": result["name"],
                "type": result["type"],
                "signature": result["signature"],
                "docstring": result.get("docstring"),
                "file": result["file_path"],
                "repository": {
                    "id": result["repo_id"],
                    "name": result["repo_name"]
                },
                "line_range": [result["start_line"], result["end_line"]]
            })
        
        return {
            "status": "success",
            "query": query,
            "total": len(results),
            "results": results,
            "search_method": "fallback_like"
        }
