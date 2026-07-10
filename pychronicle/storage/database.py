"""
Storage layer for PyChronicle: manages the SQLite connection and
provides insert / query helpers for the `variable_traces` table.
"""

import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Iterable, List, Optional, Union

from .schema import ALL_STATEMENTS, SCHEMA_VERSION


class TraceDatabase:
    def __init__(self, db_path: Union[str, Path] = "Data/traces.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.db_path))
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode = WAL;")
        self._conn.execute("PRAGMA synchronous = NORMAL;")
        self._init_schema()

    def _init_schema(self):
        with self._conn:
            for stmt in ALL_STATEMENTS:
                self._conn.execute(stmt)
            self._conn.execute(
                "INSERT OR IGNORE INTO trace_meta (key, value) VALUES (?, ?)",
                ("schema_version", str(SCHEMA_VERSION)),
            )

    @staticmethod
    def _serialize(value: Any) -> str:
        try:
            return json.dumps(value, default=repr)
        except (TypeError, ValueError):
            return repr(value)

    def insert_trace(self, line_number: int, variable_name: str, value: Any,
                      scope: str = "module", session_id: Optional[str] = None,
                      timestamp: Optional[float] = None) -> int:
        ts = timestamp if timestamp is not None else time.time()
        with self._conn:
            cur = self._conn.execute(
                """
                INSERT INTO variable_traces
                    (timestamp, line_number, variable_name, serialized_value,
                     scope, value_type, session_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (ts, line_number, variable_name, self._serialize(value),
                 scope, type(value).__name__, session_id),
            )
            return cur.lastrowid

    def insert_many(self, rows: Iterable[dict]) -> None:
        prepared = [{
            "timestamp": r.get("timestamp", time.time()),
            "line_number": r["line_number"],
            "variable_name": r["variable_name"],
            "serialized_value": self._serialize(r["value"]),
            "scope": r.get("scope", "module"),
            "value_type": type(r["value"]).__name__,
            "session_id": r.get("session_id"),
        } for r in rows]
        with self._conn:
            self._conn.executemany(
                """
                INSERT INTO variable_traces
                    (timestamp, line_number, variable_name, serialized_value,
                     scope, value_type, session_id)
                VALUES (:timestamp, :line_number, :variable_name,
                        :serialized_value, :scope, :value_type, :session_id)
                """,
                prepared,
            )

    def history_for_variable(self, variable_name: str,
                              session_id: Optional[str] = None) -> List[sqlite3.Row]:
        query = "SELECT * FROM variable_traces WHERE variable_name = ?"
        params: List[Any] = [variable_name]
        if session_id:
            query += " AND session_id = ?"
            params.append(session_id)
        query += " ORDER BY timestamp ASC"
        return self._conn.execute(query, params).fetchall()

    def traces_at_line(self, line_number: int) -> List[sqlite3.Row]:
        return self._conn.execute(
            "SELECT * FROM variable_traces WHERE line_number = ? "
            "ORDER BY timestamp ASC",
            (line_number,),
        ).fetchall()

    def all_variable_names(self) -> List[str]:
        rows = self._conn.execute(
            "SELECT DISTINCT variable_name FROM variable_traces ORDER BY variable_name"
        ).fetchall()
        return [r["variable_name"] for r in rows]

    def close(self):
        self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()