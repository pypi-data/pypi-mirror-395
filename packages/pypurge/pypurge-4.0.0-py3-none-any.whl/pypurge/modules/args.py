from __future__ import annotations

import argparse
from importlib import metadata

try:
    __version__ = metadata.version("pypurge")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"

# Defaults
DEFAULT_LOCK_TTL = 24 * 3600  # 24 hours stale lock threshold

def get_parser() -> argparse.ArgumentParser:
    """
    Creates and returns the argument parser.
    """
    parser = argparse.ArgumentParser(
        prog="pypurge", description="Production-grade Python cleanup tool"
    )
    parser.add_argument(
        "root",
        nargs="*",
        default=["."],
        help="Directories to clean (default: current).",
    )
    parser.add_argument(
        "-p", "--preview", action="store_true", help="Preview only (no deletions)."
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Assume yes (skip interactive confirm).",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Quiet mode: fewer prints."
    )
    parser.add_argument(
        "--clean-venv",
        action="store_true",
        help="Also clean virtualenv folders (.venv, venv...).",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Glob or regex (re:) pattern to exclude. Can be used multiple times.",
    )
    parser.add_argument(
        "--older-than",
        type=int,
        default=0,
        help="Only consider items older than N days.",
    )
    parser.add_argument(
        "--age-type", choices=["mtime", "atime", "ctime"], default="mtime"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force deletion by attempting chmod when needed.",
    )
    parser.add_argument(
        "--backup", action="store_true", help="Create a backup archive before deleting."
    )
    parser.add_argument(
        "--backup-dir", default=None, help="Directory to place backups (default: root)."
    )
    parser.add_argument(
        "--backup-name",
        default=None,
        help="Base name for backups (makes names reproducible).",
    )
    parser.add_argument(
        "--no-color", action="store_true", help="Disable colored output."
    )
    parser.add_argument(
        "--delete-symlinks",
        action="store_true",
        help="Include symlinks in cleanup (delete link only).",
    )
    parser.add_argument("--config", default=None, help="Path to config JSON file.")
    parser.add_argument(
        "--allow-broad-root",
        action="store_true",
        help="Allow running against broad roots like / or home.",
    )
    parser.add_argument(
        "--allow-root", action="store_true", help="Allow running as root (dangerous)."
    )
    parser.add_argument(
        "--lockfile",
        default=".pypurge.lock",
        help="Path to lockfile (relative to each root).",
    )
    parser.add_argument(
        "--lock-stale-seconds",
        type=int,
        default=DEFAULT_LOCK_TTL,
        help="Stale lock TTL in seconds.",
    )
    parser.add_argument(
        "--log-format", choices=["text", "json"], default="text", help="Logging format."
    )
    parser.add_argument("--log-file", default=None, help="Optional log file path.")
    parser.add_argument(
        "--no-rotate-log", action="store_true", help="Disable log file rotation."
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Force interactive pretty output (colors), useful when piping to terminal.",
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="Show version and exit."
    )
    parser.add_argument(
        "--init", action="store_true", help="Run the configuration wizard."
    )
    parser.add_argument(
        "--no-gitignore",
        action="store_true",
        help="Do not respect .gitignore files (enabled by default).",
    )
    parser.add_argument(
        "--completions",
        choices=["bash", "zsh", "fish"],
        help="Generate shell completion script.",
    )
    return parser

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """
    Parses command-line arguments.
    """
    parser = get_parser()
    return parser.parse_args(argv)

def get_version() -> str:
    return __version__
