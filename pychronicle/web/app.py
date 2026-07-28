"""
app.py

FastAPI backend for PyChronicle.

POST /api/parse         - upload a .py file, execute it with tracing,
                           store every assignment, return a summary.
GET  /api/sessions       - list known sessions (oldest -> newest).
GET  /api/history        - legacy flat history (repr-based values).
GET  /api/variables      - distinct variable names for a session.
GET  /api/timeline       - ordered list of assignment events.
GET  /api/snapshots      - full variable-state snapshot at each event.

Everything under /  (other than /api/*) is served from ./static,
which contains the single-file dashboard (index.html).
"""

import os
import tempfile
from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pychronicle.ast_engine.executor import run_and_trace
from pychronicle.database import TraceDatabase

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
DB_PATH = os.path.join(BASE_DIR, "..", "..", "pychronicle.db")

app = FastAPI(title="PyChronicle")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db = TraceDatabase(db_path=DB_PATH)


@app.post("/api/parse")
async def parse_python_file(file: UploadFile = File(...)):
    """Accept an uploaded .py file, execute it with tracing enabled,
    and persist every recorded assignment under a new session."""
    if not file.filename or not file.filename.endswith(".py"):
        raise HTTPException(status_code=400, detail="Please upload a .py file")

    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(await file.read())
        temp_path = temp.name

    try:
        result = run_and_trace(temp_path, db)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        os.remove(temp_path)


@app.get("/api/sessions")
async def get_sessions():
    return {"sessions": db.get_sessions()}


@app.get("/api/history")
async def get_history(session: Optional[str] = None, variable: Optional[str] = None):
    """Legacy flat history view, using human-readable repr() values."""
    records = db.get_history(session=session, variable=variable)
    return {
        "history": [
            {
                "id": r.id,
                "session": r.session,
                "variable_name": r.variable_name,
                "variable_value": r.variable_value,
                "variable_type": r.variable_type,
                "line_number": r.line_number,
                "scope": r.scope,
                "timestamp": r.timestamp,
            }
            for r in records
        ]
    }


@app.get("/api/variables")
async def get_variables(session: Optional[str] = None):
    return {"variables": db.get_variables(session=session)}


@app.get("/api/timeline")
async def get_timeline(session: Optional[str] = None):
    """Ordered list of individual assignment events, JSON-decoded
    values, for the frontend's timeline + time-travel debugger."""
    records = db.get_history(session=session)
    timeline = []
    for r in records:
        timeline.append(
            {
                "id": r.id,
                "variable_name": r.variable_name,
                "value_display": r.variable_value,
                "serialized_value": r.serialized_value,
                "type": r.variable_type,
                "line_number": r.line_number,
                "scope": r.scope,
                "timestamp": r.timestamp,
            }
        )
    return {"timeline": timeline}


@app.get("/api/snapshots")
async def get_snapshots(session: Optional[str] = None):
    """A 'snapshot' is the full state of every variable seen so far,
    as of each event in the timeline (a running merge)."""
    records = db.get_history(session=session)
    snapshots = []
    state = {}
    for r in records:
        state = dict(state)
        state[r.variable_name] = {
            "value_display": r.variable_value,
            "serialized_value": r.serialized_value,
            "type": r.variable_type,
        }
        snapshots.append(
            {
                "id": r.id,
                "line_number": r.line_number,
                "scope": r.scope,
                "timestamp": r.timestamp,
                "trigger_variable": r.variable_name,
                "state": state,
            }
        )
    return {"snapshots": snapshots}


@app.get("/api/dashboard")
async def get_dashboard(session: Optional[str] = None):
    """Summary stats for the dashboard view."""
    records = db.get_history(session=session)
    variables = db.get_variables(session=session)
    scopes = {}
    for r in records:
        scopes[r.scope] = scopes.get(r.scope, 0) + 1
    return {
        "session": session,
        "sessions": db.get_sessions(),
        "total_events": len(records),
        "variable_count": len(variables),
        "variables": variables,
        "events_by_scope": scopes,
        "last_event": (
            {
                "variable_name": records[-1].variable_name,
                "line_number": records[-1].line_number,
                "scope": records[-1].scope,
            }
            if records
            else None
        ),
    }


# Static frontend last, so it doesn't shadow the /api/* routes above.
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")