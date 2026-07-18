from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from pychronicle.storage.database import TraceDatabase

app = FastAPI(title="PyChronicle")

# Allow frontend requests
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
    return {
        "message": "PyChronicle API Running"
    }


@app.get("/health")
def health():
    return {
        "status": "running",
        "project": "PyChronicle"
    }


@app.get("/api/history")
def history():
    return db.get_history()


@app.get("/api/history/{variable}")
def variable(variable: str):
    return db.get_history(variable)


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