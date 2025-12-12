"""
Update-config command - Update MCP configuration without reinitializing.
"""

import sys
from pathlib import Path

import click

from memdocs import cli_output as out
from memdocs.cli_modules.commands.init_cmd import _setup_mcp_infrastructure


@click.command()
@click.option(
    "--mcp",
    is_flag=True,
    help="Update MCP integration (VS Code tasks/settings)",
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite existing configuration files",
)
def update_config(mcp: bool, force: bool) -> None:
    """Update MemDocs configuration files.

    Useful for updating VS Code tasks, settings, or MCP configuration
    when MemDocs templates have been improved or you want to refresh
    your setup without reinitializing.

    Examples:

        memdocs update-config --mcp         # Update MCP setup
        memdocs update-config --mcp --force # Overwrite existing
    """
    try:
        out.print_header("MemDocs Configuration Update")

        cwd = Path.cwd()

        # Check if MemDocs is initialized
        config_path = Path(".memdocs.yml")
        if not config_path.exists():
            out.error("MemDocs not initialized in this directory")
            out.info("Run: [cyan]memdocs init[/cyan]")
            sys.exit(1)

        if not mcp:
            out.warning("No update target specified")
            out.info("Use [cyan]--mcp[/cyan] to update MCP integration")
            out.info("Example: [cyan]memdocs update-config --mcp[/cyan]")
            sys.exit(1)

        # Update MCP configuration
        if mcp:
            vscode_dir = cwd / ".vscode"
            tasks_file = vscode_dir / "tasks.json"
            settings_file = vscode_dir / "settings.json"

            # Check if files exist and warn if not forcing
            if not force:
                if tasks_file.exists() or settings_file.exists():
                    out.warning("MCP configuration files already exist")
                    out.info("Use [cyan]--force[/cyan] to overwrite")
                    out.console.print()

                    if tasks_file.exists():
                        out.info(f"Existing: [cyan]{tasks_file}[/cyan]")
                    if settings_file.exists():
                        out.info(f"Existing: [cyan]{settings_file}[/cyan]")

                    try:
                        response = click.confirm("Overwrite existing files?", default=False)
                        if not response:
                            out.info("Update cancelled")
                            sys.exit(0)
                    except click.Abort:
                        out.info("Update cancelled")
                        sys.exit(0)

            # Update MCP infrastructure
            out.console.print()
            _setup_mcp_infrastructure(cwd)

            # Show success message
            out.console.print()
            out.print_rule("Update Complete", style="green")
            out.console.print()

            out.panel(
                """[bold green]✓ MCP configuration updated![/bold green]

Your VS Code/Cursor setup has been refreshed with the latest
MemDocs MCP integration templates.

[bold]What's updated:[/bold]
• .vscode/tasks.json - MCP server auto-start task
• .vscode/settings.json - Auto-task execution settings

[bold]Next steps:[/bold]
• Reload VS Code/Cursor: [cyan]Cmd+Shift+P → "Reload Window"[/cyan]
• Verify setup: [cyan]memdocs doctor[/cyan]
• Start server: [cyan]memdocs serve --mcp[/cyan]""",
                title="All Set!",
                style="green",
            )

    except Exception as e:
        out.console.print()
        out.error(f"Configuration update failed: {e}")
        sys.exit(1)
