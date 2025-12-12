"""
Base module class for HLA-Compass modules
"""

import json
import logging
import os
from abc import ABC, abstractmethod
from collections.abc import Mapping, Sized
from difflib import get_close_matches
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union

try:  # pragma: no cover - optional dependency
    from jsonschema import Draft7Validator
except Exception as exc:  # pragma: no cover - jsonschema is required for validation
    raise ImportError(
        "jsonschema is required for input validation. Install with: pip install 'jsonschema>=4.0'"
    ) from exc

try:
    from pydantic import BaseModel, ValidationError as PydanticValidationError
except ImportError:  # pragma: no cover
    BaseModel = object
    PydanticValidationError = None

from .auth import Auth, AuthError
from .config import Config
from .types import ExecutionContext, ModuleOutput
from .data import DataClient
from .storage import Storage, StorageError, S3StorageClient
from .context import RuntimeContext, CreditReservation


logger = logging.getLogger(__name__)

MANIFEST_DOCS_URL = "https://docs.alithea.bio/sdk/modules#manifest-inputs"


def _now_utc() -> datetime:
    return datetime.now(UTC)


def _now_utc_iso() -> str:
    return _now_utc().isoformat().replace("+00:00", "Z")


class ModuleError(Exception):
    """Base exception for module errors"""

    pass


class ValidationError(ModuleError):
    """Input validation error"""

    pass


