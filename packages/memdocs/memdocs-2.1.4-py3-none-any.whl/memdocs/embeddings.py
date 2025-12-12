"""
Local embeddings generation using sentence-transformers.

Zero-cost alternative to OpenAI embeddings API ($0.13/1M tokens → $0).
Model downloads once (~90MB), runs 100% locally for privacy-first operation.

Enables semantic search over code documentation without external API dependencies.
"""

import json
from pathlib import Path
from typing import Any, cast

import tiktoken

# Configuration constants
DEFAULT_EMBEDDING_BATCH_SIZE = 32  # Batch size for embedding generation


class LocalEmbedder:
    """Generate embeddings locally using sentence-transformers.

    Benefits over OpenAI:
    - $0 cost (vs $0.13 per 1M tokens)
    - 100% local (works offline)
    - Fast (GPU optional, CPU sufficient)
    - Privacy (data never leaves machine)
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        cache_dir: Path | None = None,
    ):
        """Initialize local embedder.

        Args:
            model_name: HuggingFace model name
                - all-MiniLM-L6-v2: 384-dim, 80MB, fast, good quality
                - all-mpnet-base-v2: 768-dim, 420MB, slower, best quality
            cache_dir: Directory to cache model (default: ~/.cache/memdocs)
        """
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError(  # noqa: B904
                "sentence-transformers not installed. "
                "Install with: pip install 'memdocs[embeddings]'"
            )

        self.model_name = model_name
        self.cache_dir = cache_dir or Path.home() / ".cache" / "memdocs"

        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            raise RuntimeError(
                f"Failed to create cache directory at {self.cache_dir}: {e}. "
                "Check permissions or set cache_dir to a writable location."
            ) from e

        # Load model (downloads on first run, then cached)
        try:
            self.model = SentenceTransformer(model_name, cache_folder=str(self.cache_dir))
            self.dimension = self.model.get_sentence_embedding_dimension()
        except Exception as e:
            raise RuntimeError(
                f"Failed to load embedding model '{model_name}': {e}. "
                "This may be due to:\n"
                "  - Network issues (model download failed)\n"
                "  - Insufficient disk space\n"
                "  - Invalid model name\n"
                "Install with: pip install 'memdocs[embeddings]'"
            ) from e

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for documents.

        Args:
            texts: List of text documents to embed

        Returns:
            List of embedding vectors (dimension = 384 for default model)
        """
        if not texts:
            return []

        # Generate embeddings
        embeddings = self.model.encode(
            texts,
            batch_size=DEFAULT_EMBEDDING_BATCH_SIZE,  # Process in batches for efficiency
            show_progress_bar=len(texts) > 10,  # Show progress for large batches
            convert_to_numpy=True,
        )

        return cast(list[list[float]], embeddings.tolist())

    def embed_query(self, query: str) -> list[float]:
        """Generate embedding for a single query.

        Args:
            query: Query text

        Returns:
            Embedding vector
        """
        embedding = self.model.encode([query], convert_to_numpy=True)
        return cast(list[float], embedding[0].tolist())


def chunk_document(text: str, max_tokens: int = 512, overlap: int = 50) -> list[str]:
    """Split document into chunks for embedding.

    Uses tiktoken for accurate token counting to ensure chunks respect token limits.
    This is important for embedding models that have strict token limits (e.g., 512 tokens).

    Args:
        text: Document text to chunk
        max_tokens: Maximum tokens per chunk (model limit, default: 512)
        overlap: Tokens to overlap between chunks for continuity (default: 50)

    Returns:
        List of text chunks, each respecting max_tokens limit

    Raises:
        ValueError: If max_tokens <= overlap (would create infinite loop)

    Example:
        >>> text = "Long document text..."
        >>> chunks = chunk_document(text, max_tokens=512, overlap=50)
        >>> # Each chunk has <= 512 tokens with 50 token overlap
    """
    if max_tokens <= overlap:
        raise ValueError(f"max_tokens ({max_tokens}) must be greater than overlap ({overlap})")

    # Use cl100k_base encoding (used by OpenAI's text-embedding-ada-002 and similar models)
    # This encoding is also suitable for sentence-transformers models as an approximation
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
    except Exception:
        # Fallback to a default encoding if cl100k_base is not available
        encoding = tiktoken.get_encoding("p50k_base")

    # Encode entire text into tokens
    tokens = encoding.encode(text)

    if not tokens:
        return []

    chunks = []
    start_idx = 0

    while start_idx < len(tokens):
        # Calculate end index for this chunk
        end_idx = min(start_idx + max_tokens, len(tokens))

        # Extract chunk tokens
        chunk_tokens = tokens[start_idx:end_idx]

        # Decode tokens back to text
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)

        # Move start index forward, accounting for overlap
        # For the last chunk, we're done
        if end_idx >= len(tokens):
            break

        start_idx += max_tokens - overlap

    return chunks


def save_embeddings(
    embeddings: list[list[float]],
    metadata: dict[str, Any],
    output_file: Path,
) -> None:
    """Save embeddings to file (git-committed).

    Args:
        embeddings: List of embedding vectors
        metadata: Metadata about embeddings (file paths, chunk info, etc.)
        output_file: Path to save embeddings
    """
    data = {
        "embeddings": embeddings,
        "metadata": metadata,
        "dimension": len(embeddings[0]) if embeddings else 0,
        "count": len(embeddings),
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_embeddings(embeddings_file: Path) -> tuple[list[list[float]], dict[str, Any]]:
    """Load embeddings from file.

    Args:
        embeddings_file: Path to embeddings file

    Returns:
        Tuple of (embeddings, metadata)
    """
    if not embeddings_file.exists():
        return [], {}

    with open(embeddings_file, encoding="utf-8") as f:
        data = json.load(f)

    return data.get("embeddings", []), data.get("metadata", {})
