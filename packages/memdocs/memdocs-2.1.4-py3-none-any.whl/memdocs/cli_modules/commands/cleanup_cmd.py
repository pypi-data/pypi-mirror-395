"""
Cleanup command - Cleanup old embeddings and memory data.
"""

from pathlib import Path

import click

from memdocs import cli_output as out


@click.command()
@click.option(
    "--older-than",
    type=str,
    default="90d",
    help="Cleanup items older than (e.g., 90d, 1y)",
)
@click.option(
    "--memory-dir",
    type=click.Path(exists=True, path_type=Path),
    default=Path(".memdocs/memory"),
    help="Memory directory",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be deleted without deleting",
)
def cleanup(older_than: str, memory_dir: Path, dry_run: bool) -> None:
    """Cleanup old embeddings and memory data.

    Examples:

        memdocs cleanup --older-than 90d
        memdocs cleanup --older-than 1y --dry-run
    """
    out.warning("Cleanup not yet implemented (v2.1 feature)")
    out.info(f"Would delete items older than: {older_than}")
