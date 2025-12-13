# tests/test_cli_extended.py

import pytest
import logging
from pathlib import Path
from pyinitgen.cli import main, create_inits, load_ignore_patterns

@pytest.fixture
def temp_dir(fs):
    """
    Standardize on pyfakefs 'fs' fixture.
    """
    fs.create_dir("/root")
    return Path("/root")

def test_load_ignore_patterns_no_file(temp_dir):
    assert load_ignore_patterns(temp_dir) == set()

def test_load_ignore_patterns_empty_file(temp_dir, fs):
    fs.create_file(temp_dir / ".pyinitgenignore")
    assert load_ignore_patterns(temp_dir) == set()

def test_load_ignore_patterns_complex(temp_dir, fs):
    content = """
# comment
dir1

dir2/subdir
    """
    fs.create_file(temp_dir / ".pyinitgenignore", contents=content)
    patterns = load_ignore_patterns(temp_dir)
    assert "dir1" in patterns
    assert "dir2/subdir" in patterns
    assert "# comment" not in patterns
    assert "" not in patterns

def test_main_arguments(temp_dir, mocker):
    mocker.patch("sys.argv", ["pyinitgen", "--base-dir", str(temp_dir), "--dry-run", "--quiet", "--no-emoji"])
    mock_create = mocker.patch("pyinitgen.cli.create_inits")
    mock_create.return_value = (0, 0, 0)

    with pytest.raises(SystemExit) as e:
        main()

    assert e.value.code == 0
    mock_create.assert_called_with(
        temp_dir.resolve(),
        dry_run=True,
        verbose=False,
        use_emoji=False,
        init_content="",
        check=False
    )

def test_main_verbose(temp_dir, mocker):
    mocker.patch("sys.argv", ["pyinitgen", "--base-dir", str(temp_dir), "-v"])
    mock_create = mocker.patch("pyinitgen.cli.create_inits")
    mock_create.return_value = (0, 0, 0)

    with pytest.raises(SystemExit) as e:
        main()

    assert e.value.code == 0
    mock_create.assert_called_with(
        temp_dir.resolve(),
        dry_run=False,
        verbose=True,
        use_emoji=True,
        init_content="",
        check=False
    )

def test_main_custom_content(temp_dir, mocker):
    content = "a=1"
    mocker.patch("sys.argv", ["pyinitgen", "--base-dir", str(temp_dir), "--init-content", content])
    mock_create = mocker.patch("pyinitgen.cli.create_inits")
    mock_create.return_value = (0, 0, 0)

    with pytest.raises(SystemExit) as e:
        main()

    assert e.value.code == 0
    mock_create.assert_called_with(
        temp_dir.resolve(),
        dry_run=False,
        verbose=False,
        use_emoji=True,
        init_content=content,
        check=False
    )

def test_create_inits_error_handling(temp_dir, caplog, mocker, fs):
    # Simulate an error when writing a file
    fs.create_dir(temp_dir / "subdir")

    # Mock open to raise PermissionError
    mocker.patch("builtins.open", side_effect=PermissionError("Boom"))

    exit_code, created, scanned = create_inits(temp_dir)

    assert exit_code == 1
    assert "Failed to create" in caplog.text
    assert "Boom" in caplog.text

def test_create_inits_logging(temp_dir, caplog, fs):
    caplog.set_level(logging.DEBUG)
    fs.create_dir(temp_dir / "subdir")

    exit_code, created, scanned = create_inits(temp_dir, verbose=True)

    assert "Scanning:" in caplog.text
    assert (temp_dir / "subdir" / "__init__.py").exists()

def test_create_inits_dry_run_logging(temp_dir, caplog, fs):
    caplog.set_level(logging.INFO)
    fs.create_dir(temp_dir / "subdir")

    exit_code, created, scanned = create_inits(temp_dir, dry_run=True)

    assert "[DRY-RUN] Would create" in caplog.text
    assert "Dry-run complete" in caplog.text
    assert not (temp_dir / "subdir" / "__init__.py").exists()

def test_main_version(mocker):
    mocker.patch("sys.argv", ["pyinitgen", "--version"])

    with pytest.raises(SystemExit) as e:
        main()

    assert e.value.code == 0
