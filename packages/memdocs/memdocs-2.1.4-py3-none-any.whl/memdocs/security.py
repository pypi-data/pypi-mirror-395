"""
Security utilities for input validation and safe file operations.

Provides path validation, input sanitization, and rate limiting.
"""

import os
import re
import time
from pathlib import Path
from typing import Any

from memdocs.exceptions import SecurityError


class PathValidator:
    """Validate and sanitize file paths to prevent path traversal attacks."""

    @staticmethod
    def validate_path(path: Path, base_dir: Path | None = None) -> Path:
        """Validate a path is safe and doesn't escape base directory.

        Args:
            path: Path to validate
            base_dir: Base directory path must stay within (default: current dir)

        Returns:
            Resolved absolute path

        Raises:
            SecurityError: If path attempts to escape base directory
            ValueError: If path is invalid
        """
        try:
            # Resolve to absolute path
            abs_path = path.resolve()

            # Check for base directory constraint
            if base_dir:
                abs_base = base_dir.resolve()
                try:
                    # Check if path is within base directory
                    abs_path.relative_to(abs_base)
                except ValueError:
                    raise SecurityError(
                        f"Attempts to escape base directory '{base_dir}'. Path traversal attacks are not allowed.",
                        path,
                    )

            # Check for suspicious patterns
            path_str = str(path)
            if ".." in path_str:
                # resolve() should handle this, but double-check
                if ".." in str(abs_path.relative_to(abs_path.anchor)):
                    raise SecurityError("Contains suspicious '..' traversal sequences", path)

            # Check for null bytes (path injection)
            if "\x00" in path_str:
                raise SecurityError("Contains null bytes (potential injection)", path)

            return abs_path

        except (OSError, RuntimeError) as e:
            raise ValueError(f"Invalid path '{path}': {e}") from e

    @staticmethod
    def validate_write_path(path: Path, allowed_dirs: list[Path]) -> Path:
        """Validate a path is safe for writing and within allowed directories.

        Args:
            path: Path to validate for writing
            allowed_dirs: List of allowed base directories

        Returns:
            Validated absolute path

        Raises:
            SecurityError: If path is not within allowed directories
        """
        abs_path = PathValidator.validate_path(path)

        # Check if path is within any allowed directory
        for allowed_dir in allowed_dirs:
            abs_allowed = allowed_dir.resolve()
            try:
                abs_path.relative_to(abs_allowed)
                return abs_path
            except ValueError:
                continue

        # Path not in any allowed directory
        allowed_str = ", ".join(str(d) for d in allowed_dirs)
        raise SecurityError(
            f"Not within allowed directories: {allowed_str}. Writing to arbitrary locations is not permitted.",
            path,
        )


