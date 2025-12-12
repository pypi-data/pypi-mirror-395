"""
Extract context from git diffs, code files, and repository metadata.

Core extraction engine that powers MemDocs documentation generation.

Responsibilities:
- Parse git diffs to identify changed files
- Extract code symbols (functions, classes) using AST parsing
- Gather metadata (commit info, file stats, dependencies)
- Support multi-language symbol extraction (Python, TypeScript, JavaScript)
"""

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import git
from pygments import lexers
from pygments.util import ClassNotFound

# Python 3.11+ has tomllib built-in, earlier versions need tomli
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None  # type: ignore

from memdocs.schemas import Symbol, SymbolKind
from memdocs.security import InputValidator

# Configuration constants
MAX_FILE_SIZE_MB = 10  # Maximum file size to process (10MB)


@dataclass
class GitDiff:
    """Git diff information."""

    commit: str
    author: str
    timestamp: str
    message: str
    added_files: list[Path]
    modified_files: list[Path]
    deleted_files: list[Path]
    all_changed_files: list[Path]


@dataclass
class FileContext:
    """Context for a single file."""

    path: Path
    language: str
    lines_of_code: int
    symbols: list[Symbol]
    imports: list[str]
    dependencies: list[str]


@dataclass
class ExtractedContext:
    """Complete extracted context."""

    diff: GitDiff | None
    files: list[FileContext]
    scope_paths: list[Path]


