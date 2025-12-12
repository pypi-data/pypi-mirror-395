"""Helpers for working with module manifest schemas."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict


SCHEMA_PATH = Path(__file__).parent / "manifest_schema_v1.json"


@lru_cache(maxsize=1)
def load_manifest_schema() -> Dict[str, Any]:
    """Return the cached manifest schema definition."""

    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
