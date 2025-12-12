"""
Storage utilities for HLA-Compass modules.

Quick Reference
===============
- ``save_file``: accepts ``bytes``/``str`` or any file-like object with ``read()``;
  metadata values are coerced to strings automatically.
- ``save_json`` / ``save_csv`` / ``save_text`` / ``save_html``: convenience wrappers
  that call ``save_file`` with sensible MIME types.
- ``save_excel`` and ``save_figure``: emit rich artifacts; Excel export requires the
  optional ``hla-compass[data]`` extra (``pandas`` + ``xlsxwriter``).
"""

import json
import logging
import gzip
import mimetypes
import os
from io import BytesIO
from typing import Any, Dict, List, Optional, Union, BinaryIO, IO

logger = logging.getLogger(__name__)

# Export safety: neutralize spreadsheet formulas by prefixing with a single quote
_DANGEROUS_PREFIXES = ("=", "+", "-", "@", "\t")
_ROOT_PREFIXES = (
    "files/",
    "workflows/",
    "workflow-files/",
    "parquet/",
    "database-views/",
    "misc/",
)

def _sanitize_value_for_export(value: Any) -> Any:
    """
    Sanitize a single cell value for safe CSV/Excel export.

    - Numbers and booleans are returned as-is
    - None remains None (let pandas handle NA rendering)
    - Strings beginning with = + - @ or tab are prefixed with a single quote
    - Other types are stringified and then sanitized
    """
    if value is None:
        return None
    # Fast path for numbers/bools
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value
    if isinstance(value, bool):
        return value

    # Convert to string for further checks
    s = value if isinstance(value, str) else str(value)
    if not s:
        return s
    if s[0] in _DANGEROUS_PREFIXES:
        return "'" + s
    return s

def _sanitize_dataframe_for_export(df):
    """Return a sanitized copy of a pandas DataFrame for export safety."""
    try:
        # Use applymap to sanitize cell-wise; avoids modifying original df
        return df.applymap(_sanitize_value_for_export)
    except Exception:
        # If df isn't a proper DataFrame, fall back to returning as-is
        return df


def _normalize_prefix(prefix: Optional[str]) -> str:
    if not prefix:
        return ""
    normalized = prefix.strip().replace("\\", "/")
    normalized = normalized.strip("/")
    if not normalized:
        return ""
    return f"{normalized}/"


class StorageError(Exception):
    """Storage operation error"""


class MissingDependencyError(StorageError):
    """Raised when an optional dependency is required but not installed."""