class Extractor:
    """Extract code context from repository."""

    def __init__(self, repo_path: Path = Path(".")):
        """Initialize extractor.

        Args:
            repo_path: Path to git repository
        """
        self.repo_path = repo_path
        self.repo: git.Repo | None
        try:
            self.repo = git.Repo(repo_path)
        except git.InvalidGitRepositoryError:
            self.repo = None

    def extract_diff(self, commit: str | None = None) -> GitDiff | None:
        """Extract git diff information.

        Args:
            commit: Commit SHA (default: HEAD)

        Returns:
            GitDiff object or None if not a git repo
        """
        if not self.repo:
            return None

        commit_obj = self.repo.head.commit if not commit else self.repo.commit(commit)

        # Get diff against parent
        parent = commit_obj.parents[0] if commit_obj.parents else None
        diff_index = parent.diff(commit_obj) if parent else commit_obj.diff(None)

        added_files: list[Path] = []
        modified_files: list[Path] = []
        deleted_files: list[Path] = []

        for diff_item in diff_index:
            change_type = diff_item.change_type
            if change_type == "A" and diff_item.b_path:
                added_files.append(Path(diff_item.b_path))
            elif change_type in ("M", "R"):
                path_str = diff_item.b_path or diff_item.a_path
                if path_str:
                    modified_files.append(Path(path_str))
            elif change_type == "D" and diff_item.a_path:
                deleted_files.append(Path(diff_item.a_path))

        all_changed = added_files + modified_files + deleted_files

        # Handle optional author name and message encoding
        author_name = commit_obj.author.name or "Unknown"
        message = commit_obj.message
        if isinstance(message, bytes):
            message = message.decode("utf-8", errors="replace")
        message_str = message.strip()
        # Sanitize commit message to prevent secrets/malicious content exposure
        message_str = InputValidator.sanitize_output(message_str)

        return GitDiff(
            commit=commit_obj.hexsha[:7],
            author=author_name,
            timestamp=commit_obj.committed_datetime.isoformat(),
            message=message_str,
            added_files=added_files,
            modified_files=modified_files,
            deleted_files=deleted_files,
            all_changed_files=all_changed,
        )

    def extract_file_context(self, file_path: Path) -> FileContext | None:
        """Extract context from a single file.

        Args:
            file_path: Path to file

        Returns:
            FileContext or None if file doesn't exist
        """
        full_path = self.repo_path / file_path
        if not full_path.exists() or not full_path.is_file():
            return None

        # Detect language
        try:
            lexer = lexers.get_lexer_for_filename(str(file_path))
            language = lexer.name
        except ClassNotFound:
            language = "unknown"

        # Check file size before reading (prevent DoS from huge files)
        try:
            file_size = full_path.stat().st_size
            max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
            if file_size > max_size_bytes:
                # Skip files larger than MAX_FILE_SIZE_MB
                return None
        except (OSError, PermissionError):
            return None

        # Read file
        try:
            content = full_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            return None

        lines_of_code = len([line for line in content.splitlines() if line.strip()])

        # Extract symbols (language-specific)
        symbols = self._extract_symbols(file_path, content, language)

        # Extract imports
        imports = self._extract_imports(content, language)

        # Extract dependencies from project files
        dependencies = self._parse_dependencies(self.repo_path, language)

        return FileContext(
            path=file_path,
            language=language,
            lines_of_code=lines_of_code,
            symbols=symbols,
            imports=imports,
            dependencies=dependencies,
        )

    def extract_context(self, paths: list[Path], commit: str | None = None) -> ExtractedContext:
        """Extract complete context for given paths.

        Args:
            paths: List of file/directory paths
            commit: Optional commit SHA

        Returns:
            ExtractedContext with all gathered information
        """
        # Get git diff if available
        diff = self.extract_diff(commit)

        # Expand paths to individual files
        all_files = self._expand_paths(paths)

        # Extract context for each file
        file_contexts = []
        for file_path in all_files:
            context = self.extract_file_context(file_path)
            if context:
                file_contexts.append(context)

        return ExtractedContext(diff=diff, files=file_contexts, scope_paths=paths)

    def _expand_paths(self, paths: list[Path]) -> list[Path]:
        """Expand paths to individual files.

        Args:
            paths: List of paths (files or directories with globs)

        Returns:
            List of individual file paths
        """
        expanded: list[Path] = []
        for path in paths:
            full_path = self.repo_path / path
            if full_path.is_file():
                expanded.append(path)
            elif full_path.is_dir():
                # Recursively find code files
                expanded.extend(self._find_code_files(path))
            elif "*" in str(path):
                # Handle globs
                expanded.extend(self._glob_files(path))
        return list(set(expanded))  # Deduplicate

    def _find_code_files(self, directory: Path) -> list[Path]:
        """Find code files in directory recursively.

        Args:
            directory: Directory to search

        Returns:
            List of code file paths
        """
        code_extensions = {
            ".py",
            ".ts",
            ".tsx",
            ".js",
            ".jsx",
            ".go",
            ".rs",
            ".java",
            ".c",
            ".cpp",
            ".h",
            ".hpp",
        }
        full_dir = self.repo_path / directory
        files = []
        for file_path in full_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix in code_extensions:
                rel_path = file_path.relative_to(self.repo_path)
                files.append(rel_path)
        return files

    def _glob_files(self, pattern: Path) -> list[Path]:
        """Expand glob pattern to files.

        Args:
            pattern: Glob pattern

        Returns:
            List of matching file paths
        """
        files = []
        for file_path in self.repo_path.glob(str(pattern)):
            if file_path.is_file():
                rel_path = file_path.relative_to(self.repo_path)
                files.append(rel_path)
        return files

    def _extract_symbols(self, file_path: Path, content: str, language: str) -> list[Symbol]:
        """Extract symbols from code.

        Args:
            file_path: File path
            content: File content
            language: Programming language

        Returns:
            List of symbols
        """
        # Simple regex-based extraction (MVP)
        # TODO: Use tree-sitter for proper AST parsing
        symbols: list[Symbol] = []

        if language in ("Python", "Python 3"):
            symbols.extend(self._extract_python_symbols(file_path, content))
        elif language in ("TypeScript", "JavaScript"):
            symbols.extend(self._extract_typescript_symbols(file_path, content))

        return symbols

    def _extract_python_symbols(self, file_path: Path, content: str) -> list[Symbol]:
        """Extract Python symbols using regex.

        Args:
            file_path: File path
            content: File content

        Returns:
            List of Python symbols
        """
        symbols: list[Symbol] = []
        lines = content.splitlines()

        # Functions
        for i, line in enumerate(lines, start=1):
            # def function_name(args):
            func_match = re.match(r"^\s*def\s+(\w+)\s*\((.*?)\)", line)
            if func_match:
                name = func_match.group(1)
                args = func_match.group(2)
                signature = f"def {name}({args})"

                # Look for docstring
                doc = None
                if i < len(lines) and '"""' in lines[i]:
                    doc_line = lines[i].strip().strip('"""')
                    doc = doc_line if doc_line else None

                symbols.append(
                    Symbol(
                        file=file_path,
                        kind=SymbolKind.FUNCTION,
                        name=name,
                        line=i,
                        signature=signature,
                        doc=doc,
                    )
                )

            # class ClassName:
            class_match = re.match(r"^\s*class\s+(\w+)", line)
            if class_match:
                name = class_match.group(1)
                # Extract methods (simplified)
                methods = self._extract_class_methods(lines[i:])

                symbols.append(
                    Symbol(
                        file=file_path,
                        kind=SymbolKind.CLASS,
                        name=name,
                        line=i,
                        methods=methods,
                    )
                )

        return symbols

    def _extract_typescript_symbols(self, file_path: Path, content: str) -> list[Symbol]:
        """Extract TypeScript/JavaScript symbols.

        Args:
            file_path: File path
            content: File content

        Returns:
            List of TypeScript symbols
        """
        symbols: list[Symbol] = []
        lines = content.splitlines()

        for i, line in enumerate(lines, start=1):
            # function functionName(...) or const functionName = (...) =>
            func_match = re.match(
                r"^\s*(?:export\s+)?(?:async\s+)?(?:function|const)\s+(\w+)", line
            )
            if func_match:
                name = func_match.group(1)
                symbols.append(
                    Symbol(
                        file=file_path,
                        kind=SymbolKind.FUNCTION,
                        name=name,
                        line=i,
                    )
                )

            # class ClassName or interface InterfaceName
            class_match = re.match(r"^\s*(?:export\s+)?(?:class|interface)\s+(\w+)", line)
            if class_match:
                name = class_match.group(1)
                kind = SymbolKind.CLASS if "class" in line else SymbolKind.INTERFACE
                symbols.append(
                    Symbol(
                        file=file_path,
                        kind=kind,
                        name=name,
                        line=i,
                    )
                )

        return symbols

    def _extract_class_methods(self, class_lines: list[str]) -> list[str]:
        """Extract method names from class definition.

        Args:
            class_lines: Lines starting from class definition

        Returns:
            List of method names
        """
        methods: list[str] = []
        for line in class_lines[:50]:  # Limit search depth
            method_match = re.match(r"^\s+def\s+(\w+)\s*\(", line)
            if method_match:
                methods.append(method_match.group(1))
        return methods

    def _extract_imports(self, content: str, language: str) -> list[str]:
        """Extract import statements.

        Args:
            content: File content
            language: Programming language

        Returns:
            List of imported modules
        """
        imports: list[str] = []

        if language in ("Python", "Python 3"):
            for match in re.finditer(r"^(?:from|import)\s+([\w.]+)", content, re.MULTILINE):
                imports.append(match.group(1))
        elif language in ("TypeScript", "JavaScript"):
            for match in re.finditer(r"^import\s+.*?from\s+['\"](.+?)['\"]", content, re.MULTILINE):
                imports.append(match.group(1))

        return list(set(imports))  # Deduplicate

    def _parse_dependencies(self, repo_root: Path, language: str) -> list[str]:
        """Parse project dependencies from package files.

        Args:
            repo_root: Repository root directory
            language: Programming language

        Returns:
            List of dependency strings
        """
        dependencies: list[str] = []

        if language in ("Python", "Python 3"):
            # Try requirements.txt
            deps = self._parse_requirements_txt(repo_root)
            if deps:
                dependencies.extend(deps)

            # Try pyproject.toml
            deps = self._parse_pyproject_toml(repo_root)
            if deps:
                dependencies.extend(deps)

        elif language in ("TypeScript", "JavaScript"):
            # Try package.json
            deps = self._parse_package_json(repo_root)
            if deps:
                dependencies.extend(deps)

        return list(set(dependencies))  # Deduplicate

    def _parse_requirements_txt(self, repo_root: Path) -> list[str]:
        """Parse dependencies from requirements.txt.

        Args:
            repo_root: Repository root directory

        Returns:
            List of dependency strings
        """
        req_file = repo_root / "requirements.txt"
        if not req_file.exists():
            return []

        try:
            content = req_file.read_text(encoding="utf-8")
            dependencies: list[str] = []

            for line in content.splitlines():
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue
                # Skip -e (editable) installs and other flags
                if line.startswith("-"):
                    continue
                dependencies.append(line)

            return dependencies
        except (OSError, UnicodeDecodeError):
            return []

    def _parse_pyproject_toml(self, repo_root: Path) -> list[str]:
        """Parse dependencies from pyproject.toml.

        Args:
            repo_root: Repository root directory

        Returns:
            List of dependency strings
        """
        toml_file = repo_root / "pyproject.toml"
        if not toml_file.exists():
            return []

        try:
            content = toml_file.read_bytes()
            data = tomllib.loads(content.decode("utf-8"))
            dependencies: list[str] = []

            # Check [project.dependencies] (PEP 621)
            if "project" in data and "dependencies" in data["project"]:
                deps = data["project"]["dependencies"]
                if isinstance(deps, list):
                    dependencies.extend(deps)

            # Check [tool.poetry.dependencies] (Poetry)
            if "tool" in data and "poetry" in data["tool"]:
                poetry = data["tool"]["poetry"]
                if "dependencies" in poetry:
                    deps = poetry["dependencies"]
                    if isinstance(deps, dict):
                        # Poetry uses dict format: {"package": "version"}
                        for pkg, version in deps.items():
                            if pkg != "python":  # Skip python version requirement
                                if isinstance(version, str):
                                    dependencies.append(f"{pkg}{version}" if version else pkg)
                                elif isinstance(version, dict):
                                    # Handle complex dependency specs
                                    dependencies.append(pkg)

            return dependencies
        except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
            return []

    def _parse_package_json(self, repo_root: Path) -> list[str]:
        """Parse dependencies from package.json.

        Args:
            repo_root: Repository root directory

        Returns:
            List of dependency strings
        """
        pkg_file = repo_root / "package.json"
        if not pkg_file.exists():
            return []

        try:
            content = pkg_file.read_text(encoding="utf-8")
            data = json.loads(content)
            dependencies: list[str] = []

            # Get regular dependencies
            if "dependencies" in data and isinstance(data["dependencies"], dict):
                for pkg, version in data["dependencies"].items():
                    dependencies.append(f"{pkg}@{version}")

            # Get dev dependencies
            if "devDependencies" in data and isinstance(data["devDependencies"], dict):
                for pkg, version in data["devDependencies"].items():
                    dependencies.append(f"{pkg}@{version}")

            return dependencies
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            return []
