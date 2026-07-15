"""
PyChronicle Command Line Interface

Run using:

python -m pychronicle

or

python -m pychronicle parse sample.py

or

python -m pychronicle web
"""

import argparse

from pychronicle.ast_engine.parser import parse_file
from pychronicle.ast_engine.rewriter import rewrite_file
from pychronicle.tracer.execution_tracer import ExecutionTracer


def run_demo():
    """Run a simple tracing demo."""

    tracer = ExecutionTracer()

    print("\n=== PyChronicle Demo ===\n")

    x = 10
    tracer.trace("x", x, 1)

    y = 20
    tracer.trace("y", y, 2)

    z = x + y
    tracer.trace("z", z, 3)

    print("\nExecution History\n")

    for row in tracer.history():
        print(row)

    tracer.close()


def parse_command(file_path):
    """Parse a Python file."""

    assignments = parse_file(file_path)

    print("\nAssignments Found\n")

    for assignment in assignments:
        print(assignment)


def rewrite_command(input_file, output_file):
    """Rewrite a Python file."""

    rewrite_file(input_file, output_file)

    print("\nFile rewritten successfully.")

    print(f"Output: {output_file}")


def start_web():
    """Start Flask Dashboard."""

    from pychronicle.web.app import app

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )


def main():

    parser = argparse.ArgumentParser(
        description="PyChronicle CLI"
    )

    sub = parser.add_subparsers(dest="command")

    parser_parse = sub.add_parser(
        "parse",
        help="Parse a Python file"
    )

    parser_parse.add_argument("file")

    parser_rewrite = sub.add_parser(
        "rewrite",
        help="Rewrite a Python file"
    )

    parser_rewrite.add_argument("input")

    parser_rewrite.add_argument("output")

    sub.add_parser(
        "demo",
        help="Run demo program"
    )

    sub.add_parser(
        "web",
        help="Start web dashboard"
    )

    args = parser.parse_args()

    if args.command == "parse":

        parse_command(args.file)

    elif args.command == "rewrite":

        rewrite_command(
            args.input,
            args.output,
        )

    elif args.command == "web":

        start_web()

    else:

        run_demo()


if __name__ == "__main__":
    main()