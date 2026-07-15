"""
execution_tracer.py

Records variable execution history and stores
it into the SQLite database.
"""

import inspect

from storage.database import TraceDatabase
from tracer.delta_tracker import DeltaTracker


class ExecutionTracer:
    """
    Main execution tracer.
    """

    def __init__(self, db_path="pychronicle.db"):

        self.database = TraceDatabase(db_path)

        self.delta = DeltaTracker()

    # ----------------------------------------------------

    def trace(
        self,
        variable_name,
        value,
        line_number,
        scope="global",
    ):
        """
        Record one variable assignment.
        """

        change = self.delta.update(
            variable_name,
            value,
        )

        self.database.insert_variable(
            variable_name,
            value,
            line_number,
            scope,
        )

        print(
            f"[TRACE] "
            f"{variable_name} = {value} "
            f"(Line {line_number})"
        )

        return change

    # ----------------------------------------------------

    def trace_locals(self):
        """
        Automatically trace all local variables
        from the caller frame.
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

    # ----------------------------------------------------

    def history(self):
        """
        Return database history.
        """

        return self.database.get_history()

    # ----------------------------------------------------

    def delta_history(self):
        """
        Return change history.
        """

        return self.delta.get_history()

    # ----------------------------------------------------

    def clear(self):

        self.database.clear()

        self.delta.clear()

    # ----------------------------------------------------

    def close(self):

        self.database.close()


# ----------------------------------------------------------

_global_tracer = ExecutionTracer()


def __pychronicle_trace__(
    variable_name,
    value,
    line_number,
):
    """
    Function injected by AST Rewriter.
    """

    _global_tracer.trace(
        variable_name,
        value,
        line_number,
    )


# ----------------------------------------------------------

if __name__ == "__main__":

    tracer = ExecutionTracer()

    x = 10
    tracer.trace("x", x, 1)

    x = 20
    tracer.trace("x", x, 2)

    y = 50
    tracer.trace("y", y, 3)

    print()

    print("Database History")

    for row in tracer.history():
        print(row)

    print()

    print("Delta History")

    for row in tracer.delta_history():
        print(row)

    tracer.close()