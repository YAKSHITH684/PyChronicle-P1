import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from pychronicle.storage.database import TraceDatabase
from pychronicle.ast_engine.executor import run_and_trace

app = FastAPI(title="PyChronicle")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = TraceDatabase()


@app.get("/health")
def health():
    return {
        "status": "running",
        "project": "PyChronicle"
    }


# -------------------------
# PARSE (execute + trace) A PYTHON FILE
# -------------------------

class ParseRequest(BaseModel):
    path: str


@app.post("/api/parse")
async def parse_python_file(body: ParseRequest):
    """
    Execute the Python file at `path` with tracing instrumentation
    inserted, recording every variable assignment into a new session.
    """

    try:
        result = run_and_trace(body.path, db)

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=f"Syntax error in target file: {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


# -------------------------
# HISTORY (legacy / raw access)
# -------------------------

@app.get("/api/history")
def history(session: str = None):
    return db.get_history(session=session)


@app.get("/api/history/{variable}")
def variable_history(variable: str, session: str = None):
    return db.get_history(session=session, variable=variable)


# -------------------------
# SESSIONS
# -------------------------

@app.get("/api/sessions")
def sessions():
    """Plain array of session-id strings, oldest first."""
    return db.get_sessions()


# -------------------------
# TIMELINE
# -------------------------

@app.get("/api/timeline")
def timeline(session: str = None):
    """
    Array of trace rows for the given session (or all sessions if
    omitted), shaped for the frontend's scrubber/snapshot views.
    """

    rows = db.get_history(session=session)

    return [
        {
            "id": row.id,
            "session": row.session,
            "variable_name": row.variable_name,
            "value_type": row.variable_type,
            "serialized_value": row.serialized_value,
            "line_number": row.line_number,
            "scope": row.scope,
            "timestamp": row.timestamp,
        }
        for row in rows
    ]


# -------------------------
# VARIABLES
# -------------------------

@app.get("/api/variables")
def variables(session: str = None):
    """Plain array of distinct variable-name strings for the session."""
    return db.get_variables(session=session)


# -------------------------
# DASHBOARD
# -------------------------

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    rows = db.get_history()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>PyChronicle Dashboard</title>

        <style>

        body{
            font-family:Arial;
            background:#f5f7fb;
            padding:40px;
        }

        h1{
            color:#2563eb;
        }

        table{
            width:100%;
            border-collapse:collapse;
            background:white;
        }

        th{
            background:#2563eb;
            color:white;
            padding:10px;
        }

        td{
            border:1px solid #ddd;
            padding:10px;
            text-align:center;
        }

        tr:nth-child(even){
            background:#f2f2f2;
        }

        </style>

    </head>

    <body>

    <h1>PyChronicle Execution History</h1>

    <table>

    <tr>
        <th>ID</th>
        <th>Session</th>
        <th>Variable</th>
        <th>Value</th>
        <th>Type</th>
        <th>Line</th>
        <th>Scope</th>
        <th>Timestamp</th>
    </tr>
    """

    for r in rows:

        html += f"""
        <tr>
            <td>{r.id}</td>
            <td>{r.session}</td>
            <td>{r.variable_name}</td>
            <td>{r.variable_value}</td>
            <td>{r.variable_type}</td>
            <td>{r.line_number}</td>
            <td>{r.scope}</td>
            <td>{r.timestamp}</td>
        </tr>
        """

    html += """
    </table>

    </body>
    </html>
    """

    return HTMLResponse(content=html)


# -------------------------
# FRONTEND
# -------------------------

_INDEX_PATH = os.path.join(os.path.dirname(__file__), "static", "index.html")


@app.get("/", response_class=HTMLResponse)
def home():
    """Serve the PyChronicle frontend."""
    with open(_INDEX_PATH, "r", encoding="utf-8") as f:
        return f.read()