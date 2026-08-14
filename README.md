# ⏳ PyChronicle — Time-Travel Debugger for Python

PyChronicle is an AST-powered Python debugging tool that lets developers **record program execution, travel through execution snapshots, and inspect variables at different points in time**.

Instead of relying only on traditional breakpoints and print statements, PyChronicle captures program state during execution and provides an interactive interface for understanding how Python code behaves.

## 🌐 Live Demo

🔗 **Live Application:**  
https://pychronicle-p1-1.onrender.com/

---

## 📌 Overview

Debugging a Python program can become difficult when a variable changes unexpectedly or a bug occurs several lines before the actual failure.

PyChronicle addresses this problem by recording execution information and allowing developers to move backward and forward through recorded program states.

### Core workflow

\`\`\`text
Python Source Code
       ↓
   AST Parsing
       ↓
Execution Instrumentation
       ↓
Variable Assignments
       ↓
Execution Snapshots
       ↓
Session Storage
       ↓
Time-Travel Debugger
       ↓
Variable & Snapshot Inspection
\`\`\`

## ✨ Features

### 📼 Record Execution

Parse a Python script and capture variable assignments during execution.

The application records important execution information such as:

- Variable name
- Variable value
- Source-code line
- Scope
- Execution time

### 🕰️ Time Travel

Navigate through execution snapshots and inspect the state of the program at different moments.

You can:

- Move to the previous snapshot
- Move to the next snapshot
- Jump to the beginning
- Jump to the latest snapshot

### 🧬 Variable Explorer

Explore variables recorded during program execution.

The Variables Explorer provides information including:

- Variable name
- Data type
- Last recorded value
- Scope
- Number of times the variable was seen

### 🐞 Debug & Analyze

Use recorded execution states to understand how values change throughout the program and identify the source of unexpected behavior.

### 📸 Execution Snapshots

Every recorded assignment can be displayed as a snapshot containing:

- Snapshot #
- Source Line
- Variable
- Value
- Scope
- Execution Time

### 🎨 Dark Mode

PyChronicle includes an appearance toggle for switching between dark and light themes.

## 🧠 How PyChronicle Works

PyChronicle uses Python's Abstract Syntax Tree (AST) to analyze Python source code.

The source code is parsed and execution-related information is captured while the program runs.

For example:

\`\`\`python
x = 10
y = 20
z = x + y
\`\`\`

PyChronicle can record the evolution of the variables:

\`\`\`
Snapshot 1
x = 10

Snapshot 2
y = 20

Snapshot 3
z = 30
\`\`\`

The developer can then move through these snapshots and inspect the state of the program at each point.

## 🔍 Example

Consider the following Python program:

\`\`\`python
def calculate():
    x = 10
    y = 5
    result = x * y

    return result


value = calculate()
print(value)
\`\`\`

PyChronicle can capture the execution of assignments such as:

\`\`\`
x       → 10
y       → 5
result  → 50
value   → 50
\`\`\`

These states can then be inspected through the debugger interface.

## 🖥️ Application Interface

The application contains several major sections:

**Dashboard**
Provides an overview of the current debugging session.

**Time Travel**
Allows navigation through execution snapshots.

\`\`\`
Previous ← Snapshot → Next
\`\`\`

**Snapshot Information**
Displays details about the currently selected execution state:

- Line
- Variable
- Scope
- Time
- Value

**Variables Explorer**
Allows users to search and inspect variables recorded during execution.

**Snapshots**
Displays all captured assignments in chronological order.

**Settings**
Provides:

- Python file parsing
- Session selection
- Appearance settings

## 🛠️ Technology Stack

**Backend**
- Python
- Flask
- AST (ast module)

**Frontend**
- HTML
- CSS
- JavaScript

**Data Processing**
- Python data structures
- Execution snapshots
- Session-based state management

**Deployment**
- Render

## 📂 Project Structure

\`\`\`
PyChronicle/
│
├── pychronicle/
│   ├── __init__.py
│   ├── ast/
│   ├── debugger/
│   ├── storage/
│   └── ...
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── ...
│
├── app.py
├── requirements.txt
├── Procfile
└── README.md
\`\`\`

The exact structure may vary depending on the current repository version.

## ⚙️ Installation

### 1. Clone the Repository
\`\`\`bash
git clone https://github.com/YAKSHITH684/PyChronicle.git
\`\`\`

### 2. Navigate to the Project
\`\`\`bash
cd PyChronicle
\`\`\`

### 3. Create a Virtual Environment
\`\`\`bash
python -m venv venv
\`\`\`

### 4. Activate the Virtual Environment

**Windows**
\`\`\`bash
venv\\Scripts\\activate
\`\`\`

**Linux / macOS**
\`\`\`bash
source venv/bin/activate
\`\`\`

### 5. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 6. Start the Application
\`\`\`bash
python app.py
\`\`\`

Open:
\`\`\`
http://127.0.0.1:5000/
\`\`\`

## 🚀 Usage

**Step 1**
Open the PyChronicle web application.

**Step 2**
Go to Settings.

**Step 3**
Select a Python source file.

**Step 4**
Click:
\`\`\`
Parse File
\`\`\`

**Step 5**
PyChronicle records execution information.

**Step 6**
Use the Time Travel controls to navigate through snapshots.

**Step 7**
Inspect variables and their values using the Variables Explorer.

## 🎯 Why PyChronicle?

Traditional debugging often requires developers to:

- Add print statements
- Add breakpoints
- Re-run programs repeatedly
- Guess where a variable changed

PyChronicle provides a different approach:

\`\`\`
Run Once
   ↓
Record State
   ↓
Navigate History
   ↓
Inspect Variables
   ↓
Understand the Bug
\`\`\`

This makes it easier to understand the evolution of program state.

## 🔐 Safety Considerations

PyChronicle executes Python source code for debugging purposes.

Only parse and execute Python programs that you trust.

For production deployments, additional security controls should be considered, including:

- Sandboxed execution
- Resource limits
- CPU limits
- Memory limits
- File-system restrictions
- Process isolation
- Execution timeouts

## 🔮 Future Improvements

Potential improvements include:

- Conditional breakpoints
- Step-by-step execution
- Call-stack visualization
- Exception tracking
- Function-level execution tracing
- Code editor integration
- Syntax highlighting
- Diff between snapshots
- Search through execution history
- Export debugging sessions
- Multi-file project debugging
- Docker-based sandboxing
- AI-powered bug explanations

## 📚 Concepts Used

This project demonstrates practical knowledge of:

- Python AST
- Abstract Syntax Trees
- Code instrumentation
- Program execution tracing
- Debugging systems
- Variable state tracking
- Snapshot-based debugging
- Session management
- Flask web applications
- Frontend/backend integration
- Cloud deployment

## 💡 Project Highlights

**AST-Powered**
Python source code is analyzed using the Abstract Syntax Tree rather than treating the source purely as text.

**State Tracking**
Variable assignments are captured during program execution.

**Time-Travel Debugging**
Developers can navigate through previously recorded execution states.

**Interactive Interface**
The web interface provides dedicated sections for snapshots, variables, and debugging.

**Cloud Deployment**
The application is deployed and accessible through a public Render URL.

## 🌐 Live Project

**PyChronicle — Time-Travel Debugger**

https://pychronicle-p1-1.onrender.com/

## 👨‍💻 Author

**Yakshith Anandapu**

B.Tech — Computer Science and Engineering

**GitHub**
https://github.com/YAKSHITH684

**LinkedIn**
https://www.linkedin.com/in/anandapu-yakshith684/

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.
