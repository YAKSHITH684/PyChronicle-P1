"""
Flask Web Application for PyChronicle
"""

from flask import Flask, jsonify, render_template_string

from pychronicle.storage.database import TraceDatabase

app = Flask(__name__)

db = TraceDatabase()

HTML = """
<!DOCTYPE html>
<html>
<head>

<title>PyChronicle</title>

<style>

body{
    font-family:Arial;
    background:#f3f5f8;
    margin:40px;
}

h1{
    color:#0f172a;
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
    background:#f9fafb;
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

{% for row in rows %}

<tr>
<td>{{ row.id }}</td>
<td>{{ row.variable_name }}</td>
<td>{{ row.variable_value }}</td>
<td>{{ row.variable_type }}</td>
<td>{{ row.line_number }}</td>
<td>{{ row.scope }}</td>
<td>{{ row.timestamp }}</td>
</tr>

{% endfor %}

</table>

</body>
</html>
"""

@app.route("/")
def index():
    rows = db.get_history()
    return render_template_string(HTML, rows=rows)

@app.route("/api/history")
def api_history():
    return jsonify(db.get_history())

@app.route("/api/history/<variable>")
def api_variable(variable):
    return jsonify(db.get_history(variable))

@app.route("/health")
def health():
    return {
        "status": "running",
        "project": "PyChronicle"
    }

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )