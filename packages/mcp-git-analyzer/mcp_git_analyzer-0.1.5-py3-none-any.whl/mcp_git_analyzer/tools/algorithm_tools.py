"""Algorithm analysis tools.

Provides tools for extracting, analyzing, and comparing core algorithms
in repository code. Supports both static analysis and LLM-based analysis.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from mcp_git_analyzer.db import Database
from mcp_git_analyzer.parsers.algorithm_extractor import AlgorithmExtractor
from mcp_git_analyzer.parsers.similarity import SimilarityAnalyzer


# Standard prompt template for LLM analysis
ALGORITHM_ANALYSIS_PROMPT = """다음 함수의 알고리즘을 분석해주세요:

```python
{source_code}
```

다음 항목을 분석해주세요:
1. **목적 (purpose)**: 이 함수가 해결하는 문제를 간결하게 설명
2. **알고리즘 카테고리 (category)**: 다음 중 하나 선택 - sorting, searching, graph, dp, math, string, tree, io, other
3. **시간 복잡도 (time_complexity)**: Big-O 표기법으로 추정하고 근거 설명
4. **공간 복잡도 (space_complexity)**: Big-O 표기법으로 추정하고 근거 설명
5. **사용 사례 (use_cases)**: 이 알고리즘이 적합한 상황 2-3가지
6. **개선점 (improvements)**: 가능한 최적화나 대안 1-2가지

