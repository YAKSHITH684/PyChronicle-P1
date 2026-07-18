from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pychronicle.storage.database import TraceDatabase

app = FastAPI(title="PyChronicle")

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
    <html>
    <head>
    <title>PyChronicle</title>
    </head>
    <body>
        <h1>PyChronicle Execution History</h1>
        <table border="1" cellpadding="10">
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

    return html