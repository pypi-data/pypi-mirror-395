#!/usr/bin/env python3
# src/pyinitgen/cli.py

import argparse
import logging
import os
from pathlib import Path
from .banner import print_logo
from .config import EXCLUDE_DIRS, IGNORE_FILE_NAME, load_config
from .ignores import load_ignore_patterns


def create_inits(
    base_dir: Path,
    dry_run: bool = False,
    verbose: bool = False,
    use_emoji: bool = True,
    init_content: str = "",
    check: bool = False,
):
    created_count = 0
    scanned_dirs = 0
    missing_count = 0
    
    user_excludes = load_ignore_patterns(base_dir)
    config_excludes = load_config(base_dir)
    all_excludes = EXCLUDE_DIRS.union(user_excludes).union(config_excludes)

    for root, dirs, files in os.walk(base_dir):
        # Filter out unwanted dirs
        dirs[:] = [d for d in dirs if d not in all_excludes]
        scanned_dirs += 1

        if verbose:
            logging.debug(f"Scanning: {root}")

        if "__init__.py" not in files:
            init_file = Path(root) / "__init__.py"

            if check:
                logging.error(f"Missing __init__.py in {root}")
                missing_count += 1
                continue

            if dry_run:
                logging.info(f"[DRY-RUN] Would create {init_file}")
            else:
                try:
                    with open(init_file, "w") as f:
                        f.write(init_content)
                    init_file.chmod(0o644) # Set permissions after writing
                    logging.info(f"Created {init_file}")
                    created_count += 1
                except Exception as e:
                    logging.error(f"Failed to create {init_file}: {e}")
                    return 1, created_count, scanned_dirs

    if check:
        if missing_count > 0:
            logging.error(f"Found {missing_count} missing __init__.py files.")
            return 1, created_count, scanned_dirs
        else:
            checkmark = "✅ " if use_emoji else ""
            logging.info(f"{checkmark}All directories have __init__.py files.")
            return 0, created_count, scanned_dirs

    if dry_run:
        logging.info("Dry-run complete. No files created.")
    else:
        checkmark = "✅ " if use_emoji else ""
        logging.info(
            f"{checkmark}Operation complete. "
            f"Scanned {scanned_dirs} dirs, created {created_count} new __init__.py files."
        )

    return 0, created_count, scanned_dirs


def main():
    print_logo()
    parser = argparse.ArgumentParser(
        description="Ensure all directories have __init__.py files."
    )
    parser.add_argument(
        "--base-dir",
        default=".",
        type=Path,
        help="Base directory to scan (default: current dir)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without writing"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress non-error logs"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show scanned directories"
    )
    parser.add_argument(
        "--no-emoji", action="store_true", help="Disable emoji in output"
    )
    parser.add_argument(
        "--init-content",
        type=str,
        default="",
        help="Content to write to new __init__.py files (default: empty file)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check for missing __init__.py files without creating them",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s 3.0.1", help="Show program's version number and exit"
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.ERROR
        if args.quiet
        else logging.DEBUG
        if args.verbose
        else logging.INFO,
        format="%(message)s",
    )

    exit_code, _, _ = create_inits(
        args.base_dir.resolve(),
        dry_run=args.dry_run,
        verbose=args.verbose,
        use_emoji=not args.no_emoji,
        init_content=args.init_content,
        check=args.check,
    )
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
