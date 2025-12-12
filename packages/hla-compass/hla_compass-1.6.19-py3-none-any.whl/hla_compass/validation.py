"""Module manifest validation helpers."""

from __future__ import annotations

import importlib
import json
import pkgutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

import jsonschema

from .manifest import load_manifest_schema


ValidationSeverity = str


@dataclass
class ValidationIssue:
    severity: ValidationSeverity
    code: str
    message: str
    pointer: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
        }
        if self.pointer:
            payload["pointer"] = self.pointer
        return payload


class ValidationResult:
    """Container for validation issues and metadata."""

    def __init__(
        self,
        *,
        manifest_path: Path,
        manifest: Optional[Dict[str, Any]],
        issues: List[ValidationIssue],
        checks: Sequence[str],
    ) -> None:
        self.manifest_path = manifest_path
        self.manifest = manifest or {}
        self.issues = issues
        self.checks = list(checks)

    @property
    def errors(self) -> List[ValidationIssue]:
        return [issue for issue in self.issues if issue.severity == "error"]

    @property
    def warnings(self) -> List[ValidationIssue]:
        return [issue for issue in self.issues if issue.severity == "warning"]

    @property
    def valid(self) -> bool:
        return not self.errors

    def add_issue(self, issue: ValidationIssue) -> None:
        self.issues.append(issue)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.valid,
            "manifestPath": str(self.manifest_path),
            "checks": self.checks,
            "issues": [issue.to_dict() for issue in self.issues],
        }


