"""
executor.py

Glues together:
  - parser.py         (static AST pass, used for validation + a
                        sanity-check count of expected assignments)
  - execution_tracer   (runtime pass, records real values as the
                        program actually executes)
  - database.py        (persists every recorded assignment)

run_and_trace() is what app.py's /api/parse endpoint calls. It is the
only function that actually executes the uploaded file.
"""

import runpy
import traceback
from pathlib import Path
from typing import Any, Dict

from pychronicle.ast_engine.parser import parse_file
from pychronicle.tracer.execution_tracer import ExecutionTracer


def run_and_trace(path: str, db) -> Dict[str, Any]:
    """
    Execute the target Python file with tracing enabled, recording
    every variable assignment into `db` under a fresh session.

    Returns a summary dict that the API layer returns directly to the
    frontend, e.g.:

        {
            "session": "a1b2c3d4e5f6",
            "source_path": "/tmp/tmpxyz.py",
            "static_assignment_count": 7,
            "trace_count": 42,
            "variables": ["x", "total", "items"],
            "error": None,
        }

    If the target script raises during execution, `error` is set to
    the formatted traceback but the session + everything traced up to
    the point of failure is still persisted (so partial runs are still
    inspectable in the timeline/debugger).
    """
    path_obj = Path(path)
    source_path = str(path_obj)

    # Static pass: fails fast with a clear message on invalid syntax,
    # before we ever try to execute anything.
    try:
        static_assignments = parse_file(path_obj)
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in {path_obj.name}: {exc}") from exc

    session = db.create_session(source_path=source_path)
    trace_count = 0

    def on_assignment(name, value, line_number, scope):
        nonlocal trace_count
        db.add_trace(
            session=session,
            variable_name=name,
            value=value,
            line_number=line_number,
            scope=scope,
        )
        trace_count += 1

    tracer = ExecutionTracer(on_assignment, target_filename=source_path)

    error = None
    tracer.start()
    try:
        # run_path executes the file as __main__, matching what you'd
        # get from `python file.py` (so `if __name__ == "__main__":`
        # blocks run, relative imports next to the file work, etc.)
        runpy.run_path(source_path, run_name="__main__")
    except SystemExit:
        # sys.exit() in the traced script shouldn't look like a crash.
        pass
    except BaseException:
        error = traceback.format_exc()
    finally:
        tracer.stop()

    return {
        "session": session,
        "source_path": source_path,
        "static_assignment_count": len(static_assignments),
        "trace_count": trace_count,
        "variables": db.get_variables(session=session),
        "error": error,
    }