class InputValidator:
    """Validate user inputs and configuration values."""

    # Pattern for valid API keys (Anthropic format: sk-ant-...)
    API_KEY_PATTERN = re.compile(r"^sk-ant-[a-zA-Z0-9_-]{95,}$")

    # Pattern for sensitive data that should never be in outputs
    SENSITIVE_PATTERNS = [
        re.compile(r"sk-ant-[a-zA-Z0-9_-]+"),  # Anthropic keys
        re.compile(r"sk-[a-zA-Z0-9]{32,}"),  # OpenAI keys
        re.compile(r"[a-zA-Z0-9+/]{40,}={0,2}"),  # Base64 secrets
        re.compile(r"(?i)(password|passwd|pwd)\s*[:=]\s*\S+"),  # Password fields
        re.compile(r"(?i)(api[_-]?key|apikey)\s*[:=]\s*\S+"),  # API key fields
    ]

    @staticmethod
    def validate_api_key(api_key: str, allow_empty: bool = False) -> str:
        """Validate Anthropic API key format.

        Args:
            api_key: API key to validate
            allow_empty: Whether to allow empty string (for optional keys)

        Returns:
            Validated API key

        Raises:
            ValueError: If API key format is invalid
        """
        if not api_key:
            if allow_empty:
                return api_key
            raise ValueError(
                "API key is required. Set ANTHROPIC_API_KEY environment variable or "
                "pass --api-key parameter. Get your key at: https://console.anthropic.com/"
            )

        if not InputValidator.API_KEY_PATTERN.match(api_key):
            raise ValueError(
                "Invalid API key format. Anthropic API keys start with 'sk-ant-' "
                "followed by 95+ characters. Check your API key at: "
                "https://console.anthropic.com/"
            )

        return api_key

    @staticmethod
    def validate_model_name(model: str) -> str:
        """Validate Claude model name.

        Args:
            model: Model name to validate

        Returns:
            Validated model name

        Raises:
            ValueError: If model name is invalid
        """
        valid_models = [
            "claude-sonnet-4-5-20250929",
            "claude-sonnet-4-20250514",
            "claude-opus-4-20250514",
            "claude-3-5-sonnet-20241022",
            "claude-3-5-sonnet-20240620",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
        ]

        if model not in valid_models:
            valid_str = ", ".join(valid_models)
            raise ValueError(
                f"Invalid model name '{model}'. Valid models: {valid_str}. "
                "See https://docs.anthropic.com/claude/docs/models-overview"
            )

        return model

    @staticmethod
    def sanitize_output(text: str, redact_secrets: bool = True) -> str:
        """Sanitize text output to remove sensitive data.

        Args:
            text: Text to sanitize
            redact_secrets: Whether to redact sensitive patterns

        Returns:
            Sanitized text
        """
        if not redact_secrets:
            return text

        sanitized = text
        for pattern in InputValidator.SENSITIVE_PATTERNS:
            sanitized = pattern.sub("[REDACTED]", sanitized)

        return sanitized

    @staticmethod
    def check_for_secrets(text: str) -> list[str]:
        """Check if text contains potential secrets.

        Args:
            text: Text to check

        Returns:
            List of found secret patterns (redacted)
        """
        found_secrets = []
        for pattern in InputValidator.SENSITIVE_PATTERNS:
            matches = pattern.findall(text)
            if matches:
                found_secrets.extend(["[REDACTED]"] * len(matches))

        return found_secrets

    @staticmethod
    def validate_file_size(path: Path, max_size_mb: float = 10.0) -> None:
        """Validate file size is within limits.

        Args:
            path: File path to check
            max_size_mb: Maximum file size in MB

        Raises:
            ValueError: If file is too large
        """
        if not path.exists():
            raise ValueError(f"File does not exist: {path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        size_bytes = path.stat().st_size
        size_mb = size_bytes / (1024 * 1024)

        if size_mb > max_size_mb:
            raise ValueError(
                f"File '{path.name}' is too large ({size_mb:.1f}MB). "
                f"Maximum size: {max_size_mb}MB. "
                "Large files may cause performance issues."
            )


class RateLimiter:
    """Simple rate limiter for API calls."""

    def __init__(self, max_calls: int = 50, window_seconds: int = 60):
        """Initialize rate limiter.

        Args:
            max_calls: Maximum calls allowed in window
            window_seconds: Time window in seconds
        """
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.calls: list[float] = []

    def check_rate_limit(self) -> None:
        """Check if rate limit is exceeded.

        Raises:
            SecurityError: If rate limit exceeded
        """
        now = time.time()
        window_start = now - self.window_seconds

        # Remove old calls outside window
        self.calls = [call_time for call_time in self.calls if call_time > window_start]

        if len(self.calls) >= self.max_calls:
            raise RuntimeError(
                f"Rate limit exceeded: {self.max_calls} calls per {self.window_seconds}s. "
                "Please wait before making more requests."
            )

        # Record this call
        self.calls.append(now)

    def get_remaining_calls(self) -> int:
        """Get number of remaining calls in current window.

        Returns:
            Number of calls remaining
        """
        now = time.time()
        window_start = now - self.window_seconds
        self.calls = [call_time for call_time in self.calls if call_time > window_start]
        return max(0, self.max_calls - len(self.calls))

    def reset(self) -> None:
        """Reset rate limiter."""
        self.calls = []


class ConfigValidator:
    """Validate configuration values."""

    @staticmethod
    def validate_scope_level(scope: str) -> str:
        """Validate scope level.

        Args:
            scope: Scope level to validate

        Returns:
            Validated scope level

        Raises:
            ValueError: If scope is invalid
        """
        valid_scopes = ["file", "module", "repo"]
        if scope not in valid_scopes:
            raise ValueError(f"Invalid scope '{scope}'. Valid scopes: {', '.join(valid_scopes)}")
        return scope

    @staticmethod
    def validate_output_format(output_format: str) -> str:
        """Validate output format.

        Args:
            output_format: Output format to validate

        Returns:
            Validated format

        Raises:
            ValueError: If format is invalid
        """
        valid_formats = ["json", "yaml", "markdown"]
        if output_format not in valid_formats:
            raise ValueError(
                f"Invalid format '{output_format}'. Valid formats: {', '.join(valid_formats)}"
            )
        return output_format

    @staticmethod
    def validate_positive_int(value: int, name: str, min_value: int = 1) -> int:
        """Validate positive integer value.

        Args:
            value: Value to validate
            name: Parameter name for error message
            min_value: Minimum allowed value

        Returns:
            Validated value

        Raises:
            ValueError: If value is invalid
        """
        if not isinstance(value, int):
            raise ValueError(f"{name} must be an integer, got {type(value).__name__}")

        if value < min_value:
            raise ValueError(f"{name} must be >= {min_value}, got {value}")

        return value

    @staticmethod
    def validate_temperature(temp: float) -> float:
        """Validate AI temperature parameter.

        Args:
            temp: Temperature to validate (0.0-1.0)

        Returns:
            Validated temperature

        Raises:
            ValueError: If temperature is out of range
        """
        if not isinstance(temp, (int, float)):
            raise ValueError(f"Temperature must be a number, got {type(temp).__name__}")

        if not 0.0 <= temp <= 1.0:
            raise ValueError(f"Temperature must be between 0.0 and 1.0, got {temp}")

        return float(temp)


def sanitize_for_commit(text: str) -> tuple[str, list[str]]:
    """Sanitize text before committing to git (remove secrets).

    Args:
        text: Text to sanitize

    Returns:
        Tuple of (sanitized_text, list_of_redactions)
    """
    secrets_found = InputValidator.check_for_secrets(text)
    if secrets_found:
        sanitized = InputValidator.sanitize_output(text, redact_secrets=True)
        return sanitized, secrets_found

    return text, []


def validate_environment() -> dict[str, Any]:
    """Validate environment is safe for operation.

    Returns:
        Dictionary of environment validation results
    """
    results = {
        "api_key_set": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "in_git_repo": Path(".git").exists(),
        "memdocs_initialized": Path(".memdocs.yml").exists(),
        "writable_cwd": os.access(".", os.W_OK),
    }

    return results
