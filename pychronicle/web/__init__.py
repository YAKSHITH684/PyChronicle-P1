"""
web — PyChronicle's dashboard.

A small Flask app that reads the variable_traces table (written by
storage.database.TraceDatabase) and serves a single-page dashboard
for scrubbing through a run's history.

Run with:
    python -m web.app
"""