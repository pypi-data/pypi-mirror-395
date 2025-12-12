"""
HLA-Compass Python SDK

SDK for developing modules on the HLA-Compass platform.
"""

from ._version import __version__

# Core module base class
from .module import Module, ModuleError, ValidationError

# Data access classes
from .data import DataClient, DataAccessError

# Data models
from .models import Peptide, Protein, Sample, BindingPrediction

# Authentication
from .auth import Auth, AuthError

# Storage utilities
from .storage import Storage, StorageError

# Runtime context
from .context import RuntimeContext, ContextValidationError, CreditReservation, WorkflowMetadata

# Testing utilities
from .testing import ModuleTester, MockContext, MockAPI

# CLI utilities
from .cli import main as cli_main

# Types
from .types import (
    ExecutionContext,
    ModuleInput,
    ModuleOutput,
    JobStatus,
    ComputeType,
    ModuleType,
)

# Constants
from .constants import (
    SUPPORTED_HLA_ALLELES,
    AMINO_ACIDS,
    MAX_PEPTIDE_LENGTH,
    MIN_PEPTIDE_LENGTH,
    DOCS_URLS,
    doc_link,
)

__all__ = [
    # Version
    "__version__",
    # Core classes
    "Module",
    "ModuleError",
    "ValidationError",
    # Data access
    "DataClient",
    "DataAccessError",
    "Peptide",
    "Protein",
    "Sample",
    "BindingPrediction",
    # Auth
    "Auth",
    "AuthError",
    # Storage
    "Storage",
    "StorageError",
    # Context
    "RuntimeContext",
    "ContextValidationError",
    "CreditReservation",
    "WorkflowMetadata",
    # Testing
    "ModuleTester",
    "MockContext",
    "MockAPI",
    # CLI
    "cli_main",
    # Types
    "ExecutionContext",
    "ModuleInput",
    "ModuleOutput",
    "JobStatus",
    "ComputeType",
    "ModuleType",
    # Constants
    "SUPPORTED_HLA_ALLELES",
    "AMINO_ACIDS",
    "MAX_PEPTIDE_LENGTH",
    "MIN_PEPTIDE_LENGTH",
    "DOCS_URLS",
    "doc_link",
]
