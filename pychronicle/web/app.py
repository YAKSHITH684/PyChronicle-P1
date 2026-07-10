"""
Flask app for the PyChronicle dashboard.

Reads directly from the SQLite database written by
storage.database.TraceDatabase — no write access, no dependency on
that class at runtime, so the dashboard stays decoupled from the
tracer itself.

Run with:
    python -m web.app
Then open http://127.0.0.1:5000
"""

import sqlite3
from pathlib import Path

from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Data/traces.db, relative to the project root (one level up from this file).
DB_PATH = Path(__file__).resolve().parent.parent / "Data" / "traces.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/traces")
def api_traces():
    """Every recorded assignment, oldest first — the raw timeline."""
    if not DB_PATH.exists():
        return jsonify([])

    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT id, timestamp, line_number, variable_name,
                   serialized_value, scope, value_type, session_id
            FROM variable_traces
            ORDER BY timestamp ASC, id ASC
            """
        ).fetchall()
        return jsonify([dict(row) for row in rows])
    finally:
        conn.close()


@app.route("/api/variables")
def api_variables():
    """Distinct variable names, for the track list in the sidebar."""
    if not DB_PATH.exists():
        return jsonify([])

    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT DISTINCT variable_name FROM variable_traces ORDER BY variable_name"
        ).fetchall()
        return jsonify([row["variable_name"] for row in rows])
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(debug=True)