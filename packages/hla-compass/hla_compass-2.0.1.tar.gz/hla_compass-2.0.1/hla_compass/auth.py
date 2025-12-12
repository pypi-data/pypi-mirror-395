"""Authentication management for HLA-Compass SDK"""

import base64
import json
import os
import requests
import logging
import threading
import platform
import uuid
import webbrowser
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from pathlib import Path

from .config import Config
from .utils import parse_api_error
from ._version import __version__ as SDK_VERSION

# try:  # pragma: no cover - optional dependency
#     import keyring  # type: ignore
#     from keyring.errors import KeyringError  # type: ignore
# except Exception:  # pragma: no cover - gracefully degrade when unavailable
keyring = None

class KeyringError(Exception):
    pass

from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)


class AuthError(Exception):
    """Authentication error"""

    pass


class Auth:
    """Handle authentication with HLA-Compass API"""

    _instance = None
    _lock = threading.Lock()
    _credentials_cache = None
    _cache_expiry = None

    def __new__(cls):
        """Singleton pattern for credential caching"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize auth manager"""
        if not hasattr(self, '_initialized') or os.getenv("PYTEST_CURRENT_TEST"):
            self.config = Config()
            self.credentials_path = self.config.get_credentials_path()
            self.session = requests.Session()
            ua = (
                f"hla-compass-sdk/{SDK_VERSION} "
                f"python/{platform.python_version()} "
                f"os/{platform.system()}-{platform.release()}"
            )
            self.session.headers.update(
                {
                    "Accept": "application/json",
                    "User-Agent": ua,
                }
            )
            self._initialized = True
            self._keyring_service = "hla-compass-sdk"

    def _json_headers(self) -> Dict[str, str]:
        """Default JSON headers with a unique request id"""
        headers = dict(self.session.headers)
        headers["Content-Type"] = "application/json"
        headers["X-Request-Id"] = str(uuid.uuid4())
        # Optional global correlation id
        try:
            corr = self.config.get_correlation_id()
            if corr:
                headers["X-Correlation-Id"] = corr
        except Exception:
            pass
        return headers

    def _invalidate_cache(self):
        """Invalidate credential cache"""
        self._credentials_cache = None
        self._cache_expiry = None

    def login(
        self, email: str, password: str, environment: str = None
    ) -> Dict[str, Any]:
        """
        Login to HLA-Compass API

        Args:
            email: User email
            password: User password
            environment: Target environment (dev/staging/prod)

        Returns:
            Authentication response with tokens

        Raises:
            AuthError: If login fails
        """
        # Set environment if provided
        if environment:
            os.environ["HLA_ENV"] = environment
            self.config = Config()  # Reload config with new environment

        endpoint = f"{self.config.get_api_endpoint()}/v1/auth/login"

        try:
            response = self.session.post(
                endpoint,
                json={"email": email, "password": password},
                headers=self._json_headers(),
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                # Handle both response formats:
                # 1. Direct token response (new format)
                # 2. Wrapped response with success/data fields (legacy format)
                if "access_token" in data:
                    # Direct token response
                    self._save_credentials(data)
                    self._invalidate_cache()
                    return data
                elif data.get("success") and "data" in data:
                    # Legacy wrapped response
                    self._save_credentials(data["data"])
                    self._invalidate_cache()
                    return data["data"]
                else:
                    raise AuthError(
                        data.get("error", {}).get("message", "Login failed")
                    )
            else:
                # Handle non-JSON error responses gracefully
                raise AuthError(parse_api_error(response, "Login failed"))

        except requests.RequestException as e:
            raise AuthError(f"Network error during login: {str(e)}")

    def developer_register(self, email: str, name: str) -> Dict[str, Any]:
        """
        Register as a developer

        Args:
            email: Developer email
            name: Developer name

        Returns:
            Registration response with temporary credentials

        Raises:
            AuthError: If registration fails
        """
        endpoint = f"{self.config.get_api_endpoint()}/v1/auth/developer-register"

        try:
            response = self.session.post(
                endpoint,
                json={"email": email, "name": name},
                headers=self._json_headers(),
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "data" in data:
                    return data["data"]
                else:
                    raise AuthError(
                        data.get("error", {}).get("message", "Registration failed")
                    )
            else:
                # Handle non-JSON error responses gracefully
                raise AuthError(parse_api_error(response, "Registration failed"))

        except requests.RequestException as e:
            raise AuthError(f"Network error during registration: {str(e)}")

    def register(
        self,
        email: str,
        name: str,
        environment: str = None,
        **kwargs,
    ) -> bool:
        """
        Register a new user account

        Args:
            email: User email
            name: User's full name
            environment: Target environment (dev/staging/prod)

        Returns:
            True if registration is successful

        Raises:
            AuthError: If registration fails
        """
        # Set environment if provided
        if environment:
            os.environ["HLA_ENV"] = environment
            self.config = Config()

        # For now, use the developer registration endpoint
        try:
            result = self.developer_register(email, name)
            if result:
                return True
            return False
        except AuthError:
            raise
        except Exception as e:
            raise AuthError(f"Registration failed: {str(e)}")

    def login_browser(self, environment: str = None) -> Dict[str, Any]:
        """
        Login via browser-based SSO flow (PKCE Loopback).
        
        Spins up a local HTTP server, opens the system browser to the platform login page,
        and waits for a callback with credentials.

        Args:
            environment: Target environment (dev/staging/prod)

        Returns:
            Authentication response with tokens
        """
        if environment:
            os.environ["HLA_ENV"] = environment
            self.config = Config()

        # 1. Setup local server
        # Using port 0 allows OS to pick a free port
        # However, for the redirect_uri to be whitelistable in some IDPs, fixed ports are better.
        # We'll try a few standard ports or let the platform handle dynamic ports if supported.
        # Assuming dynamic ports are supported by the /cli-login handler.
        
        auth_result = {}
        auth_error = None
        
        class CallbackHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                nonlocal auth_result, auth_error
                try:
                    # Parse URL
                    parsed = urlparse(self.path)
                    if parsed.path != "/cli-callback":
                        self.send_error(404, "Not Found")
                        return

                    params = parse_qs(parsed.query)
                    
                    # Expecting 'payload' (base64 json) or 'error'
                    if "error" in params:
                        auth_error = params["error"][0]
                        self._send_response("Login failed: " + auth_error)
                        return

                    if "payload" in params:
                        try:
                            payload_json = base64.b64decode(params["payload"][0]).decode("utf-8")
                            data = json.loads(payload_json)
                            auth_result.update(data)
                            self._send_response("Login successful! You can close this tab and return to the terminal.")
                        except Exception as e:
                            auth_error = f"Invalid payload: {str(e)}"
                            self._send_response("Error processing login data.", status=400)
                    else:
                        self._send_response("Missing credentials in callback.", status=400)
                except Exception as e:
                    auth_error = str(e)
                
            def _send_response(self, message: str, status=200):
                self.send_response(status)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                html = f"""
                <html>
                <body style="font-family: sans-serif; text-align: center; padding: 50px;">
                    <h3>HLA-Compass CLI</h3>
                    <p>{message}</p>
                    <script>window.close()</script>
                </body>
                </html>
                """
                self.wfile.write(html.encode("utf-8"))
            
            def log_message(self, format, *args):
                pass # Suppress logs

        # Try to bind to a port
        port = 0
        server = None
        try:
            server = socketserver.TCPServer(("127.0.0.1", 0), CallbackHandler)
            port = server.server_address[1]
        except Exception as e:
            raise AuthError(f"Failed to start local login server: {e}")

        # 2. Construct Login URL
        console_url = self.config.get_console_endpoint()
        callback_url = f"http://127.0.0.1:{port}/cli-callback"
        
        # Encode callback URL to pass to frontend
        # The frontend at /cli-login should:
        # 1. Authenticate user
        # 2. Construct JSON creds {access_token, refresh_token, ...}
        # 3. Base64 encode it
        # 4. Redirect to {callback_url}?payload={base64_creds}
        
        import urllib.parse
        encoded_callback = urllib.parse.quote(callback_url)
        login_url = f"{console_url}/cli-login?redirect_uri={encoded_callback}"

        print(f"Opening browser to: {login_url}")
        
        try:
            webbrowser.open(login_url)
            
            # 3. Wait for callback (single request)
            server.handle_request()
        finally:
            server.server_close()

        # 4. Process result
        if auth_error:
            raise AuthError(f"Browser login failed: {auth_error}")
            
        if not auth_result:
            raise AuthError("No credentials received from browser.")

        # Save credentials
        if "access_token" in auth_result:
            self._save_credentials(auth_result)
            self._invalidate_cache()
            return auth_result
        elif auth_result.get("data"):
             # Handle wrapped format if frontend sends it that way
             self._save_credentials(auth_result["data"])
             self._invalidate_cache()
             return auth_result["data"]
        else:
            raise AuthError("Invalid credential format received from browser.")

    def is_authenticated(self) -> bool:
        """Check if the user is currently authenticated"""
        if self.get_bearer_token() is not None:
            return True
        return self.get_api_key() is not None

    def get_status(self) -> Dict[str, Any]:
        """
        Get current authentication status.

        Returns:
            Dictionary with authentication status information
        """
        status = {
            "authenticated": self.is_authenticated(),
            "environment": self.config.get_environment(),
        }

        # Check for credentials
        if self._credentials_available():
            try:
                creds = self._load_credentials(allow_refresh=False)
                if creds:
                    if creds.get("expires_at"):
                        expires = datetime.fromisoformat(creds["expires_at"])
                        status["token_expires_at"] = creds["expires_at"]
                        status["token_expired"] = expires <= datetime.now()
                    status["has_refresh_token"] = bool(creds.get("refresh_token"))
                    status["has_api_key"] = bool(creds.get("api_key"))
            except Exception:
                pass

        # Check environment variables
        status["env_api_key_set"] = bool(self.config.get_api_key())
        status["env_access_token_set"] = bool(self.config.get_access_token())

        return status

    def logout(self):
        """Logout and clear stored credentials"""
        self._clear_stored_credentials()
        self._invalidate_cache()

    def refresh_token(self) -> Optional[str]:
        """
        Refresh access token using refresh token

        Returns:
            New access token or None if refresh fails
        """
        if not self._credentials_available():
            return None

        try:
            creds = self._load_credentials(allow_refresh=False)
            if not creds:
                return None

            refresh_token = creds.get("refresh_token")
            if not refresh_token:
                return None

            endpoint = f"{self.config.get_api_endpoint()}/v1/auth/refresh"
            response = self.session.post(
                endpoint,
                json={"refresh_token": refresh_token},
                headers=self._json_headers(),
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                # Support both new direct and legacy wrapped response formats
                if "access_token" in data:
                    self._save_credentials(data)
                    self._invalidate_cache()
                    return data.get("access_token")
                if data.get("success") and "data" in data:
                    self._save_credentials(data["data"])
                    self._invalidate_cache()
                    return data["data"].get("access_token")
        except (json.JSONDecodeError, KeyError, ValueError):
            # Token file corrupted or invalid format
            pass

        return None

    def get_bearer_token(self) -> Optional[str]:
        """
        Return a bearer access token if available.

        Lookup order:
          1. HLA_ACCESS_TOKEN environment variable (via Config)
          2. Recently cached credentials
          3. Stored credentials (with automatic refresh for expired tokens)
        """
        token = self.config.get_access_token()
        if token:
            return token

        if self._credentials_cache and self._cache_expiry:
            if datetime.now() < self._cache_expiry:
                cached = self._credentials_cache.get("access_token")
                if cached:
                    return cached
            else:
                self._invalidate_cache()

        if self._credentials_available():
            creds = self._load_credentials()
            if creds:
                access_token = creds.get("access_token")
                if access_token:
                    return access_token

        return None

    def get_api_key(self) -> Optional[str]:
        """
        Return an API key if available.

        Environment variables take precedence, followed by cached or stored
        credentials. No token refresh is attempted when only an API key exists.
        """
        api_key_env = self.config.get_api_key()
        if api_key_env:
            return api_key_env

        if self._credentials_cache and self._cache_expiry:
            if datetime.now() < self._cache_expiry:
                api_key_cached = self._credentials_cache.get("api_key")
                if api_key_cached:
                    return api_key_cached
            else:
                self._invalidate_cache()

        if self._credentials_available():
            creds = self._load_credentials(allow_refresh=False)
            if creds:
                api_key_stored = creds.get("api_key")
                if api_key_stored:
                    return api_key_stored

        return None

    def get_access_token(self) -> Optional[str]:
        """
        Backwards-compatible alias for get_bearer_token().

        Historically this method returned either a bearer token or API key,
        which confused downstream consumers. It now only returns bearer tokens;
        callers needing API keys should use get_api_key().
        """
        return self.get_bearer_token()

    def _load_credentials(self, allow_refresh: bool = True) -> Optional[Dict[str, Any]]:
        serialized = self._retrieve_from_keyring()
        if serialized is None:
            serialized = self._read_encrypted_credentials()
        if serialized is None:
            return None

        try:
            creds = json.loads(serialized)

            # Check if the token is expired
            expires_at = creds.get("expires_at")
            if expires_at:
                expires = datetime.fromisoformat(expires_at)
                if expires <= datetime.now():
                    if not allow_refresh:
                        return creds

                    # Token expired, try to refresh exactly once
                    if getattr(self, "_refresh_in_progress", False):
                        return None

                    self._refresh_in_progress = True
                    try:
                        new_token = self.refresh_token()
                    finally:
                        self._refresh_in_progress = False

                    if new_token:
                        return {"access_token": new_token}

                    # Refresh failed; clear credentials so we don't loop on bad data
                    self._clear_stored_credentials()
                    self._invalidate_cache()
                    return None

            self._credentials_cache = creds
            self._cache_expiry = datetime.now() + timedelta(seconds=60)
            return creds
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.warning(
                f"Credential storage corrupted: {e}. Clearing stored credentials."
            )
            self._clear_stored_credentials()
            return None

    def get_headers(self) -> Dict[str, str]:
        """
        Get authorization headers for API requests.
        Emits either Authorization: Bearer or X-API-Key header depending on credential type.

        Returns:
            Headers dict with authorization token or API key
        """
        headers = {"Content-Type": "application/json"}

        token = self.get_bearer_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"
            return headers

        api_key = self.get_api_key()
        if api_key:
            headers["X-API-Key"] = api_key

        return headers

    def _save_credentials(self, data: Dict[str, Any]):
        """Save credentials to a file"""
        # Calculate expiration time
        expires_in = data.get("expires_in", 3600)
        expires_at = datetime.now() + timedelta(seconds=expires_in)

        credentials = {
            "access_token": data.get("access_token"),
            "refresh_token": data.get("refresh_token"),
            "expires_at": expires_at.isoformat(),
            "environment": self.config.get_environment(),
        }
        
        # Include API key if present
        if data.get("api_key"):
            credentials["api_key"] = data.get("api_key")

        serialized = json.dumps(credentials)

        if not self._store_in_keyring(serialized):
            self._write_encrypted_credentials(serialized)

        self._invalidate_cache()

    # Secure storage helpers

    def _credentials_available(self) -> bool:
        if keyring and self._retrieve_from_keyring() is not None:
            return True
        return self.credentials_path.exists()

    def _store_in_keyring(self, serialized: str) -> bool:
        if not keyring:
            return False

        account = self._keyring_account()
        try:
            keyring.set_password(self._keyring_service, account, serialized)
            return True
        except KeyringError as err:  # pragma: no cover - depends on system keyring
            logger.warning("Keyring storage failed (%s). Falling back to encrypted file.", err)
            return False

    def _retrieve_from_keyring(self) -> Optional[str]:
        if not keyring:
            return None
        account = self._keyring_account()
        try:
            return keyring.get_password(self._keyring_service, account)
        except KeyringError as err:  # pragma: no cover - depends on system keyring
            logger.warning("Failed to read credentials from keyring: %s", err)
            return None

    def _keyring_account(self) -> str:
        env = self.config.get_environment()
        return f"{env}:tokens"

    def _write_encrypted_credentials(self, serialized: str) -> None:
        key = self._get_encryption_key()
        token = Fernet(key).encrypt(serialized.encode("utf-8"))

        self.credentials_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.credentials_path, "wb") as f:
            f.write(token)

        try:
            self.credentials_path.chmod(0o600)
        except (OSError, NotImplementedError):  # pragma: no cover - platform specific
            pass

    def _read_encrypted_credentials(self) -> Optional[str]:
        if not self.credentials_path.exists():
            return None

        key = self._get_encryption_key()
        raw_bytes = self.credentials_path.read_bytes()
        try:
            data = Fernet(key).decrypt(raw_bytes)
            return data.decode("utf-8")
        except Exception as exc:
            # Fallback for legacy plaintext credentials written before encryption support
            try:
                plaintext = raw_bytes.decode("utf-8")
                json.loads(plaintext)
            except Exception:
                logger.warning("Failed to decrypt stored credentials: %s", exc)
                self._clear_stored_credentials()
                return None

            logger.info(
                "Detected legacy plaintext credential file; migrating to encrypted storage"
            )
            # Re-encrypt credentials to move forward securely
            self._write_encrypted_credentials(plaintext)
            return plaintext

    def _get_encryption_key(self) -> bytes:
        env_key = os.getenv("HLA_COMPASS_CREDENTIAL_KEY")
        if env_key:
            try:
                key_bytes = env_key.encode("utf-8")
                decoded = base64.urlsafe_b64decode(key_bytes)
                if len(decoded) != 32:
                    raise ValueError
                return key_bytes
            except Exception as exc:
                raise AuthError(
                    "Invalid HLA_COMPASS_CREDENTIAL_KEY; must be urlsafe base64-encoded 32-byte key"
                ) from exc

        key_path = Path(self.credentials_path.parent) / "credentials.key"
        if key_path.exists():
            return key_path.read_bytes()

        key = Fernet.generate_key()
        key_path.parent.mkdir(parents=True, exist_ok=True)
        key_path.write_bytes(key)
        try:
            key_path.chmod(0o600)
        except (OSError, NotImplementedError):  # pragma: no cover
            pass
        return key

    def _clear_stored_credentials(self) -> None:
        if keyring:
            try:
                keyring.delete_password(self._keyring_service, self._keyring_account())
            except KeyringError:  # pragma: no cover - depends on keyring backend
                pass
        if self.credentials_path.exists():
            try:
                self.credentials_path.unlink()
            except OSError:
                pass
        key_path = Path(self.credentials_path.parent) / "credentials.key"
        if key_path.exists():
            try:
                key_path.unlink()
            except OSError:
                pass
