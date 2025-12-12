"""
Database access module for HLA-Compass SDK

Provides direct database access for modules running in the Lambda environment
with security constraints and optimized query patterns.
"""

from .scientific_query import ScientificQuery
from .security import validate_readonly_query, enforce_limits, QuerySecurityError

__all__ = [
    "ScientificQuery",
    "validate_readonly_query",
    "enforce_limits",
    "QuerySecurityError",
]

__version__ = "1.0.0"
