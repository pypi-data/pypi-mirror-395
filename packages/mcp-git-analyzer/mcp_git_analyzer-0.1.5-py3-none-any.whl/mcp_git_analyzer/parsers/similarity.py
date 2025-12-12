"""Similarity analysis module for algorithm comparison.

Provides hash-based duplicate detection and embedding-based similarity search.
Supports approximate nearest neighbor (ANN) search for efficient similarity at scale.
"""

import struct
import warnings
from dataclasses import dataclass
from typing import Any, Literal

from mcp_git_analyzer.db import Database

# Optional dependencies for ANN and dimensionality reduction
try:
    import faiss
    import numpy as np
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    faiss = None
    np = None

try:
    from sklearn.decomposition import PCA
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    PCA = None


@dataclass
class SimilarAlgorithm:
    """Represents a similar algorithm found in the database."""
    algorithm_id: int
    symbol_name: str
    file_path: str
    repo_name: str
    similarity_score: float
    match_method: str  # 'hash' or 'embedding'
    
    def to_dict(self) -> dict:
        return {
            "algorithm_id": self.algorithm_id,
            "symbol_name": self.symbol_name,
            "file_path": self.file_path,
            "repo_name": self.repo_name,
            "similarity_score": self.similarity_score,
            "match_method": self.match_method,
        }


