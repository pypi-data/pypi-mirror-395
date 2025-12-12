"""
Empathy Framework Adapter for DocInt.

Transforms Empathy Framework analysis results into DocInt document format
and stores them in git-committed memory.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .index import MemoryIndexer
from .schemas import (
    DocumentIndex,
    FeatureSummary,
    ImpactSummary,
    ReferenceSummary,
    ScopeInfo,
    ScopeLevel,
)


class EmpathyAdapter:
    """
    Adapter to convert Empathy Framework analysis results into DocInt format.

    Empathy provides multi-layer analysis (rules, patterns, AI, anticipatory).
    This adapter transforms those results into DocInt's document format and
    stores them in the .memdocs/ directory for git-committed memory.
    """

    def __init__(self, memdocs_root: Path = Path(".memdocs")):
        """Initialize the adapter with DocInt storage directory."""
        self.memdocs_root = Path(memdocs_root)
        self.docs_dir = self.memdocs_root / "docs"
        self.memory_dir = self.memdocs_root / "memory"

        # Create directories if they don't exist
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        # Initialize memory index
        self.memory_index = MemoryIndexer(self.memory_dir)

    def store_empathy_analysis(
        self,
        analysis_results: dict[str, Any],
        file_path: str | Path,
        commit: str | None = None,
        pr_number: int | None = None,
        issues: list[int] | None = None,
    ) -> DocumentIndex:
        """
        Store Empathy Framework analysis results in DocInt format.

        Args:
            analysis_results: Results from EmpathyService.run_wizard()
            file_path: Path to the analyzed file
            commit: Git commit hash (optional)
            pr_number: Pull request number (optional)
            issues: Related issue numbers (optional)

        Returns:
            DocumentIndex object with stored results
        """
        file_path = Path(file_path)

        # Extract features from Empathy analysis
        features = self._extract_features(analysis_results)

        # Extract impacts
        impacts = self._extract_impacts(analysis_results)

        # Create scope info
        scope = ScopeInfo(
            paths=[file_path],
            level=ScopeLevel.FILE,
            file_count=1,
            escalated=False,
        )

        # Create references
        refs = ReferenceSummary(
            pr=pr_number,
            issues=issues or [],
            files_changed=[file_path],
            commits=[commit] if commit else [],
        )

        # Create document index
        doc_index = DocumentIndex(
            commit=commit,
            timestamp=datetime.now(timezone.utc),
            scope=scope,
            features=features,
            impacts=impacts,
            refs=refs,
        )

        # Write outputs
        self._write_index_json(doc_index, file_path)
        self._write_summary_md(doc_index, analysis_results, file_path)
        self._write_symbols_yaml(analysis_results, file_path)

        # Update memory index with embeddings
        self._update_memory_index(doc_index, analysis_results, file_path)

        return doc_index

    def _extract_features(self, analysis_results: dict[str, Any]) -> list[FeatureSummary]:
        """
        Extract features from Empathy analysis results.

        Converts current_issues and predictions into feature summaries.
        """
        features = []

        # Process current issues (critical and error severity)
        issues = analysis_results.get("current_issues", [])
        critical_issues = [i for i in issues if i.get("severity") in ["critical", "error"]]

        for idx, issue in enumerate(critical_issues[:5]):  # Limit to top 5
            features.append(
                FeatureSummary(
                    id=f"feat-{idx+1:03d}",
                    title=issue.get("message", "Unknown issue")[:100],
                    description=issue.get("recommendation", None),
                    risk=[issue.get("type", "unknown"), issue.get("severity", "unknown")],
                    tags=[issue.get("layer", "unknown")],
                )
            )

        # Process predictions (Level 4 Anticipatory)
        predictions = analysis_results.get("predictions", [])
        for idx, pred in enumerate(
            predictions[:3], start=len(features) + 1
        ):  # Add top 3 predictions
            features.append(
                FeatureSummary(
                    id=f"feat-{idx:03d}",
                    title=pred.get("title", "Prediction")[:100],
                    description=pred.get("description", None),
                    risk=["anticipatory", pred.get("impact", "unknown")],
                    tags=["prediction", pred.get("timeframe", "unknown")],
                )
            )

        return features

    def _extract_impacts(self, analysis_results: dict[str, Any]) -> ImpactSummary:
        """
        Extract impact information from Empathy analysis.

        Identifies API changes, breaking changes, test coverage.
        """
        issues = analysis_results.get("current_issues", [])

        # Detect API-related issues
        apis_affected = []
        for issue in issues:
            msg = issue.get("message", "").lower()
            if "api" in msg or "endpoint" in msg or "route" in msg:
                apis_affected.append(issue.get("message", "Unknown API"))

        # Detect breaking changes
        breaking_changes = []
        for issue in issues:
            if issue.get("severity") == "critical":
                breaking_changes.append(issue.get("message", "Critical issue"))

        # Count test-related changes
        test_issues = [i for i in issues if "test" in i.get("message", "").lower()]

        return ImpactSummary(
            apis=apis_affected[:5],  # Limit to 5
            breaking_changes=breaking_changes[:5],
            tests_added=0,  # Can't detect from static analysis
            tests_modified=len(test_issues),
            migration_required=len(breaking_changes) > 0,
        )

    def _write_index_json(self, doc_index: DocumentIndex, file_path: Path) -> None:
        """Write index.json output."""
        # Create file-specific subdirectory
        file_dir = self.docs_dir / file_path.stem
        file_dir.mkdir(parents=True, exist_ok=True)

        output_file = file_dir / "index.json"
        with open(output_file, "w") as f:
            json.dump(doc_index.model_dump(mode="json"), f, indent=2, default=str)

    def _write_summary_md(
        self, doc_index: DocumentIndex, analysis_results: dict[str, Any], file_path: Path
    ) -> None:
        """Write summary.md output (human-readable)."""
        file_dir = self.docs_dir / file_path.stem
        file_dir.mkdir(parents=True, exist_ok=True)

        output_file = file_dir / "summary.md"

        # Build markdown summary
        lines = [
            f"# Empathy Analysis: {file_path.name}",
            "",
            f"**Commit:** {doc_index.commit or 'N/A'}",
            f"**Scope:** File-level ({file_path})",
            f"**Date:** {doc_index.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Severity Score:** {analysis_results.get('severity_score', 'N/A')}/100",
            "",
            "## Summary",
            "",
            f"Analyzed {len(analysis_results.get('current_issues', []))} issues across {len(doc_index.features)} features.",
            "",
            "## Features & Issues",
            "",
        ]

        for feature in doc_index.features:
            lines.extend(
                [
                    f"### {feature.title}",
                    "",
                    f"**ID:** {feature.id}",
                    f"**Risk:** {', '.join(feature.risk)}",
                    f"**Tags:** {', '.join(feature.tags)}",
                    "",
                    feature.description or "No description provided.",
                    "",
                ]
            )

        # Add impacts
        lines.extend(
            [
                "## Impact",
                "",
                f"- **APIs affected:** {len(doc_index.impacts.apis)}",
                f"- **Breaking changes:** {len(doc_index.impacts.breaking_changes)}",
                f"- **Tests modified:** {doc_index.impacts.tests_modified}",
                f"- **Migration required:** {'Yes' if doc_index.impacts.migration_required else 'No'}",
                "",
            ]
        )

        # Add predictions (Level 4)
        predictions = analysis_results.get("predictions", [])
        if predictions:
            lines.extend(
                [
                    "## Predictions (Level 4 Anticipatory)",
                    "",
                ]
            )
            for pred in predictions:
                lines.extend(
                    [
                        f"### {pred.get('title', 'Prediction')}",
                        "",
                        f"**Timeframe:** {pred.get('timeframe', 'Unknown')}",
                        f"**Confidence:** {pred.get('confidence', 'N/A')}",
                        f"**Impact:** {pred.get('impact', 'Unknown')}",
                        "",
                        pred.get("description", "No description."),
                        "",
                        f"**Recommendation:** {pred.get('recommendation', 'N/A')}",
                        "",
                    ]
                )

        # Add references
        lines.extend(
            [
                "## References",
                "",
                f"- **PR:** #{doc_index.refs.pr}" if doc_index.refs.pr else "- **PR:** N/A",
                (
                    f"- **Issues:** {', '.join([f'#{i}' for i in doc_index.refs.issues])}"
                    if doc_index.refs.issues
                    else "- **Issues:** None"
                ),
                f"- **Files changed:** {len(doc_index.refs.files_changed)}",
                "",
            ]
        )

        with open(output_file, "w") as f:
            f.write("\n".join(lines))

    def _write_symbols_yaml(self, analysis_results: dict[str, Any], file_path: Path) -> None:
        """
        Write symbols.yaml output with actual symbol extraction.

        Uses AST parsing to extract functions, classes, methods from source file.
        """
        file_dir = self.docs_dir / file_path.stem
        file_dir.mkdir(parents=True, exist_ok=True)

        output_file = file_dir / "symbols.yaml"

        # Try to extract symbols if file exists and we can parse it
        symbols = []
        if file_path.exists():
            try:
                from .symbol_extractor import SymbolExtractor

                extractor = SymbolExtractor()
                symbols = extractor.extract_from_file(file_path)
            except Exception:
                # If extraction fails, fall back to empty symbols
                symbols = []

        # Convert symbols to dict for YAML serialization
        symbols_data = {"symbols": [s.model_dump() for s in symbols]}

        with open(output_file, "w") as f:
            yaml.dump(
                symbols_data,
                f,
                default_flow_style=False,
                sort_keys=False,
            )

    def _update_memory_index(
        self, doc_index: DocumentIndex, analysis_results: dict[str, Any], file_path: Path
    ) -> None:
        """
        Update memory index with embeddings for search.

        Creates vector embeddings of analysis results for semantic search.
        """
        # Build markdown summary for indexing
        text_parts = []

        # Add features
        for feature in doc_index.features:
            text_parts.append(f"## {feature.title}\n\n{feature.description or ''}\n")

        # Add issue messages
        text_parts.append("\n## Issues\n")
        for issue in analysis_results.get("current_issues", []):
            text_parts.append(f"- {issue.get('message', '')}\n")

        # Add predictions
        if analysis_results.get("predictions"):
            text_parts.append("\n## Predictions\n")
            for pred in analysis_results.get("predictions", []):
                text_parts.append(f"- {pred.get('title', '')}: {pred.get('description', '')}\n")

        markdown_summary = "".join(text_parts)

        # Index document using MemoryIndexer's API
        try:
            self.memory_index.index_document(doc_index, markdown_summary)
        except Exception:
            # If indexing fails (e.g., optional dependencies not installed), continue
            pass


def adapt_empathy_to_memdocs(
    analysis_results: dict[str, Any],
    file_path: str | Path,
    memdocs_root: Path = Path(".memdocs"),
    **kwargs,
) -> DocumentIndex:
    """
    Convenience function to adapt Empathy results to DocInt format.

    Example:
        from empathy_service import EmpathyService
        from empathy_adapter import adapt_empathy_to_memdocs

        service = EmpathyService()
        results = await service.run_wizard("security", "python", code, "pro")

        doc_index = adapt_empathy_to_memdocs(
            results,
            "src/auth/login.py",
            commit="abc123",
            pr_number=42
        )
    """
    adapter = EmpathyAdapter(memdocs_root)
    return adapter.store_empathy_analysis(analysis_results, file_path, **kwargs)
