"""
Security validation module for database queries

Provides query validation, limit enforcement, and security checks
to ensure safe database access for module developers.
"""

import re
import logging
from typing import Tuple, Any

logger = logging.getLogger(__name__)


class QuerySecurityError(Exception):
    """Exception raised for queries that violate security constraints."""

    pass


# SQL keywords that indicate write operations (not allowed)
WRITE_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "CREATE",
    "ALTER",
    "TRUNCATE",
    "GRANT",
    "REVOKE",
    "EXECUTE",
    "CALL",
    "MERGE",
    "REPLACE",
    "UPSERT",
    "COPY",
    "IMPORT",
    "LOAD",
    "VACUUM",
    "ANALYZE",
    "REINDEX",
    "CLUSTER",
}

# SQL keywords that are allowed for read operations
READ_KEYWORDS = {
    "SELECT",
    "WITH",
    "FROM",
    "WHERE",
    "JOIN",
    "INNER",
    "LEFT",
    "RIGHT",
    "FULL",
    "OUTER",
    "ON",
    "AS",
    "AND",
    "OR",
    "NOT",
    "IN",
    "EXISTS",
    "BETWEEN",
    "LIKE",
    "ILIKE",
    "GROUP",
    "BY",
    "HAVING",
    "ORDER",
    "LIMIT",
    "OFFSET",
    "UNION",
    "INTERSECT",
    "EXCEPT",
    "DISTINCT",
}

# Patterns that might indicate injection attempts
SUSPICIOUS_PATTERNS = [
    r";\s*(?:INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)",  # Multiple statements
    r"--[^\n]*(?:INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)",  # Comment injection
    r"/\*.*?\*/",  # Block comments that might hide malicious code
    r"xp_\w+",  # SQL Server extended procedures
    r"sp_\w+",  # SQL Server stored procedures
    r"EXEC\s*\(",  # Execute commands
    r"EXECUTE\s+IMMEDIATE",  # Dynamic SQL execution
    r"dbms_",  # Oracle packages
    r"utl_",  # Oracle utilities
    r"pragma",  # PostgreSQL pragmas
    r"pg_sleep",  # Time-based attacks
    r"sleep\s*\(",  # Sleep functions
    r"benchmark\s*\(",  # MySQL benchmark
    r"waitfor\s+delay",  # SQL Server delay
    r"generate_series",  # Can be used for DoS
    r"repeat\s*\(",  # String repeat (potential DoS)
]

# Allowlist of safe SQL functions for scientific queries
ALLOWED_FUNCTIONS = {
    "COUNT", "SUM", "AVG", "MIN", "MAX", "STDDEV", "VARIANCE",
    "ROUND", "CEIL", "FLOOR", "ABS", "SQRT", "POWER", "MOD",
    "LENGTH", "UPPER", "LOWER", "TRIM", "SUBSTRING", "CONCAT",
    "COALESCE", "NULLIF", "CAST", "EXTRACT", "DATE_PART",
    "TO_CHAR", "TO_DATE", "TO_NUMBER", "TO_TIMESTAMP",
    "NOW", "CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP",
    "ROW_NUMBER", "RANK", "DENSE_RANK", "PERCENT_RANK",
    "LAG", "LEAD", "FIRST_VALUE", "LAST_VALUE",
    "STRING_AGG", "ARRAY_AGG", "JSON_AGG", "JSONB_AGG",
    "JSON_BUILD_OBJECT", "JSON_BUILD_ARRAY",
    "PERCENTILE_CONT", "PERCENTILE_DISC",
    "CORR", "COVAR_POP", "COVAR_SAMP", "REGR_SLOPE"
}


def validate_readonly_query(sql: str) -> bool:
    """
    Validate that a SQL query is read-only and safe to execute.

    Args:
        sql: SQL query string to validate

    Returns:
        True if query is safe, False otherwise

    Raises:
        QuerySecurityError: If query contains dangerous patterns
    """
    if not sql:
        raise QuerySecurityError("Empty query not allowed")

    # Normalize the query for analysis
    normalized = sql.upper().strip()

    # Remove string literals and comments for keyword analysis
    # This prevents false positives from keywords in strings
    cleaned = _remove_literals_and_comments(normalized)

    # Check if query starts with allowed keywords
    if not (cleaned.startswith("SELECT") or cleaned.startswith("WITH")):
        logger.warning("Query rejected: Does not start with SELECT or WITH")
        raise QuerySecurityError("Query must start with SELECT or WITH")

    # Check for write operations
    for keyword in WRITE_KEYWORDS:
        # Look for keyword as a whole word (not part of another word)
        pattern = r"\b" + keyword + r"\b"
        if re.search(pattern, cleaned):
            logger.warning(f"Query rejected: Contains write keyword '{keyword}'")
            raise QuerySecurityError(f"Query contains write operation: {keyword}")

    # Check for suspicious patterns in original query
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, sql, re.IGNORECASE | re.DOTALL):
            logger.warning("Query rejected: Contains suspicious pattern")
            raise QuerySecurityError("Query contains suspicious patterns")

    # Check for multiple statements (even if both are SELECT)
    if _count_statements(sql) > 1:
        logger.warning("Query rejected: Multiple statements not allowed")
        raise QuerySecurityError("Multiple statements not allowed")

    # Additional checks for common injection patterns
    if _has_unbalanced_quotes(sql):
        logger.warning("Query rejected: Unbalanced quotes detected")
        raise QuerySecurityError("Unbalanced quotes detected")

    if _has_hex_encoding(sql):
        logger.warning("Query rejected: Hex encoding detected")
        raise QuerySecurityError("Hex encoding detected")

    logger.debug("Query validated as read-only")
    return True


