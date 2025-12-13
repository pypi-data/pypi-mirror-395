from sqlalchemy import text, create_engine
import time
from typing import Tuple, List


class SQLExecutor:
    """Simple SQLExecutor using SQLAlchemy. Accepts a SQLAlchemy connection string.

    execute(sql, limit) -> (rows:list[dict], duration_seconds:float)
    """

    def __init__(self, connection_string: str):
        # connection pooling and engine creation
        self.engine = create_engine(connection_string)

    def execute(self, sql: str, limit: int = None) -> Tuple[List[dict], float]:
        start = time.time()
        with self.engine.connect() as conn:
            rs = conn.execute(text(sql))
            # SQLAlchemy 2.0 Row -> use _mapping to convert to dict
            rows = [dict(r._mapping) for r in rs.fetchall()]
        duration = time.time() - start
        return rows, duration
"""SQL Executor Module - SimpliQ

This module provides secure SQL query execution with validation and protection
against SQL injection attacks.

Classes:
    - ValidationResult: Result of SQL validation
    - ExecutionResult: Result of SQL execution
    - SQLValidator: Validates SQL queries for security
    - SQLExecutor: Executes SQL queries with timeout and limits
"""

import re
import time
import hashlib
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

import sqlparse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of SQL validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str] = field(default_factory=list)


@dataclass
class ExecutionResult:
    """Result of SQL execution."""
    success: bool
    data: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    row_count: int = 0
    execution_time_ms: int = 0
    query_hash: str = ""
    truncated: bool = False
    error_message: Optional[str] = None
    error_type: Optional[str] = None


class SQLValidator:
    """
    Validates SQL queries for security and correctness.

    This validator ensures that only SELECT statements are allowed and
    protects against SQL injection attacks.
    """

    def __init__(self):
        """Initialize the SQL validator."""
        self.allowed_statements = {'SELECT', 'WITH'}

        # Forbidden SQL patterns (case insensitive)
        self.forbidden_patterns = [
            # DML de escrita
            (r'\b(INSERT|UPDATE|DELETE|REPLACE|MERGE)\b', 'Write operations (INSERT, UPDATE, DELETE) are not allowed'),

            # DDL
            (r'\b(CREATE|ALTER|DROP|TRUNCATE|RENAME)\b', 'Schema modifications (CREATE, ALTER, DROP) are not allowed'),

            # DCL
            (r'\b(GRANT|REVOKE)\b', 'Permission modifications (GRANT, REVOKE) are not allowed'),

            # Transações
            (r'\b(BEGIN|COMMIT|ROLLBACK|SAVEPOINT)\b', 'Transaction control statements are not allowed'),

            # Múltiplos statements
            (r';\s*\w+', 'Multiple SQL statements are not allowed'),

            # Comentários SQL (possível SQL injection)
            (r'--', 'SQL comments (--) are not allowed'),
            (r'/\*', 'SQL block comments (/* */) are not allowed'),

            # Funções perigosas
            (r'\b(LOAD_FILE|INTO\s+OUTFILE|INTO\s+DUMPFILE)\b', 'File operations are not allowed'),
        ]

    def validate(self, sql: str, timeout: int = 30, limit: int = 1000) -> ValidationResult:
        """
        Validate a SQL query.

        Args:
            sql: SQL query to validate
            timeout: Configured timeout
            limit: Configured row limit

        Returns:
            ValidationResult with is_valid, errors, and warnings
        """
        errors = []
        warnings = []

        # 1. Validate SQL is not empty
        if not sql or not sql.strip():
            errors.append("SQL query is empty")
            return ValidationResult(is_valid=False, errors=errors)

        # 2. Parse with sqlparse
        try:
            parsed = sqlparse.parse(sql)
            if not parsed:
                errors.append("Failed to parse SQL")
                return ValidationResult(is_valid=False, errors=errors)
        except Exception as e:
            errors.append(f"SQL parsing error: {str(e)}")
            return ValidationResult(is_valid=False, errors=errors)

        # 3. Check for multiple statements
        if len(parsed) > 1:
            errors.append("Multiple SQL statements are not allowed")

        # 4. Check statement type
        statement = parsed[0]
        stmt_type = statement.get_type()

        if stmt_type not in self.allowed_statements:
            errors.append(
                f"{stmt_type} statements are not allowed. "
                f"Only SELECT queries are permitted."
            )

        # 5. Check forbidden patterns (SQL injection protection)
        for pattern, error_msg in self.forbidden_patterns:
            if re.search(pattern, sql, re.IGNORECASE):
                errors.append(error_msg)

        # 6. Validate timeout
        if timeout < 1 or timeout > 300:
            errors.append("Timeout must be between 1 and 300 seconds")

        # 7. Validate limit
        if limit < 1 or limit > 10000:
            errors.append("Limit must be between 1 and 10000 rows")

        # 8. Warnings (don't block execution)
        if limit > 5000:
            warnings.append(
                f"Large row limit ({limit}). Consider reducing for better performance."
            )

        if timeout > 60:
            warnings.append(
                f"Long timeout ({timeout}s). Query may impact system performance."
            )

        is_valid = len(errors) == 0
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )


