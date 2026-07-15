"""
Database schema definitions.
"""

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS execution_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    variable_name TEXT NOT NULL,

    variable_value TEXT,

    variable_type TEXT,

    line_number INTEGER,

    timestamp TEXT,

    scope TEXT
);
"""


def create_schema(connection):
    """
    Create required database tables.
    """

    cursor = connection.cursor()

    cursor.executescript(SCHEMA_SQL)

    connection.commit()