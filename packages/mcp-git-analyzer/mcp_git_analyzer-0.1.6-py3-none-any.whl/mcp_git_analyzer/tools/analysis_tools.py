"""Repository analysis tools."""

import hashlib
import json
from datetime import datetime
from pathlib import Path

from mcp_git_analyzer.db import Database
from mcp_git_analyzer.parsers import PythonParser
from mcp_git_analyzer.parsers.javascript_parser import JavaScriptParser
from mcp_git_analyzer.parsers.typescript_parser import TypeScriptParser
from mcp_git_analyzer.parsers.java_parser import JavaParser
from mcp_git_analyzer.parsers.go_parser import GoParser
from mcp_git_analyzer.parsers.rust_parser import RustParser
from mcp_git_analyzer.parsers.c_parser import CParser
from mcp_git_analyzer.parsers.cpp_parser import CppParser
from mcp_git_analyzer.parsers.csharp_parser import CSharpParser
from mcp_git_analyzer.parsers.base_parser import BaseParser
from mcp_git_analyzer.parsers.language_detector import (
    get_language_for_extension,
    clear_build_file_cache,
)
from mcp_git_analyzer.tools.git_tools import GitTools


# Supported languages and their file extensions
SUPPORTED_LANGUAGES = {
    "python": [".py", ".pyw"],
    "javascript": [".js", ".jsx", ".mjs", ".cjs"],
    "typescript": [".ts", ".tsx", ".mts", ".cts"],
    "java": [".java"],
    "go": [".go"],
    "rust": [".rs"],
    "c": [".c"],
    "cpp": [".cpp", ".cc", ".cxx", ".c++", ".hpp", ".hxx", ".h++", ".hh"],
    "csharp": [".cs"],
}

# Ambiguous extensions that require language detection
AMBIGUOUS_EXTENSIONS = {".h"}

# File patterns to skip
SKIP_PATTERNS = [
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "node_modules",
    ".egg-info",
    "dist",
    "build",
    ".pytest_cache",
    ".mypy_cache",
    ".tox",
    ".next",
    ".nuxt",
    "coverage",
]


def get_parser(language: str) -> BaseParser | None:
    """
    Factory function to get the appropriate parser for a language.
    
    Args:
        language: Language name ('python', 'javascript', 'typescript', 'java', 'go', 'rust',
                  'c', 'cpp', 'csharp')
    
    Returns:
        Parser instance or None if language not supported
    """
    parsers = {
        "python": PythonParser,
        "javascript": JavaScriptParser,
        "typescript": TypeScriptParser,
        "java": JavaParser,
        "go": GoParser,
        "rust": RustParser,
        "c": CParser,
        "cpp": CppParser,
        "csharp": CSharpParser,
    }
    parser_class = parsers.get(language)
    return parser_class() if parser_class else None