def enforce_limits(sql: str, max_limit: int = 1000) -> str:
    """
    Enforce a maximum LIMIT on a SQL query.

    If the query doesn't have a LIMIT, adds one.
    If the query has a LIMIT higher than max_limit, reduces it.

    Args:
        sql: SQL query string
        max_limit: Maximum allowed limit

    Returns:
        SQL query with enforced limit
    """
    # Check if query already has a LIMIT clause
    limit_pattern = r"\bLIMIT\s+(\d+)\b"
    limit_match = re.search(limit_pattern, sql, re.IGNORECASE)

    if limit_match:
        # Query has a limit, check if it's within bounds
        current_limit = int(limit_match.group(1))
        if current_limit > max_limit:
            # Replace with max_limit
            sql = re.sub(limit_pattern, f"LIMIT {max_limit}", sql, flags=re.IGNORECASE)
            logger.debug(f"Reduced LIMIT from {current_limit} to {max_limit}")
    else:
        # No limit found, add one
        # Handle different query endings
        sql = sql.rstrip().rstrip(";")

        # Check for OFFSET without LIMIT
        if re.search(r"\bOFFSET\s+\d+\b", sql, re.IGNORECASE):
            # Insert LIMIT before OFFSET
            sql = re.sub(
                r"(\bOFFSET\s+\d+\b)",
                f"LIMIT {max_limit} \\1",
                sql,
                flags=re.IGNORECASE,
            )
        else:
            # Add LIMIT at the end
            sql = f"{sql} LIMIT {max_limit}"

        logger.debug(f"Added LIMIT {max_limit} to query")

    return sql


def validate_function_name(function_name: str) -> bool:
    """
    Validate that a function name is safe to use.

    Args:
        function_name: Function name to validate

    Returns:
        True if function name is safe, False otherwise
    """
    # Basic validation - must be alphanumeric with underscores
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", function_name):
        return False

    # Check length (reasonable limit)
    if len(function_name) > 100:
        return False

    # Normalize function name for comparison
    normalized = function_name.upper().strip()

    # Check against allowlist for known SQL functions
    # Allow custom functions that don't match dangerous patterns
    if normalized in ALLOWED_FUNCTIONS:
        return True

    # Check for dangerous patterns in function names
    dangerous_patterns = [
        "EXEC", "EXECUTE", "SP_", "XP_", "DBMS_", "UTL_",
        "PRAGMA", "SLEEP", "DELAY", "WAITFOR", "BENCHMARK"
    ]
    for pattern in dangerous_patterns:
        if pattern in normalized:
            logger.warning(f"Function '{function_name}' contains dangerous pattern '{pattern}'")
            return False

    # Allow safe custom functions
    return True


def sanitize_identifier(identifier: str) -> str:
    """
    Sanitize a database identifier (table name, column name, etc).

    Args:
        identifier: Identifier to sanitize

    Returns:
        Sanitized identifier safe for use in queries

    Raises:
        QuerySecurityError: If identifier cannot be safely sanitized
    """
    # Remove any quotes
    identifier = identifier.replace('"', "").replace("'", "").replace("`", "")

    # Check if it's a valid identifier
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", identifier):
        raise QuerySecurityError(f"Invalid identifier: {identifier}")

    # Check length
    if len(identifier) > 63:  # PostgreSQL identifier limit
        raise QuerySecurityError(f"Identifier too long: {identifier}")

    return identifier


def _remove_literals_and_comments(sql: str) -> str:
    """Remove string literals and comments from SQL for analysis."""
    # Remove single-line comments
    sql = re.sub(r"--[^\n]*", " ", sql)

    # Remove multi-line comments
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.DOTALL)

    # Remove string literals (both single and double quotes)
    # This is a simplified approach - proper SQL parsing would be more accurate
    sql = re.sub(r"'[^']*'", " ", sql)
    sql = re.sub(r'"[^"]*"', " ", sql)

    return sql


