"""
Data schemas and models for doc-intelligence.

Uses Pydantic for validation and serialization to YAML/JSON.
"""

from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator


class ScopeLevel(str, Enum):
    """Documentation scope level."""

    FILE = "file"
    MODULE = "module"
    REPO = "repo"


class EventType(str, Enum):
    """Trigger event types."""

    PR = "pr"
    COMMIT = "commit"
    RELEASE = "release"
    SCHEDULE = "schedule"
    MANUAL = "manual"


class PHIMode(str, Enum):
    """Privacy protection mode for PHI/PII."""

    OFF = "off"
    STANDARD = "standard"
    STRICT = "strict"


class SymbolKind(str, Enum):
    """Code symbol types."""

    FUNCTION = "function"
    CLASS = "class"
    METHOD = "method"
    VARIABLE = "variable"
    CONSTANT = "constant"
    INTERFACE = "interface"
    ENUM = "enum"


# Configuration Models


class PolicyConfig(BaseModel):
    """Policy configuration for scope and escalation."""

    default_scope: ScopeLevel = Field(default=ScopeLevel.FILE)
    max_files_without_force: int = Field(default=150, ge=1)
    escalate_on: list[str] = Field(
        default_factory=lambda: [
            "cross_module_changes",
            "security_sensitive_paths",
            "public_api_signatures",
        ]
    )


class PrivacyConfig(BaseModel):
    """Privacy and PHI/PII configuration."""

    phi_mode: PHIMode = Field(default=PHIMode.STANDARD)
    scrub: list[str] = Field(default_factory=lambda: ["email", "phone", "ssn", "mrn"])
    audit_redactions: bool = Field(default=True)


class OutputsConfig(BaseModel):
    """Output directory and format configuration."""

    docs_dir: Path = Field(default=Path(".memdocs/docs"))
    memory_dir: Path = Field(default=Path(".memdocs/memory"))
    formats: list[Literal["yaml", "json", "markdown"]] = Field(
        default_factory=lambda: ["yaml", "json", "markdown"]  # type: ignore[arg-type]
    )


class RetentionConfig(BaseModel):
    """Data retention policy."""

    embeddings_days: int = Field(default=90, ge=-1)  # -1 = unlimited
    audit_logs_days: int = Field(default=365, ge=1)


class AIConfig(BaseModel):
    """AI provider and model configuration."""

    provider: Literal["anthropic", "openai"] = Field(default="anthropic")
    model: str = Field(default="claude-sonnet-4-5-20250929")
    embeddings_model: str = Field(default="text-embedding-3-small")
    max_tokens: int = Field(default=4096, ge=1024, le=200000)


class DocIntConfig(BaseModel):
    """Main configuration for doc-intelligence."""

    version: int = Field(default=1)
    policies: PolicyConfig = Field(default_factory=PolicyConfig)
    privacy: PrivacyConfig = Field(default_factory=PrivacyConfig)
    outputs: OutputsConfig = Field(default_factory=OutputsConfig)
    retention: RetentionConfig = Field(default_factory=RetentionConfig)
    ai: AIConfig = Field(default_factory=AIConfig)

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: int) -> int:
        if v != 1:
            raise ValueError("Only version 1 is supported")
        return v


# Output Models


class Symbol(BaseModel):
    """Code symbol (function, class, etc.)."""

    file: Path
    kind: SymbolKind
    name: str
    line: int = Field(ge=1)
    signature: str | None = Field(default=None)
    doc: str | None = Field(default=None)
    methods: list[str] | None = Field(default=None)  # For classes


class SymbolsOutput(BaseModel):
    """Symbols YAML output."""

    symbols: list[Symbol]


class FeatureSummary(BaseModel):
    """Feature or change summary."""

    id: str = Field(pattern=r"^feat-\d+$")
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    risk: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class ImpactSummary(BaseModel):
    """Impact assessment."""

    apis: list[str] = Field(default_factory=list)
    breaking_changes: list[str] = Field(default_factory=list)
    tests_added: int = Field(default=0, ge=0)
    tests_modified: int = Field(default=0, ge=0)
    migration_required: bool = Field(default=False)


class ReferenceSummary(BaseModel):
    """External references."""

    pr: int | None = Field(default=None, ge=1)
    issues: list[int] = Field(default_factory=list)
    files_changed: list[Path] = Field(default_factory=list)
    commits: list[str] = Field(default_factory=list)


class ScopeInfo(BaseModel):
    """Scope information for review."""

    paths: list[Path]
    level: ScopeLevel
    file_count: int = Field(ge=0)
    escalated: bool = Field(default=False)
    escalation_reason: str | None = Field(default=None)


class DocumentIndex(BaseModel):
    """Top-level index.json output."""

    model_config = ConfigDict(
        ser_json_timedelta="iso8601",
    )

    commit: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    scope: ScopeInfo
    features: list[FeatureSummary]
    impacts: ImpactSummary
    refs: ReferenceSummary

    @field_serializer("timestamp")
    def serialize_datetime(self, dt: datetime, _info) -> str:
        return dt.isoformat()


class RedactionEvent(BaseModel):
    """PHI/PII redaction audit event."""

    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event: Literal["phi_detected", "pii_detected", "redaction_applied"]
    doc_id: str
    redactions: list[dict[str, Any]]


class ReviewResult(BaseModel):
    """Result of a doc-intelligence review."""

    model_config = ConfigDict()

    success: bool
    scope: ScopeInfo
    outputs: dict[str, Path]  # format -> file path
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    duration_ms: float = Field(ge=0)
    redactions: list[RedactionEvent] = Field(default_factory=list)

    @field_serializer("outputs")
    def serialize_outputs(self, outputs: dict[str, Path], _info) -> dict[str, str]:
        return {k: str(v) for k, v in outputs.items()}