class SimilarityAnalyzer:
    """Analyze similarity between algorithms using hash and embedding methods.
    
    Supports both brute-force cosine similarity and approximate nearest neighbor (ANN)
    search using FAISS for efficient similarity search at scale.
    """
    
    def __init__(self, db: Database, use_ann: bool = True, ann_method: Literal["faiss", "brute"] = "faiss"):
        """
        Initialize similarity analyzer.
        
        Args:
            db: Database instance
            use_ann: Whether to use ANN index (default: True if FAISS available)
            ann_method: ANN method to use - 'faiss' or 'brute' (default: 'faiss')
        """
        self.db = db
        self.use_ann = use_ann and FAISS_AVAILABLE and ann_method == "faiss"
        self.ann_method = ann_method
        self._index = None
        self._index_ids = None
        self._index_dimension = None
        
        if use_ann and not FAISS_AVAILABLE and ann_method == "faiss":
            warnings.warn(
                "FAISS not available. Install with: pip install faiss-cpu numpy\n"
                "Falling back to brute-force search.",
                RuntimeWarning
            )
    
    def find_duplicates_by_hash(
        self, 
        ast_hash: str, 
        repo_id: int | None = None,
        exclude_algorithm_id: int | None = None
    ) -> list[SimilarAlgorithm]:
        """
        Find algorithms with identical AST structure hash.
        
        Args:
            ast_hash: AST hash to search for
            repo_id: Optional repository ID to limit search
            exclude_algorithm_id: Optional algorithm ID to exclude from results
        
        Returns:
            List of SimilarAlgorithm with exact hash matches
        """
        query = """
            SELECT 
                ca.id as algorithm_id,
                s.name as symbol_name,
                f.path as file_path,
                r.name as repo_name
            FROM core_algorithms ca
            JOIN symbols s ON ca.symbol_id = s.id
            JOIN files f ON ca.file_id = f.id
            JOIN repositories r ON ca.repo_id = r.id
            WHERE ca.ast_hash = ?
        """
        params: list[Any] = [ast_hash]
        
        if repo_id is not None:
            query += " AND ca.repo_id = ?"
            params.append(repo_id)
        
        if exclude_algorithm_id is not None:
            query += " AND ca.id != ?"
            params.append(exclude_algorithm_id)
        
        rows = self.db.execute(query, tuple(params))
        
        return [
            SimilarAlgorithm(
                algorithm_id=row["algorithm_id"],
                symbol_name=row["symbol_name"],
                file_path=row["file_path"],
                repo_name=row["repo_name"],
                similarity_score=1.0,  # Exact hash match
                match_method="hash"
            )
            for row in rows
        ]
    
    def compute_cosine_similarity(
        self, 
        embedding1: bytes, 
        embedding2: bytes
    ) -> float:
        """
        Compute cosine similarity between two embedding vectors.
        
        Args:
            embedding1: First embedding as bytes (float32 array)
            embedding2: Second embedding as bytes (float32 array)
        
        Returns:
            Cosine similarity score (0.0 to 1.0)
        """
        # Decode embeddings from bytes to float list
        vec1 = self._bytes_to_floats(embedding1)
        vec2 = self._bytes_to_floats(embedding2)
        
        if len(vec1) != len(vec2):
            raise ValueError(f"Embedding dimensions don't match: {len(vec1)} vs {len(vec2)}")
        
        # Compute dot product and magnitudes
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def build_ann_index(
        self,
        repo_id: int | None = None,
        index_type: Literal["flat", "ivf", "hnsw"] = "flat",
        nlist: int = 100
    ) -> dict:
        """
        Build FAISS index for approximate nearest neighbor search.
        
        Args:
            repo_id: Optional repository ID to limit index
            index_type: Type of FAISS index:
                - 'flat': Exact search (L2), slower but accurate
                - 'ivf': Inverted file index, faster approximate search
                - 'hnsw': Hierarchical NSW graph, best quality/speed tradeoff
            nlist: Number of clusters for IVF index (default: 100)
        
        Returns:
            Dict with build status and statistics
        """
        if not FAISS_AVAILABLE:
            return {
                "status": "error",
                "message": "FAISS not available. Install with: pip install faiss-cpu numpy"
            }
        
        # Get all algorithms with embeddings
        query = """
            SELECT ca.id, ca.embedding
            FROM core_algorithms ca
            WHERE ca.embedding IS NOT NULL
        """
        params = []
        if repo_id is not None:
            query += " AND ca.repo_id = ?"
            params.append(repo_id)
        
        rows = self.db.execute(query, tuple(params))
        
        if not rows:
            return {"status": "error", "message": "No embeddings found in database"}
        
        # Convert embeddings to numpy array
        embeddings_list = []
        ids_list = []
        
        for row in rows:
            try:
                embedding_floats = self._bytes_to_floats(row["embedding"])
                embeddings_list.append(embedding_floats)
                ids_list.append(row["id"])
            except Exception:
                continue
        
        if not embeddings_list:
            return {"status": "error", "message": "Failed to decode embeddings"}
        
        embeddings = np.array(embeddings_list, dtype='float32')
        dimension = embeddings.shape[1]
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Build index based on type
        if index_type == "flat":
            # Exact search using L2 (after normalization, equivalent to cosine)
            index = faiss.IndexFlatIP(dimension)
        elif index_type == "ivf":
            # IVF index for faster approximate search
            quantizer = faiss.IndexFlatIP(dimension)
            index = faiss.IndexIVFFlat(quantizer, dimension, min(nlist, len(embeddings)))
            index.train(embeddings)
            index.nprobe = min(10, nlist)  # Number of clusters to search
        elif index_type == "hnsw":
            # HNSW index for best quality/speed tradeoff
            index = faiss.IndexHNSWFlat(dimension, 32)
            index.hnsw.efConstruction = 40
            index.hnsw.efSearch = 16
        else:
            return {"status": "error", "message": f"Unknown index type: {index_type}"}
        
        # Add vectors to index
        index.add(embeddings)
        
        # Store index and metadata
        self._index = index
        self._index_ids = ids_list
        self._index_dimension = dimension
        
        return {
            "status": "success",
            "index_type": index_type,
            "dimension": dimension,
            "num_vectors": len(ids_list),
            "repo_id": repo_id
        }
    
    def _search_with_ann(
        self,
        embedding: bytes,
        limit: int = 20,
        threshold: float = 0.8
    ) -> list[tuple[int, float]]:
        """
        Search using FAISS ANN index.
        
        Args:
            embedding: Query embedding
            limit: Maximum results
            threshold: Minimum similarity threshold
        
        Returns:
            List of (algorithm_id, similarity_score) tuples
        """
        if self._index is None:
            raise RuntimeError("ANN index not built. Call build_ann_index() first.")
        
        # Convert embedding to numpy array
        vec = self._bytes_to_floats(embedding)
        if len(vec) != self._index_dimension:
            raise ValueError(
                f"Embedding dimension mismatch: {len(vec)} vs {self._index_dimension}"
            )
        
        query_vec = np.array([vec], dtype='float32')
        faiss.normalize_L2(query_vec)
        
        # Search index (k is limited by number of vectors in index)
        k = min(limit * 2, self._index.ntotal)  # Get more candidates to filter by threshold
        distances, indices = self._index.search(query_vec, k)
        
        # Convert inner product to cosine similarity (already normalized)
        # Filter by threshold and map to algorithm IDs
        results = []
        for idx, similarity in zip(indices[0], distances[0]):
            if idx >= 0 and similarity >= threshold:  # idx can be -1 if k > ntotal
                algorithm_id = self._index_ids[idx]
                results.append((algorithm_id, float(similarity)))
        
        return results[:limit]
    
    def find_similar_by_embedding(
        self,
        embedding: bytes,
        repo_id: int | None = None,
        threshold: float = 0.8,
        limit: int = 20,
        exclude_algorithm_id: int | None = None,
        use_ann: bool | None = None
    ) -> list[SimilarAlgorithm]:
        """
        Find algorithms with similar embeddings using cosine similarity.
        
        Uses FAISS ANN index if available and built, otherwise falls back to
        brute-force comparison. For large datasets (>1000 embeddings), ANN
        provides significant speedup (O(log n) vs O(n)).
        
        Args:
            embedding: Query embedding as bytes (float32 array)
            repo_id: Optional repository ID to limit search
            threshold: Minimum similarity threshold (0.0 to 1.0)
            limit: Maximum number of results
            exclude_algorithm_id: Optional algorithm ID to exclude
            use_ann: Force ANN (True) or brute-force (False), None for auto
        
        Returns:
            List of SimilarAlgorithm sorted by similarity (descending)
        """
        # Determine search method
        should_use_ann = use_ann if use_ann is not None else self.use_ann
        
        # Try ANN search if index is built and method is enabled
        if should_use_ann and self._index is not None:
            try:
                return self._find_similar_ann(
                    embedding, repo_id, threshold, limit, exclude_algorithm_id
                )
            except Exception as e:
                warnings.warn(f"ANN search failed, falling back to brute-force: {e}")
        
        # Fall back to brute-force search
        return self._find_similar_brute_force(
            embedding, repo_id, threshold, limit, exclude_algorithm_id
        )
    
    def _find_similar_ann(
        self,
        embedding: bytes,
        repo_id: int | None,
        threshold: float,
        limit: int,
        exclude_algorithm_id: int | None
    ) -> list[SimilarAlgorithm]:
        """Find similar algorithms using ANN index."""
        # Get candidates from ANN search
        candidates = self._search_with_ann(embedding, limit * 2, threshold)
        
        # Get full algorithm info from database
        if not candidates:
            return []
        
        algorithm_ids = [alg_id for alg_id, _ in candidates]
        similarity_map = {alg_id: score for alg_id, score in candidates}
        
        placeholders = ','.join('?' * len(algorithm_ids))
        query = f"""
            SELECT 
                ca.id as algorithm_id,
                s.name as symbol_name,
                f.path as file_path,
                r.name as repo_name,
                ca.repo_id
            FROM core_algorithms ca
            JOIN symbols s ON ca.symbol_id = s.id
            JOIN files f ON ca.file_id = f.id
            JOIN repositories r ON ca.repo_id = r.id
            WHERE ca.id IN ({placeholders})
        """
        
        rows = self.db.execute(query, tuple(algorithm_ids))
        
        # Build results with filtering
        results: list[SimilarAlgorithm] = []
        for row in rows:
            # Apply filters
            if exclude_algorithm_id and row["algorithm_id"] == exclude_algorithm_id:
                continue
            if repo_id is not None and row["repo_id"] != repo_id:
                continue
            
            similarity = similarity_map[row["algorithm_id"]]
            results.append(SimilarAlgorithm(
                algorithm_id=row["algorithm_id"],
                symbol_name=row["symbol_name"],
                file_path=row["file_path"],
                repo_name=row["repo_name"],
                similarity_score=round(similarity, 4),
                match_method="embedding_ann"
            ))
        
        # Sort by similarity and limit
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:limit]
    
    def _find_similar_brute_force(
        self,
        embedding: bytes,
        repo_id: int | None,
        threshold: float,
        limit: int,
        exclude_algorithm_id: int | None
    ) -> list[SimilarAlgorithm]:
        """Find similar algorithms using brute-force comparison."""
        # Get all algorithms with embeddings
        query = """
            SELECT 
                ca.id as algorithm_id,
                ca.embedding,
                s.name as symbol_name,
                f.path as file_path,
                r.name as repo_name
            FROM core_algorithms ca
            JOIN symbols s ON ca.symbol_id = s.id
            JOIN files f ON ca.file_id = f.id
            JOIN repositories r ON ca.repo_id = r.id
            WHERE ca.embedding IS NOT NULL
        """
        params: list[Any] = []
        
        if repo_id is not None:
            query += " AND ca.repo_id = ?"
            params.append(repo_id)
        
        if exclude_algorithm_id is not None:
            query += " AND ca.id != ?"
            params.append(exclude_algorithm_id)
        
        rows = self.db.execute(query, tuple(params))
        
        # Compute similarities
        results: list[SimilarAlgorithm] = []
        for row in rows:
            try:
                similarity = self.compute_cosine_similarity(embedding, row["embedding"])
                if similarity >= threshold:
                    results.append(SimilarAlgorithm(
                        algorithm_id=row["algorithm_id"],
                        symbol_name=row["symbol_name"],
                        file_path=row["file_path"],
                        repo_name=row["repo_name"],
                        similarity_score=round(similarity, 4),
                        match_method="embedding"
                    ))
            except ValueError:
                # Skip if embedding dimensions don't match
                continue
        
        # Sort by similarity and limit
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:limit]
    
    def reduce_embedding_dimension(
        self,
        embedding: bytes,
        target_dim: int,
        method: Literal["pca", "truncate"] = "pca"
    ) -> bytes:
        """
        Reduce embedding dimensionality for storage/performance optimization.
        
        Args:
            embedding: Original embedding bytes
            target_dim: Target dimension (must be < original dimension)
            method: Reduction method:
                - 'pca': Principal Component Analysis (requires sklearn)
                - 'truncate': Simple truncation (fast but loses information)
        
        Returns:
            Reduced embedding as bytes
        """
        vec = self._bytes_to_floats(embedding)
        
        if target_dim >= len(vec):
            raise ValueError(f"Target dimension {target_dim} must be less than current {len(vec)}")
        
        if method == "truncate":
            # Simple truncation
            reduced = vec[:target_dim]
        elif method == "pca":
            if not SKLEARN_AVAILABLE:
                raise ImportError(
                    "sklearn not available for PCA. Install with: pip install scikit-learn\n"
                    "Or use method='truncate' for simple truncation."
                )
            # Use PCA (requires fitting on multiple samples in practice)
            # For single vector, this is equivalent to truncation
            # In production, you'd fit PCA on all embeddings first
            reduced = vec[:target_dim]
            warnings.warn(
                "PCA on single vector is equivalent to truncation. "
                "For proper PCA, fit on all embeddings first.",
                RuntimeWarning
            )
        else:
            raise ValueError(f"Unknown reduction method: {method}")
        
        return self.floats_to_bytes(reduced)
    
    def batch_reduce_embeddings(
        self,
        repo_id: int | None,
        target_dim: int,
        method: Literal["pca"] = "pca"
    ) -> dict:
        """
        Reduce dimensionality of all embeddings in the database.
        
        Args:
            repo_id: Optional repository ID to limit reduction
            target_dim: Target dimension
            method: Reduction method (currently only 'pca' supported)
        
        Returns:
            Dict with reduction statistics
        """
        if not SKLEARN_AVAILABLE:
            return {
                "status": "error",
                "message": "sklearn not available. Install with: pip install scikit-learn"
            }
        
        # Get all embeddings
        query = """
            SELECT ca.id, ca.embedding
            FROM core_algorithms ca
            WHERE ca.embedding IS NOT NULL
        """
        params = []
        if repo_id is not None:
            query += " AND ca.repo_id = ?"
            params.append(repo_id)
        
        rows = self.db.execute(query, tuple(params))
        
        if not rows:
            return {"status": "error", "message": "No embeddings found"}
        
        # Convert to numpy array
        embeddings_list = []
        ids_list = []
        
        for row in rows:
            try:
                vec = self._bytes_to_floats(row["embedding"])
                embeddings_list.append(vec)
                ids_list.append(row["id"])
            except Exception:
                continue
        
        if not embeddings_list:
            return {"status": "error", "message": "Failed to decode embeddings"}
        
        embeddings = np.array(embeddings_list, dtype='float32')
        original_dim = embeddings.shape[1]
        
        if target_dim >= original_dim:
            return {
                "status": "error",
                "message": f"Target dimension {target_dim} must be less than current {original_dim}"
            }
        
        # Apply PCA
        pca = PCA(n_components=target_dim)
        reduced_embeddings = pca.fit_transform(embeddings)
        
        # Update database
        update_params = [
            (self.floats_to_bytes(reduced_vec.tolist()), alg_id)
            for alg_id, reduced_vec in zip(ids_list, reduced_embeddings)
        ]
        self.db.execute_many(
            "UPDATE core_algorithms SET embedding = ? WHERE id = ?",
            update_params
        )
        update_count = len(update_params)
        
        # Rebuild index if it was built
        if self._index is not None:
            self.build_ann_index(repo_id)
        
        return {
            "status": "success",
            "original_dimension": original_dim,
            "target_dimension": target_dim,
            "explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
            "total_variance_retained": float(pca.explained_variance_ratio_.sum()),
            "num_updated": update_count
        }
    
    def find_similar(
        self,
        algorithm_id: int,
        method: str = "both",
        threshold: float = 0.8,
        limit: int = 20
    ) -> dict:
        """
        Find algorithms similar to the given algorithm.
        
        Args:
            algorithm_id: ID of the algorithm to compare against
            method: 'hash', 'embedding', or 'both'
            threshold: Similarity threshold for embedding search
            limit: Maximum results per method
        
        Returns:
            Dict with hash_matches, embedding_matches, and combined results
        """
        # Get the algorithm's hash and embedding
        query = """
            SELECT ast_hash, embedding, repo_id
            FROM core_algorithms
            WHERE id = ?
        """
        rows = self.db.execute(query, (algorithm_id,))
        
        if not rows:
            return {"status": "error", "message": f"Algorithm {algorithm_id} not found"}
        
        algo = rows[0]
        ast_hash = algo["ast_hash"]
        embedding = algo["embedding"]
        algo["repo_id"]
        
        result: dict[str, Any] = {
            "status": "success",
            "algorithm_id": algorithm_id,
            "method": method,
            "hash_matches": [],
            "embedding_matches": [],
        }
        
        # Find hash duplicates
        if method in ("hash", "both") and ast_hash:
            hash_matches = self.find_duplicates_by_hash(
                ast_hash, 
                exclude_algorithm_id=algorithm_id
            )
            result["hash_matches"] = [m.to_dict() for m in hash_matches]
        
        # Find embedding similarities
        if method in ("embedding", "both") and embedding:
            embedding_matches = self.find_similar_by_embedding(
                embedding,
                threshold=threshold,
                limit=limit,
                exclude_algorithm_id=algorithm_id
            )
            result["embedding_matches"] = [m.to_dict() for m in embedding_matches]
        elif method in ("embedding", "both") and not embedding:
            result["embedding_warning"] = "No embedding stored for this algorithm"
        
        # Combine and deduplicate
        seen_ids = set()
        combined = []
        
        # Hash matches first (exact matches)
        for match in result["hash_matches"]:
            if match["algorithm_id"] not in seen_ids:
                seen_ids.add(match["algorithm_id"])
                combined.append(match)
        
        # Then embedding matches
        for match in result["embedding_matches"]:
            if match["algorithm_id"] not in seen_ids:
                seen_ids.add(match["algorithm_id"])
                combined.append(match)
        
        result["combined"] = combined
        result["total_matches"] = len(combined)
        
        return result
    
    @staticmethod
    def floats_to_bytes(floats: list[float]) -> bytes:
        """
        Convert a list of floats to bytes for storage.
        
        Args:
            floats: List of float values (embedding vector)
        
        Returns:
            Bytes representation (float32 format)
        """
        return struct.pack(f"{len(floats)}f", *floats)
    
    @staticmethod
    def _bytes_to_floats(data: bytes) -> list[float]:
        """
        Convert bytes to a list of floats.
        
        Args:
            data: Bytes in float32 format
        
        Returns:
            List of float values
        """
        count = len(data) // 4  # float32 is 4 bytes
        return list(struct.unpack(f"{count}f", data))
