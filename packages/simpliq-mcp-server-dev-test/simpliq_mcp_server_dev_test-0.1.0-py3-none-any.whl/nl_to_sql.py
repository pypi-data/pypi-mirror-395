from typing import Optional
try:
    from .llm_client import LLMClient
    from .sql_validator import SQLValidator
except ImportError:
    # Fallback for direct execution or when not installed as package
    from llm_client import LLMClient
    from sql_validator import SQLValidator


class NLtoSQLEngine:
    """Lightweight NL->SQL engine that uses an LLM client and a SQL validator.

    The engine is intentionally small: it builds a prompt, calls the LLM client,
    extracts SQL (between <SQL>..</SQL> if provided), validates it and optionally
    delegates execution to a provided executor (callable with signature execute(sql, limit)->(rows, duration)).
    """

    def __init__(
        self,
        llm_client: LLMClient,
        validator: Optional[SQLValidator] = None,
        executor: Optional[object] = None,
        config: Optional[dict] = None,
        dialect: Optional[str] = None,
    ):
        self.llm = llm_client
        self.dialect = (dialect or '').lower() if dialect else None
        self.validator = validator or SQLValidator(dialect=self.dialect)
        self.executor = executor
        self.config = config or {}

    def build_prompt(self, natural_query: str, semantic_context: str = "", schema_context: str = "", examples: str = "") -> str:
        # Minimal prompt builder following the project's plan. Keep prompt compact.
        parts = [
            "System: You are an assistant that translates natural language into safe SQL SELECT queries.",
        ]
        if semantic_context:
            parts.append("Semantic mappings:\n" + semantic_context)
        if schema_context:
            parts.append("Schema (relevant):\n" + schema_context)
        if examples:
            parts.append("Examples:\n" + examples)
        parts.append(f"User Query: \"{natural_query}\"")
        parts.append("Answer with one SQL statement only enclosed in <SQL>...</SQL>.")
        return "\n\n".join(parts)

    @staticmethod
    def _extract_sql(raw_text: str) -> str:
        # Try to extract between markers
        import re

        m = re.search(r"<SQL>(.*?)</SQL>", raw_text, re.S | re.I)
        if m:
            return m.group(1).strip()
        return raw_text.strip()

    def generate_sql(self, natural_query: str, semantic_context: str = "", schema_context: str = "", include_sql: bool = False, run_mode: str = "execute", limit: Optional[int] = None) -> dict:
        prompt = self.build_prompt(natural_query, semantic_context, schema_context)
        raw = self.llm.generate(prompt)
        sql_candidate = self._extract_sql(raw)

        # Explicitly detect failed generation placeholders
        if not sql_candidate or sql_candidate.strip().upper().startswith("UNABLE_TO_GENERATE"):
            return {"success": False, "error": {"code": "GENERATION_FAILED", "messages": ["LLM failed to generate SQL"], "raw": raw}}

        valid, errors = self.validator.validate(sql_candidate)
        if not valid:
            return {"success": False, "error": {"code": "VALIDATION_FAILED", "messages": errors}}

        # enforce limit
        max_rows = limit or self.config.get("max_rows") or self.validator.max_rows
        # quick heuristic: append LIMIT if missing
        if max_rows:
            sql_candidate = self.validator.enforce_limit(sql_candidate)

        result = {"success": True, "sql_generated": sql_candidate}

        if include_sql and run_mode != "execute":
            return result

        if run_mode == "execute":
            if not self.executor:
                result["warning"] = "no executor configured"
                return result
            rows, duration = self.executor.execute(sql_candidate, limit=max_rows)
            result.update({"results": rows, "row_count": len(rows), "execution_time_ms": int(duration * 1000)})

        return result
