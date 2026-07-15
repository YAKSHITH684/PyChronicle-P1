"""
PyChronicle

A lightweight Python execution tracing framework that records
variable assignments, tracks value changes, stores execution
history in SQLite, and provides a simple web dashboard.

Author: Your Name
Version: 1.0.0
"""

__title__ = "PyChronicle"
__version__ = "1.0.0"
__author__ = "Your Name"

from pychronicle.storage.database import TraceDatabase
from pychronicle.tracer.execution_tracer import ExecutionTracer
from pychronicle.tracer.delta_tracker import DeltaTracker
from pychronicle.ast_engine.parser import (
    VariableAssignment,
    parse_file,
    parse_source,
)
from pychronicle.ast_engine.rewriter import (
    rewrite_file,
    rewrite_source,
)

__all__ = [
    "TraceDatabase",
    "ExecutionTracer",
    "DeltaTracker",
    "VariableAssignment",
    "parse_file",
    "parse_source",
    "rewrite_file",
    "rewrite_source",
]