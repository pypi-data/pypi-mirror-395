"""
API client for HLA-Compass platform

This module provides the APIClient class that handles all communication
with the HLA-Compass REST API. It's used internally by the data access
classes (PeptideData, ProteinData, SampleData) to fetch scientific data.
"""

import requests
import httpx
import logging
import time
import platform
import uuid
import os
import json
import asyncio

from typing import Dict, Any, List, Optional, Callable, Iterator, Union

from .auth import Auth
from .config import Config
from .utils import parse_api_error, RateLimiter


logger = logging.getLogger(__name__)


class APIError(Exception):
    """API request error"""

    def __init__(self, message: str, status_code: int = None, details: Dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details or {}


class AsyncAPIClient:
    """Asynchronous Client for interacting with the HLA-Compass API."""

    def __init__(self, provider: str = None, catalog: str = None):
        self.auth = Auth()
        self.config = Config()
        self.base_url = self.config.get_api_endpoint()
        self.provider = provider or self.config.get("data_provider", "alithea-bio")
        self.catalog = catalog or self.config.get("data_catalog", "immunopeptidomics")
        
        # Shared rate limiter configuration (same limits as sync client)
        rl_settings = Config.get_rate_limit_settings()
        self.rate_limiter = RateLimiter(
            max_requests=rl_settings.get("max_requests", 100),
            time_window=rl_settings.get("time_window", 60),
        )
        
        # Setup client
        timeout_cfg = self.config.get_request_timeouts()
        timeout = httpx.Timeout(
            connect=timeout_cfg.get("connect", 5.0), 
            read=timeout_cfg.get("read", 30.0),
            write=30.0, 
            pool=10.0
        )
        
        self.client = httpx.AsyncClient(
            base_url=self.base_url, 
            timeout=timeout,
            follow_redirects=True
        )
        
        # User Agent
        try:
            from . import __version__ as SDK_VERSION
        except Exception:
            SDK_VERSION = "unknown"
            
        self.client.headers.update({
            "Accept": "application/json",
            "User-Agent": f"hla-compass-sdk/{SDK_VERSION} python/{platform.python_version()} os/{platform.system()}-{platform.release()} (async)",
        })

    async def close(self):
        """Close the underlying client session."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def _headers(self) -> Dict[str, str]:
        headers = dict(self.client.headers)
        headers.update(self.auth.get_headers())
        try:
            corr = self.config.get_correlation_id()
            if corr:
                headers["X-Correlation-Id"] = corr
        except Exception:
            pass
        return headers

    def _build_data_endpoint(self, entity: str, entity_id: str = None) -> str:
        base = f"/v1/data/{self.provider}/{self.catalog}/{entity}"
        if entity_id:
            return f"{base}/{entity_id}"
        return base

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        json_data: Dict = None,
        max_retries: int = 3,
    ) -> Dict[str, Any]:
        if not self.auth.is_authenticated():
            raise APIError("Not authenticated. Please run 'hla-compass auth login' first")

        # Manual rate limit wait (RateLimiter is sync, but acquiring is fast enough)
        self.rate_limiter.acquire()
        
        headers = self._headers()
        
        for attempt in range(max_retries):
            try:
                request_id = str(uuid.uuid4())
                headers["X-Request-Id"] = request_id
                
                response = await self.client.request(
                    method=method,
                    url=endpoint, # base_url is already set in client
                    headers=headers,
                    params=params,
                    json=json_data,
                )

                if response.status_code == 401 and attempt == 0:
                    # Refresh token synchronously (Auth is sync)
                    new_token = self.auth.refresh_token()
                    if new_token:
                        headers = self._headers()
                        continue
                    else:
                        raise APIError("Authentication expired.")

                if response.status_code == 429:
                    if attempt < max_retries - 1:
                        wait = int(response.headers.get("Retry-After", 2 ** attempt))
                        await asyncio.sleep(wait)
                        continue
                    else:
                        raise APIError("Rate limit exceeded.", 429)

                if response.status_code >= 500 and attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue

                if response.status_code >= 400:
                    raise APIError(f"API Error: {response.text}", response.status_code)

                if response.status_code == 204:
                    return {}
                
                data = response.json()
                return data.get("data", data) if isinstance(data, dict) and data.get("success") else data

            except httpx.RequestError as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise APIError(f"Network error: {str(e)}")

    # Async Data Methods
    async def get_peptides(self, filters: Dict = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        params = {"limit": limit, "offset": offset}
        if filters:
            # Simple filter mapping
            params.update(filters)
            
        result = await self._make_request("GET", self._build_data_endpoint("peptides"), params=params)
        if isinstance(result, dict):
            return result.get("peptides", result.get("items", []))
        return result if isinstance(result, list) else []

    async def get_peptide(self, peptide_id: str) -> Dict[str, Any]:
        result = await self._make_request("GET", self._build_data_endpoint("peptides", peptide_id))
        return result.get("peptide", result)

    async def get_proteins(self, filters: Dict = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        params = {"limit": limit, "offset": offset}
        if filters:
            params.update(filters)
        result = await self._make_request("GET", self._build_data_endpoint("proteins"), params=params)
        if isinstance(result, dict):
            return result.get("proteins", result.get("items", []))
        return result if isinstance(result, list) else []

    async def get_samples(self, filters: Dict = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        params = {"limit": limit, "offset": offset}
        if filters:
            params.update(filters)
        result = await self._make_request("GET", self._build_data_endpoint("samples"), params=params)
        if isinstance(result, dict):
            return result.get("samples", result.get("items", []))
        return result if isinstance(result, list) else []



class APIClient:
    """Client for interacting with the HLA-Compass API.

    Highlights
    ---------
    • **Iterators** – Use :meth:`iter_peptides`, :meth:`iter_proteins`, etc. to stream
      large result sets without manual paging::

          client = APIClient()
          for peptide in client.iter_peptides({"sequence": "SIINFEKL"}):
              print(peptide["sequence"], peptide["mass"])

    • **Rate limits** – Override defaults via environment variables
      ``HLA_RATE_LIMIT_MAX_REQUESTS`` and ``HLA_RATE_LIMIT_TIME_WINDOW``; inspect the
      active settings with :meth:`get_rate_limit_state`.

    • **Telemetry** – Attach a callback to capture structured metrics for every
      request (status, duration, retries)::

          def log_request(data: Dict[str, Any]) -> None:
              print("API", data["status_code"], data["duration_seconds"], data["url"])

          client = APIClient()
          client.set_telemetry_callback(log_request)
          client.get_peptide("pep_123")

    """

    def __init__(self, provider: str = None, catalog: str = None):
        """Initialize API client with authentication and a persistent session
        
        Args:
            provider: Data provider name (default: from config or 'alithea-bio')
            catalog: Data catalog name (default: from config or 'immunopeptidomics')
        """
        self.auth = Auth()
        self.config = Config()
        self.base_url = self.config.get_api_endpoint()
        
        # Set provider and catalog from args, config, or defaults
        self.provider = provider or self.config.get("data_provider", "alithea-bio")
        self.catalog = catalog or self.config.get("data_catalog", "immunopeptidomics")
        
        rl_settings = Config.get_rate_limit_settings()
        max_requests = rl_settings.get("max_requests", 100)
        time_window = rl_settings.get("time_window", 60)

        self.rate_limiter = RateLimiter(
            max_requests=max_requests,
            time_window=time_window,
        )
        self._rate_limit_state: Dict[str, Any] = {
            "max_requests": max_requests,
            "time_window": time_window,
            "last_wait_seconds": 0.0,
        }
        self._telemetry_callback: Optional[Callable[[Dict[str, Any]], None]] = None

        # Create a persistent HTTP session for connection reuse and default headers
        self.session = requests.Session()

        # Build a descriptive User-Agent
        try:
            from . import __version__ as SDK_VERSION  # Avoid hard dependency if import path changes
        except Exception:
            SDK_VERSION = "unknown"

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

        # Configure retries for idempotent requests (GET/HEAD/OPTIONS)
        try:  # Optional dependency present in requests.adapters
            from urllib3.util import Retry  # type: ignore
            from requests.adapters import HTTPAdapter  # type: ignore

            retry = Retry(
                total=3,
                connect=3,
                read=3,
                backoff_factor=0.5,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods={"GET", "HEAD", "OPTIONS"},
                respect_retry_after_header=True,
            )
            adapter = HTTPAdapter(max_retries=retry)
            self.session.mount("https://", adapter)
            self.session.mount("http://", adapter)
        except Exception:
            # If retry configuration fails, continue without it
            pass

    def _headers(self) -> Dict[str, str]:
        """Compose request headers by combining session defaults with auth headers"""
        headers = dict(self.session.headers)
        headers.update(self.auth.get_headers())
        # Optional correlation id for cross-service tracing
        try:
            corr = self.config.get_correlation_id()
            if corr:
                headers["X-Correlation-Id"] = corr
        except Exception:
            pass
        return headers

    def _build_data_endpoint(self, entity: str, entity_id: str = None) -> str:
        """Build a data API endpoint path.
        
        Args:
            entity: Entity name (e.g., 'peptides', 'proteins')
            entity_id: Optional entity ID for specific resource
            
        Returns:
            Complete endpoint path
        """
        base = f"/v1/data/{self.provider}/{self.catalog}/{entity}"
        if entity_id:
            return f"{base}/{entity_id}"
        return base

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        json_data: Dict = None,
        max_retries: int = 3,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Make an authenticated API request with retries and timeouts

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path (e.g., /v1/data/alithea-bio/immunopeptidomics/peptides)
            params: Query parameters
            json_data: JSON body data
            max_retries: Maximum number of retry attempts for transient errors

        Returns:
            Parsed JSON response

        Raises:
            APIError: If request fails
        """
        # Ensure we have authentication
        if not self.auth.is_authenticated():
            raise APIError(
                "Not authenticated. Please run 'hla-compass auth login' first"
            )

        # Build full URL
        url = f"{self.base_url}{endpoint}"

        # Apply rate limiting
        self.rate_limiter.acquire()
        self._rate_limit_state["last_wait_seconds"] = self.rate_limiter.last_wait

        # Get combined headers (session defaults + auth)
        headers = self._headers()

        # Retry logic for transient errors
        # For POST requests, only allow retry when an idempotency key is provided.
        # Generate a stable idempotency key per call if not provided so that
        # internal retries are safe and deduplicated server-side.
        method_upper = (method or "").upper()
        if method_upper == "POST" and not idempotency_key:
            idempotency_key = str(uuid.uuid4())
        can_retry_post = method_upper != "POST" or (idempotency_key is not None)

        for attempt in range(max_retries):
            try:
                start_time = time.perf_counter()
                # Create a fresh set of headers per attempt and add a unique request id
                attempt_headers = dict(headers)
                request_id = str(uuid.uuid4())
                attempt_headers["X-Request-Id"] = request_id
                # Add idempotency key for POSTs to make retries safe
                if method_upper == "POST" and idempotency_key:
                    attempt_headers.setdefault("Idempotency-Key", idempotency_key)
                # Make request with configurable timeout (defaults: 5s connect, 30s read)
                timeouts = self.config.get_request_timeouts()
                response = self.session.request(
                    method=method,
                    url=url,
                    headers=attempt_headers,
                    params=params,
                    json=json_data,
                    timeout=(timeouts.get("connect", 5.0), timeouts.get("read", 30.0)),
                )
                duration = time.perf_counter() - start_time

                # Handle 401 - try to refresh token once
                if response.status_code == 401 and attempt == 0:
                    logger.info("Token expired, attempting refresh")
                    new_token = self.auth.refresh_token()
                    if new_token:
                        # Rebuild base headers to include new Authorization and retry
                        headers = self._headers()
                        continue  # Retry with new token
                    else:
                        raise APIError(
                            "Authentication expired. Please run 'hla-compass auth login' again"
                        )

                # Handle rate limiting with exponential backoff
                if response.status_code == 429:
                    if attempt < max_retries - 1:
                        retry_after = int(
                            response.headers.get("Retry-After", 2**attempt)
                        )
                        logger.warning(
                            f"Rate limited, retrying after {retry_after} seconds"
                        )
                        time.sleep(retry_after)
                        continue
                    else:
                        raise APIError(
                            "Rate limit exceeded. Please try again later.", 429
                        )

                # Handle server errors with retry
                if response.status_code >= 500 and attempt < max_retries - 1:
                    # Only retry POSTs when idempotency is guaranteed
                    if method_upper == "POST" and not can_retry_post:
                        raise APIError(
                            f"Server error {response.status_code}", response.status_code
                        )
                    wait_time = 2**attempt  # Exponential backoff
                    logger.warning(
                        f"Server error {response.status_code}, retrying in {wait_time} seconds"
                    )
                    time.sleep(wait_time)
                    continue

                # Check for other errors
                if response.status_code >= 400:
                    # Sanitize error message to avoid info disclosure
                    error_msg = parse_api_error(response, "API request failed")
                    error_details = None
                    try:
                        error_details = response.json()
                    except Exception:  # pragma: no cover - defensive
                        error_details = None
                    self._emit_telemetry(
                        method=method_upper,
                        url=url,
                        status_code=response.status_code,
                        duration=duration,
                        attempt=attempt,
                        retries=max_retries,
                        params=params,
                        idempotency_key=idempotency_key,
                        request_id=request_id,
                        error=error_msg,
                    )
                    raise APIError(error_msg, response.status_code, details=error_details)

                # Parse successful response (204 = empty body)
                if response.status_code == 204:
                    data = {}
                else:
                    try:
                        data = response.json()
                    except ValueError:
                        # Non-JSON response body
                        if not response.text:
                            data = {}
                        else:
                            error_msg = parse_api_error(
                                response, "Invalid JSON response from API"
                            )
                            raise APIError(error_msg, response.status_code)

                # Handle success wrapper format
                payload = (
                    data.get("data", data)
                    if isinstance(data, dict) and data.get("success")
                    else data
                )

                self._emit_telemetry(
                    method=method_upper,
                    url=url,
                    status_code=response.status_code,
                    duration=duration,
                    attempt=attempt,
                    retries=max_retries,
                    params=params,
                    idempotency_key=idempotency_key,
                    request_id=request_id,
                )

                return payload

            except requests.Timeout as e:
                duration = time.perf_counter() - start_time
                self._emit_telemetry(
                    method=method_upper,
                    url=url,
                    status_code=None,
                    duration=duration,
                    attempt=attempt,
                    retries=max_retries,
                    params=params,
                    idempotency_key=idempotency_key,
                    request_id=request_id,
                    error="timeout",
                )

                if attempt < max_retries - 1:
                    wait_time = 2**attempt
                    logger.warning(f"Request timeout, retrying in {wait_time} seconds")
                    time.sleep(wait_time)
                    continue
                else:
                    raise APIError(
                        "Request timed out. Please check your connection and try again."
                    ) from e

            except requests.RequestException as e:
                duration = time.perf_counter() - start_time
                self._emit_telemetry(
                    method=method_upper,
                    url=url,
                    status_code=None,
                    duration=duration,
                    attempt=attempt,
                    retries=max_retries,
                    params=params,
                    idempotency_key=idempotency_key,
                    request_id=request_id,
                    error=str(e),
                )

                if attempt < max_retries - 1 and "connection" in str(e).lower():
                    wait_time = 2**attempt
                    logger.warning(f"Connection error, retrying in {wait_time} seconds")
                    time.sleep(wait_time)
                    continue
                else:
                    raise APIError(f"Network error: {str(e)}")

    def _iterate_paginated(
        self,
        fetcher: Callable[[int, int], List[Dict[str, Any]]],
        page_size: int,
        max_results: Optional[int],
    ) -> Iterator[Dict[str, Any]]:
        offset = 0
        yielded = 0

        while True:
            if max_results is not None:
                remaining = max_results - yielded
                if remaining <= 0:
                    break
                limit = min(page_size, remaining)
            else:
                limit = page_size

            page = fetcher(limit, offset)
            if not page:
                break

            for item in page:
                yield item
                yielded += 1
                if max_results is not None and yielded >= max_results:
                    return

            if len(page) < limit:
                break

            offset += limit

    # Peptide endpoints

    def get_peptides(
        self, filters: Dict = None, limit: int = 100, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Search peptides with filters

        Args:
            filters: Search filters (sequence, min_length, max_length, etc.)
            limit: Maximum results to return
            offset: Pagination offset

        Returns:
            List of peptide records
        """
        params = {"limit": limit, "offset": offset}

        # Add filters to params
        if filters:
            # Map internal filter names to API parameter names
            filter_mapping = {
                "sequence": "sequence",
                "min_length": "min_length",
                "max_length": "max_length",
                "mass": "mass",
                "mass_tolerance": "mass_tolerance",
                "modifications": "modifications",
                "hla_allele": "hla",
                "organ": "organ",
                "disease": "disease",
            }

            for key, value in filters.items():
                api_param = filter_mapping.get(key, key)
                if isinstance(value, list):
                    params[api_param] = ",".join(str(v) for v in value)
                else:
                    params[api_param] = value

        result = self._make_request("GET", self._build_data_endpoint("peptides"), params=params)

        # Extract peptides from response
        if isinstance(result, dict):
            return result.get("peptides", result.get("items", []))
        return result if isinstance(result, list) else []

    def get_peptide(self, peptide_id: str) -> Dict[str, Any]:
        """Get single peptide by ID"""
        result = self._make_request("GET", self._build_data_endpoint("peptides", peptide_id))
        return result.get("peptide", result)

    def iter_peptides(
        self,
        filters: Dict = None,
        page_size: int = 100,
        max_results: Optional[int] = None,
    ) -> Iterator[Dict[str, Any]]:
        """Yield peptides across pages without manual pagination."""

        def fetch(limit: int, offset: int) -> List[Dict[str, Any]]:
            return self.get_peptides(filters=filters, limit=limit, offset=offset)

        yield from self._iterate_paginated(fetch, page_size, max_results)

    def get_peptide_samples(self, peptide_id: str) -> List[Dict[str, Any]]:
        """Get samples containing a peptide"""
        result = self._make_request(
            "GET", f"{self._build_data_endpoint('peptides', peptide_id)}/samples"
        )
        return result.get("samples", result.get("items", []))

    def get_peptide_proteins(self, peptide_id: str) -> List[Dict[str, Any]]:
        """Get proteins containing a peptide"""
        result = self._make_request(
            "GET", f"{self._build_data_endpoint('peptides', peptide_id)}/proteins"
        )
        return result.get("proteins", result.get("items", []))

    # Protein endpoints

    def get_proteins(
        self, filters: Dict = None, limit: int = 100, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Search proteins with filters

        Args:
            filters: Search filters (accession, gene_name, organism, etc.)
            limit: Maximum results to return
            offset: Pagination offset

        Returns:
            List of protein records
        """
        params = {"limit": limit, "offset": offset}

        if filters:
            params.update(filters)

        result = self._make_request("GET", self._build_data_endpoint("proteins"), params=params)

        # Extract proteins from response
        if isinstance(result, dict):
            return result.get("proteins", result.get("items", []))
        return result if isinstance(result, list) else []

    def get_protein(self, protein_id: str) -> Dict[str, Any]:
        """Get single protein by ID"""
        result = self._make_request("GET", self._build_data_endpoint("proteins", protein_id))
        return result.get("protein", result)

    def iter_proteins(
        self,
        filters: Dict = None,
        page_size: int = 100,
        max_results: Optional[int] = None,
    ) -> Iterator[Dict[str, Any]]:
        """Yield proteins across pages without manual pagination."""

        def fetch(limit: int, offset: int) -> List[Dict[str, Any]]:
            return self.get_proteins(filters=filters, limit=limit, offset=offset)

        yield from self._iterate_paginated(fetch, page_size, max_results)

    def get_protein_peptides(self, protein_id: str) -> List[Dict[str, Any]]:
        """Get peptides from a protein"""
        result = self._make_request(
            "GET", f"{self._build_data_endpoint('proteins', protein_id)}/peptides"
        )
        return result.get("peptides", result.get("items", []))

    def get_protein_coverage(self, protein_id: str) -> Dict[str, Any]:
        """Get protein coverage information"""
        result = self._make_request(
            "GET", f"{self._build_data_endpoint('proteins', protein_id)}/coverage"
        )
        return result

    # Sample endpoints

    def get_samples(
        self, filters: Dict = None, limit: int = 100, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Search samples with filters

        Args:
            filters: Search filters (tissue, disease, cell_line, etc.)
            limit: Maximum results to return
            offset: Pagination offset

        Returns:
            List of sample records
        """
        params = {"limit": limit, "offset": offset}

        if filters:
            params.update(filters)

        result = self._make_request("GET", self._build_data_endpoint("samples"), params=params)

        # Extract samples from response
        if isinstance(result, dict):
            return result.get("samples", result.get("items", []))
        return result if isinstance(result, list) else []

    def get_sample(self, sample_id: str) -> Dict[str, Any]:
        """Get single sample by ID"""
        result = self._make_request("GET", self._build_data_endpoint("samples", sample_id))
        return result.get("sample", result)

    def iter_samples(
        self,
        filters: Dict = None,
        page_size: int = 100,
        max_results: Optional[int] = None,
    ) -> Iterator[Dict[str, Any]]:
        """Yield samples across pages without manual pagination."""

        def fetch(limit: int, offset: int) -> List[Dict[str, Any]]:
            return self.get_samples(filters=filters, limit=limit, offset=offset)

        yield from self._iterate_paginated(fetch, page_size, max_results)

    def get_sample_peptides(self, sample_id: str) -> List[Dict[str, Any]]:
        """Get peptides from a sample"""
        result = self._make_request(
            "GET", f"{self._build_data_endpoint('samples', sample_id)}/peptides"
        )
        return result.get("peptides", result.get("items", []))

    # HLA endpoints

    def get_hla_alleles(
        self, locus: str = None, resolution: str = "2-digit"
    ) -> List[str]:
        """Get list of HLA alleles"""
        params = {"resolution": resolution}
        if locus:
            params["locus"] = locus

        result = self._make_request("GET", f"{self._build_data_endpoint('hla')}/alleles", params=params)
        return result.get("alleles", result if isinstance(result, list) else [])

    def get_hla_frequencies(self, population: str = None) -> Dict[str, float]:
        """Get HLA allele frequencies"""
        params = {}
        if population:
            params["population"] = population

        result = self._make_request(
            "GET", f"{self._build_data_endpoint('hla')}/frequencies", params=params
        )
        return result.get("frequencies", result if isinstance(result, dict) else {})

    def predict_hla_binding(
        self,
        peptides: List[str],
        alleles: List[str],
        method: str = "netmhcpan",
        batch_size: int = 100,
    ) -> List[Dict[str, Any]]:
        """Predict HLA-peptide binding, with automatic batching for large inputs.

        Args:
            peptides: List of peptide sequences to evaluate
            alleles: List of HLA alleles
            method: Prediction method (default: 'netmhcpan')
            batch_size: Number of peptides per request; values <=0 disable batching
        """
        if batch_size and batch_size > 0 and len(peptides) > batch_size:
            predictions: List[Dict[str, Any]] = []
            for i in range(0, len(peptides), batch_size):
                chunk = peptides[i : i + batch_size]
                json_data = {"peptides": chunk, "alleles": alleles, "method": method}
                result = self._make_request(
                    "POST",
                    f"{self._build_data_endpoint('hla')}/predict",
                    json_data=json_data,
                )
                chunk_preds = result.get("predictions", result if isinstance(result, list) else [])
                if isinstance(chunk_preds, list):
                    predictions.extend(chunk_preds)
            return predictions
        else:
            json_data = {"peptides": peptides, "alleles": alleles, "method": method}
            result = self._make_request(
                "POST", f"{self._build_data_endpoint('hla')}/predict", json_data=json_data
            )
            return result.get("predictions", result if isinstance(result, list) else [])

    # ------------------------------------------------------------------
    # Authentication helpers
    # ------------------------------------------------------------------

    def get_current_user(self) -> Dict[str, Any]:
        """Fetch the authenticated user payload."""

        payload = self._make_request("GET", "/v1/auth/me")
        if isinstance(payload, dict):
            return payload
        return {"user": payload}

    # Module endpoints

    def start_module_run(
        self,
        module_id: str,
        *,
        parameters: Optional[Dict[str, Any]] = None,
        mode: str = "interactive",
        compute_profile: Optional[str] = None,
        version: Optional[str] = None,
        navigation_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Start a module run via the canonical /v1/module-runs API."""
        payload: Dict[str, Any] = {
            "moduleId": module_id,
            "parameters": parameters or {},
            "mode": mode,
        }
        if compute_profile:
            payload["computeProfile"] = compute_profile
        if version:
            payload["version"] = version
        if navigation_data:
            payload["navigationData"] = navigation_data
        return self._make_request("POST", "/v1/module-runs", json_data=payload)

    def get_module_run(self, run_id: str) -> Dict[str, Any]:
        """Fetch module run status."""
        return self._make_request("GET", f"/v1/module-runs/{run_id}")

    def cancel_module_run(self, run_id: str) -> Dict[str, Any]:
        """Cancel an in-progress module run."""
        return self._make_request("POST", f"/v1/module-runs/{run_id}/cancel")

    def get_module_run_logs(
        self,
        run_id: str,
        *,
        limit: Optional[int] = None,
        next_token: Optional[str] = None,
        order: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Return CloudWatch log events for the module run."""
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if next_token:
            params["nextToken"] = next_token
        if order:
            params["order"] = order
        return self._make_request("GET", f"/v1/module-runs/{run_id}/logs", params=params or None)

    def get_module_run_result(self, run_id: str) -> Dict[str, Any]:
        """Fetch module run output JSON."""
        return self._make_request("GET", f"/v1/module-runs/{run_id}/result")

    def list_modules(
        self, category: str = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List available modules"""
        params = {"limit": limit}
        if category:
            params["category"] = category

        result = self._make_request("GET", "/v1/modules", params=params)
        return result.get("modules", result.get("items", []))

    def iter_modules(
        self,
        category: str = None,
        page_size: int = 100,
        max_results: Optional[int] = None,
    ) -> Iterator[Dict[str, Any]]:
        """Yield modules across pages without manual pagination."""

        def fetch(limit: int, offset: int) -> List[Dict[str, Any]]:
            params = {"limit": limit}
            if category:
                params["category"] = category
            params["offset"] = offset
            result = self._make_request("GET", "/v1/modules", params=params)
            if isinstance(result, dict):
                return result.get("modules", result.get("items", []))
            return result if isinstance(result, list) else []

        yield from self._iterate_paginated(fetch, page_size, max_results)

    def upload_module(
        self, module_path: str, module_name: str, version: str
    ) -> Dict[str, Any]:
        """
        Upload module package to the real API endpoint using JSON (base64) payloads,
        with a multipart/form-data fallback for legacy environments.

        Args:
            module_path: Path to module zip file
            module_name: Name of the module
            version: Module version

        Returns:
            Upload response including module_id
        """
        # Validate file
        if not os.path.exists(module_path):
            raise APIError(f"Module package not found: {module_path}")
        file_size = os.path.getsize(module_path)
        if file_size > 50 * 1024 * 1024:  # 50MB limit
            raise APIError(
                f"Module package too large: {file_size / 1024 / 1024:.1f}MB (max 50MB)"
            )

        # Prepare request
        url = f"{self.base_url}/v1/modules/upload"
        metadata = {
            "name": module_name,
            "version": version,
            "filename": os.path.basename(module_path),
            "size": file_size,
        }

        base_headers = self._headers()
        base_headers.setdefault("Accept", "application/json")
        idem = str(uuid.uuid4())
        base_headers.setdefault("Idempotency-Key", idem)

        for attempt in range(2):
            headers = dict(base_headers)
            headers.pop("Content-Type", None)

            try:
                with open(module_path, "rb") as fh:
                    fh.seek(0)
                    files = {
                        "module": (
                            os.path.basename(module_path),
                            fh,
                            "application/zip",
                        )
                    }
                    form_data = {"metadata": json.dumps(metadata)} if metadata else None

                    # Use configurable connect timeout and longer, configurable read timeout for uploads
                    _timeouts = self.config.get_request_timeouts()
                    _upload_read = self.config.get_upload_read_timeout()
                    resp = self.session.post(
                        url,
                        headers=headers,
                        files=files,
                        data=form_data,
                        timeout=(_timeouts.get("connect", 5.0), _upload_read),
                    )
            except OSError as exc:
                raise APIError(f"Failed to read module package: {exc}")

            if resp.status_code == 401 and attempt == 0:
                if self.auth.refresh_token():
                    base_headers = self._headers()
                    base_headers.setdefault("Accept", "application/json")
                    base_headers.setdefault("Idempotency-Key", idem)
                    continue
                raise APIError(
                    "Authentication expired. Please run 'hla-compass auth login' again",
                    401,
                )

            if resp.status_code >= 400:
                # best-effort parse
                try:
                    err = resp.json()
                except Exception:
                    err = {"message": resp.text}
                raise APIError(
                    parse_api_error(resp, "Upload failed"),
                    resp.status_code,
                    details=err,
                )

            try:
                payload = resp.json()
            except Exception:
                raise APIError("Invalid response from upload endpoint")

            data = payload.get("data", payload)
            module_id = data.get("id") or data.get("module_id")
            if not module_id:
                raise APIError("Upload succeeded but module_id not returned")

            normalized = {"module_id": module_id}
            normalized.update(data)
            return normalized

        raise APIError("Upload failed after token refresh attempt")

    def get_rate_limit_state(self) -> Dict[str, Any]:
        """Return the active rate limit configuration and last wait duration."""
        return dict(self._rate_limit_state)

    def _emit_telemetry(
        self,
        *,
        method: str,
        url: str,
        status_code: Optional[int],
        duration: float,
        attempt: int,
        retries: int,
        params: Optional[Dict[str, Any]],
        idempotency_key: Optional[str],
        request_id: str,
        error: Optional[str] = None,
    ) -> None:
        payload = {
            "method": method,
            "url": url,
            "status_code": status_code,
            "duration_seconds": round(duration, 4),
            "attempt": attempt + 1,
            "max_retries": retries,
            "rate_limit_wait": self._rate_limit_state.get("last_wait_seconds"),
            "params": params or {},
            "idempotency_key": idempotency_key,
            "request_id": request_id,
            "error": error,
        }

        if self._telemetry_callback:
            try:
                self._telemetry_callback(dict(payload))
            except Exception as exc:  # pragma: no cover - user callback
                logger.warning("Telemetry callback raised an exception: %s", exc)

        log_method = logger.info
        if error or (status_code is not None and status_code >= 400):
            log_method = logger.warning

        sanitized = self._sanitize_telemetry_payload(payload)
        log_method("API request telemetry", extra={"api_request": sanitized})

    @staticmethod
    def _sanitize_telemetry_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Return a redacted copy of telemetry suitable for logging."""
        sanitized = dict(payload)

        params_value = payload.get("params")
        if isinstance(params_value, dict) and params_value:
            sanitized["params"] = {key: "<redacted>" for key in params_value.keys()}
        elif params_value:
            sanitized["params"] = "<redacted>"
        else:
            sanitized["params"] = {}

        if payload.get("idempotency_key"):
            sanitized["idempotency_key"] = "***"

        return sanitized

    def register_module(
        self, module_id: str, metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Publish an uploaded module version using the real API endpoint.

        Args:
            module_id: Module ID from upload
            metadata: Module metadata (expects at least 'version')

        Returns:
            Publish response from the API
        """
        json_data = {
            "version": metadata.get("version", "1.0.0"),
            "notes": metadata.get("description", "Module published via SDK"),
        }
        return self._make_request("PUT", f"/v1/modules/{module_id}/publish", json_data=json_data)

    def register_container_module(
        self, payload: Dict[str, Any], *, idempotency_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Submit a container module publish job via the intake pipeline."""

        return self._make_request(
            "POST",
            "/v1/modules/publish",
            json_data=payload,
            idempotency_key=idempotency_key,
        )

    def get_publish_config(self) -> Dict[str, Any]:
        """Retrieve registry/UI defaults for publishing modules."""

        return self._make_request("GET", "/v1/modules/publish/config")

    # ---------------------------------------------------------------------
    # Workflow templates & workflows
    # ---------------------------------------------------------------------

    def list_workflow_templates(self, limit: int = 20) -> List[Dict[str, Any]]:
        """List workflow templates from the shared assets bucket.

        Returns a list of template descriptors with ``id``, ``key``,
        ``lastModified``, and ``size`` fields.
        """
        params: Dict[str, Any] = {"limit": limit}
        result = self._make_request("GET", "/v1/workflow-templates", params=params)
        if isinstance(result, dict):
            return result.get("items", [])
        return result if isinstance(result, list) else []

    def get_workflow_template(self, template_id: str) -> Dict[str, Any]:
        """Fetch a specific workflow template document by ID."""
        return self._make_request("GET", f"/v1/workflow-templates/{template_id}")

    def adopt_workflow_template(self, template_id: str) -> Dict[str, Any]:
        """Adopt a shared workflow template into the caller's organization.

        The response mirrors the workflow upsert payload and includes
        ``metadata.workflowId`` and ``metadata.storageUri`` pointing into
        the org's private bucket.
        """
        return self._make_request(
            "POST",
            f"/v1/workflow-templates/{template_id}/adopt",
            json_data={},
        )

    def set_telemetry_callback(
        self, callback: Optional[Callable[[Dict[str, Any]], None]]
    ) -> None:
        """Register a callback that receives request telemetry dictionaries."""
        self._telemetry_callback = callback
