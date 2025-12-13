# tests/test_cli.py

import os
from pathlib import Path
import pytest
from pyinitgen.cli import create_inits
from pyinitgen.config import EXCLUDE_DIRS

# Note: We use 'fs' fixture from pyfakefs for all file system operations.
# This ensures isolation and speed, avoiding real disk IO.

@pytest.fixture
def project_structure(fs):
    """
    Creates a standard project structure for testing using pyfakefs.
    """
    # Create a basic structure
    fs.create_dir("/project_root/package_a/subpackage_a")
    fs.create_dir("/project_root/package_b/subpackage_b")
    
    # Create some excluded directories
    fs.create_dir("/project_root/.git")
    fs.create_dir("/project_root/__pycache__")
    fs.create_dir("/project_root/node_modules")
    fs.create_dir("/project_root/docs")
    fs.create_dir("/project_root/venv")
    fs.create_dir("/project_root/data")
    fs.create_dir("/project_root/assets")
    
    # Create a file to ensure it doesn't interfere
    fs.create_file("/project_root/package_a/module.py")
    
    return Path("/project_root")


def test_create_inits_dry_run(project_structure):
    """
    Test that __init__.py files are not created in dry-run mode.
    """
    # Act
    exit_code, created_count, scanned_dirs = create_inits(project_structure, dry_run=True)

    # Assert
    assert exit_code == 0
    assert created_count == 0
    assert not (project_structure / "package_a" / "__init__.py").exists()
    assert not (project_structure / "package_a" / "subpackage_a" / "__init__.py").exists()
    assert not (project_structure / "package_b" / "__init__.py").exists()
    assert not (project_structure / "package_b" / "subpackage_b" / "__init__.py").exists()


def test_create_inits_actual_run(project_structure):
    """
    Test that __init__.py files are created correctly in actual run mode,
    and excluded directories are ignored.
    """
    # Act
    exit_code, created_count, scanned_dirs = create_inits(project_structure, dry_run=False)

    # Assert
    assert exit_code == 0
    # Expecting __init__.py in:
    # project_root (base_dir itself)
    # package_a
    # package_a/subpackage_a
    # package_b
    # package_b/subpackage_b
    assert created_count == 5 
    
    assert (project_structure / "__init__.py").exists()
    assert (project_structure / "package_a" / "__init__.py").exists()
    assert (project_structure / "package_a" / "subpackage_a" / "__init__.py").exists()
    assert (project_structure / "package_b" / "__init__.py").exists()
    assert (project_structure / "package_b" / "subpackage_b" / "__init__.py").exists()

    # Assert that __init__.py are NOT created in excluded directories
    assert not (project_structure / ".git" / "__init__.py").exists()
    assert not (project_structure / "__pycache__" / "__init__.py").exists()
    assert not (project_structure / "node_modules" / "__init__.py").exists()
    assert not (project_structure / "docs" / "__init__.py").exists()
    assert not (project_structure / "venv" / "__init__.py").exists()
    assert not (project_structure / "data" / "__init__.py").exists()
    assert not (project_structure / "assets" / "__init__.py").exists()


def test_create_inits_existing_init_file(project_structure, fs):
    """
    Test that create_inits does not overwrite existing __init__.py files.
    """
    # Arrange
    fs.create_file("/project_root/package_a/__init__.py")
    
    # Act
    exit_code, created_count, scanned_dirs = create_inits(project_structure, dry_run=False)
    
    # Assert
    assert exit_code == 0
    # Only 4 new files should be created (project_root, subpackage_a, package_b, subpackage_b)
    assert created_count == 4 
    assert (project_structure / "package_a" / "__init__.py").exists() # Should still exist
    assert (project_structure / "package_a" / "subpackage_a" / "__init__.py").exists()
    assert (project_structure / "package_b" / "__init__.py").exists()
    assert (project_structure / "package_b" / "subpackage_b" / "__init__.py").exists()


def test_exclude_dirs_content():
    """
    Test that EXCLUDE_DIRS contains expected entries.
    """
    expected_excludes = {
        ".git", ".hg", ".svn", "__pycache__", ".venv", "venv", "env",
        ".mypy_cache", ".pytest_cache", ".ruff_cache", "node_modules",
        ".vscode", ".idea", ".DS_Store", "build", "dist", "eggs", ".egg-info",
        "docs", "site", ".github", "htmlcov", ".tox", ".nox",
        "pip-wheel-metadata", "tmp", "temp", "data", "assets", "static", "media"
    }
    assert EXCLUDE_DIRS == expected_excludes


def test_create_inits_with_ignore_file(fs):
    """
    Test that __init__.py files are not created in directories specified
    in a .pyinitgenignore file.
    """
    # Arrange
    project_root = Path("/project_root_with_ignore")
    fs.create_dir(project_root / "package_x/subpackage_x")
    fs.create_dir(project_root / "ignored_by_file")
    fs.create_dir(project_root / "another_ignored/sub_ignored")
    fs.create_dir(project_root / "not_ignored")

    ignore_file_content = """
# This is a comment
ignored_by_file
another_ignored
    """
    fs.create_file(project_root / ".pyinitgenignore", contents=ignore_file_content)

    # Act
    exit_code, created_count, scanned_dirs = create_inits(project_root, dry_run=False)

    # Assert
    assert exit_code == 0
    # Expected: project_root, package_x, subpackage_x, not_ignored
    assert created_count == 4

    assert (project_root / "__init__.py").exists()
    assert (project_root / "package_x" / "__init__.py").exists()
    assert (project_root / "package_x" / "subpackage_x" / "__init__.py").exists()
    assert (project_root / "not_ignored" / "__init__.py").exists()

    # Assert that __init__.py are NOT created in directories ignored by the file
    assert not (project_root / "ignored_by_file" / "__init__.py").exists()
    assert not (project_root / "another_ignored" / "__init__.py").exists()
    assert not (project_root / "another_ignored" / "sub_ignored" / "__init__.py").exists()


def test_create_inits_with_custom_content(project_structure, fs):
    """
    Test that __init__.py files are created with the specified custom content.
    """
    # Arrange
    custom_content = "# This is a custom init file\n__version__ = '0.1.0'\n"

    # Act
    exit_code, created_count, scanned_dirs = create_inits(
        project_structure, dry_run=False, init_content=custom_content
    )

    # Assert
    assert exit_code == 0
    assert created_count == 5

    # Verify content of created __init__.py files
    assert (project_structure / "__init__.py").read_text(encoding="utf-8") == custom_content
    assert (project_structure / "package_a" / "__init__.py").read_text(encoding="utf-8") == custom_content

    # Ensure existing __init__.py files are not overwritten with custom content
    # For this, we need to create an existing __init__.py with different content
    # and then run create_inits again.
    # Note: The file already exists from the previous run in this test, so we overwrite it.
    (project_structure / "package_a" / "subpackage_a" / "__init__.py").write_text("existing content", encoding="utf-8")

    exit_code, created_count, scanned_dirs = create_inits(
        project_structure, dry_run=False, init_content="new content"
    )
    assert (project_structure / "package_a" / "subpackage_a" / "__init__.py").read_text(encoding="utf-8") == "existing content"
