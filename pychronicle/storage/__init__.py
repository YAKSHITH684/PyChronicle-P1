"""
Storage package for PyChronicle.

Provides a lightweight SQLite database layer for storing
variable execution history.
"""

from .database import TraceDatabase
from .schema import create_schema

__all__ = [
    "TraceDatabase",
    "create_schema",
]