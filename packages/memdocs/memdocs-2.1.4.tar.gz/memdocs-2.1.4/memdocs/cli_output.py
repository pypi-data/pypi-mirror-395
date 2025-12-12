"""Rich terminal output formatting for CLI."""

from contextlib import contextmanager
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table
from rich.tree import Tree

# Global console instance
console = Console()


# Status messages with colors
def success(message: str) -> None:
    """Print a success message in green."""
    console.print(f"[bold green]✓[/bold green] {message}")


def error(message: str) -> None:
    """Print an error message in red."""
    console.print(f"[bold red]✗[/bold red] {message}", style="red")


def warning(message: str) -> None:
    """Print a warning message in yellow."""
    console.print(f"[bold yellow]⚠[/bold yellow] {message}", style="yellow")


def info(message: str) -> None:
    """Print an info message in blue."""
    console.print(f"[bold blue]ℹ[/bold blue] {message}")


def step(message: str) -> None:
    """Print a step message in cyan."""
    console.print(f"[bold cyan]→[/bold cyan] {message}")


# Panels for structured output
def panel(
    content: str,
    title: str | None = None,
    style: str = "blue",
    subtitle: str | None = None,
) -> None:
    """Print content in a bordered panel.

    Args:
        content: Panel content
        title: Optional panel title
        style: Panel border style (blue, green, red, yellow)
        subtitle: Optional subtitle
    """
    console.print(
        Panel(
            content,
            title=title,
            subtitle=subtitle,
            border_style=style,
            expand=False,
        )
    )


# Progress bars
@contextmanager
def progress_bar(description: str = "Processing..."):
    """Context manager for progress bars.

    Usage:
        with progress_bar("Extracting files") as progress:
            task = progress.add_task("Extracting...", total=100)
            for i in range(100):
                progress.update(task, advance=1)
    """
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        console=console,
    )
    with progress:
        yield progress


@contextmanager
def spinner(description: str = "Working..."):
    """Context manager for spinners (for indeterminate operations).

    Usage:
        with spinner("Generating documentation"):
            # do work
            pass
    """
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        TimeElapsedColumn(),
        console=console,
    )
    with progress:
        task = progress.add_task(description, total=None)
        yield progress, task


# Tables
def create_table(
    title: str | None = None,
    show_header: bool = True,
    show_lines: bool = False,
) -> Table:
    """Create a rich table.

    Args:
        title: Optional table title
        show_header: Whether to show column headers
        show_lines: Whether to show lines between rows

    Returns:
        Table instance to add columns and rows to
    """
    return Table(
        title=title,
        show_header=show_header,
        show_lines=show_lines,
        header_style="bold cyan",
        border_style="blue",
    )


def print_table(table: Table) -> None:
    """Print a table to the console."""
    console.print(table)


# File trees
def create_file_tree(root_path: Path, files: list[Path], title: str = "Files") -> Tree:
    """Create a file tree visualization.

    Args:
        root_path: Root directory path
        files: List of file paths relative to root
        title: Tree title

    Returns:
        Tree instance
    """
    tree = Tree(f"[bold blue]{title}")

    # Group files by directory
    dirs: dict[str, list[Path]] = {}
    for file_path in sorted(files):
        dir_path = file_path.parent
        dir_key = str(dir_path) if dir_path != Path(".") else "."

        if dir_key not in dirs:
            dirs[dir_key] = []
        dirs[dir_key].append(file_path)

    # Build tree
    for dir_key_str, dir_files in sorted(dirs.items()):
        if dir_key_str == ".":
            # Root level files
            for f in dir_files:
                tree.add(f"[green]{f.name}")
        else:
            # Directory with files
            dir_node = tree.add(f"[blue]{dir_key_str}/")
            for f in dir_files:
                dir_node.add(f"[green]{f.name}")

    return tree


def print_tree(tree: Tree) -> None:
    """Print a tree to the console."""
    console.print(tree)


# Key-value display
def print_key_value(key: str, value: Any, key_style: str = "cyan") -> None:
    """Print a key-value pair.

    Args:
        key: Key name
        value: Value to display
        key_style: Color style for key
    """
    console.print(f"[{key_style}]{key}:[/{key_style}] {value}")


def print_dict(data: dict[str, Any], title: str | None = None) -> None:
    """Print a dictionary as key-value pairs.

    Args:
        data: Dictionary to print
        title: Optional title
    """
    if title:
        console.print(f"\n[bold]{title}[/bold]")

    for key, value in data.items():
        print_key_value(key, value)


# Summary output
def print_summary(
    title: str,
    items: dict[str, Any],
    style: str = "green",
) -> None:
    """Print a summary panel with key-value pairs.

    Args:
        title: Summary title
        items: Dictionary of items to display
        style: Panel border style
    """
    content_lines = []
    for key, value in items.items():
        content_lines.append(f"[cyan]{key}:[/cyan] {value}")

    panel(
        "\n".join(content_lines),
        title=title,
        style=style,
    )


# Duration formatting
def format_duration(duration_ms: float) -> str:
    """Format duration in milliseconds to human-readable string.

    Args:
        duration_ms: Duration in milliseconds

    Returns:
        Formatted duration string
    """
    if duration_ms < 1000:
        return f"{duration_ms:.0f}ms"
    elif duration_ms < 60000:
        return f"{duration_ms / 1000:.1f}s"
    else:
        minutes = int(duration_ms / 60000)
        seconds = (duration_ms % 60000) / 1000
        return f"{minutes}m {seconds:.0f}s"


# File size formatting
def format_size(size_bytes: int) -> str:
    """Format file size in bytes to human-readable string.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string
    """
    size_float = float(size_bytes)
    for unit in ["B", "KB", "MB", "GB"]:
        if size_float < 1024.0:
            return f"{size_float:.1f} {unit}"
        size_float /= 1024.0
    return f"{size_float:.1f} TB"


# Header
def print_header(text: str) -> None:
    """Print a styled header.

    Args:
        text: Header text
    """
    console.print(f"\n[bold blue]{'=' * 60}[/bold blue]")
    console.print(f"[bold white]{text.center(60)}[/bold white]")
    console.print(f"[bold blue]{'=' * 60}[/bold blue]\n")


# Rule (separator line)
def print_rule(title: str | None = None, style: str = "blue") -> None:
    """Print a horizontal rule (separator).

    Args:
        title: Optional title text
        style: Line color style
    """
    from rich.rule import Rule

    console.print(Rule(title=title or "", style=style))
