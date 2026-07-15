"""
SQLite storage backend for PyChronicle.
"""

import sqlite3
from pathlib import Path
from datetime import datetime

from .schema import create_schema


class TraceDatabase:
    """
    Stores execution history of variables.
    """

    def __init__(self, db_path="pychronicle.db"):

        self.db_path = Path(db_path)

        self.connection = sqlite3.connect(self.db_path)

        self.connection.row_factory = sqlite3.Row

        create_schema(self.connection)

    # -------------------------------------------------

    def insert_variable(
        self,
        variable_name,
        variable_value,
        line_number,
        scope="global"
    ):
        """
        Store a variable snapshot.
        """

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO execution_history(

                variable_name,
                variable_value,
                variable_type,
                line_number,
                timestamp,
                scope

            )

            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                variable_name,
                str(variable_value),
                type(variable_value).__name__,
                line_number,
                datetime.now().isoformat(timespec="seconds"),
                scope,
            ),
        )

        self.connection.commit()

    # -------------------------------------------------

    def get_history(self, variable_name=None):
        """
        Retrieve execution history.
        """

        cursor = self.connection.cursor()

        if variable_name:

            cursor.execute(
                """
                SELECT *
                FROM execution_history
                WHERE variable_name=?
                ORDER BY id
                """,
                (variable_name,),
            )

        else:

            cursor.execute(
                """
                SELECT *
                FROM execution_history
                ORDER BY id
                """
            )

        return [dict(row) for row in cursor.fetchall()]

    # -------------------------------------------------

    def clear(self):
        """
        Remove all records.
        """

        cursor = self.connection.cursor()

        cursor.execute(
            "DELETE FROM execution_history"
        )

        self.connection.commit()

    # -------------------------------------------------

    def close(self):
        """
        Close database connection.
        """

        self.connection.close()


# ---------------------------------------------------------

if __name__ == "__main__":

    db = TraceDatabase()

    db.insert_variable("x", 10, 1)

    db.insert_variable("x", 20, 2)

    db.insert_variable("name", "Alice", 5)

    for row in db.get_history():
        print(row)

    db.close()