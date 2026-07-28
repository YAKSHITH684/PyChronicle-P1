# ⏳ PyChronicle

**The AST-powered time-travel debugger for Python.**
Record. Travel. Debug. Like never before.

PyChronicle parses your script, captures every variable assignment as it runs, and lets you jump back to any moment in execution to inspect state — no more sprinkling `print()` statements or restarting your debugger from scratch.

---

## ✨ Features

| | Feature | Description |
|---|---|---|
| 🎞️ | **Record Execution** | Parse your script and capture every variable assignment. |
| ⏰ | **Time Travel** | Jump back to any moment and inspect state at that point. |
| 🧬 | **Inspect Variables** | Explore every variable and its values across the run. |
| 🐞 | **Analyze & Debug** | Understand your code better and fix bugs faster. |

## 📊 Dashboard

The dashboard gives you an overview of your recent debugging sessions, each identified by a unique session ID, with the ability to reopen and replay any of them.

- **Dashboard** — session overview and quick actions
- **Time Travel** — step backward and forward through execution
- **Variables** — inspect variable state at any point in time
- **Snapshots** — saved captures of program state
- **Settings** — parse a file, switch sessions, and adjust appearance

## 🚀 Getting Started

### Requirements

- Python 3.6+

### Installation

```bash
git clone https://github.com/your-org/pychronicle.git
cd pychronicle
pip install -r requirements.txt
```

### Usage

Record a session by running your script through PyChronicle:

```bash
pychronicle record my_script.py
```

Then open the dashboard to browse sessions, or jump straight into Time Travel mode to step through captured state.

## 🧪 Example Scripts

The `examples/` folder includes a few scripts you can use to try out recording and time-traveling through a run, each demonstrating a bit more complexity:

| Script | Lines | What it demonstrates |
|---|---|---|
| `demo1.py` | 25 | A basic function call and variable assignments — good first recording. |
| `demo2.py` | 54 | Parses a file and switches between multiple sessions mid-run. |
| `demo3.py` | ~97 | Adds appearance-style settings (via classes) alongside file parsing and session switching. |

Record one of them:

```bash
pychronicle record examples/demo1.py
```

Then open the Dashboard, find the new session by its ID, and click **Open** to start traveling through it.

## ⚙️ Settings

From the Settings page you can:
- **Parse a file** — point PyChronicle at a script to record
- **Switch sessions** — move between previously recorded runs
- **Adjust appearance** — toggle light/dark mode and other display preferences

## 🤝 Contributing

Issues and pull requests are welcome. Please open an issue to discuss any significant changes before submitting a PR.

## 📄 License

[MIT](LICENSE)