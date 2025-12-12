"""
Runtime context definitions for HLA-Compass modules.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterator, Mapping, MutableMapping

from .types import ExecutionContext


class ContextValidationError(Exception):
    """Raised when a runtime context payload is invalid."""


def _isoformat(value: datetime | str | None) -> str:
    if value is None:
        return datetime.now(timezone.utc).isoformat()
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return datetime.now(timezone.utc).isoformat()
        return parsed.astimezone(timezone.utc).isoformat()
    return datetime.now(timezone.utc).isoformat()


def _normalize_roles(data: Any) -> tuple[str, ...]:
    roles: list[str] = []
    if isinstance(data, str):
        roles.append(data.strip())
    elif isinstance(data, (list, tuple, set)):
        for entry in data:
            if entry:
                roles.append(str(entry).strip())
    roles = [role for role in roles if role]
    return tuple(dict.fromkeys(roles))


def _ensure_str(value: Any, default: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    if value is not None:
        return str(value)
    return default


@dataclass(frozen=True)
class CreditReservation:
    """Credit reservation metadata embedded in the runtime context."""

    reservation_id: str
    estimated_act: float


@dataclass(frozen=True)
class WorkflowMetadata:
    workflow_id: str | None
    workflow_run_id: str | None
    workflow_step_id: str | None

    @property
    def has_workflow(self) -> bool:
        return any((self.workflow_id, self.workflow_run_id, self.workflow_step_id))


class RuntimeContext(Mapping[str, Any]):
    """
    Canonical runtime context wrapper passed to modules.

    Behaves like a mapping for backward compatibility while exposing typed accessors.
    """

    REQUIRED_FIELDS = (
        "run_id",
        "module_id",
        "module_version",
        "organization_id",
        "user_id",
        "environment",
        "correlation_id",
        "requested_at",
    )

    def __init__(self, payload: Mapping[str, Any]):
        if isinstance(payload, RuntimeContext):
            payload = payload._data

        if not isinstance(payload, Mapping):
            raise ContextValidationError("Context payload must be a mapping.")

        self._data: dict[str, Any] = dict(payload)

        # Fallback normalization for legacy contexts
        legacy_job_id = self._data.get("job_id")
        self._data.setdefault("run_id", legacy_job_id or "local-run")
        self._data.setdefault("module_id", self._data.get("moduleId") or "module-unknown")
        self._data.setdefault("module_version", self._data.get("moduleVersion") or "0.0.0")
        self._data.setdefault("organization_id", self._data.get("organizationId") or "org-unknown")
        self._data.setdefault("user_id", self._data.get("userId") or "user-unknown")
        self._data.setdefault("environment", self._data.get("env") or "unknown")
        self._data.setdefault("correlation_id", self._data.get("correlationId") or self._data["run_id"])
        self._data.setdefault("requested_at", self._data.get("requestedAt") or datetime.now(timezone.utc).isoformat())

        missing = [field for field in self.REQUIRED_FIELDS if not self._data.get(field)]
        if missing:
            raise ContextValidationError(f"Context missing required fields: {', '.join(missing)}")

        self.run_id: str = _ensure_str(self._data["run_id"], "local-run")
        self.module_id: str = _ensure_str(self._data["module_id"], "module-unknown")
        self.module_version: str = _ensure_str(self._data["module_version"], "0.0.0")
        self.organization_id: str = _ensure_str(self._data["organization_id"], "org-unknown")
        self.user_id: str = _ensure_str(self._data["user_id"], "user-unknown")
        self.environment: str = _ensure_str(self._data["environment"], "unknown")
        self.correlation_id: str = _ensure_str(self._data["correlation_id"], self.run_id)
        self.requested_at: str = _isoformat(self._data.get("requested_at"))

        # Optional metadata
        self.roles: tuple[str, ...] = _normalize_roles(
            self._data.get("roles") or self._data.get("role")
        )
        self.mode: str | None = self._data.get("mode")
        self.runtime_profile: str | None = self._data.get("runtime_profile")
        self.tier: str | None = self._data.get("tier")
        execution_arn_value = (
            self._data.get("state_machine_execution_arn")
            or self._data.get("stateMachineExecutionArn")
            or ""
        )
        execution_arn_str = _ensure_str(execution_arn_value, "")
        self.state_machine_execution_arn: str | None = execution_arn_str or None

        credit_payload = self._data.get("credit") or {}
        reservation_id = credit_payload.get("reservation_id") or credit_payload.get("reservationId")
        estimated_act = credit_payload.get("estimated_act") or credit_payload.get("amountAct")
        self.credit: CreditReservation | None = (
            CreditReservation(
                reservation_id=str(reservation_id),
                estimated_act=float(estimated_act),
            )
            if reservation_id and estimated_act is not None
            else None
        )

        self.workflow = WorkflowMetadata(
            workflow_id=_ensure_str(
                self._data.get("workflow_id")
                or self._data.get("workflowId")
                or (self._data.get("workflow") or {}).get("id"),
                "",
            )
            or None,
            workflow_run_id=_ensure_str(
                self._data.get("workflow_run_id")
                or self._data.get("workflowRunId")
                or (self._data.get("workflow") or {}).get("run_id"),
                "",
            )
            or None,
            workflow_step_id=_ensure_str(
                self._data.get("workflow_step_id")
                or self._data.get("workflowStepId")
                or (self._data.get("workflow") or {}).get("step_id"),
                "",
            )
            or None,
        )

    @classmethod
    def coerce(cls, payload: ExecutionContext | Mapping[str, Any] | None) -> RuntimeContext:
        """
        Coerce arbitrary payloads (dict or RuntimeContext) into a RuntimeContext instance.
        """
        if payload is None:
            payload = {}
        return cls(payload)

    def copy_data(self) -> dict[str, Any]:
        """Return a shallow copy of the underlying mapping."""
        return dict(self._data)

    def __getitem__(self, key: str) -> Any:  # Mapping protocol
        return self._data[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def with_updates(self, updates: Mapping[str, Any]) -> RuntimeContext:
        """Return a new runtime context with additional keys merged in."""
        merged: MutableMapping[str, Any] = dict(self._data)
        merged.update(updates)
        return RuntimeContext(merged)


__all__ = [
    "RuntimeContext",
    "ContextValidationError",
    "CreditReservation",
    "WorkflowMetadata",
]

