"""
AI-powered summarization using Claude Sonnet 4.5.

Generates structured YAML documentation from extracted code context,
transforming git diffs and AST symbols into human-readable summaries
with risk analysis, impact tracking, and feature descriptions.
"""

import os
from typing import Any

import anthropic
import yaml

from memdocs.extract import ExtractedContext
from memdocs.schemas import (
    DocumentIndex,
    FeatureSummary,
    ImpactSummary,
    ReferenceSummary,
    ScopeInfo,
)
from memdocs.security import InputValidator, RateLimiter

# Configuration constants
DEFAULT_MAX_TOKENS = 4096  # Default max tokens for Claude API response (schema default)


class Summarizer:
    """AI-powered documentation summarizer.

    Attributes:
        api_key: Anthropic API key
        model: Claude model name
        max_tokens: Maximum tokens for API responses
        client: Anthropic API client
        rate_limiter: Rate limiter for API calls
    """

    PROMPT_TEMPLATE = """You are a technical documentation AI generating machine-readable docs.

Your task: Analyze code changes and generate a structured, concise document.

## Context

### Scope
{scope_info}

### Git Diff
{git_diff}

### Files Changed
{files_context}

## Instructions

1. **Summarize** what changed (functions, classes, files) - be specific
2. **Explain WHY** these changes were made (infer from commit message, code)
3. **Identify IMPACT** (which systems/APIs affected, breaking changes)
4. **Flag RISKS** (security, performance, breaking changes)

## Output Format

Generate a YAML document with this EXACT structure:

```yaml
features:
  - id: feat-001
    title: "Brief feature title (max 100 chars)"
    description: "1-2 sentence description"
    risk:
      - "risk_category"  # e.g., timeout, security, breaking
    tags:
      - "tag1"
      - "tag2"

impacts:
  apis:
    - "/api/endpoint/path"
  breaking_changes:
    - "Description of breaking change"
  tests_added: 0
  tests_modified: 0
  migration_required: false

refs:
  pr: null
  issues: []
  files_changed:
    - "path/to/file.py"
  commits:
    - "abc123"
```

**CRITICAL RULES:**
- Output ONLY valid YAML (no prose before/after)
- Be concise but specific (no fluff)
- Use technical language (this is for AI/developer consumption)
- Always include file paths in refs.files_changed
- Flag ALL breaking changes
- Keep feature titles under 100 characters
- Use lowercase snake_case for risk categories
- Include commit SHA in refs.commits if available

Generate the YAML now:"""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "claude-sonnet-4-5-20250929",
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ):
        """Initialize summarizer.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Claude model to use
            max_tokens: Maximum tokens for Claude API response (default: 4096)
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")

        # Validate API key
        try:
            self.api_key = InputValidator.validate_api_key(self.api_key or "", allow_empty=False)
        except Exception as e:
            raise ValueError(str(e)) from e

        # Validate model name
        try:
            self.model = InputValidator.validate_model_name(model)
        except Exception as e:
            raise ValueError(str(e)) from e

        # Store max_tokens
        self.max_tokens = max_tokens

        self.client = anthropic.Anthropic(api_key=self.api_key)

        # Initialize rate limiter (50 calls per minute)
        self.rate_limiter = RateLimiter(max_calls=50, window_seconds=60)

    def __repr__(self) -> str:
        """Return string representation with masked API key for security."""
        masked_key = "***" + self.api_key[-4:] if len(self.api_key) > 4 else "***"
        return f"Summarizer(model={self.model!r}, api_key={masked_key!r})"

    def summarize(self, context: ExtractedContext, scope: ScopeInfo) -> tuple[DocumentIndex, str]:
        """Generate documentation summary from context.

        Args:
            context: Extracted code context
            scope: Scope information

        Returns:
            Tuple of (DocumentIndex, raw_markdown_summary)
        """
        # Check rate limit before API call
        self.rate_limiter.check_rate_limit()

        # Build prompt
        prompt = self._build_prompt(context, scope)

        # Call Claude
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        # Parse response (extract text from first content block)
        first_block = response.content[0]
        if hasattr(first_block, "text"):
            yaml_content = first_block.text
        else:
            raise ValueError(f"Unexpected content block type: {type(first_block)}")

        # Extract YAML from response (in case Claude adds explanation)
        yaml_content = self._extract_yaml(yaml_content)

        # Parse YAML
        try:
            parsed = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse YAML from Claude: {e}")

        # Build DocumentIndex
        doc_index = self._build_document_index(parsed, context, scope)

        # Generate markdown summary
        markdown_summary = self._generate_markdown(doc_index, context)

        return doc_index, markdown_summary

    def _build_prompt(self, context: ExtractedContext, scope: ScopeInfo) -> str:
        """Build prompt for Claude.

        Args:
            context: Extracted context
            scope: Scope info

        Returns:
            Formatted prompt
        """
        # Format scope info
        scope_info = f"""Level: {scope.level.value}
Paths: {', '.join(str(p) for p in scope.paths)}
File count: {scope.file_count}
Escalated: {scope.escalated}"""

        # Format git diff
        git_diff = "No git information available"
        if context.diff:
            git_diff = f"""Commit: {context.diff.commit}
Author: {context.diff.author}
Message: {context.diff.message}

Changed files:
- Added: {', '.join(str(f) for f in context.diff.added_files) or 'none'}
- Modified: {', '.join(str(f) for f in context.diff.modified_files) or 'none'}
- Deleted: {', '.join(str(f) for f in context.diff.deleted_files) or 'none'}"""

        # Format files context
        files_context = []
        for file_ctx in context.files[:10]:  # Limit to first 10 files
            symbols_summary = []
            for symbol in file_ctx.symbols[:5]:  # Limit symbols
                symbols_summary.append(
                    f"  - {symbol.kind.value} {symbol.name} (line {symbol.line})"
                )

            files_context.append(
                f"""File: {file_ctx.path}
