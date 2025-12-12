# 📦 Local Package Dependency Visualizer (LPV)

**LPV** is a Python command-line tool that analyzes a project’s import structure and builds a complete dependency graph. It detects cycles, dead code, oversized modules, risky dynamic imports, and generates ASCII or Graphviz visualizations.

This tool is designed for developers who want fast, accurate insights into Python project architecture — ideal for refactoring, debugging, and CI automation.

---

## 🚀 Features

- **AST-based Parsing**  
- **Dependency Graph Construction**  
- **Cycle Detection (DFS)**  
- **Dead Code Detection (BFS)**  
- **Oversized Module Detection**  
- **Module Split Suggestions**  
- **Dynamic Import Warnings**  
- **ASCII Visualization**  
- **Graphviz Export (DOT, PNG, SVG, PDF)**  
- **Fast & Lightweight**  

---

## 📁 Project Structure

```
lpv/
│
├── parser/
│   ├── ast_parser.py
│   ├── import_resolver.py
│   ├── graph_builder.py
│   └── dynamic_import_detector.py
│
├── analyzer/
│   ├── cycle_detector.py
│   ├── dead_code_detector.py
│   ├── module_analyzer.py
│   ├── split_suggester.py
│   └── visualizer.py
│
├── cli.py
└── README.md
```

---

## 📦 Installation

### Requirements
- Python **3.7+**
- Optional: **Graphviz**

### Install from PyPI:

```bash
pip install lpv
```

### Install locally:

```bash
pip install -e .
```

---

## 🛠 CLI Usage (Using `lpv`)

### Basic:

```bash
lpv .
```

### Detect cycles:

```bash
lpv . --cycles
```

### ASCII Map:

```bash
lpv . --ascii
```

### Graphviz Export:

```bash
lpv . --graphviz deps.dot
```

---

## 🔥 Complete CLI Command Reference (Using `lpv`)

### Basic Analysis
```bash
lpv .
```

### Show Summary
```bash
lpv . --summary
```

### Detect Circular Imports
```bash
lpv . --cycles
```

### Detect Dead Code
```bash
lpv . --dead-code
```

### Detect Dynamic Imports
```bash
lpv . --dynamic-imports
```

### ASCII Dependency Map
```bash
lpv . --ascii
```

### ASCII Map With Depth Limit
```bash
lpv . --ascii --max-depth 4
```

### Oversized Modules (default: 500 lines)
```bash
lpv . --oversized 500
```

### Module Split Suggestions
```bash
lpv . --suggest-splits
```

### Export Graph as DOT
```bash
lpv . --graphviz deps.dot
```

### Export Graph as PNG
```bash
lpv . --graphviz deps.png --format png
```

### Exclude Folders (venv, env, dist, build…)
```bash
lpv . --exclude venv env dist build
```

### Full Project Audit
```bash
lpv . --cycles --dead-code --dynamic-imports --oversized 500 --suggest-splits --ascii --summary
```

---

## 🧪 Sample Project Demo

```bash
lpv tests/sample_project \
  --cycles \
  --dead-code \
  --oversized 150 \
  --suggest-splits \
  --dynamic-imports \
  --ascii \
  --summary
```

Or run:

```bash
bash tests/run_sample_demo.sh
```

---

## 📌 Examples

### Circular Dependencies

```
⚠️  CIRCULAR DEPENDENCIES DETECTED:
  Cycle 1: a.py → b.py → c.py → a.py
  Cycle 2: utils.py → helpers.py → utils.py
```

### Oversized Modules

```
⚠️  OVERSIZED MODULES (> 300 lines):
  - parser/ast_parser.py : 450
  - analyzer/visualizer.py : 380
  - main.py : 320
```

### Split Suggestions

```
💡 MODULE SPLIT SUGGESTIONS:

parser/ast_parser.py:
  - Suggest splitting by class groups
  Reason: Contains 5 unrelated class groups
```

### ASCII Map

```bash
lpv . --ascii --max-depth 4
```

### PNG Export

```bash
lpv . --graphviz deps.png --format png
```

---

## 🔗 Pre-commit Integration

Add this:

```yaml
repos:
  - repo: local
    hooks:
      - id: dependency-check
        name: Check for circular dependencies
        entry: lpv
        language: system
        args: ['.', '--cycles']
        pass_filenames: false
        always_run: true
```

---

## ⚙ Algorithms

| Feature | Algorithm |
|--------|-----------|
| Cycle Detection | DFS + recursion stack |
| Dead Code Detection | BFS reachability |
| Graph Builder | Directed adjacency graph |
| Split Suggestions | Heuristic clustering |

---

## ⏱ Performance

- Time: **O(V + E)**
- Space: **O(V + E)**
- Handles hundreds of files efficiently

---

## ⚠ Limitations

- Dynamic imports detected but not resolved  
- Dead code detection is heuristic  
- External packages not resolved  
- Split suggestions are heuristic  

---

## 📄 License

Educational use only.

---

## 👥 Authors

- **Sagar Veeresh Halladakeri** — 251810700276  
- **Nesar Ravishankar Kavri** — 251810700211  
Group 127  

---

## ✔ Required PyProject Configuration

Ensure your `pyproject.toml` includes:

```toml
[project.scripts]
lpv = "cli:main"
```

This enables the **lpv** command globally.