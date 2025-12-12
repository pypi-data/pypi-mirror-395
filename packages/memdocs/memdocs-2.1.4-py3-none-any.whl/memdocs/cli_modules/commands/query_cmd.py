"""
Query command - Query project memory using natural language.
"""

import sys
from pathlib import Path

import click

from memdocs import cli_output as out


def _get_memory_indexer():
    """Lazy import to avoid circular dependency."""
    from memdocs import cli

    return cli.MemoryIndexer


@click.command()
@click.argument("query", type=str)
@click.option(
    "--k",
    type=int,
    default=5,
    help="Number of results to return",
)
@click.option(
    "--memory-dir",
    type=click.Path(path_type=Path),
    default=Path(".memdocs/memory"),
    help="Memory directory",
)
def query(query: str, k: int, memory_dir: Path) -> None:
    """Query project memory using natural language.

    Examples:

        memdocs query "How does authentication work?"
        memdocs query "payment timeout implementation" --k 10
    """
    try:
        # Initialize indexer
        out.print_header("MemDocs Query")
        out.step(f'Searching for: [cyan]"{query}"[/cyan]')

        memory_indexer_class = _get_memory_indexer()
        indexer = memory_indexer_class(memory_dir=memory_dir, use_embeddings=True)

        if not indexer.use_embeddings:
            out.error("Embeddings not available")
            out.info("Install with: [cyan]pip install 'memdocs[embeddings]'[/cyan]")
            sys.exit(1)

        # Check if index exists
        stats = indexer.get_stats()
        if stats["total"] == 0:
            out.warning("Memory index is empty")
            out.info("Run [cyan]memdocs review[/cyan] first to generate docs")
            sys.exit(1)

        out.info(f"Index contains {stats['active']} active entries")

        # Query memory
        with out.spinner("Searching memory"):
            results = indexer.query_memory(query, k=k)

        if not results:
            out.warning("No results found")
            return

        # Display results in table
        out.print_rule(f"Found {len(results)} Results", style="green")
        out.console.print()

        table = out.create_table(title="Search Results", show_lines=True)
        table.add_column("#", style="dim", width=3)
        table.add_column("Score", style="cyan", width=8)
        table.add_column("Features", style="green")
        table.add_column("Files", style="blue")

        for i, result in enumerate(results, 1):
            meta = result["metadata"]
            score = result["score"]
            features = ", ".join(meta.get("features", ["Untitled"]))[:50]
            files = ", ".join(meta.get("file_paths", []))[:60]

            table.add_row(str(i), f"{score:.3f}", features, files)

        out.print_table(table)

        # Show preview of top result
        if results:
            out.console.print()
            top_result = results[0]
            preview = top_result["metadata"].get("chunk_text", "No preview")[:200]
            out.panel(preview, title="Top Result Preview", style="green")

    except Exception as e:
        out.console.print()
        out.error(f"Query failed: {e}")
        sys.exit(1)
