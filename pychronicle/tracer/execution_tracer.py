"""
execution_tracer.py

Execution tracer for PyChronicle.
"""

import inspect

from pychronicle.storage.database import TraceDatabase
from pychronicle.tracer.delta_tracker import DeltaTracker


class ExecutionTracer:
    """
    Records variable execution history.
    """

    def __init__(self, db_path="pychronicle.db"):
        self.database = TraceDatabase(db_path)
        self.delta = DeltaTracker()

    def trace(
        self,
        variable_name,
        value,
        line_number,
        scope="global"
    ):
        """
        Trace a variable assignment.
        """

        self.delta.update(variable_name, value)

        self.database.insert_variable(
            variable_name=variable_name,
            variable_value=value,
            line_number=line_number,
            scope=scope,
        )

        print(
            f"[TRACE] {variable_name} = {value} (Line {line_number})"
        )

    def trace_locals(self):
        """
        Trace all local variables from the caller frame.
        """

        frame = inspect.currentframe().f_back

        line = frame.f_lineno
        scope = frame.f_code.co_name

        for name, value in frame.f_locals.items():
            self.trace(
                name,
                value,
                line,
                scope,
            )

    def history(self):
        return self.database.get_history()

    def delta_history(self):
        return self.delta.get_history()

    def clear(self):
        self.database.clear()
        self.delta.clear()

    def close(self):
        self.database.close()


_global_tracer = ExecutionTracer()


def __pychronicle_trace__(
    variable_name,
    value,
    line_number,
    scope="global",
):
    """
    Called by rewritten AST.
    """

    _global_tracer.trace(
        variable_name,
        value,
        line_number,
        scope,
    )


if __name__ == "__main__":

    tracer = ExecutionTracer()

    x = 10
    tracer.trace("x", x, 1)

    x = 20
    tracer.trace("x", x, 2)

    y = 50
    tracer.trace("y", y, 3)

    print("\nHistory\n")

    for row in tracer.history():
        print(row)

    tracer.close()