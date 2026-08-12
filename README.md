# PyChronicle

Python execution tracing / time-travel debugging tool, split into two
independent pieces:

```
PyChronicle_clean/
├── backend/     FastAPI + pychronicle tracing engine (the API)
└── frontend/    Static dashboard (HTML/CSS/JS) that talks to the API
```

## Backend

```
cd backend
pip install -r requirements.txt
uvicorn pychronicle.web.app:app --reload
```

Runs on `http://localhost:8000` by default and exposes `/api/*`
(parse, sessions, variables, timeline, history, snapshots, dashboard).
CORS is open to any origin, so the frontend can be served from anywhere.

`pychronicle` is also installable as a CLI (`pip install -e .` from
`backend/`, then `pychronicle run <script.py>`).

`Sample_scripts/` holds example `.py` files you can upload to `/api/parse`
to try it out.

## Frontend

Plain static files — no build step. Serve the folder with anything
(`python -m http.server`, VS Code Live Server, etc.) or open
`index.html` directly.

`frontend/config.js` sets the backend URL:

```js
const API_BASE_URL = "http://localhost:8000";
```

Change this if the backend runs somewhere else (or set it to `""` if
you ever serve frontend and backend from the same origin again).

## What changed from the original zip

- Split the single `pychronicle/web/static/index.html` (which had
  inline `<style>` and `<script>` blocks) into `index.html`,
  `styles.css`, `app.js`, and a new `config.js` for the API URL.
- Backend (`pychronicle/` package + `app.py`) no longer mounts static
  files — it's a pure API now that the dashboard lives separately.
- Removed the stray, unused root `main.py` (an old prototype API that
  wasn't wired into the real app) and updated `render.yaml` to start
  `pychronicle.web.app:app` instead.
- Deleted `venv/`, `__pycache__/`, `*.pyc`, `pychronicle.egg-info/`,
  the generated `pychronicle.db`, and `sessions_data.txt` — all
  build/runtime artifacts that shouldn't ship with source.
