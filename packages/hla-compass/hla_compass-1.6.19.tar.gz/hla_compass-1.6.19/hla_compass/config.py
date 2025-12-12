"""Configuration management for HLA-Compass SDK"""

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any


logger = logging.getLogger(__name__)


class Config:
    """SDK configuration management"""

    # API endpoints by environment (base URLs without version prefix)
    API_ENDPOINTS = {
        "dev": "https://api-dev.alithea.bio",
        "staging": "https://api-staging.alithea.bio",
        "prod": "https://api.alithea.bio",
    }

    # Console/Frontend endpoints by environment
    CONSOLE_ENDPOINTS = {
        "dev": "https://hub-dev.alithea.bio",
        "staging": "https://hub-staging.alithea.bio",
        "prod": "https://hub.alithea.bio",
    }

    @classmethod
    def get_request_timeouts(cls) -> Dict[str, float]:
        """Return request timeout settings.

        Environment variables (seconds):
          - HLA_CONNECT_TIMEOUT (default 5)
          - HLA_READ_TIMEOUT (default 30)
        """
        def _get_float(name: str, default: float) -> float:
            val = os.getenv(name)
            if val is None:
                return float(default)
            try:
                v = float(val)
                if v <= 0:
                    raise ValueError
                return v
            except ValueError:
                logger.warning("Invalid %s=%s; expected positive number (seconds)", name, val)
                return float(default)

        return {
            "connect": _get_float("HLA_CONNECT_TIMEOUT", 5.0),
            "read": _get_float("HLA_READ_TIMEOUT", 30.0),
        }

    @classmethod
    def get_upload_read_timeout(cls) -> float:
        """Return read timeout for file uploads.

        Environment variable: HLA_UPLOAD_READ_TIMEOUT (default 120)
        """
        val = os.getenv("HLA_UPLOAD_READ_TIMEOUT")
        if val is None:
            return 120.0
        try:
            v = float(val)
            if v <= 0:
                raise ValueError
            return v
        except ValueError:
            logger.warning(
                "Invalid HLA_UPLOAD_READ_TIMEOUT=%s; expected positive number (seconds)",
                val,
            )
            return 120.0

    @classmethod
    def get_environment(cls) -> str:
        """Get current environment (dev/staging/prod)

        Precedence: HLA_COMPASS_ENV > HLA_ENV > 'dev'
        """
        return os.getenv("HLA_COMPASS_ENV") or os.getenv("HLA_ENV", "dev")

    @classmethod
    def get_profile(cls, env: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Return the stored profile for an environment if available."""

        config = cls.load_config_data()
        profiles = config.get("profiles") or {}
        profile_name = env or config.get("activeProfile") or cls.get_environment()
        profile = profiles.get(profile_name)
        if profile is None:
            return None
        return dict(profile)

    @classmethod
    def update_profile(
        cls,
        env: str,
        profile_data: Dict[str, Any],
        *,
        set_active: bool = True,
    ) -> Dict[str, Any]:
        """Persist profile metadata for an environment and return the full config."""

        config = cls.load_config_data()
        profiles = config.get("profiles") or {}
        profile = dict(profile_data)
        profile.setdefault("environment", env)
        profile["updatedAt"] = datetime.now(timezone.utc).isoformat()
        profiles[env] = profile
        config["profiles"] = profiles

        active_org = profile.get("activeOrgId") or profile.get("primaryOrgId")
        if active_org:
            config["activeOrgId"] = active_org
            # Maintain backwards compatibility with older config expectations
            config["organization"] = active_org

        if set_active:
            config["activeProfile"] = env

        cls.save_config_data(config)
        return config

    @classmethod
    def get_active_org_id(cls, env: Optional[str] = None) -> Optional[str]:
        """Return the selected organization id for the environment."""

        profile = cls.get_profile(env)
        if profile:
            org_id = profile.get("activeOrgId") or profile.get("primaryOrgId")
            if org_id:
                return str(org_id)

        config = cls.load_config_data()
        org_id = config.get("activeOrgId") or config.get("organization")
        return str(org_id) if org_id else None

    @classmethod
    def set_active_org(cls, org_id: str, env: Optional[str] = None) -> None:
        """Update the active organization for the selected environment."""

        if not org_id:
            return

        config = cls.load_config_data()
        profile_name = env or config.get("activeProfile") or cls.get_environment()
        profiles = config.get("profiles") or {}
        profile = dict(profiles.get(profile_name) or {})
        profile.setdefault("environment", profile_name)
        profile["activeOrgId"] = org_id
        profile["updatedAt"] = datetime.now(timezone.utc).isoformat()
        profiles[profile_name] = profile
        config["profiles"] = profiles
        config["activeOrgId"] = org_id
        config["organization"] = org_id
        cls.save_config_data(config)

    @classmethod
    def get_api_endpoint(cls) -> str:
        """Get API endpoint for current environment"""
        env = cls.get_environment()
        return cls.API_ENDPOINTS.get(env, cls.API_ENDPOINTS["dev"])

    @classmethod
    def get_console_endpoint(cls) -> str:
        """Get Console/Frontend endpoint for current environment"""
        env = cls.get_environment()
        return cls.CONSOLE_ENDPOINTS.get(env, cls.CONSOLE_ENDPOINTS["dev"])

    @classmethod
    def get_config_dir(cls) -> Path:
        """Get configuration directory path"""
        # Honor HLA_COMPASS_CONFIG_DIR environment variable
        config_dir_str = os.getenv("HLA_COMPASS_CONFIG_DIR")
        if config_dir_str:
            raw_path = Path(config_dir_str).expanduser()
            if raw_path.is_absolute():
                config_dir = raw_path.resolve()
            else:
                resolved = (Path.cwd() / raw_path).resolve()
                home_path = Path.home().resolve()
                cwd_path = Path.cwd().resolve()

                def _within(base: Path) -> bool:
                    try:
                        resolved.relative_to(base)
                        return True
                    except ValueError:
                        return False

                if _within(home_path) or _within(cwd_path):
                    config_dir = resolved
                else:
                    import tempfile

                    temp_path = Path(tempfile.gettempdir()).resolve()
                    if _within(temp_path):
                        config_dir = resolved
                    else:
                        raise ValueError(
                            "Invalid config directory: must be absolute or within home, current, or temp directory"
                        )
        else:
            config_dir = Path.home() / ".hla-compass"

        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    @classmethod
    def get_credentials_path(cls) -> Path:
        """Get path to credentials.json file"""
        return cls.get_config_dir() / "credentials.json"

    @classmethod
    def get_config_path(cls) -> Path:
        """Get path to config file"""
        return cls.get_config_dir() / "config.json"

    @classmethod
    def load_config_data(cls) -> Dict[str, Any]:
        """Load persisted SDK configuration, returning an empty dict on failure."""

        path = cls.get_config_path()
        if not path.exists():
            return {}

        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
                if isinstance(data, dict):
                    return data
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to parse SDK config %s: %s", path, exc)

        return {}

    @classmethod
    def save_config_data(cls, data: Dict[str, Any]) -> None:
        """Persist SDK configuration to disk."""

        path = cls.get_config_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)

    @classmethod
    def set_environment(cls, env: str) -> None:
        """Force the current CLI process to operate against a specific environment."""

        if env:
            os.environ["HLA_COMPASS_ENV"] = env

    @classmethod
    def get_api_key(cls) -> Optional[str]:
        """Get API key from the environment"""
        return os.getenv("HLA_API_KEY")

    @classmethod
    def get_access_token(cls) -> Optional[str]:
        """Get access token from credentials.json file or environment"""
        # First check environment
        token = os.getenv("HLA_ACCESS_TOKEN")
        if token:
            return token

        # Then check encrypted credentials via Auth
        # Import here to avoid circular dependency
        from .auth import Auth
        try:
            auth = Auth()
            creds_serialized = auth._read_encrypted_credentials()
            if creds_serialized:
                creds = json.loads(creds_serialized)
                return creds.get("access_token")
        except Exception:
            pass

        return None

    @classmethod
    def is_authenticated(cls) -> bool:
        """Check if the user is authenticated"""
        if cls.get_access_token() is not None:
            return True
        return cls.get_api_key() is not None

    @classmethod
    def get_correlation_id(cls) -> Optional[str]:
        """Get global correlation id for tracing (optional).

        Set via environment variable `HLA_CORRELATION_ID` to propagate a
        cross-service correlation identifier in the `X-Correlation-Id` header.
        """
        return os.getenv("HLA_CORRELATION_ID")

    def get(self, key: str, default=None):
        """
        Provide dict-like access for tests/utilities that call config.get(...).

        Supported keys:
          - 'environment'
          - 'api_endpoint'
          - 'config_dir'
          - 'credentials_path'
          - 'config_path'
          - 'api_key'
          - 'access_token'
          - 'is_authenticated'
          - 'correlation_id'
        """
        rate_limit = self.get_rate_limit_settings()

        mapping = {
            "environment": self.get_environment(),
            "api_endpoint": self.get_api_endpoint(),
            "config_dir": str(self.get_config_dir()),
            "credentials_path": str(self.get_credentials_path()),
            "config_path": str(self.get_config_path()),
            "api_key": self.get_api_key(),
            "access_token": self.get_access_token(),
            "is_authenticated": self.is_authenticated(),
            "correlation_id": self.get_correlation_id(),
            "rate_limit_max_requests": rate_limit.get("max_requests"),
            "rate_limit_time_window": rate_limit.get("time_window"),
            "active_org_id": self.get_active_org_id(),
        }
        return mapping.get(key, default)

    @classmethod
    def get_rate_limit_settings(cls) -> Dict[str, int]:
        """Get rate limiter configuration from environment variables."""
        settings: Dict[str, int] = {}

        max_requests = os.getenv("HLA_RATE_LIMIT_MAX_REQUESTS")
        if max_requests:
            try:
                value = int(max_requests)
                if value > 0:
                    settings["max_requests"] = value
                else:
                    raise ValueError
            except ValueError:
                logger.warning(
                    "Invalid HLA_RATE_LIMIT_MAX_REQUESTS=%s; expected positive integer",
                    max_requests,
                )

        time_window = os.getenv("HLA_RATE_LIMIT_TIME_WINDOW")
        if time_window:
            try:
                value = int(time_window)
                if value > 0:
                    settings["time_window"] = value
                else:
                    raise ValueError
            except ValueError:
                logger.warning(
                    "Invalid HLA_RATE_LIMIT_TIME_WINDOW=%s; expected positive integer",
                    time_window,
                )

        return settings
