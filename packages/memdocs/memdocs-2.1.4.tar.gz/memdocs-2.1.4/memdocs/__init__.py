"""
Doc-Intelligence: Lightweight documentation system for AI-powered memory.

Generate machine-friendly docs from code changes without bureaucratic overhead.
"""

__version__ = "2.1.4"
__author__ = "Patrick Roebuck"
__license__ = "Apache-2.0"

from memdocs.exceptions import (
    APIError,
    ConfigurationError,
    DependencyError,
    EmbeddingError,
    ExtractionError,
    IndexingError,
    MCPServerError,
    MemDocsError,
    SecurityError,
    SummarizationError,
    ValidationError,
)
from memdocs.schemas import (
    DocIntConfig,
    DocumentIndex,
    FeatureSummary,
    ReviewResult,
    Symbol,
)

__all__ = [
    "__version__",
    # Schemas
    "DocIntConfig",
    "ReviewResult",
    "DocumentIndex",
    "Symbol",
    "FeatureSummary",
    # Exceptions
    "MemDocsError",
    "ConfigurationError",
    "APIError",
    "ValidationError",
    "ExtractionError",
    "SummarizationError",
    "IndexingError",
    "EmbeddingError",
    "MCPServerError",
    "SecurityError",
    "DependencyError",
]
