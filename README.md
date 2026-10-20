# Theory of Computing Toolkit

A web application combining two Theory of Computing course projects:

- **Regex → NFA:** convert regular expressions into nondeterministic finite automata.
- **CFG → PDA:** construct pushdown automata from context-free grammars and test input strings.

## Features

- Homepage with a separate card for each tool.
- Automaton diagrams generated using Graphviz.
- Start and accept state information.
- Transition information for both tools.
- A structured PDA transition table.
- PDA string testing, including the empty string.
- Input validation and error feedback.
- Search limits that report inconclusive results instead of false rejection.

## Technologies

- Frontend: Next.js, React, TypeScript, Tailwind CSS.
- Backend: Python, Flask, Flask-CORS.
- Visualization: Graphviz.

## Requirements

- Python 3.10 or later.
- Node.js and npm compatible with the frontend dependencies.
- Graphviz installed on the system, with `dot` available on PATH.

Check Graphviz installation:

```bash
dot -V
```

Installing the Python `graphviz` package alone does not install the
Graphviz system application.

## Run locally

Open two terminals.

### Backend

From the project root:

```bash
cd backend
python -m pip install -r requirements.txt
python -m flask --app app.main run --port 5000
```

A Python virtual environment is recommended.

### Frontend

From the project root, in the second terminal:

```bash
cd frontend
npm ci
npm run dev
```

Open http://localhost:3000.

The current frontend connects to the backend at
http://localhost:5000.

## Regex to NFA

Supported operations include:

- Alphanumeric literals.
- Concatenation: `ab`.
- Union: `a|b`.
- Kleene star: `a*`.
- Positive closure: `a+`.
- Grouping: `(a|b)*abb`.

This is a teaching subset of regular-expression syntax.

## CFG to PDA

Enter the start symbol, comma-separated terminals, and production rules:

```text
S
a,b
S -> a S b | ε
```

Separate symbols on the right-hand side with spaces.
Use `ε` or `λ` for an empty production.

For this grammar:

- `ab` is accepted.
- `aabb` is accepted.
- `abb` is rejected.
- The empty string is accepted.

In the web interface, leave the test-string input empty to test epsilon.

PDA edge labels use:

```text
input, pop → push
```

String testing explores the constructed PDA using breadth-first search.
Acceptance requires all input consumed, an empty stack, and the accept state.
If the search reaches its time or configuration limit, the result is
reported as inconclusive.

## API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/api/convert` | Convert a regex into an NFA |
| POST | `/api/cfg-to-pda` | Convert a CFG into a PDA |
| POST | `/api/cfg-to-pda/test` | Test a string against the constructed PDA |

## Project organization

- `frontend/src/app`: homepage and individual tool pages.
- `frontend/src/components`: input, result, and string-testing components.
- `backend/app/main.py`: Flask API endpoints.
- `backend/app/nfa.py`: regex parsing, NFA construction, and drawing.
- `backend/app/cfg.py`: CFG parsing, PDA construction, drawing, and string testing.

The original university submission files and report are maintained
separately from this web repository.
