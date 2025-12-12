"""
Indexing module for creating searchable memory from documentation.

Combines embeddings + vector search for semantic retrieval.
"""

from pathlib import Path
from typing import Any

from memdocs.embeddings import LocalEmbedder, chunk_document, save_embeddings
from memdocs.schemas import DocumentIndex
from memdocs.search import LocalVectorSearch


class MemoryIndexer:
    """Create and maintain searchable memory index."""

    def __init__(
        self,
        memory_dir: Path = Path(".memdocs/memory"),
        use_embeddings: bool = True,
    ):
        """Initialize memory indexer.

        Args:
            memory_dir: Directory for memory storage
            use_embeddings: Whether to generate embeddings (requires optional deps)
        """
        self.memory_dir = memory_dir
        self.use_embeddings = use_embeddings
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        # Initialize embedder and search (if enabled)
        self.embedder = None
        self.search = None

        if use_embeddings:
            try:
                self.embedder = LocalEmbedder()
                # LocalEmbedder.dimension is set after model loads, guaranteed to be int
                dimension_value = self.embedder.dimension if self.embedder.dimension else 384
                self.search = LocalVectorSearch(
                    index_path=memory_dir / "faiss.index",
                    metadata_path=memory_dir / "faiss_metadata.json",
                    dimension=dimension_value,
                )
            except ImportError:
                # Optional dependency not installed
                self.use_embeddings = False

    def index_document(
        self,
        doc_index: DocumentIndex,
        markdown_summary: str,
    ) -> dict[str, Any]:
        """Index document for semantic search.

        Args:
            doc_index: Document index metadata
            markdown_summary: Markdown summary text

        Returns:
            Indexing statistics
        """
        stats: dict[str, Any] = {
            "chunks": 0,
            "embeddings_generated": 0,
            "indexed": False,
        }

        if not self.use_embeddings or not self.embedder or not self.search:
            return stats

        # Chunk document
        chunks = chunk_document(markdown_summary, max_tokens=512, overlap=50)
        stats["chunks"] = len(chunks)

        if not chunks:
            return stats

        # Generate embeddings
        embeddings = self.embedder.embed_documents(chunks)
        stats["embeddings_generated"] = len(embeddings)

        # Prepare metadata for each chunk
        documents = []
        for i, chunk_text in enumerate(chunks):
            doc_metadata = {
                "doc_id": doc_index.commit or "unknown",
                "chunk_index": i,
                "chunk_text": chunk_text[:200],  # Store preview
                "file_paths": [str(p) for p in doc_index.scope.paths],
                "features": [f.title for f in doc_index.features],
                "timestamp": doc_index.timestamp.isoformat(),
            }
            documents.append(doc_metadata)

        # Add to search index
        indices = self.search.add_embeddings(embeddings, documents)
        stats["indexed"] = True
        stats["indices"] = indices

        # Save embeddings separately (optional, for inspection)
        embeddings_file = self.memory_dir / f"embeddings-{doc_index.commit or 'latest'}.json"
        save_embeddings(
            embeddings=embeddings,
            metadata={
                "doc_id": doc_index.commit or "unknown",
                "chunk_count": len(chunks),
                "chunks": chunks,
            },
            output_file=embeddings_file,
        )

        return stats

    def query_memory(self, query: str, k: int = 5) -> list[dict[str, Any]]:
        """Query memory using natural language.

        Args:
            query: Natural language query
            k: Number of results to return

        Returns:
            List of matching documents with scores
        """
        if not self.use_embeddings or not self.embedder or not self.search:
            return []

        # Generate query embedding
        query_embedding = self.embedder.embed_query(query)

        # Search
        results = self.search.search(query_embedding, k=k)

        return results

    def get_stats(self) -> dict[str, Any]:
        """Get indexing statistics.

        Returns:
            Dictionary with stats
        """
        if not self.search:
            return {"enabled": False}

        search_stats = self.search.get_stats()
        search_stats["enabled"] = True

        return search_stats
