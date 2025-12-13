<div align="center">
  <img src="https://raw.githubusercontent.com/dhruv13x/pyinitgen/main/pyinitgen_logo.png" alt="pyinitgen logo" width="200"/>
</div>

<div align="center">

<!-- Package Info -->
[![PyPI version](https://img.shields.io/pypi/v/pyinitgen.svg)](https://pypi.org/project/pyinitgen/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
![Wheel](https://img.shields.io/pypi/wheel/pyinitgen.svg)
[![Release](https://img.shields.io/badge/release-PyPI-blue)](https://pypi.org/project/pyinitgen/)

<!-- Build & Quality -->
[![Build status](https://github.com/dhruv13x/pyinitgen/actions/workflows/publish.yml/badge.svg)](https://github.com/dhruv13x/pyinitgen/actions/workflows/publish.yml)
[![Codecov](https://codecov.io/gh/dhruv13x/pyinitgen/graph/badge.svg)](https://codecov.io/gh/dhruv13x/pyinitgen)
[![Test Coverage](https://img.shields.io/badge/coverage-90%25%2B-brightgreen.svg)](https://github.com/dhruv13x/pyinitgen/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/linting-ruff-yellow.svg)](https://github.com/astral-sh/ruff)
![Security](https://img.shields.io/badge/security-CodeQL-blue.svg)

<!-- Usage -->
![Downloads](https://img.shields.io/pypi/dm/pyinitgen.svg)
![OS](https://img.shields.io/badge/os-Linux%20%7C%20macOS%20%7C%20Windows-blue.svg)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyinitgen.svg)](https://pypi.org/project/pyinitgen/)

<!-- License -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

# pyinitgen

Automated __init__.py generator for Python packages
Ensures every directory in your project is a proper Python package — no more mysterious ModuleNotFoundError surprises.

Perfect for:

Large refactors

Monorepos / multi-package architectures

Auto-generated project structures

Migration from namespace-less directories

CI environments ensuring package integrity



---

🚀 Features

| Feature                          | Description                                                              |
| -------------------------------- | ------------------------------------------------------------------------ |
| 📂 **Recursive Scan**            | Walks the directory tree intelligently to find all Python modules.       |
| 🛠️ **Auto-creates `__init__.py`** | Creates `__init__.py` files only where they are missing.                 |
| 🧠 **Smart Exclusions**          | Ignores common system and runtime directories by default.                |
| 📝 **Customized Ignores**        | Supports a `.pyinitgenignore` file to add your own exclusion rules.      |
| ✍️ **Custom Content**             | Lets you write custom content to newly created `__init__.py` files.      |
| 👀 **Dry-Run Mode**              | Preview which `__init__.py` files will be created without writing them.  |
| ✅ **Check Flag**                | Exit with error if files are missing (great for CI).                     |
| ⚙️ **Config File**               | Configure via `pyproject.toml` or `.pyinitgen.toml`.                    |
| 🎯 **Project-safe**              | Avoids touching non-Python folders and respects your project structure.  |
| ✨ **Emoji Status**               | Provides an optional, fancy terminal UX with emoji status indicators.    |
| 🔒 **Zero Destructive Actions**  | Never overwrites existing files or content.                              |



---

📦 Installation

pip install pyinitgen


---

⚙️ Configuration & Advanced Usage

### CLI Arguments

| Argument | Short | Description | Default |
|---|---|---|---|
| `--base-dir <path>` | | Base directory to scan. | `.` |
| `--dry-run` | | Preview changes without writing to disk. | `false` |
| `--quiet` | `-q` | Suppress all non-error output. | `false` |
| `--verbose` | `-v` | Show all scanned directories. | `false` |
| `--no-emoji` | | Disable emoji in the final output. | `false` |
| `--init-content "..."` | | Custom content to write to new `__init__.py` files. | `""` |
| `--check` | | Check for missing `__init__.py` files without creating them. Exits with 1 if missing. | `false` |
| `--version` | | Show the program's version number and exit. | |

### Customizing Exclusions with Configuration Files

You can configure exclusions in `pyproject.toml` or `.pyinitgen.toml`.

**Example `pyproject.toml`:**

```toml
[tool.pyinitgen]
exclude_dirs = ["legacy", "assets"]
```

**Example `.pyinitgen.toml`:**

```toml
[tool.pyinitgen]
exclude_dirs = ["legacy", "assets"]
```

### Customizing Exclusions with `.pyinitgenignore`

To exclude specific directories from being scanned, create a `.pyinitgenignore` file in your project's root directory. Each line in this file is treated as a pattern to be excluded.

> **Note:** This feature is ideal for excluding auto-generated folders, data directories, or any other project-specific directories that should not be treated as Python packages.

**Example `.pyinitgenignore`:**

```
# .pyinitgenignore
# Exclude the entire 'assets' directory
assets

# Exclude any directories named 'legacy'
legacy
```


---

📝 Example Output

Scanning: src/utils
Created src/utils/__init__.py
✅ Operation complete. Scanned 43 dirs, created 8 new __init__.py files.


---

🧩 Why this tool?

Problem	Solution

Large Python codebases without -inits	Auto insert all required files
ModuleNotFoundError during import	Ensures folders become packages
Hand-creating 50+ __init__.py files	One command 🤖
Accidental file writes?	Only creates missing files



---

⚙️ CLI Help

pyinitgen --help


---

🛡️ Safe by Design

Never touches existing files

Ignores system & irrelevant dirs by default

Supports dry-run to preview



---

💡 Tip

Use in CI to guarantee package consistency:

pyinitgen --dry-run


---

🏗️ Architecture

The project is structured as a standard Python CLI application:

```
src/
└── pyinitgen/
    ├── __init__.py
    ├── banner.py   # Renders the ASCII logo
    └── cli.py      # Core logic and CLI argument parsing
```

The core logic resides in `cli.py`, which performs the directory scan and `__init__.py` file creation. The `banner.py` module is a purely cosmetic addition to improve the user experience.

---

🗺️ Roadmap

- [x] Add support for customizing the default exclusion list via a configuration file.
- [x] Add a `--check` flag that will exit with a non-zero status code if any `__init__.py` files are missing, but will not create them.
- [ ] Implement a `--watch` mode to automatically create `__init__.py` files as new directories are created.

---

🤝 Contributing

PRs welcome — improve detection logic, add custom exclusion rules, enhance output UX.

👉 Repo: https://github.com/dhruv13x/pyinitgen


---

📜 License

MIT


---

🧭 Related Tools in the Suite

Tool	Purpose

importdoc	Import issue diagnosis
import-surgeon	Safe import refactoring
pypurge	Clean caches, venv junk
pyinitgen	Generate missing __init__.py ✅ (this project)



---

⭐ Support

If you like this tool:

⭐ Star the GitHub repo

🐍 Use it in CI & projects

📦 Recommend to Python dev friends



---