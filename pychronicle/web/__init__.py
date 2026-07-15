"""
PyChronicle Web Package

Provides the Flask web application for visualizing
execution history stored in the SQLite database.
"""

from .app import app

__all__ = ["app"]