from sqlalchemy import text, create_engine
import time
from typing import Tuple, List


class SimpleSQLExecutor:
    """Minimal SQL executor for tests using a SQLAlchemy connection string.

    execute(sql, limit) -> (rows:list[dict], duration_seconds:float)
    """

    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)

    def execute(self, sql: str, limit: int = None) -> Tuple[List[dict], float]:
        start = time.time()
        with self.engine.connect() as conn:
            rs = conn.execute(text(sql))
            rows = [dict(r._mapping) for r in rs.fetchall()]
        duration = time.time() - start
        return rows, duration