class SQLExecutor:
    """
    Executes SQL queries with security and resource limits.

    This executor applies timeout, row limits, and formats results safely.
    """

    def __init__(self, engine: Engine):
        """
        Initialize the SQL executor.

        Args:
            engine: SQLAlchemy engine for database connection
        """
        self.engine = engine

    def execute(
        self,
        sql: str,
        timeout: int = 30,
        limit: int = 1000,
        include_metadata: bool = False
    ) -> ExecutionResult:
        """
        Execute a SQL query.

        Args:
            sql: Validated SQL query
            timeout: Timeout in seconds
            limit: Maximum number of rows to return
            include_metadata: Include column metadata in response

        Returns:
            ExecutionResult with data, metadata, and stats
        """
        start_time = time.time()

        try:
            # 1. Apply LIMIT to query if not present
            modified_sql = self._apply_limit(sql, limit)

            logger.info(f"Executing SQL query: {modified_sql[:100]}...")

            # 2. Create connection with timeout (where supported)
            with self.engine.connect() as connection:
                # Set execution timeout (some drivers support this)
                try:
                    connection = connection.execution_options(timeout=timeout)
                except Exception:
                    # Timeout not supported by this driver, continue anyway
                    logger.warning("Query timeout not supported by database driver")

                # 3. Execute query
                result = connection.execute(text(modified_sql))

                # 4. Fetch results (with limit + 1 to check for truncation)
                rows = result.fetchmany(limit + 1)

                # 5. Check if truncated
                truncated = len(rows) > limit
                if truncated:
                    rows = rows[:limit]

                # 6. Convert to list of dicts
                columns = result.keys()
                data = [
                    dict(zip(columns, row))
                    for row in rows
                ]

                # 7. Collect metadata (if requested)
                metadata = None
                if include_metadata:
                    metadata = self._get_column_metadata(result)

                # 8. Calculate execution time
                execution_time_ms = int((time.time() - start_time) * 1000)

                # 9. Generate query hash (for caching in future)
                query_hash = hashlib.md5(sql.encode()).hexdigest()

                logger.info(
                    f"Query executed successfully: {len(data)} rows, "
                    f"{execution_time_ms}ms, truncated={truncated}"
                )

                return ExecutionResult(
                    success=True,
                    data=data,
                    metadata=metadata,
                    row_count=len(data),
                    execution_time_ms=execution_time_ms,
                    query_hash=query_hash,
                    truncated=truncated
                )

        except SQLAlchemyError as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            error_type = self._classify_error(e)
            error_message = str(e)

            logger.error(
                f"Query execution failed: {error_message}, "
                f"type={error_type}, time={execution_time_ms}ms"
            )

            return ExecutionResult(
                success=False,
                error_message=error_message,
                error_type=error_type,
                execution_time_ms=execution_time_ms
            )

        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            error_message = str(e)

            logger.error(f"Unexpected error during query execution: {error_message}")

            return ExecutionResult(
                success=False,
                error_message=error_message,
                error_type="UNEXPECTED_ERROR",
                execution_time_ms=execution_time_ms
            )

    def _apply_limit(self, sql: str, limit: int) -> str:
        """
        Add a row limit to the query respecting the target dialect.

        Behavior by dialect:
        - mssql: Prefer TOP N. If query already contains TOP/OFFSET FETCH, don't modify.
                 For simple SELECT/SELECT DISTINCT, inject TOP N after SELECT (and DISTINCT if present).
                 For queries starting with WITH (CTE) or other complex cases, leave unchanged.
        - sqlite/mysql/mariadb/postgresql: Append LIMIT N if not present.
        - oracle/other: Leave unchanged (do not try to rewrite generically).
        """
        # Normalize trailing semicolon
        original_sql = sql
        sql = sql.rstrip().rstrip(';')

        # If query already has an explicit LIMIT, respect it
        if 'LIMIT' in sql.upper():
            return sql

        # Detect dialect
        try:
            dialect = getattr(self.engine.dialect, 'name', '').lower()
        except Exception:
            dialect = ''

        if dialect == 'mssql':
            upper = sql.upper()
            # If already has TOP or OFFSET FETCH, don't change
            if ' TOP ' in upper or ' OFFSET ' in upper and ' FETCH ' in upper:
                return sql

            # Try to inject TOP N after SELECT (and after DISTINCT if present)
            import re
            m = re.match(r"^\s*SELECT\s+(DISTINCT\s+)?", sql, flags=re.IGNORECASE)
            if m:
                # Preserve exact matched DISTINCT text (original casing) if any
                distinct_txt = m.group(1) or ''
                start, end = m.span()
                prefix_ws = sql[:start]
                suffix = sql[end:]
                # Reconstruct with normalized 'SELECT ' and preserved DISTINCT
                return f"{prefix_ws}SELECT {distinct_txt}TOP {limit} {suffix}"
            # If we can't confidently rewrite (e.g., WITH CTE), leave as-is
            return sql

        # Dialects that support LIMIT n syntax
        if dialect in {'sqlite', 'mysql', 'mariadb', 'postgresql'}:
            return f"{sql} LIMIT {limit}"

        # Fallback: if unknown dialect, avoid rewriting to prevent syntax errors
        return sql

    def _get_column_metadata(self, result) -> Dict[str, Any]:
        """
        Extract column metadata from result.

        Args:
            result: SQLAlchemy result object

        Returns:
            Dictionary with column metadata
        """
        columns_metadata = []

        try:
            for col in result.cursor.description:
                columns_metadata.append({
                    "name": col[0],
                    "type": str(col[1]) if col[1] else "UNKNOWN",
                    "nullable": True  # Default, can be inferred from other sources
                })
        except Exception as e:
            logger.warning(f"Failed to extract column metadata: {str(e)}")

        return {"columns": columns_metadata}

    def _classify_error(self, error: Exception) -> str:
        """
        Classify database error for better handling.

        Args:
            error: Exception from database

        Returns:
            Error type string
        """
        error_str = str(error).lower()

        if 'timeout' in error_str or 'time' in error_str:
            return 'TIMEOUT_ERROR'
        elif 'does not exist' in error_str or 'not found' in error_str or "doesn't exist" in error_str:
            return 'OBJECT_NOT_FOUND'
        elif 'permission' in error_str or 'denied' in error_str:
            return 'PERMISSION_ERROR'
        elif 'syntax' in error_str:
            return 'SYNTAX_ERROR'
        elif 'connection' in error_str:
            return 'CONNECTION_ERROR'
        else:
            return 'DATABASE_ERROR'
