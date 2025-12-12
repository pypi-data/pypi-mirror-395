"""
Type definitions for HLA-Compass SDK
"""

from typing import Any, Union, TypedDict, Literal, NotRequired, Optional, List, Dict
from enum import Enum
from datetime import datetime


# Execution context type
class CreditContext(TypedDict, total=False):
    """Credit reservation data passed to runtimes."""

    reservation_id: str
    estimated_act: float


class ExecutionContext(TypedDict, total=False):
    """Execution context provided to modules.

    Legacy keys remain optional for backward compatibility. RuntimeContext
    (sdk/python/hla_compass/context.py) normalizes these values.
    """

    run_id: NotRequired[str]
    job_id: str
    user_id: NotRequired[str]
    organization_id: NotRequired[str]
    module_id: NotRequired[str]
    module_version: NotRequired[str]
    roles: NotRequired[List[str]]
    environment: NotRequired[str]
    correlation_id: NotRequired[str]
    requested_at: NotRequired[str]
    tier: NotRequired[str]
    mode: NotRequired[str]
    runtime_profile: NotRequired[str]
    state_machine_execution_arn: NotRequired[str]
    credit: NotRequired[CreditContext]
    workflow_id: NotRequired[str]
    workflow_run_id: NotRequired[str]
    workflow_step_id: NotRequired[str]
    api: NotRequired[Any]  # API client instance
    storage: NotRequired[Any]  # Storage client instance
    execution_time: NotRequired[datetime]


# Module types
ModuleInput = Dict[str, Any]
ModuleOutput = Dict[str, Any]


# Job status enum
class JobStatus(str, Enum):
    """Job execution status"""

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# Compute type enum
class ComputeType(str, Enum):
    """Module compute type"""

    DOCKER = "docker"


# Module type enum
class ModuleType(str, Enum):
    """Module UI type"""

    NO_UI = "no-ui"
    WITH_UI = "with-ui"


# Data types
class Peptide(TypedDict):
    """Peptide data structure"""

    id: str
    sequence: str
    length: int
    mass: float
    charge: Optional[int]
    modifications: Optional[List[str]]
    metadata: Optional[Dict[str, Any]]


class Protein(TypedDict):
    """Protein data structure"""

    id: str
    accession: str
    gene_name: Optional[str]
    organism: str
    sequence: str
    length: int
    description: Optional[str]
    metadata: Optional[Dict[str, Any]]


class Sample(TypedDict):
    """Sample data structure"""

    id: str
    name: str
    sample_type: str
    tissue: Optional[str]
    disease: Optional[str]
    cell_line: Optional[str]
    treatment: Optional[str]
    experiment_type: str
    metadata: Optional[Dict[str, Any]]


class PeptideSample(TypedDict):
    """Peptide-sample association"""

    peptide_id: str
    sample_id: str
    abundance: float
    confidence: Optional[float]
    metadata: Optional[Dict[str, Any]]


# API response types
class APIResponse(TypedDict):
    """Standard API response"""

    status: Literal["success", "error"]
    data: Optional[Any]
    error: Optional[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]]


class PaginatedResponse(TypedDict):
    """Paginated API response"""

    results: List[Any]
    total: int
    limit: int
    offset: int
    has_more: bool


# Module manifest types
class ManifestAuthor(TypedDict):
    """Module author information"""

    name: str
    email: str
    organization: Optional[str]


class ManifestInputField(TypedDict, total=False):
    """Input field definition"""

    type: str
    required: bool
    description: str
    default: Any
    min: Optional[Union[int, float]]
    max: Optional[Union[int, float]]
    enum: Optional[List[Any]]


class ManifestComputeRequirements(TypedDict):
    """Compute requirements"""

    memory: int  # MB
    timeout: int  # seconds
    environment: str  # e.g., "python3.11"
    gpu: Optional[bool]


class ModulePricingEntry(TypedDict, total=False):
    """Normalized module pricing entry"""

    tier: Literal["developer", "foundational", "advanced", "strategic"]
    model: Literal["subscription", "usage-based"]
    amountAct: float
    currency: Literal["ACT"]
    source: Literal["manifest", "override"]
    effectiveFrom: Optional[str]
    effectiveThrough: Optional[str]
    modificationReason: Optional[str]
    version: Optional[str]
    modifiedBy: Optional[str]
    pricingId: Optional[str]
    rowVersion: Optional[int]


class ModulePricingBreakdown(TypedDict):
    manifest: List[ModulePricingEntry]
    overrides: List[ModulePricingEntry]
    effective: List[ModulePricingEntry]


class ModuleManifest(TypedDict):
    """Module manifest structure"""

    name: str
    version: str
    displayName: str
    description: str
    author: ManifestAuthor
    type: Literal["no-ui", "with-ui"]
    computeType: Literal["docker"]
    computeRequirements: ManifestComputeRequirements
    inputs: Dict[str, ManifestInputField]
    outputs: Dict[str, Any]
    dependencies: Dict[str, List[str]]
    permissions: Dict[str, List[str]]
    tags: List[str]
    category: str
    pricing: Optional[ModulePricingBreakdown]
    support: Optional[Dict[str, str]]


# Error types
class ErrorDetail(TypedDict):
    """Error detail structure"""

    code: str
    message: str
    field: Optional[str]
    details: Optional[Dict[str, Any]]


# Storage types
class StorageObject(TypedDict):
    """Storage object metadata"""

    key: str
    size: int
    last_modified: datetime
    content_type: str
    etag: Optional[str]
    metadata: Optional[Dict[str, str]]


# HLA-specific types
HLAAllele = str  # e.g., "HLA-A*02:01"
HLALocus = Literal[
    "A", "B", "C", "DRB1", "DRB3", "DRB4", "DRB5", "DQA1", "DQB1", "DPA1", "DPB1"
]


class HLAPrediction(TypedDict):
    """HLA binding prediction result"""

    peptide: str
    allele: HLAAllele
    score: float
    rank: float
    binding_category: Literal["strong", "weak", "non-binder"]
    method: str


# Execution types
class ExecutionOptions(TypedDict, total=False):
    """Module execution options"""

    priority: Literal["low", "normal", "high"]
    timeout: int
    memory: int
    notifications: bool
    webhook_url: Optional[str]


class ExecutionResult(TypedDict):
    """Module execution result"""

    job_id: str
    status: JobStatus
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    result: Optional[ModuleOutput]
    error: Optional[ErrorDetail]
    metadata: Dict[str, Any]
