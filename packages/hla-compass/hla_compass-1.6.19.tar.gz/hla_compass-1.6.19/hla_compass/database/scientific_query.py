"""
Scientific database query module using AWS RDS Data API

Provides safe, parameterized access to the scientific database
for module developers with automatic security constraints.
"""

import os
import boto3
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, date
import json

from .security import validate_readonly_query, enforce_limits, QuerySecurityError

logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Base exception for database errors"""

    pass


class ScientificQuery:
    """
    Database query interface for scientific data access.

    This class provides safe, read-only access to the scientific database
    using AWS RDS Data API with built-in security constraints and optimizations.
    """

    def __init__(
        self,
        cluster_arn: Optional[str] = None,
        secret_arn: Optional[str] = None,
        database: str = "hla_compass",
        region: Optional[str] = None,
        max_limit: int = 1000,
        timeout_ms: int = 10000,
        organization_id: Optional[str] = None,
    ):
        """
        Initialize the ScientificQuery client.

        Args:
            cluster_arn: Aurora cluster ARN (defaults to env var DB_CLUSTER_ARN)
            secret_arn: Database credentials secret ARN (defaults to env var DB_SECRET_ARN)
            database: Database name (default: hla_compass)
            region: AWS region (defaults to env var AWS_REGION)
            max_limit: Maximum allowed result limit (default: 1000)
            timeout_ms: Query timeout in milliseconds (default: 10000)
        """
        # Get configuration from environment if not provided
        self.cluster_arn = cluster_arn or os.environ.get("DB_CLUSTER_ARN")
        self.secret_arn = secret_arn or os.environ.get("DB_SECRET_ARN")
        self.database = database
        self.region = region or os.environ.get("AWS_REGION", "eu-central-1")
        self.max_limit = max_limit
        self.timeout_ms = timeout_ms
        self.organization_id = organization_id or os.environ.get("HLA_COMPASS_ORGANIZATION_ID")

        # Validate configuration
        if not self.cluster_arn:
            raise DatabaseError(
                "DB_CLUSTER_ARN environment variable or cluster_arn parameter is required"
            )
        if not self.secret_arn:
            raise DatabaseError(
                "DB_SECRET_ARN environment variable or secret_arn parameter is required"
            )

        # Initialize RDS Data API client
        try:
            self.client = boto3.client("rds-data", region_name=self.region)
            logger.info(f"Initialized ScientificQuery client for region {self.region}")
        except Exception as e:
            logger.error(f"Failed to initialize RDS Data API client: {e}")
            raise DatabaseError(f"Failed to initialize database client: {e}")

        # Cache for function existence checks
        self._function_cache = set()
        self._cache_loaded = False

    def execute_function(
        self, function_name: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute a predefined PostgreSQL function from the scientific schema.

        Args:
            function_name: Name of the function (without schema prefix)
            params: Dictionary of named parameters for the function

        Returns:
            List of result dictionaries

        Raises:
            DatabaseError: If function execution fails
            QuerySecurityError: If function is not allowed
        """
        # Validate function name (alphanumeric and underscore only)
        if not function_name.replace("_", "").isalnum():
            raise QuerySecurityError(f"Invalid function name: {function_name}")

        # Build function call SQL
        full_function_name = f"scientific.{function_name}"

        if params:
            # Build parameter list for function call
            param_names = list(params.keys())
            param_placeholders = ", ".join([f":{name}" for name in param_names])
            sql = f"SELECT * FROM {full_function_name}({param_placeholders})"  # nosec B608: full_function_name is validated and parameters are bound
        else:
            sql = f"SELECT * FROM {full_function_name}()"  # nosec B608: full_function_name is validated

        logger.debug(
            f"Executing function: {function_name} with {len(params) if params else 0} parameters"
        )

        transaction_id: Optional[str] = None
        try:
            # Convert parameters to RDS Data API format
            rds_params = self._convert_parameters(params) if params else []

            # Begin scoped transaction if org-level RLS is required
            transaction_id = self._begin_scoped_transaction()

            # Execute the statement
            response = self.client.execute_statement(
                resourceArn=self.cluster_arn,
                secretArn=self.secret_arn,
                database=self.database,
                sql=sql,
                parameters=rds_params,
                continueAfterTimeout=False,
                includeResultMetadata=True,
                transactionId=transaction_id,
            )

            # Parse and return results
            results = self._parse_results(response)
            logger.info(f"Function {function_name} returned {len(results)} results")

            if transaction_id:
                self._commit_transaction(transaction_id)

            return results

        except self.client.exceptions.BadRequestException as e:
            error_msg = str(e)
            if "permission denied" in error_msg.lower():
                raise QuerySecurityError(
                    f"Permission denied for function {function_name}"
                )
            elif "does not exist" in error_msg.lower():
                raise DatabaseError(f"Function {function_name} does not exist")
            else:
                raise DatabaseError(
                    f"Failed to execute function {function_name}: {error_msg}"
                )
        except Exception as e:
            if transaction_id:
                self._rollback_transaction(transaction_id)
            logger.error(f"Error executing function {function_name}: {e}")
            raise DatabaseError(f"Database error: {str(e)}")

    def execute_readonly(
        self,
        sql: str,
        params: Optional[Union[Dict[str, Any], List[Any]]] = None,
        auto_limit: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Execute a read-only SQL query with security validation.

        Args:
            sql: SQL query string (must be SELECT or WITH)
            params: Dictionary of named parameters or list of positional parameters
            auto_limit: Automatically add LIMIT if not present (default: True)

        Returns:
            List of result dictionaries

        Raises:
            QuerySecurityError: If query violates security constraints
            DatabaseError: If query execution fails
        """
        # Validate query is read-only
        if not validate_readonly_query(sql):
            raise QuerySecurityError("Only SELECT and WITH queries are allowed")

        # Enforce limits if requested
        if auto_limit:
            sql = enforce_limits(sql, self.max_limit)

        logger.debug(
            f"Executing read-only query with {len(params) if params else 0} parameters"
        )

        transaction_id: Optional[str] = None
        try:
            # Convert parameters to RDS Data API format
            rds_params = []

            if params:
                if isinstance(params, dict):
                    # Named parameters - already in correct format for RDS Data API
                    rds_params = self._convert_parameters(params)
                else:
                    # Positional parameters - convert to named format
                    for i, value in enumerate(params):
                        # Replace %s with :param1, :param2, etc.
                        param_name = f"param{i + 1}"
                        sql = sql.replace("%s", f":{param_name}", 1)
                        rds_params.append(
                            self._convert_single_parameter(param_name, value)
                        )

            # Begin scoped transaction if org-level filtering is needed
            transaction_id = self._begin_scoped_transaction()

            # Execute the statement
            response = self.client.execute_statement(
                resourceArn=self.cluster_arn,
                secretArn=self.secret_arn,
                database=self.database,
                sql=sql,
                parameters=rds_params,
                continueAfterTimeout=False,
                includeResultMetadata=True,
                transactionId=transaction_id,
            )

            # Parse and return results
            results = self._parse_results(response)
            logger.info(f"Query returned {len(results)} results")

            if transaction_id:
                self._commit_transaction(transaction_id)

            return results

        except self.client.exceptions.BadRequestException as e:
            error_msg = str(e)
            if "permission denied" in error_msg.lower():
                raise QuerySecurityError("Permission denied for this query")
            elif "syntax error" in error_msg.lower():
                raise DatabaseError(f"SQL syntax error: {error_msg}")
            elif "timeout" in error_msg.lower():
                raise DatabaseError(f"Query timeout exceeded ({self.timeout_ms}ms)")
            else:
                raise DatabaseError(f"Query execution failed: {error_msg}")
        except Exception as e:
            if transaction_id:
                self._rollback_transaction(transaction_id)
            logger.error(f"Error executing query: {e}")
            raise DatabaseError(f"Database error: {str(e)}")

    def list_available_functions(self) -> List[str]:
        """
        List all available scientific schema functions.

        Returns:
            List of function names
        """
        if not self._cache_loaded:
            try:
                sql = """
                    SELECT routine_name
                    FROM information_schema.routines
                    WHERE routine_schema = 'scientific'
                    AND routine_type = 'FUNCTION'
                    ORDER BY routine_name
                """

                response = self.client.execute_statement(
                    resourceArn=self.cluster_arn,
                    secretArn=self.secret_arn,
                    database=self.database,
                    sql=sql,
                    includeResultMetadata=False,
                )

                self._function_cache = {
                    record[0]["stringValue"]
                    for record in response.get("records", [])
                    if record and record[0].get("stringValue")
                }
                self._cache_loaded = True

            except Exception as e:
                logger.warning(f"Could not load function list: {e}")
                return []

        return sorted(list(self._function_cache))

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics using the get_sample_statistics function.

        Returns:
            Dictionary with database statistics
        """
        try:
            results = self.execute_function("get_sample_statistics")
            return results[0] if results else {}
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {}

    def _convert_parameters(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convert Python parameters to RDS Data API format."""
        return [
            self._convert_single_parameter(name, value)
            for name, value in params.items()
        ]

    def _convert_single_parameter(self, name: str, value: Any) -> Dict[str, Any]:
        """Convert a single parameter to RDS Data API format."""
        param = {"name": name}

        if value is None:
            param["value"] = {"isNull": True}
        elif isinstance(value, bool):
            param["value"] = {"booleanValue": value}
        elif isinstance(value, int):
            param["value"] = {"longValue": value}
        elif isinstance(value, float):
            param["value"] = {"doubleValue": value}
        elif isinstance(value, str):
            param["value"] = {"stringValue": value}
        elif isinstance(value, bytes):
            param["value"] = {"blobValue": value}
        elif isinstance(value, (datetime, date)):
            param["value"] = {"stringValue": value.isoformat()}
        elif isinstance(value, (list, dict)):
            # Convert complex types to JSON string
            param["value"] = {"stringValue": json.dumps(value)}
        else:
            # Convert unknown types to string
            param["value"] = {"stringValue": str(value)}

        return param

    def _parse_results(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse RDS Data API response into list of dictionaries."""
        records = response.get("records", [])
        metadata = response.get("columnMetadata", [])

        if not metadata:
            # No metadata means no columns, return empty list
            return []

        # Extract column names
        column_names = [
            col.get("name", f"column_{i}") for i, col in enumerate(metadata)
        ]

        # Convert records to dictionaries
        results = []
        for record in records:
            row = {}
            for i, field in enumerate(record):
                if i < len(column_names):
                    row[column_names[i]] = self._extract_value(field)
            results.append(row)

        return results

    def _extract_value(self, field: Dict[str, Any]) -> Any:
        """Extract value from RDS Data API field format."""
        if field.get("isNull"):
            return None
        elif "booleanValue" in field:
            return field["booleanValue"]
        elif "longValue" in field:
            return field["longValue"]
        elif "doubleValue" in field:
            return field["doubleValue"]
        elif "stringValue" in field:
            return field["stringValue"]
        elif "blobValue" in field:
            return field["blobValue"]
        elif "arrayValue" in field:
            # Handle array types
            array_values = field["arrayValue"]
            if "booleanValues" in array_values:
                return array_values["booleanValues"]
            elif "longValues" in array_values:
                return array_values["longValues"]
            elif "doubleValues" in array_values:
                return array_values["doubleValues"]
            elif "stringValues" in array_values:
                return array_values["stringValues"]
            else:
                return None
        else:
            return None

    def _begin_scoped_transaction(self) -> Optional[str]:
        """Start a transaction and apply organization scoping if required."""

        if not self.organization_id:
            return None

        response = self.client.begin_transaction(
            resourceArn=self.cluster_arn,
            secretArn=self.secret_arn,
            database=self.database,
        )
        transaction_id = response.get("transactionId")
        if not transaction_id:
            raise DatabaseError("Failed to start scoped transaction for scientific query")

        self.client.execute_statement(
            resourceArn=self.cluster_arn,
            secretArn=self.secret_arn,
            database=self.database,
            sql="SET LOCAL app.organization_id = :org_id",
            parameters=[
                {"name": "org_id", "value": {"stringValue": str(self.organization_id)}}
            ],
            transactionId=transaction_id,
        )
        return transaction_id

    def _commit_transaction(self, transaction_id: Optional[str]) -> None:
        if not transaction_id:
            return
        self.client.commit_transaction(
            resourceArn=self.cluster_arn,
            secretArn=self.secret_arn,
            transactionId=transaction_id,
        )

    def _rollback_transaction(self, transaction_id: Optional[str]) -> None:
        if not transaction_id:
            return
        try:
            self.client.rollback_transaction(
                resourceArn=self.cluster_arn,
                secretArn=self.secret_arn,
                transactionId=transaction_id,
            )
        except Exception as exc:  # pragma: no cover - best effort rollback logging
            logger.warning("Failed to rollback scoped transaction: %s", exc, exc_info=True)


class SimplifiedQuery:
    """
    Simplified query interface for common operations.

    This class provides easy-to-use methods for the most common queries
    without requiring knowledge of function names or SQL.
    """

    def __init__(self, client: Optional[ScientificQuery] = None):
        """Initialize with a ScientificQuery client."""
        self.client = client or ScientificQuery()

    def find_peptide(self, sequence: str) -> Optional[Dict[str, Any]]:
        """Find a peptide by exact sequence."""
        results = self.client.execute_function(
            "get_peptide_by_sequence", {"exact_sequence": sequence}
        )
        return results[0] if results else None

    def search_peptides(
        self,
        pattern: str = None,
        min_length: int = None,
        max_length: int = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Search peptides with various filters."""
        if pattern:
            return self.client.execute_function(
                "search_peptides_by_sequence",
                {"pattern": pattern, "max_results": limit},
            )
        elif min_length is not None and max_length is not None:
            return self.client.execute_function(
                "search_peptides_by_length",
                {
                    "min_length": min_length,
                    "max_length": max_length,
                    "max_results": limit,
                },
            )
        else:
            return self.client.execute_function(
                "get_top_peptides", {"limit_results": limit}
            )

    def find_similar_peptides(
        self, sequence: str, threshold: float = 0.3, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Find peptides similar to a given sequence."""
        return self.client.execute_function(
            "search_peptides_by_similarity",
            {
                "target_sequence": sequence,
                "similarity_threshold": threshold,
                "max_results": limit,
            },
        )

    def peptides_by_hla(
        self, allele: str, min_intensity: float = 0.0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get peptides associated with an HLA allele."""
        return self.client.execute_function(
            "search_peptides_by_hla",
            {
                "allele_name": allele,
                "min_intensity": min_intensity,
                "max_results": limit,
            },
        )

    def peptides_by_disease(
        self, disease: str, min_intensity: float = 0.0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get peptides from samples with a specific disease."""
        return self.client.execute_function(
            "search_peptides_by_disease",
            {
                "disease_name": disease,
                "min_intensity": min_intensity,
                "max_results": limit,
            },
        )

    def compare_diseases(
        self,
        disease1: str,
        disease2: str,
        min_fold_change: float = 2.0,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Compare peptide expression between two disease groups."""
        return self.client.execute_function(
            "compare_peptides_between_groups",
            {
                "group1_disease": disease1,
                "group2_disease": disease2,
                "min_fold_change": min_fold_change,
                "max_results": limit,
            },
        )