class Storage:
    """
    Storage utilities for module results.

    Provides simplified access to S3 storage for saving module outputs.
    """

    def __init__(
        self,
        storage_client,
        *,
        base_prefix: str = "",
        default_metadata: Optional[Dict[str, Any]] = None,
        workflow_metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize storage utilities.

        Args:
            storage_client: Storage client from execution context
            base_prefix: Default prefix applied to keys (e.g., files/<run_id>/)
            default_metadata: Metadata automatically attached to every object
            workflow_metadata: Workflow identifiers for helper methods
        """
        self.client = storage_client
        self.logger = logging.getLogger(f"{__name__}.Storage")
        self.base_prefix = _normalize_prefix(base_prefix)
        self._default_metadata = self._normalize_metadata(default_metadata)
        self._workflow_metadata = workflow_metadata or {}

    def save_file(
        self,
        filename: str,
        content: Union[bytes, str, BinaryIO, IO[bytes], IO[str]],
        content_type: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Save a file to result storage.

        Args:
            filename: Name of the file
            content: File content (bytes, string, or file-like object)
            content_type: MIME type (auto-detected if not provided)
            metadata: Additional metadata

        Returns:
            URL or identifier of the saved file
        """
        normalized_metadata: Dict[str, str] = {}
        try:
            body = self._coerce_content(content)

            # Auto-detect content type if not provided
            if content_type is None:
                content_type, _ = mimetypes.guess_type(filename)
                if content_type is None:
                    content_type = "application/octet-stream"

            storage_key = self._resolve_key(filename)
            self.logger.debug(f"Saving file: {storage_key} ({content_type})")

            normalized_metadata = dict(self._default_metadata)
            normalized_metadata.update(self._normalize_metadata(metadata))

            result = self.client.put_object(
                key=storage_key,
                body=body,
                content_type=content_type,
                metadata=normalized_metadata,
            )

            self.logger.info(f"File saved successfully: {storage_key}")
            return result

        except Exception as e:
            client_type = type(self.client).__name__ if self.client else "None"
            content_summary = {
                "input_type": type(content).__name__,
                "body_type": type(body).__name__ if "body" in locals() else "unresolved",
                "content_type": content_type,
                "metadata_keys": sorted(list(normalized_metadata.keys())) if normalized_metadata else [],
            }
            self.logger.exception(
                "Failed to save file '%s' using client %s. Context: %s",
                filename,
                client_type,
                content_summary,
            )
            raise StorageError(
                f"Failed to save file '{filename}' via client {client_type}: {e}"
            ) from e

    def save_workflow_file(
        self,
        filename: str,
        content: Union[bytes, str, BinaryIO, IO[bytes], IO[str]],
        *,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
        step_id: Optional[str] = None,
        content_type: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Persist a workflow-specific artifact under workflow-files/{workflowId}/{runId}/{stepId}/.
        """

        workflow_id = workflow_id or self._workflow_metadata.get("workflow_id")
        workflow_run_id = workflow_run_id or self._workflow_metadata.get("workflow_run_id")
        step_id = step_id or self._workflow_metadata.get("workflow_step_id")

        segments = ["workflow-files"]
        if workflow_id:
            segments.append(workflow_id)
        if workflow_run_id:
            segments.append(workflow_run_id)
        if step_id:
            segments.append(step_id)

        base = "/".join(segments)
        resolved = f"{base}/{filename.lstrip('/')}"
        return self.save_file(resolved, content, content_type=content_type, metadata=metadata)

    def _coerce_content(
        self, content: Union[bytes, str, BinaryIO, IO[bytes], IO[str]]
    ) -> bytes:
        if isinstance(content, bytes):
            return content
        if isinstance(content, bytearray):
            return bytes(content)
        if isinstance(content, memoryview):
            return content.tobytes()
        if isinstance(content, str):
            return content.encode("utf-8")

        if hasattr(content, "read"):
            data = content.read()
            seek = getattr(content, "seek", None)
            if callable(seek):  # reset pointer when possible
                try:
                    seek(0)
                except Exception:  # pragma: no cover - optional
                    pass
            if isinstance(data, bytes):
                return data
            if isinstance(data, str):
                return data.encode("utf-8")
            raise StorageError(
                "Unsupported content stream type; expected bytes or str from file-like read()"
            )

        raise StorageError("Unsupported content type for storage upload")

    def _resolve_key(self, filename: str) -> str:
        if not filename:
            raise StorageError("Filename is required for storage upload")

        if filename.startswith("s3://"):
            raise StorageError("Absolute S3 URIs are not supported; provide a bucket-relative key.")

        normalized = filename.strip().replace("\\", "/").lstrip("/")
        if not normalized:
            raise StorageError("Filename resolves to empty path")

        if normalized.startswith("../"):
            raise StorageError("Relative parent paths are not supported for storage uploads")

        if any(normalized.startswith(prefix) for prefix in _ROOT_PREFIXES):
            return normalized

        if self.base_prefix:
            return f"{self.base_prefix}{normalized}"

        return normalized

    def _normalize_metadata(self, metadata: Optional[Dict[str, Any]]) -> Dict[str, str]:
        if not metadata:
            return {}

        normalized: Dict[str, str] = {}
        for key, value in metadata.items():
            if value is None:
                continue

            if isinstance(value, (list, tuple, set)):
                normalized_value = ",".join(str(item) for item in value)
            else:
                normalized_value = str(value)

            normalized[str(key)] = normalized_value

        return normalized

    def save_json(self, filename: str, data: Any, indent: int = 2, compress: bool = False) -> str:
        """
        Save JSON data to storage.

        Args:
            filename: Name of the file (should end with .json or .json.gz when compress=True)
            data: Data to save as JSON
            indent: JSON indentation
            compress: If True, gzip-compress the JSON payload

        Returns:
            URL or identifier of the saved file
        """
        if compress:
            # Normalize filename extension
            if not (filename.endswith(".json.gz") or filename.endswith(".gz")):
                if filename.endswith(".json"):
                    filename += ".gz"
                else:
                    filename += ".json.gz"
            raw = json.dumps(data, indent=indent, default=str).encode("utf-8")
            buf = BytesIO()
            with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
                gz.write(raw)
            gz_bytes = buf.getvalue()
            return self.save_file(filename, gz_bytes, "application/gzip")
        else:
            if not filename.endswith(".json"):
                filename += ".json"
            content = json.dumps(data, indent=indent, default=str)
            return self.save_file(filename, content, "application/json")

    def save_csv(self, filename: str, dataframe, index: bool = False, compress: bool = False) -> str:
        """
        Save pandas DataFrame as CSV.

        Args:
            filename: Name of the file (should end with .csv or .csv.gz when compress=True)
            dataframe: Pandas DataFrame
            index: Whether to include index
            compress: If True, gzip-compress the CSV payload

        Returns:
            URL or identifier of the saved file
        """
        # Sanitize to neutralize formula injection by transforming string-like cells
        try:
            safe_df = _sanitize_dataframe_for_export(dataframe)
        except Exception:
            safe_df = dataframe

        if compress:
            if not (filename.endswith(".csv.gz") or filename.endswith(".gz")):
                if filename.endswith(".csv"):
                    filename += ".gz"
                else:
                    filename += ".csv.gz"
            raw = safe_df.to_csv(index=index).encode("utf-8")
            buf = BytesIO()
            with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
                gz.write(raw)
            gz_bytes = buf.getvalue()
            return self.save_file(filename, gz_bytes, "application/gzip")
        else:
            if not filename.endswith(".csv"):
                filename += ".csv"
            content = safe_df.to_csv(index=index)
            return self.save_file(filename, content, "text/csv")

    def save_excel(
        self, filename: str, dataframe, sheet_name: str = "Sheet1", index: bool = False
    ) -> str:
        """
        Save pandas DataFrame as Excel file.

        Args:
            filename: Name of the file (should end with .xlsx)
            dataframe: Pandas DataFrame or dict of DataFrames
            sheet_name: Sheet name (if single DataFrame)
            index: Whether to include index

        Returns:
            URL or identifier of the saved file
        """
        if not filename.endswith(".xlsx"):
            filename += ".xlsx"

        # Import pandas lazily to avoid hard dependency for non-data users
        try:
            import pandas as pd  # type: ignore
        except Exception as e:  # pragma: no cover
            raise MissingDependencyError(
                "Excel export requires optional dependencies. Install via:\n"
                "  pip install 'hla-compass[data]'\n"
                f"(missing pandas: {e})"
            ) from e

        # Create Excel file in memory
        buffer = BytesIO()

        try:
            if isinstance(dataframe, dict):
                # Multiple sheets
                with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:  # type: ignore
                    for name, df in dataframe.items():
                        safe_df = _sanitize_dataframe_for_export(df)
                        safe_df.to_excel(writer, sheet_name=name, index=index)
            else:
                # Single sheet
                safe_df = _sanitize_dataframe_for_export(dataframe)
                safe_df.to_excel(buffer, sheet_name=sheet_name, index=index)
        except Exception as e:  # pragma: no cover
            # Provide clearer guidance when xlsxwriter engine is missing
            raise MissingDependencyError(
                "Failed to write Excel file. Ensure 'xlsxwriter' is installed.\n"
                "Install via: pip install 'hla-compass[data]'\n"
                f"(original error: {e})"
            ) from e

        buffer.seek(0)
        return self.save_file(
            filename,
            buffer.read(),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    def save_text(self, filename: str, content: str, encoding: str = "utf-8") -> str:
        """
        Save text content to storage.

        Args:
            filename: Name of the file
            content: Text content
            encoding: Text encoding

        Returns:
            URL or identifier of the saved file
        """
        return self.save_file(filename, content.encode(encoding), "text/plain")

    def save_html(self, filename: str, content: str) -> str:
        """
        Save HTML content to storage.

        Args:
            filename: Name of the file (should end with .html)
            content: HTML content

        Returns:
            URL or identifier of the saved file
        """
        if not filename.endswith(".html"):
            filename += ".html"

        return self.save_file(filename, content, "text/html")

    def save_figure(
        self, filename: str, figure, format: str = "png", dpi: int = 150
    ) -> str:
        """
        Save matplotlib figure to storage.

        Args:
            filename: Name of the file
            figure: Matplotlib figure object
            format: Image format (png, svg, pdf)
            dpi: Resolution for raster formats

        Returns:
            URL or identifier of the saved file
        """
        # Ensure correct extension
        if not filename.endswith(f".{format}"):
            filename = f"{filename}.{format}"

        # Save figure to buffer
        buffer = BytesIO()
        figure.savefig(buffer, format=format, dpi=dpi, bbox_inches="tight")
        buffer.seek(0)

        # Determine content type
        content_types = {
            "png": "image/png",
            "svg": "image/svg+xml",
            "pdf": "application/pdf",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
        }
        content_type = content_types.get(format, "application/octet-stream")

        return self.save_file(filename, buffer.read(), content_type)

    def create_download_url(self, filename: str, expires_in: int = 3600) -> str:
        """
        Create a pre-signed download URL.

        Args:
            filename: Name of the file
            expires_in: URL expiration time in seconds

        Returns:
            Pre-signed download URL
        """
        try:
            return self.client.create_presigned_url(key=filename, expires_in=expires_in)
        except Exception as e:
            self.logger.error(f"Failed to create download URL: {e}")
            raise StorageError(f"Failed to create download URL: {str(e)}")

    def list_files(self, prefix: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List files in storage.

        Args:
            prefix: Optional prefix to filter files

        Returns:
            List of file metadata
        """
        try:
            return self.client.list_objects(prefix=prefix)
        except Exception as e:
            self.logger.error(f"Failed to list files: {e}")
            raise StorageError(f"Failed to list files: {str(e)}")

    def delete_file(self, filename: str) -> bool:
        """
        Delete a file from storage.

        Args:
            filename: Name of the file to delete

        Returns:
            True if successful
        """
        try:
            self.client.delete_object(key=filename)
            self.logger.info(f"Deleted file: {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete file {filename}: {e}")
            raise StorageError(f"Failed to delete file: {str(e)}")


# Convenience function for working with multiple files
class ResultBundle:
    """
    Helper for bundling multiple result files.
    """

    def __init__(self, storage: Storage, prefix: str = "results"):
        """
        Initialize result bundle.

        Args:
            storage: Storage instance
            prefix: Prefix for all files in the bundle
        """
        self.storage = storage
        self.prefix = prefix
        self.files = []

    def add_json(self, name: str, data: Any) -> str:
        """Add JSON file to bundle"""
        filename = f"{self.prefix}/{name}.json"
        url = self.storage.save_json(filename, data)
        self.files.append({"name": name, "type": "json", "url": url})
        return url

    def add_csv(self, name: str, dataframe) -> str:
        """Add CSV file to bundle"""
        filename = f"{self.prefix}/{name}.csv"
        url = self.storage.save_csv(filename, dataframe)
        self.files.append({"name": name, "type": "csv", "url": url})
        return url

    def add_figure(self, name: str, figure, format: str = "png") -> str:
        """Add figure to bundle"""
        filename = f"{self.prefix}/{name}.{format}"
        url = self.storage.save_figure(filename, figure, format)
        self.files.append({"name": name, "type": format, "url": url})
        return url

    def get_manifest(self) -> Dict[str, Any]:
        """Get manifest of all files in bundle"""
        return {
            "prefix": self.prefix,
            "file_count": len(self.files),
            "files": self.files,
        }

    def save_manifest(self) -> str:
        """Save bundle manifest"""
        return self.storage.save_json(
            f"{self.prefix}/manifest.json", self.get_manifest()
        )


class S3StorageClient:
    """
    Minimal S3 client wrapper conforming to the storage client protocol expected by Storage.
    """

    def __init__(
        self,
        bucket: str,
        *,
        region: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        addressing_style: str = "virtual",
    ):
        try:
            import boto3
            from botocore.config import Config as BotoConfig
        except ImportError as exc:  # pragma: no cover - boto3 is an optional dependency
            raise StorageError(
                "boto3 is required for S3 storage helpers. Install with `pip install boto3`."
            ) from exc

        self.bucket = bucket
        config = BotoConfig(s3={"addressing_style": addressing_style})
        self._client = boto3.client(
            "s3",
            region_name=region,
            endpoint_url=endpoint_url,
            config=config,
        )

    def put_object(
        self,
        key: str,
        body: bytes,
        content_type: str,
        metadata: Dict[str, str],
    ) -> str:
        try:
            self._client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=body,
                ContentType=content_type,
                Metadata=metadata,
            )
        except Exception as exc:  # pragma: no cover - boto3 specific
            raise StorageError(f"S3 upload failed for {key}: {exc}") from exc
        return f"s3://{self.bucket}/{key}"

    def create_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        try:
            return self._client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": key},
                ExpiresIn=expires_in,
            )
        except Exception as exc:  # pragma: no cover - boto3 specific
            raise StorageError(f"Failed to create pre-signed URL for {key}: {exc}") from exc

    def list_objects(self, prefix: Optional[str] = None) -> List[Dict[str, Any]]:
        try:
            paginator = self._client.get_paginator("list_objects_v2")
            page_iterator = paginator.paginate(
                Bucket=self.bucket,
                Prefix=prefix or "",
            )
            results: List[Dict[str, Any]] = []
            for page in page_iterator:
                for item in page.get("Contents", []):
                    results.append(
                        {
                            "key": item.get("Key"),
                            "size": int(item.get("Size", 0)),
                            "last_modified": item.get("LastModified"),
                        }
                    )
            return results
        except Exception as exc:  # pragma: no cover - boto3 specific
            raise StorageError(f"Failed to list S3 objects: {exc}") from exc

    def delete_object(self, key: str) -> None:
        try:
            self._client.delete_object(Bucket=self.bucket, Key=key)
        except Exception as exc:  # pragma: no cover - boto3 specific
            raise StorageError(f"Failed to delete S3 object {key}: {exc}") from exc
