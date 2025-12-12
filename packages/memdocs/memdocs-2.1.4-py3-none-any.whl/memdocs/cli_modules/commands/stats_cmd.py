"""
Stats command - Show memory and documentation statistics.
"""

import sys
from pathlib import Path
from typing import Any

import click

from memdocs import cli_output as out


def _get_memory_indexer():
    """Lazy import to avoid circular dependency."""
    from memdocs import cli

    return cli.MemoryIndexer


@click.command()
@click.option(
    "--docs-dir",
    type=click.Path(path_type=Path),
    default=Path(".memdocs/docs"),
    help="Documentation directory",
)
@click.option(
    "--memory-dir",
    type=click.Path(path_type=Path),
    default=Path(".memdocs/memory"),
    help="Memory directory",
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["table", "json"]),
    default="table",
    help="Output format",
)
def stats(docs_dir: Path, memory_dir: Path, output_format: str) -> None:
    """Show memory and documentation statistics.

    Examples:

        memdocs stats
        memdocs stats --format json
    """
    try:
        out.print_header("MemDocs Statistics")

        # Docs stats
        docs_stats: dict[str, Any] = {
            "exists": docs_dir.exists(),
            "total_files": 0,
            "formats": [],
        }

        if docs_dir.exists():
            docs_stats["total_files"] = len(list(docs_dir.rglob("*")))
            if (docs_dir / "index.json").exists():
                docs_stats["formats"].append("json")
            if (docs_dir / "summary.md").exists():
                docs_stats["formats"].append("markdown")
            if (docs_dir / "symbols.yaml").exists():
                docs_stats["formats"].append("yaml")

        # Memory stats
        memory_stats = {
            "exists": memory_dir.exists(),
            "embeddings": False,
            "graph": False,
        }

        if memory_dir.exists():
            memory_stats["embeddings"] = (memory_dir / "embeddings.json").exists()
            memory_stats["graph"] = (memory_dir / "graph.json").exists()

        # Embedding index stats
        index_stats = None
        try:
            memory_indexer_class = _get_memory_indexer()
            indexer = memory_indexer_class(memory_dir=memory_dir, use_embeddings=True)
            if indexer.use_embeddings:
                index_stats = indexer.get_stats()
        except Exception:
            pass

        if output_format == "json":
            # JSON output
            output = {
                "docs": docs_stats,
                "memory": memory_stats,
                "index": index_stats,
            }
            out.console.print_json(data=output)
        else:
            # Table output
            out.console.print()

            # Documentation table
            docs_table = out.create_table(title="Documentation", show_lines=True)
            docs_table.add_column("Property", style="cyan")
            docs_table.add_column("Value", style="green")

            docs_table.add_row("Directory", str(docs_dir))
            docs_table.add_row("Exists", "✓" if docs_stats["exists"] else "✗")
            docs_table.add_row("Total Files", str(docs_stats["total_files"]))
            docs_table.add_row("Formats", ", ".join(docs_stats["formats"]) or "None")

            out.print_table(docs_table)
            out.console.print()

            # Memory table
            memory_table = out.create_table(title="Memory", show_lines=True)
            memory_table.add_column("Property", style="cyan")
            memory_table.add_column("Value", style="green")

            memory_table.add_row("Directory", str(memory_dir))
            memory_table.add_row("Exists", "✓" if memory_stats["exists"] else "✗")
            memory_table.add_row("Embeddings", "✓" if memory_stats["embeddings"] else "✗")
            memory_table.add_row("Graph", "✓" if memory_stats["graph"] else "✗")

            out.print_table(memory_table)

            # Index stats
            if index_stats:
                out.console.print()
                index_table = out.create_table(title="Embedding Index", show_lines=True)
                index_table.add_column("Property", style="cyan")
                index_table.add_column("Value", style="green")

                index_table.add_row("Total Entries", str(index_stats.get("total", 0)))
                index_table.add_row("Active Entries", str(index_stats.get("active", 0)))
                index_table.add_row("Dimensions", str(index_stats.get("dimensions", 0)))

                out.print_table(index_table)

    except Exception as e:
        out.console.print()
        out.error(f"Stats failed: {e}")
        sys.exit(1)
