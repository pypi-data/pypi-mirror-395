"""Search tools using FTS5 full-text search."""

import json
from pathlib import Path
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
        visibility: Literal["public", "private", "all"] | None = None,
        limit: int = 100,
        group_by_file: bool = False
    ) -> dict:
        """
        List all symbols in a repository.
        
        Args:
            repo_id: Repository ID
            symbol_type: Filter by symbol type
            file_path: Filter by file path
            visibility: Filter by visibility ('public', 'private', 'all'). Default: 'all'
            limit: Maximum results to return
            group_by_file: If True, group results by file path for easier reading
        
        Returns:
            List of symbols with their details.
            If group_by_file=True, returns {"by_file": {"path": [symbols...]}} structure.
        
        Response Integration:
            MUST show actual symbols in your response:
            - results[].name → List function/class names
            - results[].signature → Include full signatures
            - total → Use exact count ("N개의 심볼")
            
            When group_by_file=True, organize output by file:
            "**header1.h**
            - `func1(int x) -> int`
            - `func2(float y) -> float`
            
            **header2.h**
            - `func3(void) -> void`"
            
            IMPORTANT: Do not summarize as "다수의 함수" - list actual names.
        """
        sql = """
            SELECT s.*, f.path as file_path, f.language
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
            
            # Apply visibility filter
            if visibility and visibility != "all":
                is_public = self._is_symbol_public(result, metadata)
                if visibility == "public" and not is_public:
                    continue
                if visibility == "private" and is_public:
                    continue
            
            results.append({
                "id": result["id"],
                "name": result["name"],
                "type": result["type"],
                "signature": result["signature"],
                "docstring": result.get("docstring"),
                "file": result["file_path"],
                "line_range": [result["start_line"], result["end_line"]],
                "parameters": metadata.get("parameters", []),
                "decorators": metadata.get("decorators", []),
                "is_public": self._is_symbol_public(result, metadata)
            })
        
        # Group by file if requested
        if group_by_file:
            by_file: dict[str, list] = {}
            for r in results:
                fpath = r["file"]
                if fpath not in by_file:
                    by_file[fpath] = []
                by_file[fpath].append(r)
            
            # Generate summary text
            file_summaries = []
            for fpath, symbols in by_file.items():
                func_count = sum(1 for s in symbols if s["type"] == "function")
                class_count = sum(1 for s in symbols if s["type"] == "class")
                method_count = sum(1 for s in symbols if s["type"] == "method")
                parts = []
                if func_count > 0:
                    parts.append(f"{func_count}개 함수")
                if class_count > 0:
                    parts.append(f"{class_count}개 클래스")
                if method_count > 0:
                    parts.append(f"{method_count}개 메서드")
                file_summaries.append(f"{fpath}: {', '.join(parts) if parts else '0개 심볼'}")
            
            return {
                "status": "success",
                "total": len(results),
                "file_count": len(by_file),
                "by_file": by_file,
                "summary_text": f"총 {len(results)}개 심볼이 {len(by_file)}개 파일에서 발견됨:\n" + "\n".join(file_summaries)
            }
        
        return {
            "status": "success",
            "total": len(results),
            "results": results,
            "summary_text": f"총 {len(results)}개 심볼 발견"
        }
    
    def inspect_symbol(
        self,
        repo_id: int,
        symbol_name: str,
        include_source: bool = True,
        context_lines: int = 0
    ) -> dict:
        """
        Get detailed information about a specific symbol including source code.
        
        This tool provides complete symbol details with the actual source code
        for accurate analysis. Use this when you need to see implementation
        details, not just signatures.
        
        Args:
            repo_id: Repository ID
            symbol_name: Name of the symbol to inspect
            include_source: Include source code snippet (default: True)
            context_lines: Extra lines of context around symbol (default: 0)
        
        Returns:
            Symbol details with source code, parameters, and relationships
        """
        # Find symbol(s) by name
        rows = self.db.execute(
            """SELECT s.*, f.path as file_path, f.language, r.local_path as repo_path
               FROM symbols s
               JOIN files f ON s.file_id = f.id
               JOIN repositories r ON f.repo_id = r.id
               WHERE f.repo_id = ? AND s.name = ?
               ORDER BY f.path, s.start_line""",
            (repo_id, symbol_name)
        )
        
        if not rows:
            # Try partial match
            rows = self.db.execute(
                """SELECT s.*, f.path as file_path, f.language, r.local_path as repo_path
                   FROM symbols s
                   JOIN files f ON s.file_id = f.id
                   JOIN repositories r ON f.repo_id = r.id
                   WHERE f.repo_id = ? AND s.name LIKE ?
                   ORDER BY f.path, s.start_line
                   LIMIT 10""",
                (repo_id, f"%{symbol_name}%")
            )
        
        if not rows:
            return {
                "status": "not_found",
                "message": f"Symbol '{symbol_name}' not found in repository {repo_id}"
            }
        
        results = []
        for row in rows:
            sym = self.db.row_to_dict(row)
            
            # Parse metadata
            metadata = {}
            if sym.get("metadata"):
                try:
                    metadata = json.loads(sym["metadata"]) if isinstance(sym["metadata"], str) else sym["metadata"]
                except json.JSONDecodeError:
                    pass
            
            symbol_info = {
                "name": sym["name"],
                "type": sym["type"],
                "signature": sym["signature"],
                "docstring": sym.get("docstring"),
                "file": sym["file_path"],
                "language": sym.get("language"),
                "line_range": [sym["start_line"], sym["end_line"]],
                "parameters": metadata.get("parameters", []),
                "return_type": metadata.get("return_type"),
                "decorators": metadata.get("decorators", []),
                "generic_params": metadata.get("generic_params", []),
                "fields": metadata.get("fields", []),
                "is_public": self._is_symbol_public(sym, metadata)
            }
            
            # Extract source code if requested
            if include_source:
                source = self._extract_source_code(
                    sym["repo_path"],
                    sym["file_path"],
                    sym["start_line"],
                    sym["end_line"],
                    context_lines
                )
                if source:
                    symbol_info["source_code"] = source
            
            # Get child symbols (methods for classes)
            children = self.db.execute(
                """SELECT name, type, signature, start_line, end_line, metadata
                   FROM symbols WHERE parent_id = ?
                   ORDER BY start_line""",
                (sym["id"],)
            )
            if children:
                symbol_info["children"] = []
                for child_row in children:
                    child = self.db.row_to_dict(child_row)
                    child_meta = {}
                    if child.get("metadata"):
                        try:
                            child_meta = json.loads(child["metadata"])
                        except json.JSONDecodeError:
                            pass
                    symbol_info["children"].append({
                        "name": child["name"],
                        "type": child["type"],
                        "signature": child["signature"],
                        "line_range": [child["start_line"], child["end_line"]],
                        "parameters": child_meta.get("parameters", []),
                        "return_type": child_meta.get("return_type")
                    })
            
            # Get patterns associated with this symbol
            patterns = self.db.execute(
                "SELECT pattern_type, pattern_name, confidence, evidence FROM patterns WHERE symbol_id = ?",
                (sym["id"],)
            )
            if patterns:
                symbol_info["patterns"] = [self.db.row_to_dict(p) for p in patterns]
            
            results.append(symbol_info)
        
        if len(results) == 1:
            return {
                "status": "success",
                "symbol": results[0]
            }
        
        return {
            "status": "success",
            "message": f"Found {len(results)} symbols matching '{symbol_name}'",
            "symbols": results
        }
    
    def _extract_source_code(
        self,
        repo_path: str,
        file_path: str,
        start_line: int,
        end_line: int,
        context_lines: int = 0
    ) -> str | None:
        """
        Extract source code from a file.
        
        Args:
            repo_path: Repository local path
            file_path: Relative file path
            start_line: Start line (1-indexed)
            end_line: End line (1-indexed)
            context_lines: Extra lines of context
        
        Returns:
            Source code string or None if file not found
        """
        try:
            full_path = Path(repo_path) / file_path
            if not full_path.exists():
                return None
            
            content = full_path.read_text(encoding="utf-8", errors="ignore")
            lines = content.splitlines()
            
            # Adjust for context and bounds
            actual_start = max(1, start_line - context_lines) - 1  # Convert to 0-indexed
            actual_end = min(len(lines), end_line + context_lines)
            
            return "\n".join(lines[actual_start:actual_end])
        except Exception:
            return None
    
    def _is_symbol_public(self, sym: dict, metadata: dict) -> bool:
        """
        Determine if a symbol is public/exported based on language conventions.
        """
        language = sym.get("language", "")
        signature = sym.get("signature", "")
        name = sym.get("name", "")
        decorators = metadata.get("decorators", [])
        
        # Rust: check for 'pub' in signature
        if language == "rust":
            return "pub " in signature or signature.startswith("pub ")
        
        # C/C++: check for extern, not static
        if language in ("c", "cpp"):
            if "static" in decorators:
                return False
            return True
        
        # Go: PascalCase = exported
        if language == "go":
            return name and name[0].isupper()
        
        # Python: no leading underscore
        if language == "python":
            if name.startswith("__") and name.endswith("__"):
                return True
            return not name.startswith("_")
        
        # TypeScript/JavaScript: check for export
        if language in ("typescript", "javascript"):
            return "export" in decorators or "export " in signature
        
        # Java/C#: check for public
        if language in ("java", "csharp"):
            return "public" in decorators or "public " in signature
        
        return True
    
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
