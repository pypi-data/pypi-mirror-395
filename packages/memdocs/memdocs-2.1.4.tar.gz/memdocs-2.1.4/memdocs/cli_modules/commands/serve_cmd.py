"""
Serve command - Start MCP server for AI assistant integration.
"""

import json
import os
import signal
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import click

from memdocs import cli_output as out


class MemDocsHTTPHandler(BaseHTTPRequestHandler):
    """HTTP handler for MemDocs MCP server."""

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        """Override to use our logger."""
        if self.server.verbose:  # type: ignore
            out.info(f"{self.address_string()} - {format % args}")

    def do_GET(self) -> None:
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Health check endpoint
        if path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
            return

        # Stats endpoint
        elif path == "/stats":
            try:
                stats = self._get_stats()
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(stats).encode())
            except Exception as e:
                self._send_error(500, str(e))
            return

        # Default response
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            b"""
            <html>
            <head><title>MemDocs MCP Server</title></head>
            <body>
            <h1>MemDocs MCP Server</h1>
            <p>Server is running.</p>
            <ul>
                <li><a href="/health">Health Check</a></li>
                <li><a href="/stats">Statistics</a></li>
            </ul>
            </body>
            </html>
            """
        )

    def do_POST(self) -> None:
        """Handle POST requests for MCP tools."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Read request body
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode() if content_length > 0 else "{}"

        try:
            request_data = json.loads(body)
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON")
            return

        # Search endpoint
        if path == "/search":
            try:
                query = request_data.get("query", "")
                k = request_data.get("k", 5)
                results = self._search_memory(query, k)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(results).encode())
            except Exception as e:
                self._send_error(500, str(e))
            return

        # Unknown endpoint
        self._send_error(404, "Not found")

    def _send_error(self, code: int, message: str) -> None:
        """Send error response."""
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode())

    def _get_stats(self) -> dict[str, Any]:
        """Get memory statistics."""
        docs_dir = self.server.docs_dir  # type: ignore
        memory_dir = self.server.memory_dir  # type: ignore

        stats: dict[str, Any] = {
            "docs_dir": str(docs_dir),
            "memory_dir": str(memory_dir),
            "status": "ok",
        }

        # Count files
        if docs_dir.exists():
            json_files = list(docs_dir.glob("**/*.json"))
            stats["documented_files"] = len(json_files)

        # Check embeddings
        if memory_dir.exists():
            faiss_index = memory_dir / "faiss.index"
            stats["embeddings_available"] = faiss_index.exists()

        return stats

    def _search_memory(self, query: str, k: int = 5) -> dict[str, Any]:
        """Search memory (placeholder for now)."""
        return {
            "query": query,
            "results": [],
            "message": "Search functionality requires embeddings. Run 'memdocs review' first.",
        }


@click.command()
@click.option(
    "--host",
    default="localhost",
    help="Host to bind to",
)
@click.option(
    "--port",
    default=8765,
    type=int,
    help="Port to listen on",
)
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
    "--daemon",
    is_flag=True,
    help="Run in background (daemon mode)",
)
@click.option(
    "--mcp",
    "use_mcp",
    is_flag=True,
    help="Enable MCP protocol mode",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Verbose output",
)
def serve(
    host: str,
    port: int,
    docs_dir: Path,
    memory_dir: Path,
    daemon: bool,
    use_mcp: bool,
    verbose: bool,
) -> None:
    """Start MCP server for AI assistant integration.

    The MCP server serves project memory to AI assistants like Claude Desktop,
    Cursor, and Continue.dev.

    Examples:

        # Start server (foreground)
        memdocs serve --mcp

        # Start on custom port
        memdocs serve --mcp --port 9000

        # Run in background
        memdocs serve --mcp --daemon

        # Verbose logging
        memdocs serve --mcp --verbose
    """
    # Check if memory exists
    if not docs_dir.exists() and not memory_dir.exists():
        out.warning("No MemDocs memory found. Run 'memdocs review' first to generate memory.")
        out.info("Starting server anyway for testing...")

    # Daemon mode
    if daemon:
        out.info(f"Starting MCP server in daemon mode on {host}:{port}...")
        # Fork to background (Unix only)
        if os.name != "nt":
            try:
                pid = os.fork()
                if pid > 0:
                    # Parent process
                    out.success(f"MCP server started with PID: {pid}")
                    return
            except OSError as e:
                out.error(f"Fork failed: {e}")
                sys.exit(1)
        else:
            out.warning("Daemon mode not supported on Windows. Running in foreground.")

    # Create server
    server = HTTPServer((host, port), MemDocsHTTPHandler)
    server.docs_dir = docs_dir  # type: ignore
    server.memory_dir = memory_dir  # type: ignore
    server.verbose = verbose  # type: ignore

    # Handle graceful shutdown
    def signal_handler(sig: int, frame: Any) -> None:
        out.info("\nShutting down MCP server...")
        server.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    if not daemon:
        out.success(f"MCP server started on http://{host}:{port}")
        out.info("Press Ctrl+C to stop")
        out.info("")
        out.info("Available endpoints:")
        out.info(f"  Health: http://{host}:{port}/health")
        out.info(f"  Stats:  http://{host}:{port}/stats")
        out.info("")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        out.info("\nServer stopped")
