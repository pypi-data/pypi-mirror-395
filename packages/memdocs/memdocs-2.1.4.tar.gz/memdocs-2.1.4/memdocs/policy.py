"""
Policy engine for intelligent scope determination and escalation.

Automatically expands documentation scope from file → module → repo based on:
- Security-sensitive paths (auth/*, security/*)
- Cross-module dependencies and import chains
- Public API signature changes
- File count thresholds (configurable)

Ensures critical changes get comprehensive documentation while keeping
costs low for routine single-file updates.
"""

from pathlib import Path

from memdocs.extract import ExtractedContext
from memdocs.schemas import DocIntConfig, ScopeInfo, ScopeLevel


class PolicyEngine:
    """Policy engine for scope and escalation decisions."""

    def __init__(self, config: DocIntConfig):
        """Initialize policy engine.

        Args:
            config: Configuration object
        """
        self.config = config
        self.policies = config.policies

    def determine_scope(
        self,
        requested_paths: list[Path],
        context: ExtractedContext,
        force: bool = False,
    ) -> ScopeInfo:
        """Determine final scope based on policies.

        Args:
            requested_paths: Paths requested by user
            context: Extracted context
            force: Override file count limits

        Returns:
            ScopeInfo with final scope and escalation details
        """
        file_count = len(context.files)

        # Check file count limit
        if not force and file_count > self.policies.max_files_without_force:
            raise ValueError(
                f"File count ({file_count}) exceeds limit "
                f"({self.policies.max_files_without_force}). Use --force to override."
            )

        # Determine base scope from paths
        base_scope = self._infer_scope_from_paths(requested_paths)

        # Check escalation rules
        escalated, reason = self._should_escalate(context)

        final_scope = self._escalate_scope(base_scope) if escalated else base_scope

        return ScopeInfo(
            paths=requested_paths,
            level=final_scope,
            file_count=file_count,
            escalated=escalated,
            escalation_reason=reason,
        )

    def _infer_scope_from_paths(self, paths: list[Path]) -> ScopeLevel:
        """Infer scope level from requested paths.

        Args:
            paths: Requested paths

        Returns:
            Inferred scope level
        """
        if not paths:
            return self.policies.default_scope

        # Single file
        if len(paths) == 1 and not self._is_directory_pattern(paths[0]):
            return ScopeLevel.FILE

        # Multiple files in same directory = module
        if self._are_paths_in_same_module(paths):
            return ScopeLevel.MODULE

        # Multiple modules or root = repo
        return ScopeLevel.REPO

    def _is_directory_pattern(self, path: Path) -> bool:
        """Check if path is a directory or glob pattern.

        Args:
            path: Path to check

        Returns:
            True if directory pattern
        """
        return path.is_dir() or "*" in str(path) or "**" in str(path)

    def _are_paths_in_same_module(self, paths: list[Path]) -> bool:
        """Check if all paths are in the same module (directory).

        Args:
            paths: Paths to check

        Returns:
            True if same module
        """
        if not paths:
            return False

        parents = {path.parent for path in paths}
        return len(parents) == 1

    def _should_escalate(self, context: ExtractedContext) -> tuple[bool, str | None]:
        """Determine if scope should be escalated.

        Args:
            context: Extracted context

        Returns:
            Tuple of (should_escalate, reason)
        """
        escalate_rules = self.policies.escalate_on

        # Check security-sensitive paths
        if "security_sensitive_paths" in escalate_rules:
            if self._touches_security_paths(context):
                return True, "Changes touch security-sensitive paths"

        # Check cross-module changes
        if "cross_module_changes" in escalate_rules:
            if self._has_cross_module_changes(context):
                return True, "Changes span multiple modules"

        # Check public API signatures
        if "public_api_signatures" in escalate_rules:
            if self._modifies_public_api(context):
                return True, "Public API signatures modified"

        return False, None

    def _touches_security_paths(self, context: ExtractedContext) -> bool:
        """Check if changes touch security-sensitive paths.

        Args:
            context: Extracted context

        Returns:
            True if security paths touched
        """
        sensitive_patterns = ["auth", "security", "crypto", "secret", "password"]

        for file_ctx in context.files:
            path_str = str(file_ctx.path).lower()
            if any(pattern in path_str for pattern in sensitive_patterns):
                return True

        return False

    def _has_cross_module_changes(self, context: ExtractedContext) -> bool:
        """Check if changes span multiple modules.

        Args:
            context: Extracted context

        Returns:
            True if cross-module changes detected
        """
        if len(context.files) < 2:
            return False

        # Get top-level directories
        modules = {file_ctx.path.parts[0] for file_ctx in context.files if file_ctx.path.parts}

        return len(modules) > 1

    def _modifies_public_api(self, context: ExtractedContext) -> bool:
        """Check if public API is modified.

        Args:
            context: Extracted context

        Returns:
            True if public API modified
        """
        # Check if files contain exported functions/classes
        for file_ctx in context.files:
            for symbol in file_ctx.symbols:
                # Check for export keywords in signature
                if symbol.signature and "export" in symbol.signature.lower():
                    return True

        # Check for API route files
        api_patterns = ["api", "route", "endpoint", "controller"]
        for file_ctx in context.files:
            path_str = str(file_ctx.path).lower()
            if any(pattern in path_str for pattern in api_patterns):
                return True

        return False

    def _escalate_scope(self, current_scope: ScopeLevel) -> ScopeLevel:
        """Escalate scope to next level.

        Args:
            current_scope: Current scope level

        Returns:
            Escalated scope level
        """
        if current_scope == ScopeLevel.FILE:
            return ScopeLevel.MODULE
        elif current_scope == ScopeLevel.MODULE:
            return ScopeLevel.REPO
        else:
            return ScopeLevel.REPO  # Already at max

    def validate_scope(self, scope: ScopeInfo) -> list[str]:
        """Validate scope against policies.

        Args:
            scope: Scope information

        Returns:
            List of validation warnings
        """
        warnings: list[str] = []

        # Warn if repo-level without force
        if scope.level == ScopeLevel.REPO and scope.file_count > 100:
            warnings.append(
                f"Repository-level scope with {scope.file_count} files may be slow. "
                "Consider module-level scope."
            )

        # Warn if escalated
        if scope.escalated:
            warnings.append(f"Scope escalated from default due to: {scope.escalation_reason}")

        return warnings
