"""
Local vector search using FAISS (Facebook AI Similarity Search).

Zero-cost alternative to Pinecone ($70-200/month → $0).
Index stored in .memdocs/memory/ (git-committed, version-controlled).

Provides fast L2 distance similarity search for semantic code queries.
Works offline with no external dependencies or API latency.
"""

import json
from pathlib import Path
from typing import Any, cast


class LocalVectorSearch:
    """Local vector similarity search using FAISS.

    Benefits over Pinecone:
    - $0 cost (vs $70-200/month)
    - 100% local (works offline)
    - Git-committed index (version controlled)
    - No API latency
    """

    def __init__(
        self,
        index_path: Path = Path(".memdocs/memory/faiss.index"),
        metadata_path: Path = Path(".memdocs/memory/faiss_metadata.json"),
        dimension: int = 384,
    ):
        """Initialize local vector search.

        Args:
            index_path: Path to FAISS index file (git-committed)
            metadata_path: Path to metadata JSON (git-committed)
            dimension: Embedding dimension (384 for all-MiniLM-L6-v2)
        """
        try:
            import faiss
        except ImportError:
            raise ImportError(
                "faiss not installed. " "Install with: pip install 'memdocs[embeddings]'"
            )

        self.faiss = faiss
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.dimension = dimension

        # Ensure directories exist
        index_path.parent.mkdir(parents=True, exist_ok=True)

        # Load or create index
        if index_path.exists():
            self.index = faiss.read_index(str(index_path))
        else:
            # Create new index (flat L2 distance for accuracy)
            self.index = faiss.IndexFlatL2(dimension)

        # Load or create metadata
        self.metadata = self._load_metadata()

    def add_embeddings(
        self,
        embeddings: list[list[float]],
        documents: list[dict[str, Any]],
    ) -> list[int]:
        """Add embeddings and associated documents to index.

        Args:
            embeddings: List of embedding vectors
            documents: List of document metadata (same length as embeddings)

        Returns:
            List of assigned indices
        """
        if len(embeddings) != len(documents):
            raise ValueError("Embeddings and documents must have same length")

        if not embeddings:
            return []

        # Import numpy (only needed for embeddings feature)
        try:
            import numpy as np
        except ImportError:
            raise ImportError(
                "numpy not installed. " "Install with: pip install 'memdocs[embeddings]'"
            ) from None

        # Convert to numpy array
        vectors = np.array(embeddings).astype("float32")

        # Add to index
        start_idx = self.index.ntotal
        self.index.add(vectors)

        # Store metadata
        indices = list(range(start_idx, start_idx + len(embeddings)))
        for idx, doc in zip(indices, documents, strict=False):
            self.metadata[str(idx)] = doc

        # Save to disk (git-committable)
        self.save()

        return indices

    def search(
        self,
        query_embedding: list[float],
        k: int = 5,
        min_score: float = 0.0,
    ) -> list[dict[str, Any]]:
        """Search for similar vectors.

        Args:
            query_embedding: Query embedding vector
            k: Number of results to return
            min_score: Minimum similarity score (0-1, optional filter)

        Returns:
            List of results with scores and metadata
        """
        if self.index.ntotal == 0:
            return []

        # Import numpy (only needed for embeddings feature)
        try:
            import numpy as np
        except ImportError:
            raise ImportError(
                "numpy not installed. " "Install with: pip install 'memdocs[embeddings]'"
            ) from None

        # Convert to numpy array
        query = np.array([query_embedding]).astype("float32")

        # Search (returns distances and indices)
        distances, indices = self.index.search(query, min(k, self.index.ntotal))

        # Convert distances to similarity scores (0-1 scale)
        # L2 distance → similarity: smaller distance = higher similarity
        # Use exponential decay: similarity = exp(-distance)
        similarities = np.exp(-distances[0])

        # Build results
        results = []
        for idx, similarity in zip(indices[0], similarities, strict=False):
            if idx == -1:  # FAISS returns -1 for empty slots
                continue

            if similarity < min_score:
                continue

            result = {
                "index": int(idx),
                "score": float(similarity),
                "metadata": self.metadata.get(str(idx), {}),
            }
            results.append(result)

        return results

    def remove_by_indices(self, indices: list[int]) -> None:
        """Remove vectors by indices (for incremental updates).

        Note: FAISS doesn't support true deletion, so we:
        1. Mark metadata as deleted
        2. Rebuild index periodically (via cleanup command)

        Args:
            indices: List of indices to remove
        """
        for idx in indices:
            if str(idx) in self.metadata:
                self.metadata[str(idx)]["deleted"] = True

        self.save()

    def rebuild_index(self) -> int:
        """Rebuild index excluding deleted entries.

        Returns:
            Number of entries removed
        """
        # Collect non-deleted entries
        active_entries = []
        for idx_str, meta in self.metadata.items():
            if not meta.get("deleted", False):
                active_entries.append((int(idx_str), meta))

        if not active_entries:
            # Empty index
            self.index = self.faiss.IndexFlatL2(self.dimension)
            self.metadata = {}
            self.save()
            return 0

        # Get embeddings for active entries (need to load from source)
        # This is called during cleanup, so embeddings should be available
        # For now, just clear metadata of deleted entries
        removed_count = 0
        new_metadata = {}
        for idx_str, meta in self.metadata.items():
            if not meta.get("deleted", False):
                new_metadata[idx_str] = meta
            else:
                removed_count += 1

        self.metadata = new_metadata
        self.save()

        return removed_count

    def save(self) -> None:
        """Save index and metadata to disk (git-committable)."""
        # Save FAISS index
        self.faiss.write_index(self.index, str(self.index_path))

        # Save metadata
        with open(self.metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2)

    def _load_metadata(self) -> dict[str, Any]:
        """Load metadata from disk."""
        if not self.metadata_path.exists():
            return {}

        with open(self.metadata_path, encoding="utf-8") as f:
            return cast(dict[str, Any], json.load(f))

    def get_stats(self) -> dict[str, Any]:
        """Get index statistics.

        Returns:
            Dictionary with stats (total, active, deleted)
        """
        total = self.index.ntotal
        deleted = sum(1 for meta in self.metadata.values() if meta.get("deleted", False))
        active = total - deleted

        return {
            "total": total,
            "active": active,
            "deleted": deleted,
            "dimension": self.dimension,
        }


def search_memory(
    query: str,
    embedder: Any,
    search: LocalVectorSearch,
    k: int = 5,
) -> list[dict[str, Any]]:
    """Search memory using natural language query.

    Args:
        query: Natural language query
        embedder: LocalEmbedder instance
        search: LocalVectorSearch instance
        k: Number of results

    Returns:
        List of matching documents with scores
    """
    # Generate query embedding
    query_embedding = embedder.embed_query(query)

    # Search
    results = search.search(query_embedding, k=k)

    return results
