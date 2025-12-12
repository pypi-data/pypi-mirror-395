"""Utilities for generating Model Context Protocol descriptors."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_mcp_descriptor(manifest: dict[str, Any], output_dir: Path) -> Path:
    """Create an MCP tool descriptor from module manifest data.

    Args:
        manifest: Loaded manifest dictionary.
        output_dir: Directory where the descriptor should be written.

    Returns:
        Path to the generated descriptor file.
    """

    execution = manifest.get("execution", {})
    descriptor = {
        "schema_version": "1.0",
        "name": manifest.get("name", "unknown"),
        "description": manifest.get("description", "HLA-Compass module"),
        "capabilities": execution.get("supports", ["async"]),
        "input_schema": manifest.get("inputs", {}),
        "output_schema": manifest.get("outputs", {}),
        "requires_auth": execution.get("requiresAuth", True),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "tool.json"
    with target.open("w", encoding="utf-8") as fh:
        json.dump(descriptor, fh, indent=2)
    return target