class ModuleValidator:
    """Performs layered validation against module manifests and project layout."""

    AVAILABLE_CHECKS: Sequence[str] = (
        "schema",
        "structure",
        "entrypoint",
        "ui",
        "security",
        "pricing",
        "openapi",
    )

    def __init__(
        self,
        manifest_path: Path | str = "manifest.json",
        *,
        openapi_path: Path | str | None = None,
    ) -> None:
        manifest_path = Path(manifest_path)
        if not manifest_path.is_absolute():
            manifest_path = Path.cwd() / manifest_path
        self.manifest_path = manifest_path
        self.module_dir = self.manifest_path.parent.resolve()
        self.openapi_path = Path(openapi_path) if openapi_path else None
        self._manifest_error: Optional[str] = None

    def run(
        self,
        *,
        checks: Iterable[str] | None = None,
        strict: bool = False,
    ) -> ValidationResult:
        active_checks: List[str] = list(checks) if checks else list(self.AVAILABLE_CHECKS)
        manifest = self._load_manifest()
        issues: List[ValidationIssue] = []

        if manifest is None:
            if self._manifest_error:
                issues.append(
                    ValidationIssue(
                        severity="error",
                        code="manifest.invalid",
                        message=self._manifest_error,
                    )
                )
            else:
                issues.append(
                    ValidationIssue(
                        severity="error",
                        code="manifest.not_found",
                        message=f"Manifest file not found at {self.manifest_path}",
                    )
                )
            return ValidationResult(
                manifest_path=self.manifest_path,
                manifest=None,
                issues=issues,
                checks=active_checks,
            )

        if "schema" in active_checks:
            issues.extend(self._check_schema(manifest))
        if "structure" in active_checks:
            issues.extend(self._check_structure(manifest))
        if "entrypoint" in active_checks:
            issues.extend(self._check_entrypoint(manifest))
        if "ui" in active_checks:
            issues.extend(self._check_ui(manifest))
        if "security" in active_checks:
            issues.extend(self._check_security(manifest, strict=strict))
        if "pricing" in active_checks:
            issues.extend(self._check_pricing(manifest, strict=strict))
        if "openapi" in active_checks:
            issues.extend(self._check_openapi(manifest, strict=strict))

        return ValidationResult(
            manifest_path=self.manifest_path,
            manifest=manifest,
            issues=issues,
            checks=active_checks,
        )

    # ---- individual checks -------------------------------------------------

    def _load_manifest(self) -> Optional[Dict[str, Any]]:
        if not self.manifest_path.exists():
            return None
        try:
            return json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            self._manifest_error = f"Invalid JSON in manifest: {exc}"
            return None

    def _check_schema(self, manifest: Dict[str, Any]) -> List[ValidationIssue]:
        issues: List[ValidationIssue] = []
        schema = load_manifest_schema()
        validator = jsonschema.Draft7Validator(schema)
        for error in sorted(validator.iter_errors(manifest), key=lambda e: e.path):
            pointer = "/" + "/".join(str(entry) for entry in error.absolute_path) if error.absolute_path else None
            issues.append(
                ValidationIssue(
                    severity="error",
                    code="schema.invalid",
                    message=error.message,
                    pointer=pointer,
                )
            )
        return issues

    def _check_structure(self, manifest: Dict[str, Any]) -> List[ValidationIssue]:
        issues: List[ValidationIssue] = []
        backend_dir = self.module_dir / "backend"
        if not backend_dir.exists():
            issues.append(
                ValidationIssue(
                    severity="error",
                    code="structure.backend_missing",
                    message="backend/ directory not found",
                    pointer="/backend",
                )
            )
        else:
            if not (backend_dir / "main.py").exists():
                issues.append(
                    ValidationIssue(
                        severity="error",
                        code="structure.entrypoint_missing",
                        message="backend/main.py not found",
                        pointer="/backend/main.py",
                    )
                )
            if not (backend_dir / "requirements.txt").exists():
                issues.append(
                    ValidationIssue(
                        severity="warning",
                        code="structure.requirements_missing",
                        message="backend/requirements.txt not found",
                        pointer="/backend/requirements.txt",
                    )
                )

        examples_dir = self.module_dir / "examples"
        if not examples_dir.exists():
            issues.append(
                ValidationIssue(
                    severity="warning",
                    code="structure.examples_missing",
                    message="examples/ directory not found (recommended for sample payloads)",
                    pointer="/examples",
                )
            )

        return issues

    def _check_entrypoint(self, manifest: Dict[str, Any]) -> List[ValidationIssue]:
        issues: List[ValidationIssue] = []
        execution = manifest.get("execution") or {}
        entrypoint = execution.get("entrypoint") or manifest.get("entrypoint")
        if not entrypoint:
            issues.append(
                ValidationIssue(
                    severity="error",
                    code="entrypoint.missing",
                    message="execution.entrypoint is required (e.g., backend.main:Module)",
                    pointer="/execution/entrypoint",
                )
            )
            return issues

        if ":" not in entrypoint:
            issues.append(
                ValidationIssue(
                    severity="error",
                    code="entrypoint.invalid",
                    message="Entrypoint must be in 'module:ClassName' format",
                    pointer="/execution/entrypoint",
                )
            )
            return issues

        module_name, class_name = entrypoint.split(":", 1)
        sys_path_added = False
        if str(self.module_dir) not in sys.path:
            sys.path.insert(0, str(self.module_dir))
            sys_path_added = True

        try:
            root_package = module_name.split(".", 1)[0]
            for name in list(sys.modules.keys()):
                if name == module_name or name == root_package or name.startswith(f"{root_package}."):
                    sys.modules.pop(name)
            module = importlib.import_module(module_name)
            attr = getattr(module, class_name)
            from .module import Module as BaseModule  # Local import to avoid cycle

            if not isinstance(attr, type) or not issubclass(attr, BaseModule):
                issues.append(
                    ValidationIssue(
                        severity="warning",
                        code="entrypoint.not_subclass",
                        message="Entrypoint does not inherit from hla_compass.module.Module",
                        pointer="/execution/entrypoint",
                    )
                )
        except Exception as exc:
            issues.append(
                ValidationIssue(
                    severity="warning",
                    code="entrypoint.import_failed",
                    message=f"Unable to import entrypoint '{entrypoint}': {exc}",
                    pointer="/execution/entrypoint",
                )
            )
        finally:
            if sys_path_added and str(self.module_dir) in sys.path:
                sys.path.remove(str(self.module_dir))

        return issues

    def _check_ui(self, manifest: Dict[str, Any]) -> List[ValidationIssue]:
        issues: List[ValidationIssue] = []
        if manifest.get("type") != "with-ui":
            return issues

        frontend_dir = self.module_dir / "frontend"
        if not frontend_dir.exists():
            issues.append(
                ValidationIssue(
                    severity="error",
                    code="ui.frontend_missing",
                    message="Frontend directory required for with-ui modules",
                    pointer="/frontend",
                )
            )
        else:
            bundle_entry = frontend_dir / "index.tsx"
            if not bundle_entry.exists():
                issues.append(
                    ValidationIssue(
                        severity="warning",
                        code="ui.entry_missing",
                        message="frontend/index.tsx not found (UMD entry is required)",
                        pointer="/frontend/index.tsx",
                    )
                )

        return issues

    def _check_security(self, manifest: Dict[str, Any], *, strict: bool) -> List[ValidationIssue]:
        issues: List[ValidationIssue] = []
        permissions = manifest.get("permissions") or {}
        db_perms = permissions.get("database") or []
        if any(str(perm).lower() == "delete" for perm in db_perms):
            issues.append(
                ValidationIssue(
                    severity="error" if strict else "warning",
                    code="security.database_delete",
                    message="Database permission 'delete' requested; ensure this is intentional",
                    pointer="/permissions/database",
                )
            )

        network_perms = permissions.get("network") or []
        if any(entry in {"*", "0.0.0.0/0"} for entry in network_perms):
            issues.append(
                ValidationIssue(
                    severity="error" if strict else "warning",
                    code="security.network_wildcard",
                    message="Wildcard network access requested; restrict to specific domains",
                    pointer="/permissions/network",
                )
            )

        resources = manifest.get("resources") or {}
        timeout = resources.get("timeout")
        if isinstance(timeout, (int, float)) and not (3 <= timeout <= 900):
            issues.append(
                ValidationIssue(
                    severity="error",
                    code="security.timeout_out_of_range",
                    message="resources.timeout must be between 3 and 900 seconds",
                    pointer="/resources/timeout",
                )
            )

        return issues

    def _check_pricing(self, manifest: Dict[str, Any], *, strict: bool) -> List[ValidationIssue]:
        issues: List[ValidationIssue] = []
        tiers = (manifest.get("pricing") or {}).get("tiers") or []
        if not tiers:
            issues.append(
                ValidationIssue(
                    severity="error" if strict else "warning",
                    code="pricing.tiers_missing",
                    message="Pricing tiers are required before publishing",
                    pointer="/pricing/tiers",
                )
            )
            return issues

        for index, tier in enumerate(tiers):
            amount = tier.get("amountAct")
            if amount in (None, ""):
                issues.append(
                    ValidationIssue(
                        severity="error",
                        code="pricing.amount_missing",
                        message=f"Tier entry #{index + 1} is missing amountAct",
                        pointer=f"/pricing/tiers/{index}/amountAct",
                    )
                )

        return issues

    def _check_openapi(self, manifest: Dict[str, Any], *, strict: bool) -> List[ValidationIssue]:
        spec = self._load_openapi_spec()
        if not spec:
            return [
                ValidationIssue(
                    severity="warning",
                    code="openapi.unavailable",
                    message="OpenAPI document not found; run scripts/docs-generate-openapi.py",
                )
            ]

        issues: List[ValidationIssue] = []
        components = spec.get("components", {}).get("schemas", {})
        manifest_schema = components.get("ModuleManifest", {})
        required_fields = manifest_schema.get("required", [])
        missing = [field for field in required_fields if field not in manifest]
        for field in missing:
            issues.append(
                ValidationIssue(
                    severity="error" if strict else "warning",
                    code="openapi.missing_required_field",
                    message=f"Manifest missing field required by OpenAPI contract: {field}",
                    pointer=f"/{field}",
                )
            )

        schema_version = manifest.get("schemaVersion")
        documented_version = spec.get("info", {}).get("version")
        if schema_version and documented_version and str(schema_version) != str(documented_version):
            issues.append(
                ValidationIssue(
                    severity="warning",
                    code="openapi.schema_version_mismatch",
                    message=f"schemaVersion {schema_version} differs from documented version {documented_version}",
                    pointer="/schemaVersion",
                )
            )

        return issues

    def _load_openapi_spec(self) -> Optional[Dict[str, Any]]:
        candidates: List[Path] = []
        if self.openapi_path:
            candidates.append(self.openapi_path)

        cwd_candidate = Path.cwd() / "docs" / "api" / "openapi.mini.json"
        repo_candidate = Path(__file__).resolve().parents[3] / "docs" / "api" / "openapi.mini.json"
        candidates.extend([cwd_candidate, repo_candidate])

        for candidate in candidates:
            if candidate.exists():
                try:
                    return json.loads(candidate.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    continue

        data = pkgutil.get_data("hla_compass", "data/openapi.mini.json")
        if data:
            try:
                return json.loads(data.decode("utf-8"))
            except json.JSONDecodeError:
                return None

        return None
