"""
Doctor command - Health check for MemDocs setup.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import click
import requests

from memdocs import cli_output as out


def _check_item(label: str, check_fn: callable, fix_hint: str = "") -> bool:
    """Run a single health check and display result."""
    try:
        result = check_fn()
        if result:
            out.success(f"{label}")
            return True
        else:
            out.warning(f"{label}")
            if fix_hint:
                out.info(f"  → {fix_hint}")
            return False
    except Exception as e:
        out.error(f"{label}")
        out.info(f"  → Error: {e}")
        if fix_hint:
            out.info(f"  → {fix_hint}")
        return False


def _check_memdocs_initialized() -> bool:
    """Check if .memdocs.yml exists."""
    return Path(".memdocs.yml").exists()


def _check_docs_exist() -> bool:
    """Check if documentation has been generated."""
    docs_dir = Path(".memdocs/docs")
    if not docs_dir.exists():
        return False
    json_files = list(docs_dir.glob("**/*.json"))
    return len(json_files) > 0


def _check_memory_exists() -> bool:
    """Check if memory/embeddings have been generated."""
    memory_dir = Path(".memdocs/memory")
    if not memory_dir.exists():
        return False
    faiss_index = memory_dir / "faiss.index"
    return faiss_index.exists()


def _check_api_key() -> bool:
    """Check if ANTHROPIC_API_KEY is set."""
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def _check_vscode_tasks() -> bool:
    """Check if VS Code tasks.json exists."""
    return Path(".vscode/tasks.json").exists()


def _check_vscode_settings() -> bool:
    """Check if VS Code settings.json exists and has auto-task enabled."""
    settings_file = Path(".vscode/settings.json")
    if not settings_file.exists():
        return False

    try:
        settings = json.loads(settings_file.read_text(encoding="utf-8"))
        return settings.get("task.allowAutomaticTasks") == "on"
    except (json.JSONDecodeError, Exception):
        return False


def _check_mcp_server_responsive() -> bool:
    """Check if MCP server is running and responsive."""
    try:
        response = requests.get("http://localhost:8765/health", timeout=2)
        return response.status_code == 200 and response.json().get("status") == "ok"
    except Exception:
        return False


def _check_memdocs_command() -> bool:
    """Check if memdocs command is accessible."""
    try:
        result = subprocess.run(
            ["memdocs", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except Exception:
        return False


def _get_stats() -> dict[str, Any]:
    """Get memory statistics if available."""
    stats: dict[str, Any] = {}

    docs_dir = Path(".memdocs/docs")
    if docs_dir.exists():
        json_files = list(docs_dir.glob("**/*.json"))
        stats["documented_files"] = len(json_files)
    else:
        stats["documented_files"] = 0

    memory_dir = Path(".memdocs/memory")
    if memory_dir.exists():
        faiss_index = memory_dir / "faiss.index"
        stats["embeddings_available"] = faiss_index.exists()
    else:
        stats["embeddings_available"] = False

    return stats


@click.command()
@click.option(
    "--fix",
    is_flag=True,
    help="Attempt to fix common issues",
)
def doctor(fix: bool) -> None:
    """Health check for MemDocs setup.

    Verifies that MemDocs is properly configured and all components
    are working correctly.

    Examples:

        memdocs doctor
        memdocs doctor --fix
    """
    out.print_header("MemDocs Health Check")

    checks_passed = 0
    checks_total = 0

    # Core checks
    out.console.print("\n[bold]Core Setup[/bold]")
    checks_total += 1
    if _check_item(
        "✓ MemDocs initialized",
        _check_memdocs_initialized,
        "Run: memdocs init",
    ):
        checks_passed += 1

    checks_total += 1
    if _check_item(
        "✓ Documentation generated",
        _check_docs_exist,
        "Run: memdocs review --path src/",
    ):
        checks_passed += 1

    checks_total += 1
    if _check_item(
        "✓ Memory/embeddings available",
        _check_memory_exists,
        "Run: memdocs review --path src/",
    ):
        checks_passed += 1

    # API configuration
    out.console.print("\n[bold]API Configuration[/bold]")
    checks_total += 1
    if _check_item(
        "✓ ANTHROPIC_API_KEY set",
        _check_api_key,
        'Set: export ANTHROPIC_API_KEY="your-key"',
    ):
        checks_passed += 1

    # MCP setup
    out.console.print("\n[bold]MCP Integration[/bold]")
    checks_total += 1
    if _check_item(
        "✓ VS Code tasks.json exists",
        _check_vscode_tasks,
        "Run: memdocs init --force",
    ):
        checks_passed += 1

    checks_total += 1
    if _check_item(
        "✓ VS Code auto-tasks enabled",
        _check_vscode_settings,
        "Run: memdocs init --force",
    ):
        checks_passed += 1

    checks_total += 1
    if _check_item(
        "✓ MCP server responsive",
        _check_mcp_server_responsive,
        "Start: memdocs serve --mcp",
    ):
        checks_passed += 1

    # Statistics
    out.console.print("\n[bold]Statistics[/bold]")
    stats = _get_stats()
    out.info(f"Documented files: {stats['documented_files']}")
    out.info(f"Embeddings available: {stats['embeddings_available']}")

    # Summary
    out.console.print()
    out.print_rule("Summary", style="blue")

    if checks_passed == checks_total:
        out.console.print(
            f"\n[bold green]✓ All checks passed![/bold green] ({checks_passed}/{checks_total})\n"
        )
        out.panel(
            """Your MemDocs setup is working perfectly! 🎉

[bold]What's working:[/bold]
• Configuration is valid
• Memory is generated and accessible
• MCP server is running
• VS Code integration is configured

[bold]Ready to use:[/bold]
• Query memory: [cyan]memdocs query "your question"[/cyan]
• Update docs: [cyan]memdocs review --path src/[/cyan]
• View stats: [cyan]memdocs stats[/cyan]""",
            title="All Systems Go!",
            style="green",
        )
        sys.exit(0)
    else:
        out.console.print(
            f"\n[bold yellow]⚠ Some checks failed[/bold yellow] ({checks_passed}/{checks_total} passed)\n"
        )

        if fix:
            out.info("Attempting to fix common issues...")
            # Add auto-fix logic here in the future
            out.warning("Auto-fix not yet implemented")

        out.panel(
            """[bold]Common fixes:[/bold]

• Not initialized?
  [cyan]memdocs init[/cyan]

• No documentation?
  [cyan]memdocs review --path src/[/cyan]

• API key missing?
  [cyan]export ANTHROPIC_API_KEY="your-key"[/cyan]

• MCP not working?
  [cyan]memdocs serve --mcp[/cyan]
  Then check: [cyan]curl http://localhost:8765/health[/cyan]

• VS Code setup?
  [cyan]memdocs init --force[/cyan]""",
            title="Fix Suggestions",
            style="yellow",
        )
        sys.exit(1)
