# src/pyinitgen/config.py
import sys
from pathlib import Path
from typing import Set

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

EXCLUDE_DIRS = {
    # VCS
    ".git",
    ".hg",
    ".svn",

    # Python Caches/Tools
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",

    # JS/Node
    "node_modules",

    # IDE / OS
    ".vscode",
    ".idea",
    ".DS_Store",

    # Build / Dist
    "build",
    "dist",
    "eggs",
    ".egg-info",

    # Docs
    "docs",
    "site",

    # Other tools
    ".github",

    # Python test/build artifacts
    "htmlcov",
    ".tox",
    ".nox",
    "pip-wheel-metadata",

    # Temporary/data directories
    "tmp",
    "temp",
    "data",
    "assets",
    "static",
    "media",
}

IGNORE_FILE_NAME = ".pyinitgenignore"

def load_config(base_dir: Path) -> Set[str]:
    """
    Loads configuration from pyproject.toml or .pyinitgen.toml.
    Returns a set of exclude dirs found in the config.
    """
    config_files = [".pyinitgen.toml", "pyproject.toml"]

    for filename in config_files:
        config_path = base_dir / filename
        if config_path.is_file():
            try:
                with open(config_path, "rb") as f:
                    data = tomllib.load(f)

                # Check for [tool.pyinitgen]
                if "tool" in data and "pyinitgen" in data["tool"]:
                    config = data["tool"]["pyinitgen"]
                    exclude_dirs = config.get("exclude_dirs", [])
                    if isinstance(exclude_dirs, list):
                        return set(exclude_dirs)
            except Exception:
                # If parsing fails, just ignore
                pass

    return set()
