"""
database.py

Storage layer for PyChronicle.

Persists every traced variable assignment (one row per assignment,
per execution) to a local SQLite database, grouped by "session" —
one session per file that gets parsed/executed via /api/parse.
"""

import json
import sqlite3
import threading
import time
import uuid
from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class TraceRecord:
    """
    A single recorded variable assignment.

    variable_value holds a human-readable repr() of the value (used by
    the legacy /api/history and /dashboard views). serialized_value
    holds a JSON-encoded version of the value, which is what the
    frontend's timeline/snapshots/variables views consume.
    """

    id: int
    session: str
    variable_name: str
    variable_value: str
    variable_type: str
    serialized_value: str
    line_number: int
    scope: str
    timestamp: float


def _serialize(value: Any) -> str:
    """Best-effort JSON serialization of a traced value."""
    try:
        return json.dumps(value)
    except (TypeError, ValueError):
        return json.dumps(repr(value))


class TraceDatabase:
    """
    SQLite-backed store for trace records and sessions.

    A single instance is shared across requests (see app.py), so the
    underlying connection is created with check_same_thread=False and
    all access is protected by a lock.
    """

    def __init__(self, db_path: str = "pychronicle.db"):
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        with self._lock, self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    source_path TEXT,
                    created_at REAL NOT NULL
                )
                """
            )
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS traces (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session TEXT NOT NULL,
                    variable_name TEXT NOT NULL,
                    variable_value TEXT,
                    variable_type TEXT,
                    serialized_value TEXT,
                    line_number INTEGER,
                    scope TEXT,
                    timestamp REAL NOT NULL
                )
                """
            )

    # ------------------------------------------------------------------
    # Sessions
    # ------------------------------------------------------------------

    def create_session(self, source_path: Optional[str] = None) -> str:
        """Create and register a new (initially empty) session."""
        session_id = uuid.uuid4().hex[:12]
        with self._lock, self._conn:
            self._conn.execute(
                "INSERT INTO sessions (session_id, source_path, created_at) VALUES (?, ?, ?)",
                (session_id, source_path, time.time()),
            )
        return session_id

    def get_sessions(self) -> List[str]:
        """Return session ids ordered oldest -> newest (so callers can
        treat the last element as 'most recent')."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT session_id FROM sessions ORDER BY created_at ASC"
            ).fetchall()
        return [row["session_id"] for row in rows]

    # ------------------------------------------------------------------
    # Traces
    # ------------------------------------------------------------------

    def add_trace(
        self,
        session: str,
        variable_name: str,
        value: Any,
        line_number: int,
        scope: str = "module",
    ) -> TraceRecord:
        variable_type = type(value).__name__
        variable_value = repr(value)
        serialized_value = _serialize(value)
        timestamp = time.time()

        with self._lock, self._conn:
            cursor = self._conn.execute(
                """
                INSERT INTO traces
                    (session, variable_name, variable_value, variable_type,
                     serialized_value, line_number, scope, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session,
                    variable_name,
                    variable_value,
                    variable_type,
                    serialized_value,
                    line_number,
                    scope,
                    timestamp,
                ),
            )
            row_id = cursor.lastrowid

        return TraceRecord(
            id=row_id,
            session=session,
            variable_name=variable_name,
            variable_value=variable_value,
            variable_type=variable_type,
            serialized_value=serialized_value,
            line_number=line_number,
            scope=scope,
            timestamp=timestamp,
        )

    def get_history(
        self,
        session: Optional[str] = None,
        variable: Optional[str] = None,
    ) -> List[TraceRecord]:
        query = "SELECT * FROM traces"
        clauses = []
        params: List[Any] = []

        if session:
            clauses.append("session = ?")
            params.append(session)

        if variable:
            clauses.append("variable_name = ?")
            params.append(variable)

        if clauses:
            query += " WHERE " + " AND ".join(clauses)

        query += " ORDER BY id ASC"

        with self._lock:
            rows = self._conn.execute(query, params).fetchall()

        return [
            TraceRecord(
                id=row["id"],
                session=row["session"],
                variable_name=row["variable_name"],
                variable_value=row["variable_value"],
                variable_type=row["variable_type"],
                serialized_value=row["serialized_value"],
                line_number=row["line_number"],
                scope=row["scope"],
                timestamp=row["timestamp"],
            )
            for row in rows
        ]

    def get_variables(self, session: Optional[str] = None) -> List[str]:
        """Distinct variable names, in order of first appearance."""
        query = "SELECT variable_name FROM traces"
        params: List[Any] = []
        if session:
            query += " WHERE session = ?"
            params.append(session)
        query += " ORDER BY id ASC"

        with self._lock:
            rows = self._conn.execute(query, params).fetchall()

        seen = []
        seen_set = set()
        for row in rows:
            name = row["variable_name"]
            if name not in seen_set:
                seen_set.add(name)
                seen.append(name)
        return seen