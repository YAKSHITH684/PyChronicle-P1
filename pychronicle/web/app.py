import os
import tempfile

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from pychronicle.storage.database import TraceDatabase
from pychronicle.ast_engine.parser import parse_file

app = FastAPI(title="PyChronicle")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = TraceDatabase()


@app.get("/")
def home():
    return {"message": "PyChronicle API Running"}


@app.get("/health")
def health():
    return {
        "status": "running",
        "project": "PyChronicle"
    }


# -------------------------
# PARSE PYTHON FILE
# -------------------------

@app.post("/api/parse")
async def parse_python_file(file: UploadFile = File(...)):
    """
    Upload a Python file and parse it.
    """

    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(await file.read())
        temp_path = temp.name

    try:
        assignments = parse_file(temp_path)

        return {
            "success": True,
            "filename": file.filename,
            "assignments": assignments
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)


# -------------------------
# HISTORY
# -------------------------

@app.get("/api/history")
def history():
    return db.get_history()


@app.get("/api/history/{variable}")
def variable(variable: str):
    return db.get_history(variable)


# -------------------------
# SESSIONS
# -------------------------

@app.get("/api/sessions")
def sessions():

    history = db.get_history()

    return {
        "total_sessions": len(history),
        "history": history
    }


# -------------------------
# TIMELINE
# -------------------------

@app.get("/api/timeline")
def timeline():

    return db.get_history()


# -------------------------
# VARIABLES
# -------------------------

@app.get("/api/variables")
def variables():

    history = db.get_history()

    data = []

    seen = set()

    for row in history:

        name = row.variable_name

        if name not in seen:

            seen.add(name)

            data.append({
                "variable": row.variable_name,
                "value": row.variable_value,
                "type": row.variable_type,
                "line": row.line_number,
                "scope": row.scope,
                "timestamp": row.timestamp
            })

    return data


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