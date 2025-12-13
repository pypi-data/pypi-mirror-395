#!/usr/bin/env python3
# src/pypurge/cli.py

"""
pypurge - A production-grade Python cleanup utility.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import signal
import shutil
import sys
from pathlib import Path

from .modules.backup import backup_targets_atomic
from .modules.config import load_config
from .modules.config_wizard import run_init_wizard
from .modules.deletion import force_rmtree, force_unlink
from .modules.locking import acquire_lock, release_lock
from .modules.logging import setup_logging
from .modules.safety import is_dangerous_root
from .modules.scan import scan_for_targets
from .modules.ui import (
    get_colors,
    print_error,
    print_info,
    print_rich_preview,
    print_success,
    print_warning,
)
from .modules.utils import format_bytes, get_size
from .modules.args import parse_args, get_version, get_parser
from .modules.completions import generate_completion_script
from .banner import print_logo


# Exit codes
EXIT_OK = 0
EXIT_CANCELLED = 2
EXIT_PARTIAL_FAILURE = 3
EXIT_DANGEROUS_ROOT = 4
EXIT_LOCK_ERROR = 5
EXIT_UNKNOWN_ERROR = 6

# Defaults
DEFAULT_LARGE_THRESHOLD = 100 * 1024 * 1024  # 100MB

logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.completions:
        parser = get_parser()
        script = generate_completion_script(args.completions, parser)
        print(script)
        return EXIT_OK

    print_logo()

    if args.version:
        print(get_version())
        return EXIT_OK

    # logging
    log_file = Path(args.log_file) if args.log_file else None
    level = logging.INFO
    setup_logging(args.log_format, log_file, level=level, rotate=not args.no_rotate_log)

    if args.init:
        return run_init_wizard()

    # determine whether we should use pretty printing
    use_pretty = (
        (args.interactive or sys.stdout.isatty())
        and not args.no_color
        and args.log_format == "text"
    )
    colors = get_colors(use_pretty)

    # root checks (POSIX only)
    try:
        running_as_root = hasattr(os, "geteuid") and os.geteuid() == 0
    except Exception:
        running_as_root = False
    if running_as_root and not args.allow_root:
        logger.error(
            "Running as root is dangerous. Re-run with --allow-root if you really mean it."
        )
        if use_pretty:
            print_error(
                "Running as root is dangerous. Re-run with --allow-root if you really mean it.",
                colors,
            )
        return EXIT_DANGEROUS_ROOT

    root_paths = [Path(r).resolve() for r in args.root]

    if not args.allow_broad_root:
        for rp in root_paths:
            if is_dangerous_root(rp):
                logger.error(
                    "Target root %s looks dangerously broad. Re-run with --allow-broad-root if you mean it.",
                    rp,
                )
                if use_pretty:
                    print_warning(
                        f"Target root {rp} looks dangerously broad. Re-run with --allow-broad-root if you mean it.",
                        colors,
                    )
                return EXIT_DANGEROUS_ROOT

    # signal-safe storage for locks
    acquired_locks: dict[Path, int] = {}

    def _release_all_and_exit(signum=None, frame=None):
        logger.info("Signal received (%s). Releasing locks and exiting.", signum)
        for lp, fd in list(acquired_locks.items()):
            release_lock(fd, lp)
            acquired_locks.pop(lp, None)
        sys.exit(EXIT_CANCELLED)

    # register signals
    for s in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(s, _release_all_and_exit)
        except Exception:
            pass

    overall_failed = False

    for root_path in root_paths:
        logger.info("Starting cleanup in %s", root_path)
        if use_pretty:
            print_info(f"Starting Python project cleanup in {root_path}...", colors)

        lock_path = root_path / args.lockfile
        lock_fd = acquire_lock(lock_path, stale_seconds=args.lock_stale_seconds)
        if lock_fd is None:
            logger.error(
                "Unable to acquire lock for %s. Another run might be active (lockfile=%s).",
                root_path,
                lock_path,
            )
            if use_pretty:
                print_error(
                    f"Unable to acquire lock for {root_path}. Another run might be active (lockfile={lock_path}).",
                    colors,
                )
            for lp, fd in list(acquired_locks.items()):
                release_lock(fd, lp)
            return EXIT_LOCK_ERROR
        acquired_locks[lock_path] = lock_fd

        try:
            # load config
            cfg_path = (
                Path(args.config) if args.config else root_path / ".pypurge.json"
            )
            config = load_config(cfg_path)
            if config:
                logger.info("Loaded config %s", cfg_path)

            dir_groups = {
                "Python Caches": ["__pycache__"],
                "Build/Packaging": [
                    "*.egg-info",
                    "build",
                    "dist",
                    ".eggs",
                    "wheels",
                    "__pypackages__",
                    ".pdm-build",
                    "pip-wheel-metadata",
                    ".hatch",
                ],
                "Testing/Linting/Type-Checking": [
                    ".pytest_cache",
                    ".mypy_cache",
                    ".ruff_cache",
                    ".tox",
                    ".nox",
                    "htmlcov",
                    ".coverage_html",
                    ".hypothesis",
                    ".benchmarks",
                    ".dmypy",
                    ".pytype",
                    ".pyre",
                    "cover",
                ],
                "Jupyter": [".ipynb_checkpoints"],
                "Documentation": ["docs/_build"],
                "Cython": ["cython_debug"],
            }
            for g, pats in config.get("dir_groups", {}).items():
                if g in dir_groups:
                    dir_groups[g] += pats
                else:
                    dir_groups[g] = pats
            if args.clean_venv:
                venv_pats = [".venv", "venv", "env", "ENV", ".virtualenv"]
                dir_groups.setdefault("Virtual Environments", []).extend(venv_pats)

            file_groups = {
                "Python Bytecode": ["*.pyc", "*.pyo", "*.pyd"],
                "Coverage": [".coverage", "coverage.xml", "nosetests.xml", "*.cover"],
                "Editor/OS Temps": [
                    "*.swp",
                    "*.swo",
                    "*~",
                    "*.bak",
                    ".DS_Store",
                    "Thumbs.db",
                    "desktop.ini",
                    "._*",
                ],
                "DB Temps": ["*.db-wal", "*.db-shm"],
                "General Temps": ["*.tmp", "*.temp", "*.log", "CACHEDIR.TAG"],
                "Profiling": ["*.prof"],
                "Installer Logs": ["pip-log.txt", "pip-delete-this-directory.txt"],
                "PyInstaller": ["*.manifest", "*.spec"],
            }
            for g, pats in config.get("file_groups", {}).items():
                if g in file_groups:
                    file_groups[g] += pats
                else:
                    file_groups[g] = pats

            exclude_dirs = {".git", ".svn", ".hg", ".idea", ".vscode"} | set(
                config.get("exclude_dirs", [])
            )
            exclude_patterns = []
            excludes = list(args.exclude) + config.get("exclude_patterns", [])
            for ex in excludes:
                if isinstance(ex, str) and ex.startswith("re:"):
                    try:
                        exclude_patterns.append(("re", re.compile(ex[3:])))
                    except re.error:
                        logger.warning("Invalid regex exclude %s", ex)
                else:
                    exclude_patterns.append(("glob", ex))

            older_than_sec = args.older_than * 86400 if args.older_than > 0 else 0

            # scan
            targets = scan_for_targets(
                root_path,
                dir_groups,
                file_groups,
                exclude_dirs,
                exclude_patterns,
                older_than_sec,
                args.age_type,
                args.delete_symlinks,
                use_gitignore=not args.no_gitignore,
            )

            all_targets = [
                p for group_targets in targets.values() for p in group_targets
            ]
            total_items = len(all_targets)

            if total_items == 0:
                logger.info("Project is already clean. No targets found.")
                if use_pretty:
                    print_success("Project is already clean. No targets found.", colors)
                release_lock(lock_fd, lock_path)
                acquired_locks.pop(lock_path, None)
                continue

            sizes = {p: get_size(p) for p in all_targets}
            total_size = sum(sizes.values())
            size_str = format_bytes(total_size)

            if args.quiet:
                logger.info(
                    "Found %d items (estimated space: %s).", total_items, size_str
                )
            else:
                if use_pretty:
                    print_rich_preview(root_path, targets, sizes, colors)
                else:
                    logger.info(
                        "Found %d items to clean (approx %s).", total_items, size_str
                    )

            if args.preview:
                logger.info("Dry run complete. No files were deleted.")
                if use_pretty:
                    print_info("Dry run complete. No files were deleted.", colors)
                release_lock(lock_fd, lock_path)
                acquired_locks.pop(lock_path, None)
                continue

            if total_size > DEFAULT_LARGE_THRESHOLD:
                logger.warning(
                    "Large amount of data to delete (%s > 100MB). Proceed with caution.",
                    size_str,
                )
                if use_pretty:
                    print_warning(
                        f"Large amount of data to delete ({size_str} > 100MB). Proceed with caution.",
                        colors,
                    )

            if not args.yes:
                try:
                    prompt = "Proceed with deletion? (y/N): "
                    ans = input(prompt).strip().lower()
                except EOFError:
                    ans = "n"
                if ans not in ("y", "yes"):
                    logger.info("Operation cancelled by user.")
                    if use_pretty:
                        print_info("Operation cancelled by user.", colors)
                    release_lock(lock_fd, lock_path)
                    acquired_locks.pop(lock_path, None)
                    return EXIT_CANCELLED

            # backup
            if args.backup:
                backup_root = (
                    Path(args.backup_dir).resolve() if args.backup_dir else root_path
                )
                logger.info("Creating backup in %s", backup_root)
                res = backup_targets_atomic(
                    all_targets, backup_root, root_path, name=args.backup_name
                )
                if not res:
                    logger.error("Backup failed; aborting deletion for safety.")
                    release_lock(lock_fd, lock_path)
                    acquired_locks.pop(lock_path, None)
                    return EXIT_UNKNOWN_ERROR
                else:
                    archive_file, sha = res
                    logger.info("Backup created: %s (sha256=%s)", archive_file, sha)
                    if use_pretty:
                        print_success(
                            f"Backup created: {archive_file} (sha256={sha})", colors
                        )

            # deletion
            failed = False
            sorted_targets = sorted(
                all_targets, key=lambda p: str(p.relative_to(root_path))
            )
            total = len(sorted_targets)
            for i, p in enumerate(sorted_targets, 1):
                if not args.quiet:
                    suffix = (
                        "/"
                        if p.is_dir() and not p.is_symlink()
                        else " (symlink)"
                        if p.is_symlink()
                        else ""
                    )
                    msg = (
                        f"[{i}/{total}] Deleting {p.relative_to(root_path)}{suffix}..."
                    )
                    if use_pretty:
                        print(msg)
                    else:
                        logger.info(msg)
                try:
                    if p.is_symlink():
                        if args.delete_symlinks:
                            p.unlink(missing_ok=True)
                    elif p.is_file():
                        if args.force:
                            force_unlink(p)
                        else:
                            p.unlink(missing_ok=True)
                    elif p.is_dir():
                        if args.force:
                            force_rmtree(p)
                        else:
                            try:
                                shutil.rmtree(p)
                            except FileNotFoundError:
                                pass
                except Exception as e:
                    logger.warning("Failed to delete %s: %s", p, e)
                    if use_pretty:
                        print_warning(
                            f"Failed to delete {p.relative_to(root_path)}: {e}", colors
                        )
                    failed = True

            if failed:
                logger.warning(
                    "Some items could not be deleted. Consider --force or check permissions."
                )
                overall_failed = True
            else:
                logger.info(
                    "Cleanup complete for %s. Freed approximately %s.",
                    root_path,
                    size_str,
                )
                if use_pretty:
                    print_success(
                        f"Cleanup complete! Freed approximately {size_str}.", colors
                    )

        finally:
            # release this lock
            release_lock(lock_fd, lock_path)
            acquired_locks.pop(lock_path, None)

    if overall_failed:
        return EXIT_PARTIAL_FAILURE
    return EXIT_OK


def _main():
    """Wrapper for the main function to handle exceptions."""
    exit_code = EXIT_OK
    try:
        exit_code = main()
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
        exit_code = EXIT_CANCELLED
    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        exit_code = EXIT_UNKNOWN_ERROR
    finally:
        sys.exit(exit_code)

if __name__ == "__main__":
    _main()
