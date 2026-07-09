"""
SQLite schema for PyChronicle's variable-trace storage.

Table `variable_traces` stores one row per observed assignment:
(timestamp, line_number, variable_name, serialized_value), plus a
few extra columns that make the two dominant queries fast:
  1. "show the history of variable X over time"
  2. "show everything that happened at/around line N"
"""

SCHEMA_VERSION = 1

CREATE_TRACES_TABLE = """
CREATE TABLE IF NOT EXISTS variable_traces (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp         REAL    NOT NULL,
    line_number       INTEGER NOT NULL,
    variable_name     TEXT    NOT NULL,
    serialized_value  TEXT    NOT NULL,
    scope             TEXT    DEFAULT 'module',
    value_type        TEXT,
    session_id        TEXT
);
"""

# Composite indexes: variable_name/line_number first (equality filter),
# timestamp second (range/order) -- lets SQLite satisfy WHERE + ORDER BY
# from the index alone without a separate sort step.
CREATE_INDEX_VARIABLE_NAME = """
CREATE INDEX IF NOT EXISTS idx_traces_variable_name
ON variable_traces (variable_name, timestamp);
"""

CREATE_INDEX_LINE_NUMBER = """
CREATE INDEX IF NOT EXISTS idx_traces_line_number
ON variable_traces (line_number, timestamp);
"""

CREATE_INDEX_SESSION = """
CREATE INDEX IF NOT EXISTS idx_traces_session
ON variable_traces (session_id, timestamp);
"""

CREATE_META_TABLE = """
CREATE TABLE IF NOT EXISTS trace_meta (
    key   TEXT PRIMARY KEY,
    value TEXT
);
"""

ALL_STATEMENTS = [
    CREATE_TRACES_TABLE,
    CREATE_INDEX_VARIABLE_NAME,
    CREATE_INDEX_LINE_NUMBER,
    CREATE_INDEX_SESSION,
    CREATE_META_TABLE,
]