class Module(ABC):
    """
    Base class for HLA-Compass modules.

    All modules should inherit from this class and implement the execute method.
    """

    Input: Optional[Type[BaseModel]] = None

    def __init__(self, manifest_path: Optional[str] = None):
        """
        Initialize module with manifest.

        Args:
            manifest_path: Path to manifest.json file
        """
        self.manifest = self._load_manifest(manifest_path)
        self.name = self.manifest.get("name", "unknown")
        self.version = self.manifest.get("version", "0.0.0")
        
        # If Input model is defined, we can optionally sync the manifest
        if self.Input and not self.manifest.get("inputs"):
             # If inputs are missing from manifest but Input class is defined,
             # we use the Input class to derive schema for validation.
             # However, validation logic below handles this directly.
             pass

        self._base_logger = logging.getLogger(f"hla_compass.module.{self.name}")
        self.logger: logging.Logger | logging.LoggerAdapter = self._base_logger
        self._metadata_parameter_paths = self._load_metadata_parameter_paths()
        self._helpers_initialized = False
        self._context: RuntimeContext | None = None
        self._storage_client = None
        self._db_client = None
        self._offline_mode = False

    def _load_manifest(self, manifest_path: Optional[str] = None) -> Dict[str, Any]:
        """Load module manifest from file"""
        if manifest_path is None:
            manifest_path = Path.cwd() / "manifest.json"
        else:
            manifest_path = Path(manifest_path)

        if not manifest_path.exists():
            return {}

        try:
            with open(manifest_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load manifest: {e}")
            return {}

    def run(
        self, input_data: Dict[str, Any], context: ExecutionContext
    ) -> ModuleOutput:
        """
        Main entry point for module execution.

        This method handles:
        1. Input validation
        2. Execution
        3. Error handling
        4. Result formatting

        Args:
            input_data: Module input parameters
            context: Execution context with API clients

        Returns:
            ModuleOutput with results
        """
        runtime_context = RuntimeContext.coerce(context)
        self._context = runtime_context
        previous_logger = self.logger
        bound_logger = logging.LoggerAdapter(
            self._base_logger,
            {
                "run_id": runtime_context.run_id,
                "module_id": runtime_context.module_id,
                "module_version": runtime_context.module_version,
                "organization_id": runtime_context.organization_id,
                "state_machine_execution_arn": runtime_context.state_machine_execution_arn,
            },
        )
        self.logger = bound_logger

        start_time = _now_utc()
        safe_parameters: Dict[str, Any] = {}

        try:
            # Log execution start
            self.logger.info(
                "Starting module execution",
            )

            # Validate inputs
            self.logger.debug("Validating inputs")
            validated_input = self.validate_inputs(input_data)
            safe_parameters = self._filter_metadata_parameters(validated_input)

            # Initialize data access helpers
            self._initialize_helpers(runtime_context)

            # Execute module logic
            self.logger.debug("Executing module logic")
            results = self.execute(validated_input, runtime_context)

            # Format successful output
            output = self._format_output(
                status="success",
                results=results,
                input_data=validated_input,
                start_time=start_time,
                metadata_parameters=safe_parameters,
            )

            duration = (_now_utc() - start_time).total_seconds()
            log_extra = {"duration": duration}

            if isinstance(results, Sized):
                try:
                    log_extra["result_count"] = len(results)
                except TypeError:
                    pass

            self.logger.info("Module execution completed successfully", extra=log_extra)

            return output

        except ValidationError as e:
            self.logger.error(f"Validation error: {e}")
            error_params = self._filter_metadata_parameters(input_data)
            return self._format_error(
                e,
                "validation_error",
                input_data,
                start_time,
                metadata_parameters=error_params,
            )

        except ModuleError as e:
            self.logger.error(f"Module error: {e}")
            error_params = safe_parameters or self._filter_metadata_parameters(input_data)
            return self._format_error(
                e,
                "module_error",
                input_data,
                start_time,
                metadata_parameters=error_params,
            )

        except Exception as e:
            self.logger.error(f"Unexpected error: {e}", exc_info=True)
            error_params = safe_parameters or self._filter_metadata_parameters(input_data)
            return self._format_error(
                e,
                "internal_error",
                input_data,
                start_time,
                metadata_parameters=error_params,
            )
        finally:
            self.logger = previous_logger

    def _initialize_helpers(self, context: RuntimeContext):
        """Initialize data access helpers"""

        api_client = context.get("api")

        offline_requested = bool(context.get("offline")) or str(
            os.getenv("HLA_COMPASS_OFFLINE", "")
        ).lower() in {"1", "true", "yes"}
        self._offline_mode = offline_requested

        self.peptides = None
        self.proteins = None
        self.samples = None
        self.hla = None
        self.data: Optional[DataClient] = None
        self.storage: Optional[Storage] = None
        self.db = None
        self.has_api_client = False
        self.has_db_client = False
        self.has_storage_client = False

        # If no API client provided, create one for SDK usage
        if not api_client:
            if offline_requested:
                self.logger.info("Offline mode: skipping API client initialization")
                api_client = None
            else:
                from .client import APIClient

                auth = Auth()
                has_token = auth.is_authenticated()
                has_api_key = bool(Config.get_api_key())

                if not (has_token or has_api_key):
                    raise AuthError(
                        "No HLA-Compass API credentials available. "
                        "Set HLA_API_KEY or run 'hla-compass auth login' before executing modules."
                    )
                api_client = APIClient()

        # Initialize database client when RDS Data API env vars are available
        db_client = self._db_client
        if offline_requested:
            self.logger.debug("Offline mode: skipping database client initialization")
        elif db_client is None and os.environ.get("DB_CLUSTER_ARN") and os.environ.get("DB_SECRET_ARN"):
            try:
                from .database import ScientificQuery

                db_client = ScientificQuery(organization_id=context.organization_id)
                self._db_client = db_client
                self.logger.info("Initialized direct database access for module")
            except Exception as e:
                self.logger.warning(f"Could not initialize database client: {e}")

        if db_client:
            self.db = db_client
            self.has_db_client = True

        # Initialize data helpers with both API and database access
        if api_client or db_client:
            # Initialize generic DataClient
            # TODO: Allow manifest to specify which catalog to load?
            # For now, default to the main immunopeptidomics catalog
            self.data = DataClient(provider="alithea-bio", catalog="immunopeptidomics", api_client=api_client)
            
            self.has_api_client = bool(api_client)
            self.has_db_client = bool(db_client)

        storage_client = context.get("storage")
        if not storage_client:
            if offline_requested:
                self.logger.info("Offline mode: storage helper disabled (no client provided)")
            else:
                storage_client = self._build_storage_client(context)

        if storage_client:
            workflow_meta = {
                "workflow_id": context.workflow.workflow_id,
                "workflow_run_id": context.workflow.workflow_run_id,
                "workflow_step_id": context.workflow.workflow_step_id,
            }
            self.storage = Storage(
                storage_client,
                base_prefix=f"files/{context.run_id}/",
                default_metadata={
                    "run_id": context.run_id,
                    "module_id": context.module_id,
                    "organization_id": context.organization_id,
                },
                workflow_metadata=workflow_meta,
            )
            self.has_storage_client = True
            self._storage_client = storage_client

        self._helpers_initialized = True

    def _build_storage_client(self, context: RuntimeContext):
        bucket = os.environ.get("HLA_COMPASS_RESULTS_BUCKET")
        if not bucket:
            self.logger.debug(
                "HLA_COMPASS_RESULTS_BUCKET env var not set; default storage helper disabled."
            )
            return None

        region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
        endpoint = os.environ.get("S3_ENDPOINT_URL")

        try:
            return S3StorageClient(
                bucket=bucket,
                region=region,
                endpoint_url=endpoint,
            )
        except StorageError as exc:
            self.logger.warning("Unable to initialize S3 storage client: %s", exc)
            return None

    @property
    def context(self) -> RuntimeContext:
        """Typed runtime context for the current execution."""
        if self._context is None:
            raise ModuleError(
                "Runtime context is not available. Access self.context inside execute()."
            )
        return self._context

    @property
    def run_id(self) -> str:
        return self.context.run_id

    @property
    def module_id(self) -> str:
        return self.context.module_id

    @property
    def module_version(self) -> str:
        return self.context.module_version

    @property
    def organization_id(self) -> str:
        return self.context.organization_id

    @property
    def user_id(self) -> str:
        return self.context.user_id

    @property
    def environment(self) -> str:
        return self.context.environment

    @property
    def credit(self) -> Optional[CreditReservation]:
        return self.context.credit

    def bootstrap(self) -> Dict[str, Any]:
        """
        Provide a guided overview of available helpers and usage hints.

        Returns a dictionary describing helper availability so modules can
        programmatically inspect capabilities, while also logging human-friendly
        guidance the first time it is invoked.
        """
        info = {
            "module": self.name,
            "version": self.version,
            "helpers": {
                "data": bool(getattr(self, "data", None)),
                "storage": bool(getattr(self, "storage", None)),
            },
            "has_api_client": getattr(self, "has_api_client", False),
            "has_db_client": getattr(self, "has_db_client", False),
            "has_storage_client": getattr(self, "has_storage_client", False),
            "metadata_fields": self._metadata_parameter_paths,
        }

        if not self._helpers_initialized:
            self.logger.warning(
                "Helpers not yet initialized. Call bootstrap after run() or manually invoke _initialize_helpers(context)."
            )
            return info

        friendly_lines = [
            f"Module '{self.name}' bootstrap summary:",
            f"- API client available: {info['has_api_client']}",
            f"- Database client available: {info['has_db_client']}",
            f"- Storage client available: {info['has_storage_client']}",
            "- Data helpers:", 
        ]

        for helper, available in info["helpers"].items():
            usage = "example: self.data.sql.query('SELECT 1')" if helper == "data" else None
            line = f"  • {helper}: {available}"
            if available and usage:
                line += f" ({usage})"
            friendly_lines.append(line)

        metadata_fields = info["metadata_fields"]

        if metadata_fields is None:
            friendly_lines.append(
                "- Metadata parameters exposed: all (exposedParameters enabled)"
            )
        elif metadata_fields:
            friendly_lines.append(
                f"- Metadata parameters exposed: {', '.join(metadata_fields)}"
            )
        else:
            friendly_lines.append(
                "- Metadata parameters exposed: none (add metadata.exposedParameters in manifest to whitelist fields)"
            )

        self.logger.info("\n".join(friendly_lines))
        return info

    def validate_inputs(self, input_data: Dict[str, Any]) -> Union[Dict[str, Any], BaseModel]:
        """
        Validate input data against manifest schema or Pydantic model.

        Supports both JSON Schema format and flat format for backward compatibility.
        If `Input` Pydantic model is defined on the class, it takes precedence.

        Args:
            input_data: Raw input data

        Returns:
            Validated input data (as dict or Pydantic model)

        Raises:
            ValidationError: If validation fails
        """
        # 1. Pydantic Validation (if available)
        if self.Input:
            if PydanticValidationError is None:
                 raise ImportError("Pydantic is required to use 'Input' model definition.")
            try:
                return self.Input(**input_data)
            except PydanticValidationError as e:
                raise ValidationError(str(e))

        # 2. Manifest-based Validation (fallback)
        # Get input schema from manifest
        input_schema = self.manifest.get("inputs", {})

        # Detect schema format
        if input_schema.get("type") == "object" and "properties" in input_schema:
            return self._validate_json_schema(input_data, input_schema)

        return self._validate_flat_schema(input_data, input_schema)

    def sync_manifest(self, manifest_path: Optional[str] = None) -> None:
        """
        Update the manifest.json file with the schema derived from the Input Pydantic model.
        
        Args:
            manifest_path: Path to manifest.json to update. Defaults to CWD/manifest.json
        """
        if not self.Input:
            self.logger.warning("No Input model defined; skipping manifest sync.")
            return

        if PydanticValidationError is None:
             raise ImportError("Pydantic is required to sync manifest.")
             
        if manifest_path is None:
            manifest_path = Path.cwd() / "manifest.json"
        else:
            manifest_path = Path(manifest_path)
            
        # Load existing or create new
        if manifest_path.exists():
            with open(manifest_path, "r") as f:
                try:
                    manifest = json.load(f)
                except json.JSONDecodeError:
                    self.logger.warning(f"Corrupt manifest at {manifest_path}, starting fresh")
                    manifest = {}
        else:
            manifest = {"name": self.name or "unknown-module", "version": "0.1.0"}

        # Auto-detect UI type based on directory structure
        # If "frontend" folder exists alongside the manifest (or parent), it's likely a UI module
        root_dir = manifest_path.parent
        has_frontend = (root_dir / "frontend").exists() or (root_dir.parent / "frontend").exists()
        
        if has_frontend:
            manifest["type"] = "with-ui"
            self.logger.info("Detected frontend directory: setting type='with-ui'")
        else:
            # Only default to no-ui if not set, to preserve manual overrides
            if "type" not in manifest:
                manifest["type"] = "no-ui"
                self.logger.info("No frontend directory detected: setting type='no-ui'")

        # Enforce Docker compute type
        if "compute_config" not in manifest:
            manifest["compute_config"] = {}
        manifest["compute_config"]["type"] = "docker"

        # Generate JSON Schema from Pydantic
        # Pydantic v2
        if hasattr(self.Input, "model_json_schema"):
             schema = self.Input.model_json_schema()
        # Pydantic v1 (fallback)
        elif hasattr(self.Input, "schema"):
             schema = self.Input.schema()
        else:
             raise ModuleError("Input model does not support schema generation")

        # Clean up schema for manifest inclusion (remove $defs if we want inline, 
        # but keeping them is fine for modern JSON schema tools). 
        # Ideally, we want the 'inputs' field to BE the schema object.
        manifest["inputs"] = schema
        
        # Write back
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
            f.write("\n")
        
        self.logger.info(f"Updated manifest inputs schema at {manifest_path}")

    def _validate_json_schema(
        self, input_data: Dict[str, Any], schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        validator = Draft7Validator(schema)
        errors = sorted(validator.iter_errors(input_data), key=lambda e: e.path)

        if errors:
            messages = [self._format_schema_error(error, schema) for error in errors]
            messages.append(f"See {MANIFEST_DOCS_URL} for input schema reference")
            raise ValidationError("; ".join(messages))

        # Apply defaults and return a normalized copy
        normalized = dict(input_data)
        for prop, prop_schema in schema.get("properties", {}).items():
            if prop not in normalized and "default" in prop_schema:
                normalized[prop] = prop_schema["default"]
        return normalized

    def _validate_flat_schema(
        self, input_data: Dict[str, Any], schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        properties = {}
        required: List[str] = []

        for field, field_schema in schema.items():
            json_schema: Dict[str, Any] = {
                key: field_schema[key]
                for key in (
                    "type",
                    "enum",
                    "minimum",
                    "maximum",
                    "minItems",
                    "maxItems",
                    "minLength",
                    "maxLength",
                    "pattern",
                )
                if key in field_schema
            }

            if "min" in field_schema:
                json_schema["minimum"] = field_schema["min"]
            if "max" in field_schema:
                json_schema["maximum"] = field_schema["max"]
            if "default" in field_schema:
                json_schema["default"] = field_schema["default"]

            properties[field] = json_schema

            if field_schema.get("required"):
                required.append(field)

        json_schema_wrapper = {
            "type": "object",
            "properties": properties,
            "required": required,
        }

        return self._validate_json_schema(input_data, json_schema_wrapper)

    def _format_schema_error(self, error, schema: Dict[str, Any]) -> str:
        path_parts = list(error.path)
        path = ".".join(str(p) for p in path_parts)
        field = str(path_parts[-1]) if path_parts else None
        properties = schema.get("properties", {})

        if error.validator == "required":
            # message like "'foo' is a required property"
            missing = None
            if error.message.startswith("'"):
                missing = error.message.split("'")[1]
            missing = missing or field or "unknown"
            suggestion = self._suggest_field(missing, properties)
            hint = f"Missing required field '{missing}'"
            if suggestion and suggestion != missing:
                hint += f" (did you mean '{suggestion}'?)"
            return hint

        if error.validator == "type":
            expected = error.schema.get("type")
            actual = type(error.instance).__name__
            target = path or "value"
            return f"{target} must be of type {expected}, got {actual}"

        if error.validator == "enum":
            allowed = ", ".join(map(str, error.schema.get("enum", [])))
            target = path or field or "value"
            return f"{target} must be one of [{allowed}]"

        if error.validator in {"minimum", "maximum"}:
            target = path or field or "value"
            limit = error.schema.get(error.validator)
            comparator = ">=" if error.validator == "minimum" else "<="
            return f"{target} must be {comparator} {limit}"

        if error.validator == "additionalProperties":
            unexpected = None
            if "'" in error.message:
                parts = error.message.split("'")
                if len(parts) >= 2:
                    unexpected = parts[1]
            unexpected = unexpected or field or "property"
            suggestion = self._suggest_field(unexpected, properties)
            hint = f"Unexpected field '{unexpected}'"
            if suggestion and suggestion != unexpected:
                hint += f" (did you mean '{suggestion}'?)"
            return hint

        if error.validator == "pattern":
            target = path or field or "value"
            pattern = error.schema.get("pattern")
            return f"{target} does not match required pattern {pattern}"

        target = path or field or "value"
        return f"{target}: {error.message}"

    def _suggest_field(self, candidate: str, properties: Dict[str, Any]) -> Optional[str]:
        if not candidate or not properties:
            return None
        matches = get_close_matches(candidate, properties.keys(), n=1, cutoff=0.6)
        return matches[0] if matches else None

    @abstractmethod
    def execute(self, input_data: Union[Dict[str, Any], BaseModel], context: ExecutionContext) -> Any:
        """
        Execute module logic.

        This method must be implemented by all modules.

        Args:
            input_data: Validated input parameters (Dict or Pydantic model)
            context: Execution context with API clients

        Returns:
            Module results (format depends on module)
        """
        pass

    def _format_output(
        self,
        status: str,
        results: Any,
        input_data: dict[str, Any],
        start_time: datetime,
        metadata_parameters: dict[str, Any] | None = None,
    ) -> ModuleOutput:
        """Format module output"""
        duration = (_now_utc() - start_time).total_seconds()

        # Generate summary if not provided
        summary = results.get("summary") if isinstance(results, dict) else None
        if summary is None:
            summary = self._generate_summary(results)

        metadata = {
            "module": self.name,
            "version": self.version,
            "execution_time": _now_utc_iso(),
            "duration_seconds": round(duration, 2),
        }

        if metadata_parameters:
            metadata["parameters"] = metadata_parameters

        return {
            "status": status,
            "results": (
                results
                if not isinstance(results, dict)
                else results.get("results", results)
            ),
            "summary": summary,
            "metadata": metadata,
        }

    def _format_error(
        self,
        error: Exception,
        error_type: str,
        input_data: dict[str, Any],
        start_time: datetime,
        metadata_parameters: dict[str, Any] | None = None,
    ) -> ModuleOutput:
        """Format error output"""
        duration = (_now_utc() - start_time).total_seconds()

        metadata = {
            "module": self.name,
            "version": self.version,
            "execution_time": _now_utc_iso(),
            "duration_seconds": round(duration, 2),
        }

        if metadata_parameters:
            metadata["parameters"] = metadata_parameters

        return {
            "status": "error",
            "error": {
                "type": error_type,
                "message": str(error),
                "details": getattr(error, "details", None),
            },
            "metadata": metadata,
        }

    def _load_metadata_parameter_paths(self) -> Optional[List[str]]:
        metadata_cfg = self.manifest.get("metadata", {})
        exposed = metadata_cfg.get("exposedParameters") or metadata_cfg.get(
            "exposed_parameters"
        )

        if exposed is True or exposed == "*":
            return None

        if not exposed:
            return []

        if not isinstance(exposed, list):
            logger.warning("metadata.exposedParameters must be a list of field names")
            return []

        normalized: list[str] = []
        for item in exposed:
            if isinstance(item, str) and item.strip():
                normalized.append(item.strip())
            else:
                logger.warning("Ignoring invalid metadata.exposedParameters entry: %s", item)
        return normalized

    def _filter_metadata_parameters(
        self, parameters: Any
    ) -> dict[str, Any]:
        if parameters is None:
            return {}
            
        # Handle Pydantic models
        if self.Input and isinstance(parameters, self.Input):
            # Convert to dict for metadata filtering
            # model_dump for v2, dict() for v1
            if hasattr(parameters, "model_dump"):
                parameters = parameters.model_dump()
            else:
                parameters = parameters.dict()
                
        if not isinstance(parameters, Mapping):
            return {}

        allowed = self._metadata_parameter_paths

        if allowed is None:
            return {k: self._copy_value(v) for k, v in parameters.items()}

        if not allowed:
            return {}

        sanitized: dict[str, Any] = {}
        for path in allowed:
            value, found = self._extract_value(parameters, path)
            if found:
                self._assign_value(sanitized, path, self._copy_value(value))
        return sanitized

    def _extract_value(self, data: Mapping[str, Any], path: str) -> tuple[Any, bool]:
        current: Any = data
        for part in path.split("."):
            if not isinstance(current, Mapping) or part not in current:
                return None, False
            current = current[part]
        return current, True

    def _assign_value(self, target: Dict[str, Any], path: str, value: Any) -> None:
        parts = path.split(".")
        current = target
        for part in parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value

    def _copy_value(self, value: Any) -> Any:
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        try:
            return json.loads(json.dumps(value, default=str))
        except (TypeError, ValueError):
            return str(value)

    def _generate_summary(self, results: Any) -> Dict[str, Any]:
        """Generate default summary from results"""
        if isinstance(results, list):
            return {
                "total_results": len(results),
                "execution_time": _now_utc_iso(),
            }
        elif isinstance(results, dict):
            return {
                "total_keys": len(results),
                "execution_time": _now_utc_iso(),
            }
        else:
            return {"execution_time": _now_utc_iso()}

    # Convenience methods

    def success(
        self, results: Any, summary: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Create a success response.

        Args:
            results: Module results
            summary: Optional summary data

        Returns:
            Formatted success response
        """
        output = {"results": results}
        if summary:
            output["summary"] = summary
        return output

    def error(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """
        Raise a module error.

        Args:
            message: Error message
            details: Optional error details
        """
        error = ModuleError(message)
        if details:
            error.details = details
        raise error

    def handle_lambda(self, event: Dict[str, Any], context: Any) -> Dict[str, Any]:
        """
        AWS Lambda handler wrapper

        Args:
            event: Lambda event containing input_data
            context: Lambda context

        Returns:
            Module execution result
        """
        # Extract input data from event
        input_data = event.get("parameters", event.get("input_data", {}))

        # Create execution context
        run_id = event.get(
            "run_id",
            event.get("job_id", context.request_id if hasattr(context, "request_id") else "local"),
        )
        exec_context = {
            "run_id": run_id,
            "job_id": run_id,
            "module_id": event.get("module_id") or self.manifest.get("id") or self.manifest.get("name") or self.name,
            "module_version": event.get("module_version") or self.version,
            "user_id": event.get("user_id") or "local-user",
            "organization_id": event.get("organization_id") or "local-org",
            "roles": event.get("roles") or [],
            "environment": os.getenv("HLA_COMPASS_ENV") or os.getenv("HLA_ENV", "local"),
            "correlation_id": event.get("correlation_id") or run_id,
            "requested_at": _now_utc_iso(),
        }

        # Run module
        return self.run(input_data, exec_context)

    def serve(self, host: str = "0.0.0.0", port: int = 8080) -> None:
        """
        Start a web server to serve the module API and frontend.
        
        This is used for:
        1. Local development (previewing the UI)
        2. Production execution in Fargate (handling session requests)
        
        Args:
            host: Host to bind to (default: 0.0.0.0)
            port: Port to bind to (default: 8080)
        """
        try:
            import uvicorn
            from fastapi import FastAPI, Request, HTTPException
            from fastapi.middleware.cors import CORSMiddleware
            from fastapi.responses import JSONResponse, FileResponse
            from fastapi.staticfiles import StaticFiles
        except ImportError:
            self.logger.error(
                "FastAPI and Uvicorn are required for module serving. "
                "Install them with: pip install 'fastapi' 'uvicorn' 'python-multipart'"
            )
            return

        app = FastAPI(title=self.name, version=self.version)

        # Enable CORS for local dev
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @app.post("/execute")
        async def execute_endpoint(request: Request):
            try:
                body = await request.json()
                input_data = body.get("input", {})
                # In session mode, context is minimal or inferred
                context = {
                    "run_id": "session-" + datetime.now(UTC).strftime("%Y%m%d%H%M%S"),
                    "module_id": self.manifest.get("id", self.name),
                    "mode": "interactive",
                    "environment": os.getenv("HLA_COMPASS_ENV", "local"),
                }
                
                # Execute logic
                output = self.run(input_data, context)
                
                if output.get("status") == "error":
                    error_info = output.get("error", {})
                    raise HTTPException(status_code=500, detail=error_info.get("message", "Module execution failed"))
                    
                return output
            except Exception as e:
                self.logger.error(f"Execution error: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=str(e))

        @app.get("/health")
        async def health():
            return {"status": "ok", "module": self.name}

        # Serve static frontend if available
        frontend_dist = Path.cwd() / "frontend" / "dist"
        if not frontend_dist.exists():
            # Fallback for local dev structure
            frontend_dist = Path.cwd().parent / "frontend" / "dist"

        if frontend_dist.exists():
            self.logger.info(f"Serving frontend from {frontend_dist}")
            app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="static")
        else:
            self.logger.warning("Frontend dist directory not found. Only API endpoints will be available.")

        self.logger.info(f"Starting module server on {host}:{port}")
        uvicorn.run(app, host=host, port=port)
