"""Environment helpers for resolving publish targets."""

from __future__ import annotations

from functools import lru_cache
from typing import Any, Dict, Optional

from .client import APIClient, APIError
from .config import Config


class PublishConfigError(RuntimeError):
    """Raised when the SDK cannot determine publish defaults from the API."""


@lru_cache(maxsize=8)
def _fetch_publish_config(env: str) -> Dict[str, Any]:
    Config.set_environment(env)
    client = APIClient()
    payload = client.get_publish_config() or {}
    payload.setdefault("environment", env)
    return payload


def get_publish_defaults(env: Optional[str] = None, *, force_refresh: bool = False) -> Dict[str, Any]:
    """Return registry/UI defaults for publishing modules.

    Args:
        env: Optional explicit environment (dev/staging/prod). Defaults to current env.
        force_refresh: When True, bypass the memoized cache.
    """

    target_env = env or Config.get_environment()
    if force_refresh:
        _fetch_publish_config.cache_clear()

    try:
        return dict(_fetch_publish_config(target_env))
    except APIError as exc:  # pragma: no cover - network/env specific
        raise PublishConfigError(str(exc)) from exc