class AnalysisTools:
    """Code analysis operations."""
    
    def __init__(self, db: Database):
        self.db = db
        # Initialize parsers lazily via factory
        self._parsers: dict[str, BaseParser] = {}
        self.git_tools = GitTools(db)
    
    def _get_parser(self, language: str) -> BaseParser | None:
        """Get or create parser for a language."""
        if language not in self._parsers:
            parser = get_parser(language)
            if parser:
                self._parsers[language] = parser
        return self._parsers.get(language)
    
    # Legacy property for backward compatibility
    @property
    def python_parser(self) -> PythonParser:
        parser = self._get_parser("python")
        if parser is None:
            parser = PythonParser()
            self._parsers["python"] = parser
        return parser  # type: ignore
    
    def analyze_repo(
        self, 
        repo_id: int, 
        languages: list[str] | None = None,
        include_call_graph: bool = False
    ) -> dict:
        """
        Analyze all files in a repository.
        
        Args:
            repo_id: Repository ID
            languages: List of languages to analyze (default: all supported)
            include_call_graph: If True, extract function call graph (optional)
        
        Returns:
            Analysis summary with statistics and detected patterns
        
        Response Integration:
            MUST include these exact values from `statistics` in your response:
            - statistics.total_files → "총 N개 파일 분석"
            - statistics.total_functions → "N개의 함수"
            - statistics.total_classes → "N개의 클래스"
            - statistics.total_methods → "N개의 메서드"
            
            NEVER estimate with "약 50개", "50+" - use exact numbers.
            
            Example usage in response:
            "분석 결과: 47개의 함수, 12개의 클래스, 89개의 메서드가 발견되었습니다."
        """
        repo = self.git_tools.get_repo_by_id(repo_id)
        if not repo:
            return {"status": "error", "message": f"Repository {repo_id} not found"}
        
        repo_path = Path(repo["local_path"])
        if not repo_path.exists():
            return {"status": "error", "message": f"Repository path not found: {repo_path}"}
        
        # Filter languages
        if languages:
            target_languages = {lang: ext for lang, ext in SUPPORTED_LANGUAGES.items() 
                              if lang in languages}
        else:
            target_languages = SUPPORTED_LANGUAGES
        
        # Collect all target files
        target_extensions = set()
        for exts in target_languages.values():
            target_extensions.update(exts)
        
        files_to_analyze = []
        for file_path in repo_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in target_extensions:
                # Skip unwanted directories
                if any(skip in str(file_path) for skip in SKIP_PATTERNS):
                    continue
                files_to_analyze.append(file_path)
        
        # Analysis results
        stats = {
            "total_files": len(files_to_analyze),
            "analyzed_files": 0,
            "total_symbols": 0,
            "total_functions": 0,
            "total_classes": 0,
            "total_methods": 0,
            "total_imports": 0,
            "total_patterns": 0,
            "total_calls": 0,
            "errors": []
        }
        
        all_patterns = []
        
        # Analyze each file
        for file_path in files_to_analyze:
            try:
                result = self._analyze_file(
                    repo_id, repo_path, file_path, 
                    extract_calls=include_call_graph
                )
                if result.get("status") == "success":
                    stats["analyzed_files"] += 1
                    summary = result.get("summary", {})
                    stats["total_symbols"] += summary.get("total_symbols", 0)
                    stats["total_functions"] += summary.get("functions", 0)
                    stats["total_classes"] += summary.get("classes", 0)
                    stats["total_methods"] += summary.get("methods", 0)
                    stats["total_imports"] += summary.get("total_imports", 0)
                    stats["total_patterns"] += summary.get("patterns_detected", 0)
                    stats["total_calls"] += summary.get("total_calls", 0)
                    
                    # Collect patterns
                    for pattern in result.get("patterns", []):
                        pattern["file"] = str(file_path.relative_to(repo_path))
                        all_patterns.append(pattern)
                else:
                    stats["errors"].append({
                        "file": str(file_path.relative_to(repo_path)),
                        "error": result.get("message", "Unknown error")
                    })
            except Exception as e:
                stats["errors"].append({
                    "file": str(file_path.relative_to(repo_path)),
                    "error": str(e)
                })
        
        # Resolve callee IDs across the repository if call graph was extracted
        if include_call_graph:
            self._resolve_callees(repo_id)
        
        # Update repository last_analyzed timestamp
        with self.db.connection() as conn:
            conn.execute(
                "UPDATE repositories SET last_analyzed = ? WHERE id = ?",
                (datetime.now().isoformat(), repo_id)
            )
            conn.commit()
        
        # Group patterns by type
        pattern_summary = {}
        for pattern in all_patterns:
            ptype = pattern["pattern_type"]
            pname = pattern["pattern_name"]
            key = f"{ptype}:{pname}"
            if key not in pattern_summary:
                pattern_summary[key] = {
                    "type": ptype,
                    "name": pname,
                    "count": 0,
                    "files": []
                }
            pattern_summary[key]["count"] += 1
            pattern_summary[key]["files"].append(pattern["file"])
        
        # Generate summary text for easy inclusion in responses
        summary_parts = [
            f"{stats['total_files']}개 파일 분석 완료",
            f"{stats['total_functions']}개 함수",
            f"{stats['total_classes']}개 클래스",
            f"{stats['total_methods']}개 메서드",
        ]
        summary_text = f"분석 결과: {', '.join(summary_parts)}"
        
        return {
            "status": "success",
            "repository": {
                "id": repo_id,
                "name": repo["name"],
                "url": repo["url"]
            },
            "statistics": stats,
            "patterns": list(pattern_summary.values()),
            "message": f"Analyzed {stats['analyzed_files']}/{stats['total_files']} files",
            "summary_text": summary_text
        }
    
    def analyze_changed_files(
        self,
        repo_id: int,
        base_ref: str = "HEAD~1",
        target_ref: str = "HEAD",
        languages: list[str] | None = None,
        include_call_graph: bool = False
    ) -> dict:
        """
        Incrementally analyze only files that changed between two Git refs.
        
        This is more efficient than full repository analysis when only a few
        files have changed (e.g., after a commit, between branches).
        
        Args:
            repo_id: Repository ID
            base_ref: Base Git reference (commit, branch, tag). Default: "HEAD~1"
            target_ref: Target Git reference to compare against. Default: "HEAD"
            languages: List of languages to analyze (default: all supported)
            include_call_graph: If True, extract function call graph
        
        Returns:
            Analysis summary with statistics for changed files only
        
        Examples:
            # Analyze changes in last commit
            analyze_changed_files(repo_id, "HEAD~1", "HEAD")
            
            # Analyze changes between branches
            analyze_changed_files(repo_id, "main", "feature-branch")
            
            # Analyze changes from a specific commit
            analyze_changed_files(repo_id, "abc123", "HEAD")
        """
        from git import Repo as GitRepo
        from git.exc import GitCommandError, InvalidGitRepositoryError
        
        repo = self.git_tools.get_repo_by_id(repo_id)
        if not repo:
            return {"status": "error", "message": f"Repository {repo_id} not found"}
        
        repo_path = Path(repo["local_path"])
        if not repo_path.exists():
            return {"status": "error", "message": f"Repository path not found: {repo_path}"}
        
        # Open git repository
        try:
            git_repo = GitRepo(repo_path)
        except InvalidGitRepositoryError:
            return {"status": "error", "message": f"Invalid git repository: {repo_path}"}
        
        # Get changed files between refs
        try:
            # Get the diff between base and target
            diff_index = git_repo.commit(base_ref).diff(target_ref)
        except GitCommandError as e:
            return {"status": "error", "message": f"Git diff failed: {e}"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to get diff: {e}"}
        
        # Filter languages
        if languages:
            target_languages = {lang: ext for lang, ext in SUPPORTED_LANGUAGES.items() 
                              if lang in languages}
        else:
            target_languages = SUPPORTED_LANGUAGES
        
        # Collect target extensions
        target_extensions = set()
        for exts in target_languages.values():
            target_extensions.update(exts)
        
        # Categorize changed files
        changed_files: list[Path] = []
        deleted_files: list[str] = []
        
        for diff_item in diff_index:
            # Handle different diff types
            # a_path: source path (before change)
            # b_path: target path (after change)
            
            if diff_item.deleted_file:
                # File was deleted
                if diff_item.a_path:
                    deleted_files.append(diff_item.a_path)
            elif diff_item.new_file or diff_item.renamed_file:
                # New file or renamed file - analyze the new path
                if diff_item.b_path:
                    file_path = repo_path / diff_item.b_path
                    if file_path.suffix in target_extensions:
                        if not any(skip in str(file_path) for skip in SKIP_PATTERNS):
                            if file_path.exists():
                                changed_files.append(file_path)
            else:
                # Modified file
                path = diff_item.b_path or diff_item.a_path
                if path:
                    file_path = repo_path / path
                    if file_path.suffix in target_extensions:
                        if not any(skip in str(file_path) for skip in SKIP_PATTERNS):
                            if file_path.exists():
                                changed_files.append(file_path)
        
        # Handle deleted files - remove from database
        for deleted_path in deleted_files:
            existing = self.db.execute(
                "SELECT id FROM files WHERE repo_id = ? AND path = ?",
                (repo_id, deleted_path)
            )
            if existing:
                file_id = existing[0]["id"]
                with self.db.connection() as conn:
                    conn.execute("DELETE FROM symbols WHERE file_id = ?", (file_id,))
                    conn.execute("DELETE FROM imports WHERE file_id = ?", (file_id,))
                    conn.execute("DELETE FROM patterns WHERE file_id = ?", (file_id,))
                    conn.execute("DELETE FROM calls WHERE file_id = ?", (file_id,))
                    conn.execute("DELETE FROM files WHERE id = ?", (file_id,))
                    conn.commit()
        
        # Analysis results
        stats = {
            "total_changed_files": len(changed_files),
            "deleted_files": len(deleted_files),
            "analyzed_files": 0,
            "unchanged_files": 0,
            "total_symbols": 0,
            "total_functions": 0,
            "total_classes": 0,
            "total_methods": 0,
            "total_imports": 0,
            "total_patterns": 0,
            "total_calls": 0,
            "errors": []
        }
        
        all_patterns = []
        
        # Analyze each changed file
        for file_path in changed_files:
            try:
                result = self._analyze_file(
                    repo_id, repo_path, file_path,
                    extract_calls=include_call_graph
                )
                if result.get("status") == "success":
                    stats["analyzed_files"] += 1
                    summary = result.get("summary", {})
                    stats["total_symbols"] += summary.get("total_symbols", 0)
                    stats["total_functions"] += summary.get("functions", 0)
                    stats["total_classes"] += summary.get("classes", 0)
                    stats["total_methods"] += summary.get("methods", 0)
                    stats["total_imports"] += summary.get("total_imports", 0)
                    stats["total_patterns"] += summary.get("patterns_detected", 0)
                    stats["total_calls"] += summary.get("total_calls", 0)
                    
                    # Collect patterns
                    for pattern in result.get("patterns", []):
                        pattern["file"] = str(file_path.relative_to(repo_path))
                        all_patterns.append(pattern)
                elif result.get("status") == "unchanged":
                    stats["unchanged_files"] += 1
                else:
                    stats["errors"].append({
                        "file": str(file_path.relative_to(repo_path)),
                        "error": result.get("message", "Unknown error")
                    })
            except Exception as e:
                stats["errors"].append({
                    "file": str(file_path.relative_to(repo_path)),
                    "error": str(e)
                })
        
        # Resolve callee IDs if call graph was extracted
        if include_call_graph:
            self._resolve_callees(repo_id)
        
        # Update repository last_analyzed timestamp
        with self.db.connection() as conn:
            conn.execute(
                "UPDATE repositories SET last_analyzed = ? WHERE id = ?",
                (datetime.now().isoformat(), repo_id)
            )
            conn.commit()
        
        # Group patterns by type
        pattern_summary = {}
        for pattern in all_patterns:
            ptype = pattern["pattern_type"]
            pname = pattern["pattern_name"]
            key = f"{ptype}:{pname}"
            if key not in pattern_summary:
                pattern_summary[key] = {
                    "type": ptype,
                    "name": pname,
                    "count": 0,
                    "files": []
                }
            pattern_summary[key]["count"] += 1
            pattern_summary[key]["files"].append(pattern["file"])
        
        return {
            "status": "success",
            "repository": {
                "id": repo_id,
                "name": repo["name"],
                "url": repo["url"]
            },
            "diff_info": {
                "base_ref": base_ref,
                "target_ref": target_ref
            },
            "statistics": stats,
            "patterns": list(pattern_summary.values()),
            "message": (
                f"Incremental analysis: {stats['analyzed_files']} files analyzed, "
                f"{stats['unchanged_files']} unchanged, {stats['deleted_files']} deleted"
            )
        }
    
    def _analyze_file(
        self, 
        repo_id: int, 
        repo_path: Path, 
        file_path: Path,
        extract_calls: bool = False
    ) -> dict:
        """Analyze a single file and store results in database."""
        relative_path = str(file_path.relative_to(repo_path))
        
        # Detect language (pass file_path for .h file detection)
        language = self._detect_language(file_path.suffix, file_path)
        if not language:
            return {"status": "skipped", "message": f"Unsupported file type: {file_path.suffix}"}
        
        # Read file content
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
        # Calculate content hash
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Check if already analyzed (same hash)
        existing = self.db.execute(
            "SELECT id, content_hash FROM files WHERE repo_id = ? AND path = ?",
            (repo_id, relative_path)
        )
        
        file_id = None
        if existing:
            if existing[0]["content_hash"] == content_hash:
                # File unchanged, skip re-analysis
                return {
                    "status": "unchanged",
                    "message": "File unchanged since last analysis",
                    "file_id": existing[0]["id"]
                }
            file_id = existing[0]["id"]
            # Delete old symbols, imports, patterns, calls for re-analysis
            with self.db.connection() as conn:
                conn.execute("DELETE FROM symbols WHERE file_id = ?", (file_id,))
                conn.execute("DELETE FROM imports WHERE file_id = ?", (file_id,))
                conn.execute("DELETE FROM patterns WHERE file_id = ?", (file_id,))
                conn.execute("DELETE FROM calls WHERE file_id = ?", (file_id,))
                conn.execute(
                    "UPDATE files SET content_hash = ?, line_count = ?, analyzed_at = ? WHERE id = ?",
                    (content_hash, content.count("\n") + 1, datetime.now().isoformat(), file_id)
                )
                conn.commit()
        else:
            # Insert new file record
            file_id = self.db.insert(
                """INSERT INTO files (repo_id, path, language, content_hash, line_count, analyzed_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (repo_id, relative_path, language, content_hash, 
                 content.count("\n") + 1, datetime.now().isoformat())
            )
        
        # Parse file based on language
        parser = self._get_parser(language)
        if not parser:
            return {"status": "skipped", "message": f"Parser not implemented for {language}"}
        
        parse_result = parser.parse_source(
            content, relative_path, extract_calls=extract_calls
        )
        
        if "error" in parse_result:
            return {"status": "error", "message": parse_result["error"]}
        
        # Store symbols
        symbol_id_map = {}  # name -> id for parent reference
        
        with self.db.connection() as conn:
            for symbol in parse_result.get("symbols", []):
                parent_id = None
                if symbol.get("parent_name"):
                    parent_id = symbol_id_map.get(symbol["parent_name"])
                
                cursor = conn.execute(
                    """INSERT INTO symbols 
                       (file_id, name, type, signature, docstring, start_line, end_line, parent_id, metadata)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (file_id, symbol["name"], symbol["type"], symbol["signature"],
                     symbol.get("docstring"), symbol["start_line"], symbol["end_line"],
                     parent_id, json.dumps({
                         "parameters": symbol.get("parameters", []),
                         "return_type": symbol.get("return_type"),
                         "decorators": symbol.get("decorators", [])
                     }))
                )
                symbol_id_map[symbol["name"]] = cursor.lastrowid
            
            # Store imports
            for imp in parse_result.get("imports", []):
                conn.execute(
                    """INSERT OR IGNORE INTO imports 
                       (file_id, module, alias, imported_names, is_relative, line_number)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (file_id, imp["module"], imp.get("alias"),
                     json.dumps(imp.get("imported_names", [])),
                     imp.get("is_relative", False), imp.get("line_number"))
                )
            
            # Store patterns
            for pattern in parse_result.get("patterns", []):
                # Find associated symbol if mentioned in evidence
                symbol_id = None
                for name, sid in symbol_id_map.items():
                    if name in pattern.get("evidence", ""):
                        symbol_id = sid
                        break
                
                conn.execute(
                    """INSERT INTO patterns 
                       (symbol_id, file_id, pattern_type, pattern_name, confidence, evidence)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (symbol_id, file_id, pattern["pattern_type"], pattern["pattern_name"],
                     pattern.get("confidence", 1.0), pattern.get("evidence"))
                )
            
            # Store calls if extracted
            if extract_calls:
                # Build caller_name -> symbol_id mapping (fully qualified names)
                caller_id_map: dict[str, int] = {}
                for symbol in parse_result.get("symbols", []):
                    if symbol["type"] in ("function", "method"):
                        if symbol.get("parent_name"):
                            full_name = f"{symbol['parent_name']}.{symbol['name']}"
                        else:
                            full_name = symbol["name"]
                        if symbol["name"] in symbol_id_map:
                            caller_id_map[full_name] = symbol_id_map[symbol["name"]]
                
                for call in parse_result.get("calls", []):
                    caller_id = caller_id_map.get(call["caller_name"])
                    conn.execute(
                        """INSERT INTO calls 
                           (file_id, caller_id, caller_name, callee_name, callee_id, 
                            call_type, line_number, is_external, module, is_resolved, metadata)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (file_id, caller_id, call["caller_name"], call["callee_name"],
                         None,  # callee_id resolved later
                         call["call_type"], call["line_number"], call["is_external"],
                         call.get("module"), False,
                         json.dumps({"arguments": call.get("arguments", [])}))
                    )
            
            conn.commit()
        
        return {
            "status": "success",
            "file_id": file_id,
            "summary": parse_result.get("summary", {}),
            "patterns": parse_result.get("patterns", [])
        }
    
    def _resolve_callees(self, repo_id: int) -> int:
        """
        Resolve callee_id for calls within the repository.
        
        Matches callee_name to symbol names in the same repository.
        
        Args:
            repo_id: Repository ID
        
        Returns:
            Number of calls resolved
        """
        resolved_count = 0
        
        with self.db.connection() as conn:
            # Get all unresolved calls for this repo
            calls = conn.execute("""
                SELECT c.id, c.callee_name, c.file_id
                FROM calls c
                JOIN files f ON c.file_id = f.id
                WHERE f.repo_id = ? AND c.is_resolved = FALSE AND c.is_external = FALSE
            """, (repo_id,)).fetchall()
            
            # Get all symbols in repo for matching
            symbols = conn.execute("""
                SELECT s.id, s.name, s.type, s.parent_id, f.id as file_id,
                       (SELECT p.name FROM symbols p WHERE p.id = s.parent_id) as parent_name
                FROM symbols s
                JOIN files f ON s.file_id = f.id
                WHERE f.repo_id = ? AND s.type IN ('function', 'method')
            """, (repo_id,)).fetchall()
            
            # Build lookup: name -> symbol_id (prefer same file, then any)
            # For methods, match both "method" and "ClassName.method"
            symbol_lookup: dict[str, list[tuple[int, int]]] = {}  # name -> [(symbol_id, file_id), ...]
            for sym in symbols:
                # Simple name
                if sym["name"] not in symbol_lookup:
                    symbol_lookup[sym["name"]] = []
                symbol_lookup[sym["name"]].append((sym["id"], sym["file_id"]))
                
                # Fully qualified name for methods
                if sym["parent_name"]:
                    full_name = f"{sym['parent_name']}.{sym['name']}"
                    if full_name not in symbol_lookup:
                        symbol_lookup[full_name] = []
                    symbol_lookup[full_name].append((sym["id"], sym["file_id"]))
            
            # Resolve each call
            for call in calls:
                callee_name = call["callee_name"]
                call_file_id = call["file_id"]
                
                # Try exact match first
                if callee_name in symbol_lookup:
                    candidates = symbol_lookup[callee_name]
                    
                    # Prefer same file
                    same_file = [c for c in candidates if c[1] == call_file_id]
                    if same_file:
                        callee_id = same_file[0][0]
                    else:
                        callee_id = candidates[0][0]
                    
                    conn.execute(
                        "UPDATE calls SET callee_id = ?, is_resolved = TRUE WHERE id = ?",
                        (callee_id, call["id"])
                    )
                    resolved_count += 1
                else:
                    # Try matching just the method name if it's a qualified name
                    if "." in callee_name:
                        method_name = callee_name.split(".")[-1]
                        if method_name in symbol_lookup:
                            candidates = symbol_lookup[method_name]
                            same_file = [c for c in candidates if c[1] == call_file_id]
                            if same_file:
                                callee_id = same_file[0][0]
                            else:
                                callee_id = candidates[0][0]
                            
                            conn.execute(
                                "UPDATE calls SET callee_id = ?, is_resolved = TRUE WHERE id = ?",
                                (callee_id, call["id"])
                            )
                            resolved_count += 1
            
            conn.commit()
        
        return resolved_count
    
    def get_file_analysis(self, repo_id: int, file_path: str) -> dict:
        """
        Get detailed analysis for a specific file.
        
        Args:
            repo_id: Repository ID
            file_path: Relative path to file within repository
        
        Returns:
            Detailed analysis including symbols, imports, patterns
        
        Response Integration:
            MUST list actual symbols from this file in your response:
            - symbols[].name → Show each function/class name
            - symbols[].signature → Include full signature with parameters
            - symbols[].parameters → Detail parameter names and types
            
            Example format in response:
            "**{file_path}** (N개 함수)
            - `function_name(param1: int, param2: str) -> bool`
            - `another_function(data: list) -> None`"
            
            IMPORTANT: List ALL symbols from the response, do not summarize as
            "여러 유틸리티 함수" or omit any.
        """
        # Get file record
        rows = self.db.execute(
            "SELECT * FROM files WHERE repo_id = ? AND path = ?",
            (repo_id, file_path)
        )
        if not rows:
            return {"status": "error", "message": f"File not found: {file_path}"}
        
        file_info = self.db.row_to_dict(rows[0])
        file_id = file_info["id"]
        
        # Get symbols
        symbols = self.db.execute(
            """SELECT * FROM symbols WHERE file_id = ? ORDER BY start_line""",
            (file_id,)
        )
        
        # Get imports
        imports = self.db.execute(
            "SELECT * FROM imports WHERE file_id = ? ORDER BY line_number",
            (file_id,)
        )
        
        # Get patterns
        patterns = self.db.execute(
            "SELECT * FROM patterns WHERE file_id = ?",
            (file_id,)
        )
        
        return {
            "status": "success",
            "file": file_info,
            "symbols": [self._format_symbol(self.db.row_to_dict(s)) for s in symbols],
            "imports": [self.db.row_to_dict(i) for i in imports],
            "patterns": [self.db.row_to_dict(p) for p in patterns]
        }
    
    def get_symbol_details(self, symbol_name: str, repo_id: int | None = None) -> dict:
        """
        Get detailed information about a symbol.
        
        Args:
            symbol_name: Name of the symbol to look up
            repo_id: Optional repository ID to limit search
        
        Returns:
            Symbol details with location, signature, docstring, and related patterns
        """
        if repo_id:
            rows = self.db.execute(
                """SELECT s.*, f.path as file_path, f.repo_id, r.name as repo_name
                   FROM symbols s
                   JOIN files f ON s.file_id = f.id
                   JOIN repositories r ON f.repo_id = r.id
                   WHERE s.name = ? AND f.repo_id = ?""",
                (symbol_name, repo_id)
            )
        else:
            rows = self.db.execute(
                """SELECT s.*, f.path as file_path, f.repo_id, r.name as repo_name
                   FROM symbols s
                   JOIN files f ON s.file_id = f.id
                   JOIN repositories r ON f.repo_id = r.id
                   WHERE s.name = ?""",
                (symbol_name,)
            )
        
        if not rows:
            return {"status": "not_found", "message": f"Symbol '{symbol_name}' not found"}
        
        results = []
        for row in rows:
            symbol = self.db.row_to_dict(row)
            
            # Get patterns for this symbol
            patterns = self.db.execute(
                "SELECT * FROM patterns WHERE symbol_id = ?",
                (symbol["id"],)
            )
            
            # Get child symbols (methods for classes)
            children = self.db.execute(
                "SELECT * FROM symbols WHERE parent_id = ?",
                (symbol["id"],)
            )
            
            results.append({
                **self._format_symbol(symbol),
                "file": symbol["file_path"],
                "repository": {
                    "id": symbol["repo_id"],
                    "name": symbol["repo_name"]
                },
                "patterns": [self.db.row_to_dict(p) for p in patterns],
                "children": [self._format_symbol(self.db.row_to_dict(c)) for c in children]
            })
        
        if len(results) == 1:
            return {"status": "found", "symbol": results[0]}
        
        return {
            "status": "found",
            "message": f"Found {len(results)} symbols with name '{symbol_name}'",
            "symbols": results
        }
    
    def get_repo_summary(self, repo_id: int) -> dict:
        """
        Get comprehensive summary of a repository's analysis.
        
        Args:
            repo_id: Repository ID
        
        Returns:
            Summary with language breakdown, top patterns, key symbols
        """
        repo = self.git_tools.get_repo_by_id(repo_id)
        if not repo:
            return {"status": "error", "message": f"Repository {repo_id} not found"}
        
        # Language breakdown
        lang_stats = self.db.execute(
            """SELECT language, COUNT(*) as file_count, SUM(line_count) as total_lines
               FROM files WHERE repo_id = ? GROUP BY language""",
            (repo_id,)
        )
        
        # Symbol counts by type
        symbol_stats = self.db.execute(
            """SELECT s.type, COUNT(*) as count
               FROM symbols s
               JOIN files f ON s.file_id = f.id
               WHERE f.repo_id = ?
               GROUP BY s.type""",
            (repo_id,)
        )
        
        # Top patterns
        pattern_stats = self.db.execute(
            """SELECT pattern_type, pattern_name, COUNT(*) as count
               FROM patterns p
               JOIN files f ON p.file_id = f.id
               WHERE f.repo_id = ?
               GROUP BY pattern_type, pattern_name
               ORDER BY count DESC
               LIMIT 10""",
            (repo_id,)
        )
        
        # Most used imports
        import_stats = self.db.execute(
            """SELECT module, COUNT(*) as count
               FROM imports i
               JOIN files f ON i.file_id = f.id
               WHERE f.repo_id = ? AND i.is_relative = 0
               GROUP BY module
               ORDER BY count DESC
               LIMIT 15""",
            (repo_id,)
        )
        
        # Key classes (with most methods)
        key_classes = self.db.execute(
            """SELECT c.name, c.signature, c.docstring, f.path as file_path,
                      COUNT(m.id) as method_count
               FROM symbols c
               JOIN files f ON c.file_id = f.id
               LEFT JOIN symbols m ON m.parent_id = c.id
               WHERE f.repo_id = ? AND c.type = 'class'
               GROUP BY c.id
               ORDER BY method_count DESC
               LIMIT 10""",
            (repo_id,)
        )
        
        # Calculate totals for summary text
        symbol_counts = {r["type"]: r["count"] for r in symbol_stats}
        total_functions = symbol_counts.get("function", 0)
        total_classes = symbol_counts.get("class", 0)
        total_methods = symbol_counts.get("method", 0)
        total_files = sum(r["file_count"] for r in lang_stats)
        
        # Generate summary text
        summary_parts = []
        if total_files > 0:
            summary_parts.append(f"{total_files}개 파일")
        if total_functions > 0:
            summary_parts.append(f"{total_functions}개 함수")
        if total_classes > 0:
            summary_parts.append(f"{total_classes}개 클래스")
        if total_methods > 0:
            summary_parts.append(f"{total_methods}개 메서드")
        summary_text = f"저장소 요약: {', '.join(summary_parts)}" if summary_parts else "분석 데이터 없음"
        
        return {
            "status": "success",
            "repository": {
                "id": repo["id"],
                "name": repo["name"],
                "url": repo["url"],
                "last_analyzed": repo.get("last_analyzed")
            },
            "languages": [self.db.row_to_dict(r) for r in lang_stats],
            "symbol_counts": symbol_counts,
            "top_patterns": [self.db.row_to_dict(r) for r in pattern_stats],
            "top_imports": [self.db.row_to_dict(r) for r in import_stats],
            "key_classes": [self.db.row_to_dict(r) for r in key_classes],
            "summary_text": summary_text
        }
    
    def _detect_language(self, extension: str, file_path: Path | None = None) -> str | None:
        """
        Detect language from file extension.
        
        For ambiguous extensions like .h, uses content-based detection
        via the language_detector module.
        
        Args:
            extension: File extension (e.g., '.py', '.h')
            file_path: Full path to file (needed for .h detection)
        
        Returns:
            Language name or None if unsupported
        """
        # Handle ambiguous extensions
        if extension in AMBIGUOUS_EXTENSIONS:
            if file_path is not None:
                return get_language_for_extension(extension, file_path)
            # Default to C for .h files when path not provided
            return "c"
        
        # Standard extension lookup
        for lang, extensions in SUPPORTED_LANGUAGES.items():
            if extension in extensions:
                return lang
        return None
    
    def _format_symbol(self, symbol: dict) -> dict:
        """Format symbol for JSON output."""
        result = {
            "id": symbol["id"],
            "name": symbol["name"],
            "type": symbol["type"],
            "signature": symbol["signature"],
            "docstring": symbol.get("docstring"),
            "line_range": [symbol["start_line"], symbol["end_line"]]
        }
        
        # Parse metadata if present
        if symbol.get("metadata"):
            try:
                metadata = json.loads(symbol["metadata"]) if isinstance(symbol["metadata"], str) else symbol["metadata"]
                result.update({
                    "parameters": metadata.get("parameters", []),
                    "return_type": metadata.get("return_type"),
                    "decorators": metadata.get("decorators", [])
                })
            except json.JSONDecodeError:
                pass
        
        return result

    def get_call_graph(
        self, 
        repo_id: int, 
        symbol_name: str | None = None,
        depth: int = 3,
        direction: str = "both",
        output_format: str = "json"
    ) -> dict:
        """
        Get call graph for a repository or specific symbol.
        
        Args:
            repo_id: Repository ID
            symbol_name: Optional symbol name to focus on
            depth: Maximum traversal depth (default: 3)
            direction: "callers", "callees", or "both" (default: "both")
            output_format: "json" or "mermaid" (default: "json")
        
        Returns:
            Call graph data in requested format
        """
        repo = self.git_tools.get_repo_by_id(repo_id)
        if not repo:
            return {"status": "error", "message": f"Repository {repo_id} not found"}
        
        with self.db.connection() as conn:
            # Get all calls for this repository
            all_calls = conn.execute("""
                SELECT c.*, f.path as file_path,
                       s1.name as caller_symbol_name, s1.type as caller_type,
                       s2.name as callee_symbol_name, s2.type as callee_type
                FROM calls c
                JOIN files f ON c.file_id = f.id
                LEFT JOIN symbols s1 ON c.caller_id = s1.id
                LEFT JOIN symbols s2 ON c.callee_id = s2.id
                WHERE f.repo_id = ?
            """, (repo_id,)).fetchall()
        
        if not all_calls:
            return {
                "status": "success",
                "message": "No call graph data available. Run analyze_repo with include_call_graph=True first.",
                "nodes": [],
                "edges": []
            }
        
        # Build graph structure
        nodes: dict[str, dict] = {}
        edges: list[dict] = []
        
        for call in all_calls:
            caller = call["caller_name"]
            callee = call["callee_name"]
            
            # Add nodes
            if caller not in nodes:
                nodes[caller] = {
                    "name": caller,
                    "type": call["caller_type"] or "function",
                    "file": call["file_path"],
                    "is_resolved": call["caller_id"] is not None
                }
            
            if callee not in nodes:
                nodes[callee] = {
                    "name": callee,
                    "type": call["callee_type"] or call["call_type"],
                    "is_external": call["is_external"],
                    "module": call["module"],
                    "is_resolved": call["callee_id"] is not None
                }
            
            # Add edge
            edges.append({
                "caller": caller,
                "callee": callee,
                "call_type": call["call_type"],
                "line_number": call["line_number"],
                "file": call["file_path"]
            })
        
        # Filter by symbol if specified
        if symbol_name:
            filtered_nodes, filtered_edges = self._filter_call_graph(
                nodes, edges, symbol_name, depth, direction
            )
        else:
            filtered_nodes = nodes
            filtered_edges = edges
        
        # Format output
        if output_format == "mermaid":
            return {
                "status": "success",
                "format": "mermaid",
                "diagram": self._format_call_graph_mermaid(filtered_nodes, filtered_edges),
                "node_count": len(filtered_nodes),
                "edge_count": len(filtered_edges)
            }
        else:
            return {
                "status": "success",
                "format": "json",
                "nodes": list(filtered_nodes.values()),
                "edges": filtered_edges,
                "statistics": {
                    "total_nodes": len(filtered_nodes),
                    "total_edges": len(filtered_edges),
                    "external_calls": len([n for n in filtered_nodes.values() if n.get("is_external")]),
                    "resolved_calls": len([e for e in filtered_edges if filtered_nodes.get(e["callee"], {}).get("is_resolved")])
                }
            }
    
    def _filter_call_graph(
        self,
        nodes: dict[str, dict],
        edges: list[dict],
        symbol_name: str,
        depth: int,
        direction: str
    ) -> tuple[dict[str, dict], list[dict]]:
        """
        Filter call graph to show only nodes within depth of symbol.
        
        Args:
            nodes: All nodes in graph
            edges: All edges in graph
            symbol_name: Symbol to center on
            depth: Maximum depth to traverse
            direction: "callers", "callees", or "both"
        
        Returns:
            Filtered (nodes, edges) tuple
        """
        # Find matching symbol (exact or partial match)
        matching_nodes = [
            name for name in nodes 
            if name == symbol_name or name.endswith(f".{symbol_name}")
        ]
        
        if not matching_nodes:
            return {}, []
        
        target_node = matching_nodes[0]
        included_nodes: set[str] = {target_node}
        
        # Build adjacency lists
        callers_of: dict[str, set[str]] = {}  # callee -> set of callers
        callees_of: dict[str, set[str]] = {}  # caller -> set of callees
        
        for edge in edges:
            caller, callee = edge["caller"], edge["callee"]
            if callee not in callers_of:
                callers_of[callee] = set()
            callers_of[callee].add(caller)
            
            if caller not in callees_of:
                callees_of[caller] = set()
            callees_of[caller].add(callee)
        
        # BFS to find nodes within depth
        if direction in ("callers", "both"):
            queue = [(target_node, 0)]
            while queue:
                node, d = queue.pop(0)
                if d < depth:
                    for caller in callers_of.get(node, set()):
                        if caller not in included_nodes:
                            included_nodes.add(caller)
                            queue.append((caller, d + 1))
        
        if direction in ("callees", "both"):
            queue = [(target_node, 0)]
            while queue:
                node, d = queue.pop(0)
                if d < depth:
                    for callee in callees_of.get(node, set()):
                        if callee not in included_nodes:
                            included_nodes.add(callee)
                            queue.append((callee, d + 1))
        
        # Filter nodes and edges
        filtered_nodes = {k: v for k, v in nodes.items() if k in included_nodes}
        filtered_edges = [
            e for e in edges 
            if e["caller"] in included_nodes and e["callee"] in included_nodes
        ]
        
        return filtered_nodes, filtered_edges
    
    def _format_call_graph_mermaid(
        self, 
        nodes: dict[str, dict], 
        edges: list[dict]
    ) -> str:
        """
        Format call graph as Mermaid flowchart diagram.
        
        Args:
            nodes: Node dict with name -> info
            edges: List of edge dicts with caller, callee
        
        Returns:
            Mermaid diagram string
        """
        lines = ["flowchart LR"]
        
        # Generate node definitions
        node_ids: dict[str, str] = {}
        for i, (name, info) in enumerate(nodes.items()):
            node_id = f"n{i}"
            node_ids[name] = node_id
            
            # Format node label
            display_name = name.replace('"', "'")
            
            # Use different shapes for different node types
            if info.get("is_external"):
                # External calls use double brackets {{}}
                lines.append(f"    {node_id}{{{{{display_name}}}}}")
            elif info.get("type") == "method":
                # Methods use rounded rectangle
                lines.append(f"    {node_id}({display_name})")
            elif info.get("type") == "builtin":
                # Builtins use stadium shape
                lines.append(f"    {node_id}([{display_name}])")
            else:
                # Regular functions use rectangle
                lines.append(f"    {node_id}[{display_name}]")
        
        # Generate edges
        seen_edges: set[tuple[str, str]] = set()
        for edge in edges:
            caller_id = node_ids.get(edge["caller"])
            callee_id = node_ids.get(edge["callee"])
            if caller_id and callee_id:
                edge_key = (caller_id, callee_id)
                if edge_key not in seen_edges:
                    seen_edges.add(edge_key)
                    lines.append(f"    {caller_id} --> {callee_id}")
        
        return "\n".join(lines)
    
    def find_callers(self, symbol_name: str, repo_id: int | None = None) -> dict:
        """
        Find all callers of a specific function or method.
        
        Args:
            symbol_name: Name of the function/method
            repo_id: Optional repository ID to limit search
        
        Returns:
            List of callers with context
        """
        with self.db.connection() as conn:
            if repo_id:
                rows = conn.execute("""
                    SELECT c.*, f.path as file_path, r.name as repo_name
                    FROM calls c
                    JOIN files f ON c.file_id = f.id
                    JOIN repositories r ON f.repo_id = r.id
                    WHERE (c.callee_name = ? OR c.callee_name LIKE ?)
                      AND f.repo_id = ?
                    ORDER BY c.caller_name
                """, (symbol_name, f"%.{symbol_name}", repo_id)).fetchall()
            else:
                rows = conn.execute("""
                    SELECT c.*, f.path as file_path, r.name as repo_name
                    FROM calls c
                    JOIN files f ON c.file_id = f.id
                    JOIN repositories r ON f.repo_id = r.id
                    WHERE c.callee_name = ? OR c.callee_name LIKE ?
                    ORDER BY r.name, c.caller_name
                """, (symbol_name, f"%.{symbol_name}")).fetchall()
        
        callers = []
        for row in rows:
            callers.append({
                "caller": row["caller_name"],
                "callee": row["callee_name"],
                "file": row["file_path"],
                "line": row["line_number"],
                "call_type": row["call_type"],
                "repository": row["repo_name"]
            })
        
        return {
            "status": "success",
            "symbol": symbol_name,
            "caller_count": len(callers),
            "callers": callers
        }
    
    def find_callees(self, symbol_name: str, repo_id: int) -> dict:
        """
        Find all functions called by a specific function or method.
        
        Args:
            symbol_name: Name of the function/method
            repo_id: Repository ID
        
        Returns:
            List of callees with context
        """
        with self.db.connection() as conn:
            rows = conn.execute("""
                SELECT c.*, f.path as file_path
                FROM calls c
                JOIN files f ON c.file_id = f.id
                WHERE (c.caller_name = ? OR c.caller_name LIKE ?)
                  AND f.repo_id = ?
                ORDER BY c.line_number
            """, (symbol_name, f"%.{symbol_name}", repo_id)).fetchall()
        
        callees = []
        for row in rows:
            callees.append({
                "callee": row["callee_name"],
                "caller": row["caller_name"],
                "file": row["file_path"],
                "line": row["line_number"],
                "call_type": row["call_type"],
                "is_external": row["is_external"],
                "module": row["module"],
                "is_resolved": row["is_resolved"]
            })
        
        return {
            "status": "success",
            "symbol": symbol_name,
            "callee_count": len(callees),
            "callees": callees
        }
    
    def get_public_api(
        self,
        repo_id: int,
        include_fields: bool = True,
        include_methods: bool = True,
        file_path: str | None = None
    ) -> dict:
        """
        Extract public API surface from a repository.
        
        Specifically designed for porting analysis: extracts only exported/public
        symbols (functions, structs, classes) with their signatures, fields, and
        method definitions. LLM clients should use this output verbatim rather
        than hallucinating API structures.
        
        Args:
            repo_id: Repository ID
            include_fields: Include struct/class field definitions (default: True)
            include_methods: Include method definitions for classes (default: True)
            file_path: Optional file path to limit scope
        
        Returns:
            Public API surface with:
            - functions: Exported/public function signatures with parameters
            - types: Structs, classes, interfaces with their fields
            - constants: Exported constants/static values
        """
        repo = self.git_tools.get_repo_by_id(repo_id)
        if not repo:
            return {"status": "error", "message": f"Repository {repo_id} not found"}
        
        # Build query for public symbols
        if file_path:
            symbols = self.db.execute(
                """SELECT s.*, f.path as file_path, f.language
                   FROM symbols s
                   JOIN files f ON s.file_id = f.id
                   WHERE f.repo_id = ? AND f.path = ?
                   ORDER BY f.path, s.start_line""",
                (repo_id, file_path)
            )
        else:
            symbols = self.db.execute(
                """SELECT s.*, f.path as file_path, f.language
                   FROM symbols s
                   JOIN files f ON s.file_id = f.id
                   WHERE f.repo_id = ?
                   ORDER BY f.path, s.start_line""",
                (repo_id,)
            )
        
        # Categorize symbols
        functions: list[dict] = []
        types: list[dict] = []
        constants: list[dict] = []
        
        for row in symbols:
            sym = self.db.row_to_dict(row)
            
            # Parse metadata
            metadata = {}
            if sym.get("metadata"):
                try:
                    metadata = json.loads(sym["metadata"]) if isinstance(sym["metadata"], str) else sym["metadata"]
                except json.JSONDecodeError:
                    pass
            
            # Check if symbol is exported/public
            # Different languages have different export conventions:
            # - Rust: pub keyword (check signature)
            # - C/C++: extern, non-static (check decorators)
            # - Go: PascalCase names
            # - Python: no leading underscore
            # - TypeScript/JS: export keyword
            is_public = self._is_symbol_public(sym, metadata)
            
            if not is_public:
                continue
            
            if sym["type"] == "function" and sym.get("parent_id") is None:
                # Top-level function
                functions.append({
                    "name": sym["name"],
                    "signature": sym["signature"],
                    "parameters": metadata.get("parameters", []),
                    "return_type": metadata.get("return_type"),
                    "docstring": sym.get("docstring"),
                    "file": sym["file_path"],
                    "line_range": [sym["start_line"], sym["end_line"]],
                    "decorators": metadata.get("decorators", [])
                })
            
            elif sym["type"] in ("class", "interface"):
                type_info: dict = {
                    "name": sym["name"],
                    "kind": sym["type"],
                    "signature": sym["signature"],
                    "docstring": sym.get("docstring"),
                    "file": sym["file_path"],
                    "line_range": [sym["start_line"], sym["end_line"]],
                    "generic_params": metadata.get("generic_params", [])
                }
                
                # Extract fields if available (from metadata or struct parsing)
                if include_fields:
                    fields = metadata.get("fields", [])
                    if fields:
                        type_info["fields"] = fields
                
                # Get methods if requested
                if include_methods:
                    methods = self.db.execute(
                        """SELECT * FROM symbols
                           WHERE parent_id = ? AND type IN ('method', 'function')
                           ORDER BY start_line""",
                        (sym["id"],)
                    )
                    type_info["methods"] = []
                    for method_row in methods:
                        method = self.db.row_to_dict(method_row)
                        method_meta = {}
                        if method.get("metadata"):
                            try:
                                method_meta = json.loads(method["metadata"]) if isinstance(method["metadata"], str) else method["metadata"]
                            except json.JSONDecodeError:
                                pass
                        
                        type_info["methods"].append({
                            "name": method["name"],
                            "signature": method["signature"],
                            "parameters": method_meta.get("parameters", []),
                            "return_type": method_meta.get("return_type"),
                            "docstring": method.get("docstring"),
                            "decorators": method_meta.get("decorators", [])
                        })
                
                types.append(type_info)
            
            elif sym["type"] == "variable":
                # Constants/static values
                constants.append({
                    "name": sym["name"],
                    "signature": sym["signature"],
                    "docstring": sym.get("docstring"),
                    "file": sym["file_path"],
                    "line": sym["start_line"]
                })
        
        # Group by file for header_files
        header_files: dict[str, dict] = {}
        source_files: dict[str, dict] = {}
        
        for func in functions:
            file_path = func.get("file", "")
            is_header = self._is_header_file(file_path)
            target = header_files if is_header else source_files
            
            if file_path not in target:
                target[file_path] = {"functions": [], "types": [], "constants": []}
            target[file_path]["functions"].append(func)
        
        for type_info in types:
            file_path = type_info.get("file", "")
            is_header = self._is_header_file(file_path)
            target = header_files if is_header else source_files
            
            if file_path not in target:
                target[file_path] = {"functions": [], "types": [], "constants": []}
            target[file_path]["types"].append(type_info)
        
        for const in constants:
            file_path = const.get("file", "")
            is_header = self._is_header_file(file_path)
            target = header_files if is_header else source_files
            
            if file_path not in target:
                target[file_path] = {"functions": [], "types": [], "constants": []}
            target[file_path]["constants"].append(const)
        
        # Generate formatted summary markdown
        formatted_summary = self._generate_api_summary_markdown(
            repo["name"], header_files, source_files, functions, types, constants
        )
        
        # Build grounded_values for AI response validation
        grounded_values = {
            "total_functions": len(functions),
            "total_types": len(types),
            "total_constants": len(constants),
            "total_public_symbols": len(functions) + len(types) + len(constants),
            "header_file_count": len(header_files),
            "source_file_count": len(source_files),
            "must_quote": [
                "functions[*].name",
                "functions[*].signature",
                "types[*].name",
                "types[*].fields",
                "constants[*].name",
                "statistics.*"
            ],
            "warning": "이 값들은 도구 결과에서 직접 추출됨. 응답에 그대로 사용할 것. 추측하지 말 것."
        }
        
        return {
            "status": "success",
            "repository": {
                "id": repo_id,
                "name": repo["name"]
            },
            "public_api": {
                "functions": functions,
                "types": types,
                "constants": constants
            },
            "header_files": header_files,
            "source_files": source_files,
            "statistics": {
                "total_functions": len(functions),
                "total_types": len(types),
                "total_constants": len(constants),
                "by_file": {
                    path: {
                        "functions": len(data["functions"]),
                        "types": len(data["types"]),
                        "constants": len(data["constants"])
                    }
                    for path, data in {**header_files, **source_files}.items()
                }
            },
            "grounded_values": grounded_values,
            "formatted_summary": formatted_summary,
            "usage_note": "Use formatted_summary for direct inclusion in response. Use grounded_values for exact counts."
        }
    
    def _is_symbol_public(self, sym: dict, metadata: dict) -> bool:
        """
        Determine if a symbol is public/exported based on language conventions.
        
        Args:
            sym: Symbol dict with name, signature, etc.
            metadata: Parsed metadata dict
        
        Returns:
            True if symbol should be considered part of public API
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
            if "extern" in decorators:
                return True
            # Default to public for C/C++ unless static
            return True
        
        # Go: PascalCase = exported
        if language == "go":
            return name and name[0].isupper()
        
        # Python: no leading underscore (except __init__ etc)
        if language == "python":
            if name.startswith("__") and name.endswith("__"):
                return True  # Dunder methods are public
            return not name.startswith("_")
        
        # TypeScript/JavaScript: check for export decorator or keyword
        if language in ("typescript", "javascript"):
            return "export" in decorators or "export " in signature
        
        # Java/C#: check for public modifier
        if language in ("java", "csharp"):
            return "public" in decorators or "public " in signature
        
        # Default: assume public
        return True
    
    def _is_header_file(self, file_path: str) -> bool:
        """
        Determine if a file is a header file based on extension.
        
        Args:
            file_path: File path to check
        
        Returns:
            True if file is a header file (.h, .hpp, etc.)
        """
        if not file_path:
            return False
        
        header_extensions = {".h", ".hpp", ".hxx", ".h++", ".hh"}
        ext = Path(file_path).suffix.lower()
        return ext in header_extensions
    
    def _get_source_type(self, file_path: str) -> str:
        """
        Determine the source type of a file.
        
        Args:
            file_path: File path to check
        
        Returns:
            "header", "source", or "test"
        """
        if not file_path:
            return "source"
        
        path = Path(file_path)
        name = path.name.lower()
        ext = path.suffix.lower()
        
        # Check for test files
        if (name.startswith("test_") or 
            name.endswith("_test.c") or 
            name.endswith("_test.cpp") or
            name.endswith(".test.c") or
            name.endswith(".test.cpp") or
            "tests/" in file_path.lower() or
            "test/" in file_path.lower()):
            return "test"
        
        # Check for header files
        if ext in {".h", ".hpp", ".hxx", ".h++", ".hh"}:
            return "header"
        
        return "source"
    
    def _generate_api_summary_markdown(
        self,
        repo_name: str,
        header_files: dict[str, dict],
        source_files: dict[str, dict],
        functions: list[dict],
        types: list[dict],
        constants: list[dict]
    ) -> str:
        """
        Generate markdown summary of the public API.
        
        This output can be directly included in AI responses.
        
        Args:
            repo_name: Repository name
            header_files: Header file → symbols mapping
            source_files: Source file → symbols mapping
            functions: List of public functions
            types: List of public types
            constants: List of public constants
        
        Returns:
            Formatted markdown string
        """
        lines = [
            f"## 원본 라이브러리 API 요약: {repo_name}",
            "",
            f"**총계**: {len(functions)}개 함수, {len(types)}개 타입, {len(constants)}개 상수",
            "",
        ]
        
        # Header files section (prioritized for C/C++)
        if header_files:
            lines.append("### 헤더 파일 (Public API)")
            lines.append("")
            
            for file_path, data in sorted(header_files.items()):
                file_name = Path(file_path).name
                func_count = len(data["functions"])
                type_count = len(data["types"])
                const_count = len(data["constants"])
                
                lines.append(f"#### `{file_name}` ({func_count}개 함수, {type_count}개 타입)")
                lines.append("")
                
                # Functions
                if data["functions"]:
                    lines.append("**함수:**")
                    for func in data["functions"]:
                        sig = func.get("signature", func["name"])
                        lines.append(f"- `{sig}`")
                    lines.append("")
                
                # Types
                if data["types"]:
                    lines.append("**타입:**")
                    for t in data["types"]:
                        kind = t.get("kind", "type")
                        name = t["name"]
                        fields = t.get("fields", [])
                        if fields:
                            field_str = ", ".join(f["name"] for f in fields[:5])
                            if len(fields) > 5:
                                field_str += f", ... (+{len(fields) - 5})"
                            lines.append(f"- `{kind} {name}` (필드: {field_str})")
                        else:
                            lines.append(f"- `{kind} {name}`")
                    lines.append("")
                
                # Constants
                if data["constants"]:
                    lines.append("**상수:**")
                    for const in data["constants"]:
                        lines.append(f"- `{const['name']}`")
                    lines.append("")
        
        # Source files section (implementation details)
        if source_files:
            lines.append("### 소스 파일 (Implementation)")
            lines.append("")
            
            for file_path, data in sorted(source_files.items()):
                file_name = Path(file_path).name
                func_count = len(data["functions"])
                
                if func_count > 0:
                    lines.append(f"#### `{file_name}` ({func_count}개 함수)")
                    lines.append("")
                    
                    for func in data["functions"]:
                        sig = func.get("signature", func["name"])
                        lines.append(f"- `{sig}`")
                    lines.append("")
        
        # Summary statistics
        lines.append("---")
        lines.append("")
        lines.append("### 통계")
        lines.append("")
        lines.append(f"- 헤더 파일: {len(header_files)}개")
        lines.append(f"- 소스 파일: {len(source_files)}개")
        lines.append(f"- 공개 함수: {len(functions)}개")
        lines.append(f"- 공개 타입: {len(types)}개")
        lines.append(f"- 공개 상수: {len(constants)}개")
        
        return "\n".join(lines)