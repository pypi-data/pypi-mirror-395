"""
Shared utilities for CLI commands.
"""

import json
import sys
from pathlib import Path
from typing import Any

import yaml

from memdocs import cli_output as out
from memdocs.schemas import DocIntConfig, SymbolsOutput
from memdocs.security import ConfigValidator, InputValidator, PathValidator


def load_config(config_path: Path) -> DocIntConfig:
    """Load configuration from file.

    Args:
        config_path: Path to config file

    Returns:
        Loaded configuration
    """
    if not config_path.exists():
        return DocIntConfig()  # Use defaults

    # Validate config path
    try:
        validated_path = PathValidator.validate_path(config_path)
    except Exception as e:
        out.error(f"Invalid config path: {e}")
        sys.exit(1)

    # Validate file size
    try:
        InputValidator.validate_file_size(validated_path, max_size_mb=1.0)
    except Exception as e:
        out.error(f"Config file validation failed: {e}")
        sys.exit(1)

    with open(validated_path, encoding="utf-8") as f:
        config_dict = yaml.safe_load(f)

    # Validate configuration values
    if config_dict:
        try:
            if "policies" in config_dict and "default_scope" in config_dict["policies"]:
                ConfigValidator.validate_scope_level(config_dict["policies"]["default_scope"])

            if "ai" in config_dict:
                if "model" in config_dict["ai"]:
                    InputValidator.validate_model_name(config_dict["ai"]["model"])
                if "temperature" in config_dict["ai"]:
                    ConfigValidator.validate_temperature(config_dict["ai"]["temperature"])
        except Exception as e:
            out.error(f"Config validation failed: {e}")
            sys.exit(1)

    return DocIntConfig(**config_dict)


def _write_docs(
    config: DocIntConfig,
    doc_index: Any,
    markdown: str,
    context: Any,
) -> dict[str, Path]:
    """Write documentation outputs.

    Args:
        config: Configuration
        doc_index: Document index
        markdown: Markdown summary
        context: Extracted context

    Returns:
        Dict of format -> file path
    """
    outputs = {}
    docs_dir = config.outputs.docs_dir
    docs_dir.mkdir(parents=True, exist_ok=True)

    # index.json
    if "json" in config.outputs.formats:
        index_path = docs_dir / "index.json"
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(doc_index.model_dump(mode="json"), f, indent=2, default=str)
        outputs["index.json"] = index_path

    # summary.md
    if "markdown" in config.outputs.formats:
        summary_path = docs_dir / "summary.md"
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        outputs["summary.md"] = summary_path

    # symbols.yaml
    if "yaml" in config.outputs.formats:
        symbols_path = docs_dir / "symbols.yaml"
        all_symbols = [symbol for file_ctx in context.files for symbol in file_ctx.symbols]
        symbols_output = SymbolsOutput(symbols=all_symbols)
        with open(symbols_path, "w", encoding="utf-8") as f:
            yaml.dump(symbols_output.model_dump(mode="json"), f, default_flow_style=False)
        outputs["symbols.yaml"] = symbols_path

    return outputs


def _write_memory(config: DocIntConfig, doc_index: Any) -> dict[str, Path]:
    """Write memory outputs (embeddings, graph).

    Args:
        config: Configuration
        doc_index: Document index

    Returns:
        Dict of format -> file path
    """
    outputs = {}
    memory_dir = config.outputs.memory_dir
    memory_dir.mkdir(parents=True, exist_ok=True)

    # graph.json (commit → feature → files relationships)
    graph_path = memory_dir / "graph.json"
    graph = {
        "commit": doc_index.commit,
        "features": [{"id": f.id, "title": f.title} for f in doc_index.features],
        "files": [str(f) for f in doc_index.refs.files_changed],
        "timestamp": doc_index.timestamp.isoformat(),
    }
    with open(graph_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2)
    outputs["graph.json"] = graph_path

    # embeddings.idx (placeholder for v1.1)
    # TODO: Implement embedding generation

    return outputs
