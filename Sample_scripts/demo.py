r"""
Demo: parse sample_target.py with the AST engine, then persist every
assignment found into the SQLite trace store.

Run with:  python Sample_scripts\demo.py   (from the PyChronicle P1 root)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pychronicle.ast_engine.parser import parse_file
from pychronicle.storage.database import TraceDatabase

TARGET_FILE = Path(__file__).parent / "sample_target.py"
DB_PATH = Path(__file__).resolve().parent.parent / "Data" / "traces.db"


def main():
    assignments = parse_file(TARGET_FILE)
    print(f"Found {len(assignments)} assignment(s) in {TARGET_FILE.name}:\n")

    with TraceDatabase(DB_PATH) as db:
        for a in assignments:
            print(f"  L{a.line_number:<3} [{a.scope:<10}] {a.name} = {a.value_expr}")
            db.insert_trace(
                line_number=a.line_number,
                variable_name=a.name,
                value=a.value_expr,   # storing the source expression as the "value"
                scope=a.scope,
                session_id="demo-run",
            )

        print("\nStored history for 'total':")
        for row in db.history_for_variable("total"):
            print(f"  {dict(row)}")


if __name__ == "__main__":
    main()