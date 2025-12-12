"""
MCP (Model Context Protocol) server for Claude Desktop integration.

Enables Claude Desktop to query project memory stored in .memdocs/
via semantic search, symbol lookup, and documentation retrieval.

This is MemDocs' flagship feature - allowing AI assistants to autonomously
query git-committed memory without file system access.
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, cast

import yaml
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from memdocs.embeddings import LocalEmbedder
from memdocs.search import LocalVectorSearch
from memdocs.security import PathValidator


class DocIntMCPServer:
    """MCP server exposing .memdocs/ memory to Claude Desktop.

    Claude Desktop can call these tools to:
    - Search project memory semantically
    - Get code symbols
    - Retrieve documentation
    """

    def __init__(self, repo_path: Path = Path(".")):
        """Initialize MCP server.

        Args:
            repo_path: Path to repository containing .memdocs/
        """
        self.repo_path = repo_path
        self.docs_dir = repo_path / ".memdocs" / "docs"
        self.memory_dir = repo_path / ".memdocs" / "memory"

        # Initialize search (if available)
        try:
            self.embedder = LocalEmbedder()
            # LocalEmbedder.dimension is set after model loads, guaranteed to be int
            dimension_value = self.embedder.dimension if self.embedder.dimension else 384
            self.search = LocalVectorSearch(
                index_path=self.memory_dir / "faiss.index",
                metadata_path=self.memory_dir / "faiss_metadata.json",
                dimension=dimension_value,
            )
            self.search_enabled = True
        except (ImportError, FileNotFoundError):
            self.search_enabled = False

    def search_memory(self, query: str, k: int = 5) -> list[dict[str, Any]]:
        """Search project memory using natural language.

        Args:
            query: Natural language query
            k: Number of results to return

        Returns:
            List of matching documents with scores
        """
        if not self.search_enabled:
            return [{"error": "Search not available. Run 'memdocs review' first."}]

        # Generate query embedding
        query_embedding = self.embedder.embed_query(query)

        # Search
        results = self.search.search(query_embedding, k=k)

        # Format for Claude
        formatted = []
        for result in results:
            meta = result["metadata"]
            formatted.append(
                {
                    "score": result["score"],
                    "features": meta.get("features", []),
                    "files": meta.get("file_paths", []),
                    "preview": meta.get("chunk_text", ""),
                    "doc_id": meta.get("doc_id", "unknown"),
                }
            )

        return formatted

    def get_symbols(self, file_path: str | None = None) -> dict[str, Any]:
        """Get code symbols from memory.

        Args:
            file_path: Optional filter to specific file

        Returns:
            Dictionary of symbols
        """
        symbols_file = self.docs_dir / "symbols.yaml"
        if not symbols_file.exists():
            return {"error": "No symbols found. Run 'memdocs review' first."}

        with open(symbols_file, encoding="utf-8") as f:
            symbols = cast(dict[str, Any], yaml.safe_load(f))

        if file_path:
            # Filter to specific file
            return {
                "symbols": [
                    s for s in symbols.get("symbols", []) if str(s.get("file")) == file_path
                ]
            }

        return symbols

    def get_documentation(self, doc_id: str | None = None) -> dict[str, Any]:
        """Get generated documentation.

        Args:
            doc_id: Optional doc ID (commit SHA)

        Returns:
            Documentation content
        """
        if doc_id:
            # Get specific doc
            doc_file = self.docs_dir / f"{doc_id}.json"
            if not doc_file.exists():
                return {"error": f"Document not found: {doc_id}"}

            with open(doc_file, encoding="utf-8") as f:
                return cast(dict[str, Any], json.load(f))
        else:
            # Get latest (index.json)
            index_file = self.docs_dir / "index.json"
            if not index_file.exists():
                return {"error": "No documentation found. Run 'memdocs review' first."}

            with open(index_file, encoding="utf-8") as f:
                return cast(dict[str, Any], json.load(f))

    def get_summary(self) -> str:
        """Get human-readable summary.

        Returns:
            Markdown summary
        """
        summary_file = self.docs_dir / "summary.md"
        if not summary_file.exists():
            return "No summary found. Run 'memdocs review' first."

        return summary_file.read_text(encoding="utf-8")

    def query_analysis(
        self,
        file_path: str | None = None,
        query_type: str = "all",
    ) -> dict[str, Any]:
        """Query Empathy Framework analysis results stored in DocInt.

        This tool allows Claude to retrieve specific Empathy analysis data:
        - "issues": Current code issues (rules, patterns, AI insights)
        - "patterns": Pattern-based analysis results
        - "predictions": Level 4 Anticipatory predictions
        - "empathy": Full Empathy Framework analysis
        - "all": Everything (default)

        Args:
            file_path: Optional path to specific file (e.g., "src/auth/login.py")
            query_type: Type of analysis to retrieve

        Returns:
            Dictionary with analysis results
        """
        # Validate query type
        valid_types = ["issues", "patterns", "predictions", "empathy", "all"]
        if query_type not in valid_types:
            return {
                "error": f"Invalid query_type: {query_type}. Must be one of: {', '.join(valid_types)}"
            }

        results = {}

        if file_path:
            # Query specific file
            file_name = Path(file_path).stem
            file_dir = self.docs_dir / file_name

            if not file_dir.exists():
                return {
                    "error": f"No analysis found for file: {file_path}. Run Empathy analysis first.",
                    "hint": "Use EmpathyService.run_wizard() and empathy_adapter.store_empathy_analysis()",
                }

            # Load index.json
            index_file = file_dir / "index.json"
            if index_file.exists():
                with open(index_file, encoding="utf-8") as f:
                    index_data = json.load(f)

                # Extract requested data
                if query_type in ["issues", "all"]:
                    results["issues"] = index_data.get("features", [])
                    results["impacts"] = index_data.get("impacts", {})

                if query_type in ["predictions", "empathy", "all"]:
                    # Load full summary for predictions
                    summary_file = file_dir / "summary.md"
                    if summary_file.exists():
                        results["summary"] = summary_file.read_text(encoding="utf-8")

                if query_type in ["empathy", "all"]:
                    results["full_analysis"] = index_data

            else:
                return {"error": f"No index.json found for {file_path}"}

        else:
            # Query all files
            results["files"] = []

            for file_dir in self.docs_dir.iterdir():
                if file_dir.is_dir():
                    index_file = file_dir / "index.json"
                    if index_file.exists():
                        with open(index_file, encoding="utf-8") as f:
                            index_data = json.load(f)

                        file_result = {
                            "file": str(index_data.get("scope", {}).get("paths", ["unknown"])[0]),
                            "commit": index_data.get("commit"),
                            "timestamp": index_data.get("timestamp"),
                        }

                        if query_type in ["issues", "all"]:
                            file_result["issue_count"] = len(index_data.get("features", []))
                            file_result["severity_score"] = index_data.get("severity_score", "N/A")

                        if query_type in ["predictions", "empathy", "all"]:
                            # Count predictions from features with "prediction" tag
                            features = index_data.get("features", [])
                            predictions = [f for f in features if "prediction" in f.get("tags", [])]
                            file_result["prediction_count"] = len(predictions)

                        results["files"].append(file_result)

            results["total_files"] = len(results["files"])

        return results


# MCP Server Protocol Implementation using official SDK
async def serve_mcp() -> None:
    """Run MCP server (stdio protocol for Claude Desktop)."""
    import logging

    # Use secure temporary file for logging
    log_file = tempfile.NamedTemporaryFile(
        mode="w", prefix="memdocs-mcp-", suffix=".log", delete=False
    )
    logging.basicConfig(level=logging.INFO, filename=log_file.name)

    # Get repo path from environment or use current directory, with validation
    repo_path_str = os.environ.get("REPO_PATH", ".")
    repo_path = PathValidator.validate_path(Path(repo_path_str))
    memdocs_server = DocIntMCPServer(repo_path)

    logging.info(f"MCP server started for repo: {repo_path}")

    # Create MCP server
    server = Server("memdocs")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools."""
        return [
            Tool(
                name="search_memory",
                description="Search project memory using natural language query",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Natural language search query"},
                        "k": {
                            "type": "integer",
                            "description": "Number of results to return (default: 5)",
                            "default": 5,
                        },
                    },
                    "required": ["query"],
                },
            ),
            Tool(
                name="get_symbols",
                description="Get code symbols (functions, classes, methods) from project",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Optional: filter to specific file path",
                        }
                    },
                },
            ),
            Tool(
                name="get_documentation",
                description="Get generated documentation for the project",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_id": {
                            "type": "string",
                            "description": "Optional: specific document ID (commit SHA)",
                        }
                    },
                },
            ),
            Tool(
                name="get_summary",
                description="Get human-readable project summary in markdown format",
                inputSchema={"type": "object", "properties": {}},
            ),
            Tool(
                name="query_analysis",
                description="Query Empathy Framework analysis results (issues, patterns, predictions)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Optional: specific file to query",
                        },
                        "query_type": {
                            "type": "string",
                            "description": "Type of analysis: issues, patterns, predictions, empathy, or all",
                            "enum": ["issues", "patterns", "predictions", "empathy", "all"],
                            "default": "all",
                        },
                    },
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Any) -> list[TextContent]:
        """Handle tool calls."""
        logging.info(f"Tool called: {name} with arguments: {arguments}")

        try:
            if name == "search_memory":
                query = arguments.get("query", "")
                k = arguments.get("k", 5)
                results = memdocs_server.search_memory(query, k)
                return [TextContent(type="text", text=json.dumps(results, indent=2))]

            elif name == "get_symbols":
                file_path = arguments.get("file_path")
                symbol_data = memdocs_server.get_symbols(file_path)
                return [TextContent(type="text", text=json.dumps(symbol_data, indent=2))]

            elif name == "get_documentation":
                doc_id = arguments.get("doc_id")
                doc_data = memdocs_server.get_documentation(doc_id)
                return [TextContent(type="text", text=json.dumps(doc_data, indent=2))]

            elif name == "get_summary":
                summary = memdocs_server.get_summary()
                return [TextContent(type="text", text=summary)]

            elif name == "query_analysis":
                file_path = arguments.get("file_path")
                query_type = arguments.get("query_type", "all")
                analysis_data = memdocs_server.query_analysis(file_path, query_type)
                return [TextContent(type="text", text=json.dumps(analysis_data, indent=2))]

            else:
                error_msg = f"Unknown tool: {name}"
                logging.error(error_msg)
                return [TextContent(type="text", text=json.dumps({"error": error_msg}))]

        except Exception as e:
            error_msg = f"Error executing {name}: {str(e)}"
            logging.error(error_msg, exc_info=True)
            return [TextContent(type="text", text=json.dumps({"error": error_msg}))]

    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(serve_mcp())
