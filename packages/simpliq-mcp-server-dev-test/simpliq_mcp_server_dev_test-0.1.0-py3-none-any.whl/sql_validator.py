import re
from typing import Tuple, List


class SQLValidator:
    """Minimal SQL validator to enforce SELECT-only policies and detect dangerous patterns.

    This is intentionally conservative. It uses regex checks to avoid adding heavy parser
    dependencies. For production, replace or complement with `sqlglot` or a proper SQL parser.
    """

    FORBIDDEN_RE = re.compile(r"\b(insert|update|delete|drop|alter|truncate|create|merge)\b", re.I)
    # Allow trailing semicolon (common in LLM responses), but block multiple statements
    MULTIPLE_STATEMENTS_RE = re.compile(r";\s*\S", re.I)  # semicolon followed by non-whitespace
    DANGEROUS_FUNCS_RE = re.compile(r"\b(pg_sleep|sleep\s*\(|xp_cmdshell)\b", re.I)
    ALLOWED_START_RE = re.compile(r"^\s*(select|with)\b", re.I)
    LLM_PLACEHOLDER_RE = re.compile(r"\bUNABLE_TO_GENERATE\b", re.I)

    def __init__(self, max_rows: int = 1000, dialect: str = None):
        self.max_rows = int(max_rows)
        self.dialect = (dialect or '').lower() if dialect else None

    def validate(self, sql: str) -> Tuple[bool, List[str]]:
        """Validate SQL string. Returns (is_valid, errors)."""
        errors: List[str] = []
        if not sql or not sql.strip():
            errors.append("Empty SQL")

        # Must start with SELECT or WITH (CTE)
        if sql and not self.ALLOWED_START_RE.search(sql):
            errors.append("Only SELECT/CTE (WITH) statements are allowed")

        # Block multiple statements (semicolon followed by another statement)
        if self.MULTIPLE_STATEMENTS_RE.search(sql):
            errors.append("Multiple statements detected (semicolon followed by code)")

        if self.FORBIDDEN_RE.search(sql):
            errors.append("DDL/DML or forbidden keyword detected")

        if self.DANGEROUS_FUNCS_RE.search(sql):
            errors.append("Dangerous function detected in SQL")

        # Detect placeholder outputs from failed LLM generation
        if self.LLM_PLACEHOLDER_RE.search(sql):
            errors.append("LLM generation failed (placeholder detected)")

        return (len(errors) == 0, errors)

    def enforce_limit(self, sql: str) -> str:
        """Apply row limit using the appropriate syntax for the database dialect.
        
        Behavior by dialect:
        - mssql: Use TOP N syntax (e.g., SELECT TOP 1000 ...)
        - sqlite/mysql/mariadb/postgresql: Use LIMIT N syntax
        - oracle: Use ROWNUM or FETCH FIRST (not implemented yet, falls back to LIMIT)
        - unknown: Use LIMIT N as fallback
        
        Also strips trailing semicolon if present (common in LLM outputs).
        """
        import re
        
        # Remove trailing semicolon and whitespace
        sql_clean = sql.rstrip().rstrip(';').rstrip()
        
        # If already has LIMIT or TOP, don't modify
        if re.search(r"\b(limit|top)\b", sql_clean, re.I):
            return sql_clean
        
        # SQL Server (mssql) - use TOP N
        if self.dialect == 'mssql':
            # Try to inject TOP N after SELECT (and after DISTINCT if present)
            m = re.match(r"^\s*SELECT\s+(DISTINCT\s+)?", sql_clean, flags=re.IGNORECASE)
            if m:
                # Preserve exact matched DISTINCT text (original casing) if any
                distinct_txt = m.group(1) or ''
                start, end = m.span()
                prefix_ws = sql_clean[:start]
                suffix = sql_clean[end:]
                # Reconstruct with normalized 'SELECT ' and preserved DISTINCT
                return f"{prefix_ws}SELECT {distinct_txt}TOP {self.max_rows} {suffix}"
            # If we can't confidently rewrite (e.g., WITH CTE), leave as-is
            return sql_clean
        
        # PostgreSQL, MySQL, MariaDB, SQLite - use LIMIT N
        elif self.dialect in ('postgresql', 'mysql', 'mariadb', 'sqlite'):
            return sql_clean + f" LIMIT {self.max_rows}"
        
        # Oracle - TODO: implement FETCH FIRST or ROWNUM
        elif self.dialect == 'oracle':
            # For now, fallback to LIMIT (may not work on older Oracle versions)
            return sql_clean + f" LIMIT {self.max_rows}"
        
        # Unknown dialect - use LIMIT as fallback
        else:
            return sql_clean + f" LIMIT {self.max_rows}"
