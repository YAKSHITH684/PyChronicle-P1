from fastapi import FastAPI, UploadFile, File
import subprocess
import uuid
import os

app = FastAPI(
    title="PyChronicle API",
    description="Python execution tracing and time-travel debugging API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "PyChronicle API Running",
        "version": "1.0.0"
    }


@app.post("/trace")
async def trace_script(file: UploadFile = File(...)):

    filename = f"temp_{uuid.uuid4()}.py"

    with open(filename, "wb") as f:
        f.write(await file.read())

    result = subprocess.run(
        ["pychronicle", "run", filename],
        capture_output=True,
        text=True
    )

    os.remove(filename)

    return {
        "output": result.stdout,
        "error": result.stderr
    }