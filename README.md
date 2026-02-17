# AI-Q7

A small Python project containing algorithm and grid utilities with a simple runner in `main.py`.

## Project Overview

This repository contains modular implementations of algorithms and dynamic/grid helpers used by `main.py` to demonstrate or run sample tasks.

## Files
- `main.py` — Entry point to run examples or demos.
- `algorithms.py` — Algorithm implementations and helpers.
- `dynamic.py` — Dynamic programming related utilities.
- `grid.py` — Grid-based helper functions (traversal, neighbors, etc.).
- `constants.py` — Project-wide constants and configuration values.
- `__pycache__/` — Compiled Python files (auto-generated).


# AI Grid Pathfinder – Uninformed Search Visualization

## Description
This project implements and visualizes six uninformed search algorithms in a dynamic grid environment.

Algorithms Included:
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Uniform-Cost Search (UCS)
- Depth-Limited Search (DLS)
- Iterative Deepening DFS (IDDFS)
- Bidirectional Search

The system visualizes:
- Frontier nodes
- Explored nodes
- Final path
- Dynamic obstacles that spawn during execution
- Automatic re-planning behavior


## Requirements

- Python 3.8+ (Anaconda recommended, but not required).

## Installation

1. Clone the repo:

```bash
git clone <repo-url>
cd AI-Q7
```

2. (Optional) Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

3. Install dependencies if your project adds them later (none required right now):

```bash
pip install -r requirements.txt
```

## Running

Run the main script to execute the project's demo or entry routine:

```bash
python main.py
```

## Contributing

Contributions are welcome. Please open issues for bugs or feature requests and submit pull requests for changes.

## License

Specify a license if you wish (MIT, Apache 2.0, etc.).

---
Generated README for the workspace located at the project root.
