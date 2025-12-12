"""
Setup-hooks command - Install git hooks for automatic memory updates.
"""

import subprocess
import sys
from pathlib import Path

import click

from memdocs import cli_output as out


def _is_git_repo() -> bool:
    """Check if current directory is a git repository."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def _get_git_hooks_dir() -> Path:
    """Get the .git/hooks directory."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            check=True,
        )
        git_dir = Path(result.stdout.strip())
        return git_dir / "hooks"
    except subprocess.CalledProcessError:
        return Path(".git/hooks")


def _create_pre_commit_hook(hooks_dir: Path) -> None:
    """Create pre-commit hook that reviews staged files."""
    hook_file = hooks_dir / "pre-commit"

    hook_content = """#!/bin/sh
# MemDocs pre-commit hook
# Reviews staged files before commit

echo "🧠 MemDocs: Reviewing staged files..."

# Get list of staged Python files
staged_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\\.(py|js|ts|go|rs|java|rb)$' || true)

if [ -z "$staged_files" ]; then
    echo "✓ No code files staged for commit"
    exit 0
fi

# Review only staged files
for file in $staged_files; do
    if [ -f "$file" ]; then
        memdocs review --path "$file" --on commit > /dev/null 2>&1 || {
            echo "⚠ Failed to review $file (non-blocking)"
        }
    fi
done

echo "✓ MemDocs review complete"
exit 0
"""

    hook_file.write_text(hook_content, encoding="utf-8")
    hook_file.chmod(0o755)
    out.success(f"Created pre-commit hook: [green]{hook_file}[/green]")


def _create_post_commit_hook(hooks_dir: Path) -> None:
    """Create post-commit hook that reviews changed files."""
    hook_file = hooks_dir / "post-commit"

    hook_content = """#!/bin/sh
# MemDocs post-commit hook
# Reviews files in the last commit

echo "🧠 MemDocs: Updating memory for commit..."

# Review files changed in HEAD
memdocs review --since HEAD~1 --on commit > /dev/null 2>&1 || {
    echo "⚠ MemDocs review failed (non-blocking)"
    exit 0
}

echo "✓ MemDocs memory updated"
exit 0
"""

    hook_file.write_text(hook_content, encoding="utf-8")
    hook_file.chmod(0o755)
    out.success(f"Created post-commit hook: [green]{hook_file}[/green]")


def _create_pre_push_hook(hooks_dir: Path) -> None:
    """Create pre-push hook that reviews all changes before push."""
    hook_file = hooks_dir / "pre-push"

    hook_content = """#!/bin/sh
# MemDocs pre-push hook
# Reviews all unpushed commits before push

echo "🧠 MemDocs: Reviewing unpushed changes..."

# Get remote branch being pushed to
remote="$1"
url="$2"

# Review all changed files since origin
memdocs review --changed > /dev/null 2>&1 || {
    echo "⚠ MemDocs review failed (non-blocking)"
    exit 0
}

echo "✓ MemDocs review complete"
exit 0
"""

    hook_file.write_text(hook_content, encoding="utf-8")
    hook_file.chmod(0o755)
    out.success(f"Created pre-push hook: [green]{hook_file}[/green]")


@click.command()
@click.option(
    "--pre-commit",
    is_flag=True,
    help="Install pre-commit hook (reviews staged files)",
)
@click.option(
    "--post-commit",
    is_flag=True,
    help="Install post-commit hook (reviews after commit)",
)
@click.option(
    "--pre-push",
    is_flag=True,
    help="Install pre-push hook (reviews before push)",
)
@click.option(
    "--all",
    "install_all",
    is_flag=True,
    help="Install all hooks",
)
@click.option(
    "--remove",
    is_flag=True,
    help="Remove MemDocs git hooks",
)
def setup_hooks(
    pre_commit: bool,
    post_commit: bool,
    pre_push: bool,
    install_all: bool,
    remove: bool,
) -> None:
    """Install git hooks for automatic memory updates.

    Git hooks automatically run memdocs review when you commit or push,
    keeping your memory up-to-date with zero manual effort.

    Hook types:
        pre-commit:  Reviews staged files before commit
        post-commit: Reviews files after successful commit
        pre-push:    Reviews all changes before push

    Examples:

        memdocs setup-hooks --all           # Install all hooks
        memdocs setup-hooks --post-commit   # Just post-commit
        memdocs setup-hooks --remove        # Remove hooks
    """
    try:
        out.print_header("MemDocs Git Hooks Setup")

        # Check if git repo
        if not _is_git_repo():
            out.error("Not a git repository")
            out.info("Initialize git: [cyan]git init[/cyan]")
            sys.exit(1)

        # Get hooks directory
        hooks_dir = _get_git_hooks_dir()
        hooks_dir.mkdir(parents=True, exist_ok=True)

        if remove:
            # Remove hooks
            out.step("Removing MemDocs git hooks")
            removed = []

            for hook_name in ["pre-commit", "post-commit", "pre-push"]:
                hook_file = hooks_dir / hook_name
                if hook_file.exists():
                    # Check if it's a MemDocs hook
                    content = hook_file.read_text(encoding="utf-8")
                    if "MemDocs" in content:
                        hook_file.unlink()
                        removed.append(hook_name)
                        out.success(f"Removed {hook_name} hook")

            if removed:
                out.console.print()
                out.panel(
                    f"Removed {len(removed)} hook(s): {', '.join(removed)}",
                    title="Hooks Removed",
                    style="green",
                )
            else:
                out.info("No MemDocs hooks found")
            return

        # Determine which hooks to install
        if not (pre_commit or post_commit or pre_push or install_all):
            out.error("No hooks selected")
            out.info("Use --all or specify individual hooks:")
            out.info("  --pre-commit, --post-commit, --pre-push")
            sys.exit(1)

        # Install hooks
        out.step("Installing git hooks")
        installed = []

        if install_all or post_commit:
            _create_post_commit_hook(hooks_dir)
            installed.append("post-commit")

        if install_all or pre_commit:
            _create_pre_commit_hook(hooks_dir)
            installed.append("pre-commit")

        if install_all or pre_push:
            _create_pre_push_hook(hooks_dir)
            installed.append("pre-push")

        # Show summary
        out.console.print()
        out.print_rule("Installation Complete", style="green")
        out.console.print()

        out.panel(
            f"""[bold green]✓ Installed {len(installed)} hook(s)[/bold green]

Hooks installed: {', '.join(installed)}

[bold]What happens now:[/bold]
{'• Pre-commit: Reviews staged files before commit' if 'pre-commit' in installed else ''}
{'• Post-commit: Updates memory after each commit' if 'post-commit' in installed else ''}
{'• Pre-push: Reviews all changes before push' if 'pre-push' in installed else ''}

[bold]Your memory stays automatically updated! 🎉[/bold]

[dim]Test it:[/dim] Make a change and commit it
[dim]Remove hooks:[/dim] [cyan]memdocs setup-hooks --remove[/cyan]""",
            title="Git Hooks Active",
            style="green",
        )

    except Exception as e:
        out.console.print()
        out.error(f"Hook setup failed: {e}")
        sys.exit(1)
