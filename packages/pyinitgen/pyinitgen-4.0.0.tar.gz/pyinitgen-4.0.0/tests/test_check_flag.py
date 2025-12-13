
import pytest
import os
from pathlib import Path
from pyinitgen.cli import create_inits

def test_check_flag_fail(fs):
    """
    Test that --check returns 1 if __init__.py is missing
    """
    # Arrange
    fs.create_dir("test_dir")

    # Act
    exit_code, created, scanned = create_inits(Path("."), check=True)

    # Assert
    assert exit_code == 1
    assert created == 0
    assert not os.path.exists("test_dir/__init__.py")

def test_check_flag_pass(fs):
    """
    Test that --check returns 0 if all __init__.py exist
    """
    # Arrange
    fs.create_dir("test_dir")
    fs.create_file("test_dir/__init__.py")
    fs.create_file("__init__.py")

    # Act
    exit_code, created, scanned = create_inits(Path("."), check=True)

    # Assert
    assert exit_code == 0
    assert created == 0
