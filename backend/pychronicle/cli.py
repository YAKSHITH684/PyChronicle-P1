import typer
from pathlib import Path

from pychronicle.ast_engine.executor import run_and_trace
from pychronicle.database import TraceDatabase

app = typer.Typer(
    name="pychronicle",
    help="PyChronicle - Python execution tracing and time-travel debugging tool"
)


@app.command()
def run(
    script: str = typer.Argument(..., help="Python script to trace")
):
    """Run and trace a Python script."""

    script_path = Path(script).resolve()

    if not script_path.exists():
        typer.echo(f"Error: File not found: {script}")
        raise typer.Exit(code=1)

    if script_path.suffix.lower() != ".py":
        typer.echo("Error: Please provide a Python (.py) file.")
        raise typer.Exit(code=1)

    typer.echo(f"Running: {script_path}")
    typer.echo("Tracing execution...")

    try:
        db = TraceDatabase()

        result = run_and_trace(
            str(script_path),
            db
        )

        typer.echo("")
        typer.echo("PyChronicle execution completed.")
        typer.echo(f"Session: {result['session']}")
        typer.echo(f"Assignments traced: {result['trace_count']}")

        variables = result["variables"]

        if variables:
            typer.echo(f"Variables: {', '.join(variables)}")
        else:
            typer.echo("Variables: None")

        if result["error"]:
            typer.echo("")
            typer.echo("Program error:")
            typer.echo(result["error"])

    except Exception as exc:
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=1)


@app.command()
def version():
    """Show PyChronicle version."""
    typer.echo("PyChronicle 1.0.0")


if __name__ == "__main__":
    app()
# CLI entry points reuse the same tracing engine as the web API.