def _count_statements(sql: str) -> int:
    """Count the number of SQL statements in a query."""
    # Remove string literals first to avoid counting semicolons in strings
    cleaned = _remove_literals_and_comments(sql)

    # Split by semicolon and count non-empty statements
    statements = [s.strip() for s in cleaned.split(";") if s.strip()]
    return len(statements)


def _has_unbalanced_quotes(sql: str) -> bool:
    """Check if the query has unbalanced quotes."""
    single_quotes = 0
    double_quotes = 0
    i = 0

    while i < len(sql):
        if sql[i] == "'":
            # Check for escaped quote
            if i + 1 < len(sql) and sql[i + 1] == "'":
                i += 1  # Skip escaped quote
            else:
                single_quotes += 1
        elif sql[i] == '"':
            # Check for escaped quote
            if i + 1 < len(sql) and sql[i + 1] == '"':
                i += 1  # Skip escaped quote
            else:
                double_quotes += 1
        i += 1

    # Both quote counts should be even (pairs)
    return (single_quotes % 2 != 0) or (double_quotes % 2 != 0)


def _has_hex_encoding(sql: str) -> bool:
    """Check if the query contains hex encoding (potential obfuscation)."""
    # Look for hex literals that might be used to obfuscate SQL
    hex_pattern = r"0x[0-9a-fA-F]{4,}"  # At least 4 hex digits

    # Remove legitimate uses (in WHERE clauses with specific columns)
    # This is a simplified check - you might want to be more specific
    cleaned = re.sub(r"WHERE\s+\w+\s*=\s*0x[0-9a-fA-F]+", "", sql, flags=re.IGNORECASE)

    return bool(re.search(hex_pattern, cleaned))


def estimate_query_cost(sql: str) -> Tuple[str, int]:
    """
    Estimate the relative cost/complexity of a query.

    Returns a tuple of (severity, score) where:
    - severity: "low", "medium", "high", or "very_high"
    - score: numeric score (0-100)

    This is a heuristic approach for warning users about potentially expensive queries.
    """
    score = 0

    # Normalize query
    normalized = sql.upper()

    # Check for expensive operations
    if "DISTINCT" in normalized:
        score += 5

    # Count JOINs (each join adds complexity)
    join_count = len(re.findall(r"\bJOIN\b", normalized))
    score += join_count * 10

    # Subqueries are expensive
    subquery_count = normalized.count("(SELECT")
    score += subquery_count * 15

    # CTEs (WITH clauses) add complexity
    if normalized.startswith("WITH"):
        cte_count = len(re.findall(r"\bAS\s*\(", normalized))
        score += cte_count * 8

    # Window functions are expensive
    window_functions = ["ROW_NUMBER", "RANK", "DENSE_RANK", "LAG", "LEAD", "OVER"]
    for func in window_functions:
        if func in normalized:
            score += 12

    # GROUP BY with many columns
    if "GROUP BY" in normalized:
        score += 8
        # Additional penalty for HAVING
        if "HAVING" in normalized:
            score += 5

    # ORDER BY (especially without LIMIT)
    if "ORDER BY" in normalized:
        score += 5
        if "LIMIT" not in normalized:
            score += 10  # Sorting without limit is expensive

    # LIKE with wildcards at the beginning
    if re.search(r"LIKE\s+['\"]%", normalized):
        score += 15  # Leading wildcard prevents index usage

    # UNION operations
    if "UNION" in normalized:
        union_count = len(re.findall(r"\bUNION\b", normalized))
        score += union_count * 10

    # Determine severity level
    if score <= 20:
        severity = "low"
    elif score <= 40:
        severity = "medium"
    elif score <= 60:
        severity = "high"
    else:
        severity = "very_high"

    return severity, min(score, 100)


def create_safe_binding(param_name: str, param_value: Any) -> Tuple[str, Any]:
    """
    Create a safe parameter binding for use in queries.

    Args:
        param_name: Name of the parameter
        param_value: Value of the parameter

    Returns:
        Tuple of (safe_param_name, safe_param_value)
    """
    # Sanitize parameter name
    safe_name = re.sub(r"[^a-zA-Z0-9_]", "", param_name)
    if not safe_name:
        safe_name = "param"

    # Ensure the name starts with a letter
    if safe_name[0].isdigit():
        safe_name = "p" + safe_name

    # The value doesn't need sanitization as it will be properly bound
    # by the database driver, but we can add some basic checks

    # Check for extremely large strings (potential DoS)
    if isinstance(param_value, str) and len(param_value) > 10000:
        logger.warning(f"Large parameter value truncated: {safe_name}")
        param_value = param_value[:10000]

    # Check for extremely large lists
    if isinstance(param_value, list) and len(param_value) > 1000:
        logger.warning(f"Large list parameter truncated: {safe_name}")
        param_value = param_value[:1000]

    return safe_name, param_value