JSON 형식으로 응답해주세요:
```json
{{
    "purpose": "...",
    "category": "...",
    "time_complexity": {{"notation": "O(...)", "explanation": "..."}},
    "space_complexity": {{"notation": "O(...)", "explanation": "..."}},
    "use_cases": ["...", "..."],
    "improvements": ["...", "..."]
}}
```
"""


class AlgorithmTools:
    """Algorithm extraction and analysis operations."""
    
    def __init__(self, db: Database):
        self.db = db
        self.extractor = AlgorithmExtractor()
        self.similarity = SimilarityAnalyzer(db)
    
    def extract_algorithms(
        self, 
        repo_id: int, 
        min_lines: int = 5,
        force_reextract: bool = False
    ) -> dict:
        """
        Extract and store all algorithms from a repository.
        
        Analyzes functions and methods, computing complexity metrics
        and static categories. Requires the repository to be analyzed first.
        
        Args:
            repo_id: Repository ID
            min_lines: Minimum line count for algorithm extraction (default: 5)
            force_reextract: If True, re-extract even if already exists
        
        Returns:
            Extraction summary with statistics
        """
        # Get repository info
        repo_rows = self.db.execute(
            "SELECT id, name, local_path FROM repositories WHERE id = ?",
            (repo_id,)
        )
        if not repo_rows:
            return {"status": "error", "message": f"Repository {repo_id} not found"}
        
        repo = repo_rows[0]
        repo_path = Path(repo["local_path"])
        
        if not repo_path.exists():
            return {"status": "error", "message": f"Repository path not found: {repo_path}"}
        
        # Get all analyzed files with symbols
        files = self.db.execute(
            "SELECT id, path FROM files WHERE repo_id = ?",
            (repo_id,)
        )
        
        if not files:
            return {
                "status": "error", 
                "message": "No analyzed files found. Run analyze_repo first."
            }
        
        stats = {
            "total_symbols": 0,
            "extracted": 0,
            "skipped_short": 0,
            "skipped_exists": 0,
            "errors": [],
            "categories": {}
        }
        
        for file_row in files:
            file_id = file_row["id"]
            file_path = repo_path / file_row["path"]
            
            # Read file content
            try:
                if not file_path.exists():
                    continue
                source = file_path.read_text(encoding="utf-8", errors="ignore")
            except Exception as e:
                stats["errors"].append({"file": file_row["path"], "error": str(e)})
                continue
            
            # Get symbols from this file
            symbols = self.db.execute(
                """SELECT id, name, type, start_line, end_line, parent_id, docstring
                   FROM symbols WHERE file_id = ?""",
                (file_id,)
            )
            
            for symbol in symbols:
                stats["total_symbols"] += 1
                
                # Check if should extract
                if not self.extractor.should_extract(
                    symbol["type"], 
                    symbol["start_line"], 
                    symbol["end_line"],
                    min_lines
                ):
                    stats["skipped_short"] += 1
                    continue
                
                # Check if already exists
                if not force_reextract:
                    existing = self.db.execute(
                        "SELECT id FROM core_algorithms WHERE symbol_id = ?",
                        (symbol["id"],)
                    )
                    if existing:
                        stats["skipped_exists"] += 1
                        continue
                
                # Get parent name if method
                parent_name = None
                if symbol["parent_id"]:
                    parent_rows = self.db.execute(
                        "SELECT name FROM symbols WHERE id = ?",
                        (symbol["parent_id"],)
                    )
                    if parent_rows:
                        parent_name = parent_rows[0]["name"]
                
                try:
                    # Extract algorithm info
                    algo_info = self.extractor.extract_algorithm(
                        source=source,
                        start_line=symbol["start_line"],
                        end_line=symbol["end_line"],
                        symbol_name=symbol["name"],
                        symbol_type=symbol["type"],
                        parent_name=parent_name
                    )
                    
                    # Store in database
                    self._store_algorithm(
                        symbol_id=symbol["id"],
                        file_id=file_id,
                        repo_id=repo_id,
                        algo_info=algo_info,
                        force_update=force_reextract
                    )
                    
                    stats["extracted"] += 1
                    
                    # Track categories
                    cat = algo_info.static_category
                    stats["categories"][cat] = stats["categories"].get(cat, 0) + 1
                    
                except Exception as e:
                    stats["errors"].append({
                        "symbol": symbol["name"],
                        "file": file_row["path"],
                        "error": str(e)
                    })
        
        return {
            "status": "success",
            "repository": repo["name"],
            "statistics": stats,
            "message": f"Extracted {stats['extracted']} algorithms from {len(files)} files"
        }
    
    def _store_algorithm(
        self,
        symbol_id: int,
        file_id: int,
        repo_id: int,
        algo_info: Any,
        force_update: bool = False
    ) -> int:
        """Store algorithm in database."""
        if force_update:
            # Delete existing
            self.db.execute(
                "DELETE FROM core_algorithms WHERE symbol_id = ?",
                (symbol_id,)
            )
        
        return self.db.insert(
            """INSERT INTO core_algorithms 
               (symbol_id, file_id, repo_id, source_code, normalized_code,
                ast_hash, complexity_metrics, static_category, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                symbol_id,
                file_id,
                repo_id,
                algo_info.source_code,
                algo_info.normalized_code,
                algo_info.ast_hash,
                json.dumps(algo_info.complexity_metrics.to_dict()),
                algo_info.static_category,
                datetime.now().isoformat(),
                datetime.now().isoformat(),
            )
        )
    
    def get_llm_analysis_prompt(self, algorithm_id: int) -> dict:
        """
        Get the standard LLM analysis prompt with source code for an algorithm.
        
        The client should call the LLM with this prompt and then save
        the result using save_llm_analysis().
        
        Args:
            algorithm_id: ID of the algorithm
        
        Returns:
            Dict with prompt, source_code, and metadata for LLM call
        """
        rows = self.db.execute(
            """SELECT ca.id, ca.source_code, ca.static_category, 
                      ca.complexity_metrics, s.name, s.signature, s.docstring,
                      f.path, r.name as repo_name
               FROM core_algorithms ca
               JOIN symbols s ON ca.symbol_id = s.id
               JOIN files f ON ca.file_id = f.id
               JOIN repositories r ON ca.repo_id = r.id
               WHERE ca.id = ?""",
            (algorithm_id,)
        )
        
        if not rows:
            return {"status": "error", "message": f"Algorithm {algorithm_id} not found"}
        
        algo = rows[0]
        
        # Format the prompt with source code
        prompt = ALGORITHM_ANALYSIS_PROMPT.format(source_code=algo["source_code"])
        
        return {
            "status": "success",
            "algorithm_id": algorithm_id,
            "prompt": prompt,
            "context": {
                "symbol_name": algo["name"],
                "signature": algo["signature"],
                "docstring": algo["docstring"],
                "file_path": algo["path"],
                "repo_name": algo["repo_name"],
                "static_category": algo["static_category"],
                "complexity_metrics": json.loads(algo["complexity_metrics"]) if algo["complexity_metrics"] else None,
            },
            "source_code": algo["source_code"],
            "instructions": (
                "Call your LLM with the 'prompt' field. "
                "Then use save_llm_analysis to store the JSON response."
            )
        }
    
    def save_llm_analysis(
        self, 
        algorithm_id: int, 
        analysis: dict | str
    ) -> dict:
        """
        Save LLM analysis results for an algorithm.
        
        Args:
            algorithm_id: ID of the algorithm
            analysis: LLM analysis result (dict or JSON string)
                Expected fields: purpose, category, time_complexity, 
                space_complexity, use_cases, improvements
        
        Returns:
            Success/error status
        """
        # Parse if string
        if isinstance(analysis, str):
            try:
                analysis = json.loads(analysis)
            except json.JSONDecodeError as e:
                return {"status": "error", "message": f"Invalid JSON: {e}"}
        
        # Validate required fields
        required = ["purpose", "category"]
        missing = [f for f in required if f not in analysis]
        if missing:
            return {
                "status": "error", 
                "message": f"Missing required fields: {missing}"
            }
        
        # Extract LLM category
        llm_category = analysis.get("category", "other")
        
        # Update database
        with self.db.connection() as conn:
            conn.execute(
                """UPDATE core_algorithms 
                   SET llm_analysis = ?, llm_category = ?, updated_at = ?
                   WHERE id = ?""",
                (
                    json.dumps(analysis, ensure_ascii=False),
                    llm_category,
                    datetime.now().isoformat(),
                    algorithm_id
                )
            )
            conn.commit()
        
        return {
            "status": "success",
            "algorithm_id": algorithm_id,
            "llm_category": llm_category,
            "message": "LLM analysis saved successfully"
        }
    
    def save_embedding(
        self,
        algorithm_id: int,
        embedding: list[float],
        model_name: str
    ) -> dict:
        """
        Save an embedding vector for an algorithm.
        
        The client should generate the embedding using their preferred
        embedding model and provide it here.
        
        Args:
            algorithm_id: ID of the algorithm
            embedding: List of float values (embedding vector)
            model_name: Name of the model used to generate the embedding
        
        Returns:
            Success/error status
        """
        # Validate embedding
        if not embedding or not isinstance(embedding, list):
            return {"status": "error", "message": "Invalid embedding: must be a non-empty list"}
        
        if not all(isinstance(v, (int, float)) for v in embedding):
            return {"status": "error", "message": "Invalid embedding: all values must be numbers"}
        
        # Convert to bytes
        embedding_bytes = self.similarity.floats_to_bytes(embedding)
        dimension = len(embedding)
        
        # Update database
        with self.db.connection() as conn:
            conn.execute(
                """UPDATE core_algorithms 
                   SET embedding = ?, embedding_model = ?, embedding_dimension = ?, updated_at = ?
                   WHERE id = ?""",
                (
                    embedding_bytes,
                    model_name,
                    dimension,
                    datetime.now().isoformat(),
                    algorithm_id
                )
            )
            conn.commit()
        
        return {
            "status": "success",
            "algorithm_id": algorithm_id,
            "embedding_dimension": dimension,
            "embedding_model": model_name,
            "message": "Embedding saved successfully"
        }
    
    def find_similar(
        self,
        algorithm_id: int,
        method: str = "both",
        threshold: float = 0.8,
        limit: int = 20
    ) -> dict:
        """
        Find algorithms similar to the specified algorithm.
        
        Args:
            algorithm_id: ID of the algorithm to compare against
            method: Comparison method - 'hash', 'embedding', or 'both'
            threshold: Similarity threshold for embedding search (0.0-1.0)
            limit: Maximum number of results
        
        Returns:
            Dict with similar algorithms found
        """
        if method not in ("hash", "embedding", "both"):
            return {"status": "error", "message": f"Invalid method: {method}"}
        
        return self.similarity.find_similar(
            algorithm_id=algorithm_id,
            method=method,
            threshold=threshold,
            limit=limit
        )
    
    def get_algorithm(self, algorithm_id: int) -> dict:
        """
        Get detailed information about an algorithm.
        
        Args:
            algorithm_id: ID of the algorithm
        
        Returns:
            Complete algorithm details including source, metrics, and analyses
        """
        rows = self.db.execute(
            """SELECT ca.*, s.name, s.signature, s.type as symbol_type,
                      s.docstring, s.start_line, s.end_line,
                      f.path as file_path, r.name as repo_name, r.url as repo_url
               FROM core_algorithms ca
               JOIN symbols s ON ca.symbol_id = s.id
               JOIN files f ON ca.file_id = f.id
               JOIN repositories r ON ca.repo_id = r.id
               WHERE ca.id = ?""",
            (algorithm_id,)
        )
        
        if not rows:
            return {"status": "error", "message": f"Algorithm {algorithm_id} not found"}
        
        row = rows[0]
        
        return {
            "status": "success",
            "algorithm": {
                "id": row["id"],
                "symbol_name": row["name"],
                "symbol_type": row["symbol_type"],
                "signature": row["signature"],
                "docstring": row["docstring"],
                "file_path": row["file_path"],
                "repo_name": row["repo_name"],
                "repo_url": row["repo_url"],
                "start_line": row["start_line"],
                "end_line": row["end_line"],
                "source_code": row["source_code"],
                "normalized_code": row["normalized_code"],
                "ast_hash": row["ast_hash"],
                "complexity_metrics": json.loads(row["complexity_metrics"]) if row["complexity_metrics"] else None,
                "static_category": row["static_category"],
                "llm_category": row["llm_category"],
                "llm_analysis": json.loads(row["llm_analysis"]) if row["llm_analysis"] else None,
                "has_embedding": row["embedding"] is not None,
                "embedding_model": row["embedding_model"],
                "embedding_dimension": row["embedding_dimension"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
        }
    
    def list_algorithms(
        self,
        repo_id: int,
        category: str | None = None,
        category_type: str = "static",
        min_complexity: int | None = None,
        limit: int = 100
    ) -> dict:
        """
        List algorithms in a repository with optional filters.
        
        Args:
            repo_id: Repository ID
            category: Filter by category (sorting, searching, graph, dp, math, etc.)
            category_type: Which category to filter by - 'static', 'llm', or 'any'
            min_complexity: Minimum cyclomatic complexity
            limit: Maximum results
        
        Returns:
            List of algorithms with basic info
        
        Response Integration:
            MUST include in your response:
            - algorithms[].symbol_name → List each algorithm name
            - algorithms[].signature → Show function signatures
            - category_summary → Show category distribution
            
            Example format:
            "### 알고리즘 분석 결과
            - math: 15개
            - sorting: 3개
            - other: 8개
            
            주요 알고리즘:
            - `fast_log2(float x)` - math 카테고리
            - `quick_sort(int* arr, int n)` - sorting 카테고리"
            
            Use exact counts from category_summary, never estimate.
        """
        query = """
            SELECT ca.id, ca.static_category, ca.llm_category,
                   ca.complexity_metrics, ca.ast_hash,
                   s.name, s.signature, s.type as symbol_type,
                   f.path as file_path
            FROM core_algorithms ca
            JOIN symbols s ON ca.symbol_id = s.id
            JOIN files f ON ca.file_id = f.id
            WHERE ca.repo_id = ?
        """
        params: list[Any] = [repo_id]
        
        if category:
            if category_type == "static":
                query += " AND ca.static_category = ?"
            elif category_type == "llm":
                query += " AND ca.llm_category = ?"
            else:  # 'any'
                query += " AND (ca.static_category = ? OR ca.llm_category = ?)"
                params.append(category)
            params.append(category)
        
        query += " ORDER BY s.name LIMIT ?"
        params.append(limit)
        
        rows = self.db.execute(query, tuple(params))
        
        algorithms = []
        for row in rows:
            metrics = json.loads(row["complexity_metrics"]) if row["complexity_metrics"] else {}
            
            # Filter by complexity if specified
            if min_complexity and metrics.get("cyclomatic", 0) < min_complexity:
                continue
            
            algorithms.append({
                "id": row["id"],
                "symbol_name": row["name"],
                "symbol_type": row["symbol_type"],
                "signature": row["signature"],
                "file_path": row["file_path"],
                "static_category": row["static_category"],
                "llm_category": row["llm_category"],
                "complexity": metrics.get("cyclomatic", 0),
                "lines": metrics.get("lines", 0),
            })
        
        # Get category summary
        category_counts = self.db.execute(
            """SELECT static_category, COUNT(*) as count
               FROM core_algorithms WHERE repo_id = ?
               GROUP BY static_category""",
            (repo_id,)
        )
        
        category_summary = {row["static_category"]: row["count"] for row in category_counts}
        
        # Generate summary text
        total = len(algorithms)
        category_parts = [f"{cat}: {cnt}개" for cat, cnt in sorted(category_summary.items(), key=lambda x: -x[1])]
        summary_text = f"총 {total}개 알고리즘 발견. 카테고리별: {', '.join(category_parts)}" if category_parts else f"총 {total}개 알고리즘 발견"
        
        return {
            "status": "success",
            "repo_id": repo_id,
            "total": total,
            "algorithms": algorithms,
            "category_summary": category_summary,
            "summary_text": summary_text
        }
    
    def search_algorithms(
        self,
        query: str,
        repo_id: int | None = None,
        limit: int = 20
    ) -> dict:
        """
        Search algorithms using full-text search.
        
        Searches in source code and LLM analysis.
        
        Args:
            query: Search query (supports FTS5 operators)
            repo_id: Optional repository filter
            limit: Maximum results
        
        Returns:
            List of matching algorithms with snippets
        """
        # Use FTS5 search
        fts_query = """
            SELECT ca.id, ca.static_category, ca.llm_category,
                   s.name, f.path as file_path, r.name as repo_name,
                   snippet(algorithms_fts, 0, '<mark>', '</mark>', '...', 32) as snippet
            FROM algorithms_fts
            JOIN core_algorithms ca ON algorithms_fts.rowid = ca.id
            JOIN symbols s ON ca.symbol_id = s.id
            JOIN files f ON ca.file_id = f.id
            JOIN repositories r ON ca.repo_id = r.id
            WHERE algorithms_fts MATCH ?
        """
        params: list[Any] = [query]
        
        if repo_id is not None:
            fts_query += " AND ca.repo_id = ?"
            params.append(repo_id)
        
        fts_query += " LIMIT ?"
        params.append(limit)
        
        try:
            rows = self.db.execute(fts_query, tuple(params))
        except Exception:
            # Fallback to LIKE search if FTS fails
            like_query = """
                SELECT ca.id, ca.static_category, ca.llm_category,
                       s.name, f.path as file_path, r.name as repo_name,
                       NULL as snippet
                FROM core_algorithms ca
                JOIN symbols s ON ca.symbol_id = s.id
                JOIN files f ON ca.file_id = f.id
                JOIN repositories r ON ca.repo_id = r.id
                WHERE ca.source_code LIKE ? OR ca.llm_analysis LIKE ?
            """
            like_pattern = f"%{query}%"
            params = [like_pattern, like_pattern]
            
            if repo_id is not None:
                like_query += " AND ca.repo_id = ?"
                params.append(repo_id)
            
            like_query += " LIMIT ?"
            params.append(limit)
            
            rows = self.db.execute(like_query, tuple(params))
        
        return {
            "status": "success",
            "query": query,
            "total": len(rows),
            "results": [
                {
                    "id": row["id"],
                    "symbol_name": row["name"],
                    "file_path": row["file_path"],
                    "repo_name": row["repo_name"],
                    "static_category": row["static_category"],
                    "llm_category": row["llm_category"],
                    "snippet": row["snippet"],
                }
                for row in rows
            ]
        }
    
    def build_similarity_index(
        self,
        repo_id: int | None = None,
        index_type: str = "flat"
    ) -> dict:
        """
        Build ANN index for fast embedding similarity search.
        
        This significantly improves performance for large datasets (>1000 embeddings).
        The index is kept in memory and should be rebuilt after adding new embeddings.
        
        Args:
            repo_id: Optional repository ID to limit index (None for all repos)
            index_type: Type of FAISS index:
                - 'flat': Exact search, slower but most accurate (default)
                - 'ivf': Inverted file index, faster approximate search
                - 'hnsw': Hierarchical NSW graph, best quality/speed tradeoff
        
        Returns:
            Build status and index statistics
        """
        valid_types = ["flat", "ivf", "hnsw"]
        if index_type not in valid_types:
            return {
                "status": "error",
                "message": f"Invalid index_type: {index_type}. Must be one of {valid_types}"
            }
        
        return self.similarity.build_ann_index(repo_id=repo_id, index_type=index_type)
    
    def reduce_embedding_dimensions(
        self,
        repo_id: int | None,
        target_dimension: int,
        method: str = "pca"
    ) -> dict:
        """
        Reduce embedding dimensions for storage/performance optimization.
        
        Uses PCA to reduce dimensionality while preserving maximum variance.
        This can significantly reduce storage size and improve search speed.
        
        Warning: This modifies embeddings in the database. Consider backing up first.
        
        Args:
            repo_id: Optional repository ID to limit reduction (None for all repos)
            target_dimension: Target dimension (must be < current dimension)
            method: Reduction method (currently only 'pca' supported)
        
        Returns:
            Reduction statistics including variance retained
        """
        if method != "pca":
            return {
                "status": "error",
                "message": f"Invalid method: {method}. Currently only 'pca' is supported."
            }
        
        return self.similarity.batch_reduce_embeddings(
            repo_id=repo_id,
            target_dim=target_dimension,
            method=method
        )
