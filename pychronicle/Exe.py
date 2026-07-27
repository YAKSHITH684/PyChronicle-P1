"""
executor.py

Ties the AST rewriter to real execution: given a path to a Python
file, rewrite it to insert trace calls, then execute it in a fresh
namespace with __pychronicle_trace__ wired up to write straight into
the TraceDatabase under a brand-new session.
"""

import os

from pychronicle.ast_engine.rewriter import rewrite_source
from pychronicle.storage.database import TraceDatabase


def run_and_trace(path: str, db: TraceDatabase) -> dict:
    """
    Rewrite + execute the file at `path`, recording every traced
    assignment into `db` under a new session.

    Returns {"session": <session_id>, "assignments_found": <count>}.
    """

    if not os.path.isfile(path):
        raise FileNotFoundError(f"No such file: {path}")

    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    rewritten = rewrite_source(source)

    session = db.create_session(source_path=path)
    count = 0

    def _trace(name, value, lineno, scope):
        nonlocal count
        db.add_trace(session, name, value, lineno, scope)
        count += 1

    exec_globals = {
        "__name__": "__main__",
        "__file__": path,
        "__pychronicle_trace__": _trace,
    }

    code = compile(rewritten, filename=path, mode="exec")
    exec(code, exec_globals)

    return {"session": session, "assignments_found": count}