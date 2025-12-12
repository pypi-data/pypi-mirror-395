"""
Command-line interface for doc-intelligence.
"""

import click
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from memdocs import __version__  # noqa: E402

# Import commands from modular structure
from memdocs.cli_modules.commands import (  # noqa: E402
    cleanup,
    doctor,
    export,
    init,
    query,
    review,
    serve,
    setup_hooks,
    stats,
    update_config,
)

# Import classes that tests need to patch (for backward compatibility)
from memdocs.extract import Extractor  # noqa: E402
from memdocs.index import MemoryIndexer  # noqa: E402
from memdocs.policy import PolicyEngine  # noqa: E402
from memdocs.summarize import Summarizer  # noqa: E402

# Re-export for backward compatibility with tests
__all__ = [
    "cleanup",
    "doctor",
    "export",
    "Extractor",
    "init",
    "main",
    "MemoryIndexer",
    "PolicyEngine",
    "query",
    "review",
    "serve",
    "setup_hooks",
    "stats",
    "Summarizer",
    "update_config",
]


@click.group()
@click.version_option(version=__version__)
@click.pass_context
def main(ctx: click.Context) -> None:
    """MemDocs: Persistent memory management for AI projects."""
    ctx.ensure_object(dict)


# Register commands
main.add_command(init)
main.add_command(review)
main.add_command(export)
main.add_command(query)
main.add_command(serve)
main.add_command(doctor)
main.add_command(setup_hooks)
main.add_command(stats)
main.add_command(update_config)
main.add_command(cleanup)


if __name__ == "__main__":
    main()
