# src/pyinitgen/ignores.py

from pathlib import Path
from .config import IGNORE_FILE_NAME

def load_ignore_patterns(base_dir: Path) -> set[str]:
    """
    Loads ignore patterns from a .pyinitgenignore file in the base_dir.
    """
    ignore_file_path = base_dir / IGNORE_FILE_NAME
    if not ignore_file_path.is_file():
        return set()

    patterns = set()
    with open(ignore_file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.add(line)
    return patterns
