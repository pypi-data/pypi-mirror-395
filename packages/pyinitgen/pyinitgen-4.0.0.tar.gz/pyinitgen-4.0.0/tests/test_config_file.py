import pytest
import os
from pathlib import Path
from pyinitgen.cli import create_inits

# Tests for loading configuration from toml files.
# Uses pyfakefs 'fs' fixture.

def test_config_from_pyproject_toml(fs):
    """
    Test that excludes are read from pyproject.toml
    """
    # Arrange
    # Create pyproject.toml with custom excludes
    fs.create_file(
        "pyproject.toml",
        contents="""
[tool.pyinitgen]
exclude_dirs = ["ignored_dir"]
"""
    )

    # Create directory structure
    fs.create_dir("ignored_dir")
    fs.create_dir("normal_dir")

    # Act
    create_inits(Path("."))

    # Assert ignored_dir does not have __init__.py
    assert not os.path.exists("ignored_dir/__init__.py")

    # Assert normal_dir has __init__.py
    assert os.path.exists("normal_dir/__init__.py")

def test_config_from_pyinitgen_toml(fs):
    """
    Test that excludes are read from .pyinitgen.toml
    """
    # Arrange
    # Create .pyinitgen.toml with custom excludes
    fs.create_file(
        ".pyinitgen.toml",
        contents="""
[tool.pyinitgen]
exclude_dirs = ["ignored_dir_2"]
"""
    )

    # Create directory structure
    fs.create_dir("ignored_dir_2")
    fs.create_dir("normal_dir_2")

    # Act
    create_inits(Path("."))

    # Assert ignored_dir_2 does not have __init__.py
    assert not os.path.exists("ignored_dir_2/__init__.py")

    # Assert normal_dir_2 has __init__.py
    assert os.path.exists("normal_dir_2/__init__.py")
