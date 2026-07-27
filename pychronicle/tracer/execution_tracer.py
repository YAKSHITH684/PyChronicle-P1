"""
execution_tracer.py

Execution tracer for PyChronicle.
Compatible with the current FastAPI + executor architecture.
"""

from pychronicle.storage.database import TraceDatabase


class ExecutionTracer:
    """
    Handles execution tracing and stores variable assignments
    in the TraceDatabase.
    """

    def __init__(self, database=None):
        if database is None:
            self.database = TraceDatabase()
        else:
            self.database = database

        self.session = None

    def start_session(self, source_path=""):
        """
        Create a new tracing session.
        """
        self.session = self.database.create_session(source_path)

    def trace(self, variable_name, value, line_number, scope="global"):
        """
        Record one variable assignment.
        """

        if self.session is None:
            self.start_session()

        self.database.add_trace(
            session=self.session,
            name=variable_name,
            value=value,
            lineno=line_number,
            scope=scope,
        )

    def history(self):
        """
        Return all recorded traces.
        """
        return self.database.get_history(session=self.session)

    def sessions(self):
        return self.database.get_sessions()

    def variables(self):
        return self.database.get_variables(session=self.session)

    def clear(self):
        """
        Clear all stored traces.
        """
        if hasattr(self.database, "rows"):
            self.database.rows.clear()

    def close(self):
        """
        Compatibility method.
        """
        pass


# Global tracer instance used by rewritten AST
_global_tracer = ExecutionTracer()


def __pychronicle_trace__(
    variable_name,
    value,
    line_number,
    scope="global",
):
    """
    Function inserted into rewritten code by the AST rewriter.
    """

    _global_tracer.trace(
        variable_name=variable_name,
        value=value,
        line_number=line_number,
        scope=scope,
    )


if __name__ == "__main__":

    tracer = ExecutionTracer()

    tracer.start_session("sample.py")

    tracer.trace("x", 10, 1)
    tracer.trace("x", 20, 2)
    tracer.trace("y", 50, 3)

    print("\nExecution History\n")

    for row in tracer.history():
        print(row)