Language: {file_ctx.language}
LOC: {file_ctx.lines_of_code}
Symbols:
{chr(10).join(symbols_summary) if symbols_summary else '  (none)'}"""
            )

        files_str = "\n\n".join(files_context)
        if len(context.files) > 10:
            files_str += f"\n\n... and {len(context.files) - 10} more files"

        return self.PROMPT_TEMPLATE.format(
            scope_info=scope_info,
            git_diff=git_diff,
            files_context=files_str,
        )

    def _extract_yaml(self, text: str) -> str:
        """Extract YAML from Claude's response.

        Args:
            text: Response text

        Returns:
            Extracted YAML content
        """
        # Remove markdown code fences if present
        if "```yaml" in text:
            start = text.find("```yaml") + 7
            end = text.find("```", start)
            return text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            return text[start:end].strip()
        else:
            return text.strip()

    def _build_document_index(
        self, parsed: dict[str, Any], context: ExtractedContext, scope: ScopeInfo
    ) -> DocumentIndex:
        """Build DocumentIndex from parsed YAML.

        Args:
            parsed: Parsed YAML dict
            context: Extracted context
            scope: Scope info

        Returns:
            DocumentIndex
        """
        # Parse features
        features = [
            FeatureSummary(
                id=f.get("id", f"feat-{i+1:03d}"),
                title=f["title"],
                description=f.get("description"),
                risk=f.get("risk", []),
                tags=f.get("tags", []),
            )
            for i, f in enumerate(parsed.get("features", []))
        ]

        # Parse impacts
        impacts_dict = parsed.get("impacts", {})
        impacts = ImpactSummary(
            apis=impacts_dict.get("apis", []),
            breaking_changes=impacts_dict.get("breaking_changes", []),
            tests_added=impacts_dict.get("tests_added", 0),
            tests_modified=impacts_dict.get("tests_modified", 0),
            migration_required=impacts_dict.get("migration_required", False),
        )

        # Parse refs
        refs_dict = parsed.get("refs", {})

        # Use actual files from context, or parse from refs_dict if context is empty
        if context.files:
            files_changed = [f.path for f in context.files]
        else:
            from pathlib import Path

            files_changed = [Path(f) for f in refs_dict.get("files_changed", [])]

        refs = ReferenceSummary(
            pr=refs_dict.get("pr"),
            issues=refs_dict.get("issues", []),
            files_changed=files_changed,
            commits=refs_dict.get("commits", []),
        )

        # Get commit from context if available
        commit = context.diff.commit if context.diff else None

        return DocumentIndex(
            commit=commit,
            scope=scope,
            features=features,
            impacts=impacts,
            refs=refs,
        )

    def _generate_markdown(self, doc_index: DocumentIndex, context: ExtractedContext) -> str:
        """Generate human-readable markdown summary.

        Args:
            doc_index: Document index
            context: Extracted context

        Returns:
            Markdown summary
        """
        lines = []

        # Title
        if doc_index.features:
            title = doc_index.features[0].title
        else:
            title = "Code Changes Summary"
        lines.append(f"# {title}\n")

        # Metadata
        lines.append(f"**Commit:** {doc_index.commit or 'N/A'}")
        lines.append(f"**Scope:** {doc_index.scope.level.value.title()}-level")
        lines.append(f"**Date:** {doc_index.timestamp.strftime('%Y-%m-%d')}")
        lines.append("")

        # Summary
        lines.append("## Summary\n")
        if doc_index.features:
            for feature in doc_index.features:
                lines.append(f"- {feature.title}")
                if feature.description:
                    lines.append(f"  {feature.description}")
        lines.append("")

        # Changes
        if context.diff:
            lines.append("## Changes\n")
            if context.diff.added_files:
                lines.append(f"**Added:** {len(context.diff.added_files)} files")
                for f in context.diff.added_files[:5]:
                    lines.append(f"- {f}")
            if context.diff.modified_files:
                lines.append(f"\n**Modified:** {len(context.diff.modified_files)} files")
                for f in context.diff.modified_files[:5]:
                    lines.append(f"- {f}")
            if context.diff.deleted_files:
                lines.append(f"\n**Deleted:** {len(context.diff.deleted_files)} files")
                for f in context.diff.deleted_files[:5]:
                    lines.append(f"- {f}")
            lines.append("")

        # Impact
        if doc_index.impacts.apis or doc_index.impacts.breaking_changes:
            lines.append("## Impact\n")
            if doc_index.impacts.apis:
                lines.append(f"**APIs affected:** {', '.join(doc_index.impacts.apis)}")
            if doc_index.impacts.breaking_changes:
                lines.append("\n**Breaking changes:**")
                for change in doc_index.impacts.breaking_changes:
                    lines.append(f"- {change}")
            lines.append("")

        # Risks
        risks = [risk for f in doc_index.features for risk in f.risk]
        if risks:
            lines.append("## Risks\n")
            for risk in set(risks):
                lines.append(f"- {risk}")
            lines.append("")

        # References
        lines.append("## References\n")
        if doc_index.refs.pr:
            lines.append(f"- PR #{doc_index.refs.pr}")
        if doc_index.refs.issues:
            for issue in doc_index.refs.issues:
                lines.append(f"- Issue #{issue}")
        if doc_index.refs.commits:
            for commit in doc_index.refs.commits:
                lines.append(f"- Commit: {commit}")

        return "\n".join(lines)
