"""
Privacy guard for PII/PHI detection and redaction.

Detects and redacts sensitive information:
- Email addresses
- Phone numbers
- Social Security Numbers (SSN)
- Medical Record Numbers (MRN)
- Credit card numbers
- IP addresses
- API keys/tokens
"""

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from memdocs.schemas import PHIMode


@dataclass
class RedactionMatch:
    """A detected PII/PHI match."""

    type: str
    value: str
    start: int
    end: int
    context: str  # Surrounding text


class Guard:
    """Privacy guard for PII/PHI detection and redaction."""

    # Regex patterns for common PII/PHI
    PATTERNS = {
        "email": re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            re.IGNORECASE,
        ),
        "phone": re.compile(r"\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b"),
        "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
        "credit_card": re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b"),
        "ipv4": re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"),
        "api_key": re.compile(
            r"\b(?:api[_-]?key|token)[:\s=]+['\"]?([a-zA-Z0-9_-]{20,})['\"]?", re.IGNORECASE
        ),
        "mrn": re.compile(r"\b(?:MRN|mrn)[:\s#]+([A-Z0-9]{6,})\b"),
    }

    def __init__(self, mode: PHIMode, scrub_types: list[str], audit_path: Path | None = None):
        """Initialize guard.

        Args:
            mode: Privacy protection mode
            scrub_types: List of PII/PHI types to scrub
            audit_path: Path to audit log file
        """
        self.mode = mode
        self.scrub_types = scrub_types
        self.audit_path = audit_path
        self.audit_log: list[dict[str, Any]] = []

    def scan(self, text: str) -> list[RedactionMatch]:
        """Scan text for PII/PHI.

        Args:
            text: Text to scan

        Returns:
            List of detected matches
        """
        if self.mode == PHIMode.OFF:
            return []

        matches: list[RedactionMatch] = []

        for scrub_type in self.scrub_types:
            if scrub_type not in self.PATTERNS:
                continue

            pattern = self.PATTERNS[scrub_type]
            for match in pattern.finditer(text):
                # Get surrounding context (20 chars before/after)
                start = max(0, match.start() - 20)
                end = min(len(text), match.end() + 20)
                context = text[start:end]

                matches.append(
                    RedactionMatch(
                        type=scrub_type,
                        value=match.group(0),
                        start=match.start(),
                        end=match.end(),
                        context=context,
                    )
                )

        return matches

    def redact(self, text: str, doc_id: str) -> tuple[str, list[RedactionMatch]]:
        """Redact PII/PHI from text.

        Args:
            text: Text to redact
            doc_id: Document ID for audit trail

        Returns:
            Tuple of (redacted_text, matches)
        """
        if self.mode == PHIMode.OFF:
            return text, []

        matches = self.scan(text)

        if not matches:
            return text, []

        # Sort matches by start position (reverse order for safe replacement)
        matches_sorted = sorted(matches, key=lambda m: m.start, reverse=True)

        redacted_text = text
        for match in matches_sorted:
            replacement = f"[REDACTED:{match.type.upper()}]"
            redacted_text = redacted_text[: match.start] + replacement + redacted_text[match.end :]

        # Log redactions
        self._audit_redactions(doc_id, matches)

        return redacted_text, matches

    def _audit_redactions(self, doc_id: str, matches: list[RedactionMatch]) -> None:
        """Log redactions to audit trail.

        Args:
            doc_id: Document ID
            matches: List of redacted matches
        """
        if not matches:
            return

        audit_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "redaction_applied",
            "doc_id": doc_id,
            "redactions": [
                {
                    "type": m.type,
                    "location": f"char:{m.start}-{m.end}",
                    "context": m.context[:50],  # Truncate context
                }
                for m in matches
            ],
        }

        self.audit_log.append(audit_entry)

        # Write to audit file if configured
        if self.audit_path:
            self._write_audit_log(audit_entry)

    def _write_audit_log(self, entry: dict[str, Any]) -> None:
        """Write audit entry to log file.

        Args:
            entry: Audit log entry
        """
        if not self.audit_path:
            return

        # Ensure directory exists
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)

        # Append to audit log (JSONL format)
        with open(self.audit_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def validate_content(self, content: str) -> tuple[bool, list[str]]:
        """Validate content doesn't contain unredacted PII/PHI.

        Args:
            content: Content to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        if self.mode == PHIMode.OFF:
            return True, []

        matches = self.scan(content)

        if not matches:
            return True, []

        errors = [
            f"Unredacted {match.type} found at position {match.start}: {match.context[:30]}..."
            for match in matches[:5]  # Limit to first 5
        ]

        if len(matches) > 5:
            errors.append(f"... and {len(matches) - 5} more")

        return False, errors

    def get_audit_summary(self) -> dict[str, Any]:
        """Get summary of redactions in current session.

        Returns:
            Summary dictionary
        """
        if not self.audit_log:
            return {"total_events": 0, "total_redactions": 0, "by_type": {}}

        total_redactions = sum(len(entry["redactions"]) for entry in self.audit_log)

        by_type: dict[str, int] = {}
        for entry in self.audit_log:
            for redaction in entry["redactions"]:
                redaction_type = redaction["type"]
                by_type[redaction_type] = by_type.get(redaction_type, 0) + 1

        return {
            "total_events": len(self.audit_log),
            "total_redactions": total_redactions,
            "by_type": by_type,
        }


def create_guard_from_config(
    mode: PHIMode, scrub_types: list[str], audit_dir: Path | None = None
) -> Guard:
    """Create guard from configuration.

    Args:
        mode: Privacy mode
        scrub_types: Types to scrub
        audit_dir: Directory for audit logs

    Returns:
        Configured Guard instance
    """
    audit_path = audit_dir / "audit.log" if audit_dir else None
    return Guard(mode=mode, scrub_types=scrub_types, audit_path=audit_path)
