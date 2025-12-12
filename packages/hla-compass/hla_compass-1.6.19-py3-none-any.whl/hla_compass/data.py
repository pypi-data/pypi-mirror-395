"""
Data access utilities for HLA-Compass modules.
Architecture: Scoped Vending Machine.

Access is provided via generic interfaces (SQL, Storage) but scoped to specific
Provider/Catalog domains to ensure extensibility and isolation.
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class DataAccessError(Exception):
    """Error accessing HLA-Compass data"""
    pass

class DataClient:
    """
    Entry point for accessing scientific data from a specific catalog.
    
    Example:
        >>> genetics = DataClient(provider="alithea", catalog="genetics")
        >>> genetics.sql.query("SELECT * FROM genes")
    """
    
    def __init__(self, provider: str = "alithea-bio", catalog: str = "immunopeptidomics", api_client=None):
        self.provider = provider
        self.catalog = catalog
        self.api = api_client
        
        # Initialize sub-clients
        self.sql = SQLClient(self)
        self.storage = StorageClient(self)
        
    def _get_api(self):
        """Lazy load API client if not provided"""
        if self.api:
            return self.api
        # Import here to avoid circular dependency if client imports data
        from .client import APIClient
        return APIClient()


class SQLClient:
    """
    Execute SQL queries against the Catalog's Schema.
    
    For available tables and columns, see the Data Catalog documentation:
    https://docs.alithea.bio/sdk-reference/guides/data-access
    """

    def __init__(self, parent: DataClient):
        self.parent = parent
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def query(self, sql: str, params: Optional[List[Any]] = None) -> Dict[str, Any]:
        """
        Execute a raw SQL query.
        
        Args:
            sql: SQL query string with %s placeholders for parameters
            params: List of parameter values to bind safely
            
        Returns:
            Dictionary with 'columns', 'data', 'count'
            
        Example:
            >>> result = self.data.sql.query(
            ...     "SELECT sequence, mass FROM peptides WHERE length >= %s LIMIT 10",
            ...     params=[8]
            ... )
            >>> print(result["data"])
        """
        api = self.parent._get_api()
        
        try:
            payload = {"sql": sql}
            if params:
                payload["params"] = params
            
            # Endpoint: /v1/data/{provider}/{catalog}/query
            endpoint = f"/v1/data/{self.parent.provider}/{self.parent.catalog}/query"
            result = api._make_request("POST", endpoint, json_data=payload)
            return result
            
        except Exception as e:
            self.logger.error(f"SQL query failed: {e}")
            raise DataAccessError(f"Failed to execute query: {str(e)}")


class StorageClient:
    """
    Access the Catalog's Object Storage.
    """
    
    def __init__(self, parent: DataClient):
        self.parent = parent
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
    def get_credentials(self, mode: str = "read") -> Dict[str, Any]:
        """
        Get temporary AWS STS credentials scoped to the catalog's bucket prefix.
        """
        api = self.parent._get_api()
        
        try:
            # Endpoint: /v1/data/{provider}/{catalog}/storage/token
            endpoint = f"/v1/data/{self.parent.provider}/{self.parent.catalog}/storage/token"
            creds = api._make_request("GET", endpoint, params={"mode": mode})
            return creds
        except Exception as e:
            self.logger.error(f"Failed to get storage credentials: {e}")
            raise DataAccessError(f"Storage access denied: {str(e)}")
            
    def get_s3_client(self, mode: str = "read"):
        """
        Get a boto3 S3 client configured with scoped credentials.
        """
        try:
            import boto3
        except ImportError:
            raise ImportError("boto3 is required for get_s3_client")
            
        creds = self.get_credentials(mode)
        return boto3.client(
            "s3",
            aws_access_key_id=creds["accessKeyId"],
            aws_secret_access_key=creds["secretAccessKey"],
            aws_session_token=creds["sessionToken"],
            region_name=creds["region"]
        )

    def read_parquet(self, key: str, engine: str = "polars"):
        """
        Read a parquet file from the catalog's storage.
        
        Args:
            key: Relative path (e.g. "runs/123.parquet")
            engine: "polars" or "pandas"
        """
        creds = self.get_credentials(mode="read")
        
        # Construct full S3 URI using the bucket and prefix returned by the token vendor
        bucket = creds["bucket"]
        prefix = creds.get("prefix", "")
        
        # Handle if key is already absolute
        if key.startswith("s3://"):
            uri = key
        else:
            # Ensure cleanly joined path
            clean_prefix = prefix.rstrip("/")
            clean_key = key.lstrip("/")
            if clean_prefix:
                uri = f"s3://{bucket}/{clean_prefix}/{clean_key}"
            else:
                uri = f"s3://{bucket}/{clean_key}"
            
        storage_options = {
            "key": creds["accessKeyId"],
            "secret": creds["secretAccessKey"],
            "token": creds["sessionToken"],
            "region": creds["region"]
        }
        
        if engine == "polars":
            try:
                import polars as pl
                return pl.read_parquet(uri, storage_options=storage_options)
            except ImportError:
                raise ImportError("polars is required")
                
        elif engine == "pandas":
            try:
                import pandas as pd
                return pd.read_parquet(uri, storage_options=storage_options)
            except ImportError:
                raise ImportError("pandas is required")
        else:
            raise ValueError(f"Unknown engine: {engine}")

