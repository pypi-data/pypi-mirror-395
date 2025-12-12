"""
Custom exceptions for MemDocs.

Provides clear, actionable error messages with suggestions for resolution.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


class MemDocsError(Exception):
    """Base exception for all MemDocs errors."""

    def __init__(self, message: str, suggestion: str | None = None):
        self.message = message
        self.suggestion = suggestion
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """Format error message with optional suggestion."""
        if self.suggestion:
            return f"{self.message}\n\n💡 Suggestion: {self.suggestion}"
        return self.message


class ConfigurationError(MemDocsError):
    """Configuration file is invalid or missing."""

    def __init__(self, message: str, config_path: Path | None = None):
        suggestion = None
        if config_path:
            suggestion = f"Check your configuration at: {config_path}"
        else:
            suggestion = "Run 'memdocs init' to create a default configuration"
        super().__init__(message, suggestion)


class APIError(MemDocsError):
    """Error calling external API (Claude, OpenAI, etc.)."""

    def __init__(
        self,
        message: str,
        provider: str = "Anthropic",
        status_code: int | None = None,
    ):
        self.provider = provider
        self.status_code = status_code

        suggestion = self._get_api_suggestion(status_code)
        super().__init__(message, suggestion)

    def _get_api_suggestion(self, status_code: int | None) -> str:
        """Get helpful suggestion based on status code."""
        if status_code == 401:
            return "Check your ANTHROPIC_API_KEY environment variable"
        elif status_code == 429:
            return "Rate limit exceeded. Wait a moment and try again"
        elif status_code == 500:
            return "API server error. Try again in a few minutes"
        elif status_code:
            return f"API returned status code {status_code}"
        else:
            return "Check your API key and internet connection"


class FileNotFoundError(MemDocsError):  # noqa: A001
    """Requested file or directory not found."""

    def __init__(self, path: Path, context: str | None = None):
        message = f"File or directory not found: {path}"
        if context:
            message += f"\n{context}"

        suggestion = None
        if path.suffix:  # It's a file
            suggestion = f"Make sure '{path}' exists and is accessible"
        else:  # It's a directory
            suggestion = f"Make sure directory '{path}' exists"

        super().__init__(message, suggestion)


class ValidationError(MemDocsError):
    """Input validation failed."""

    def __init__(self, field: str, value: Any, reason: str):
        message = f"Invalid value for '{field}': {value}\nReason: {reason}"
        suggestion = "Check the documentation for valid values"
        super().__init__(message, suggestion)


class ExtractionError(MemDocsError):
    """Failed to extract symbols or analyze code."""

    def __init__(self, file_path: Path, reason: str):
        message = f"Failed to extract code from {file_path}: {reason}"
        suggestion = "Ensure the file is valid code and supported language"
        super().__init__(message, suggestion)


class SummarizationError(MemDocsError):
    """Failed to generate summary with AI."""

    def __init__(self, reason: str):
        message = f"Failed to generate documentation summary: {reason}"
        suggestion = "Check your API key and try again with a smaller scope"
        super().__init__(message, suggestion)


class IndexingError(MemDocsError):
    """Failed to index or search memory."""

    def __init__(self, operation: str, reason: str):
        message = f"Indexing operation '{operation}' failed: {reason}"
        suggestion = "Check memory directory permissions and disk space"
        super().__init__(message, suggestion)


class EmbeddingError(MemDocsError):
    """Failed to generate or use embeddings."""

    def __init__(self, reason: str):
        message = f"Embedding operation failed: {reason}"
        suggestion = "Install embeddings support with: pip install memdocs[embeddings]"
        super().__init__(message, suggestion)


class MCPServerError(MemDocsError):
    """MCP server error."""

    def __init__(self, operation: str, reason: str):
        message = f"MCP server error during '{operation}': {reason}"
        suggestion = "Check MCP server logs and configuration"
        super().__init__(message, suggestion)


class SecurityError(MemDocsError):
    """Security-related error (e.g., path traversal attempt)."""

    def __init__(self, issue: str, path: Path | str):
        message = f"Security violation: {issue}\nPath: {path}"
        suggestion = "Only access files within your project directory"
        super().__init__(message, suggestion)


class DependencyError(MemDocsError):
    """Required dependency not installed."""

    def __init__(self, package: str, feature: str):
        message = f"Required dependency '{package}' not installed for feature '{feature}'"
        suggestion = f"Install with: pip install memdocs[{feature}]"
        super().__init__(message, suggestion)


# Convenience functions for common errors


def require_api_key(provider: str = "Anthropic") -> None:
    """Raise error if API key is not set."""
    import os

    key_var = f"{provider.upper()}_API_KEY"
    if not os.environ.get(key_var):
        raise APIError(
            f"{provider} API key required but not found",
            provider=provider,
            status_code=401,
        )


def validate_file_path(path: Path, must_exist: bool = True) -> None:
    """Validate file path for security and existence."""
    # Security: Prevent path traversal
    try:
        path.resolve().relative_to(Path.cwd().resolve())
    except ValueError:
        raise SecurityError("Path traversal detected", path)

    # Check existence
    if must_exist and not path.exists():
        raise FileNotFoundError(path)


def validate_config_version(version: int, supported: list[int] = None) -> None:
    """Validate configuration version."""
    if supported is None:
        supported = [1]
    if version not in supported:
        raise ConfigurationError(
            f"Unsupported configuration version: {version}. "
            f"Supported versions: {', '.join(map(str, supported))}"
        )
