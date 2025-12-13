<div align="center">
  <img src="https://raw.githubusercontent.com/dhruv13x/pypurge/main/pypurge_logo.png" alt="pypurge logo" width="200"/>
</div>

<div align="center">

<!-- Package Info -->
[![PyPI version](https://img.shields.io/pypi/v/pypurge.svg)](https://pypi.org/project/pypurge/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
![Wheel](https://img.shields.io/pypi/wheel/pypurge.svg)
[![Release](https://img.shields.io/badge/release-PyPI-blue)](https://pypi.org/project/pypurge/)

<!-- Build & Quality -->
[![Build status](https://github.com/dhruv13x/pypurge/actions/workflows/publish.yml/badge.svg)](https://github.com/dhruv13x/pypurge/actions/workflows/publish.yml)
[![Codecov](https://codecov.io/gh/dhruv13x/pypurge/graph/badge.svg)](https://codecov.io/gh/dhruv13x/pypurge)
[![Test Coverage](https://img.shields.io/badge/coverage-90%25%2B-brightgreen.svg)](https://github.com/dhruv13x/pypurge/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/linting-ruff-yellow.svg)](https://github.com/astral-sh/ruff)
![Security](https://img.shields.io/badge/security-CodeQL-blue.svg)

<!-- Usage -->
![Downloads](https://img.shields.io/pypi/dm/pypurge.svg)
![OS](https://img.shields.io/badge/os-Linux%20%7C%20macOS%20%7C%20Windows-blue.svg)
[![Python Versions](https://img.shields.io/pypi/pyversions/pypurge.svg)](https://pypi.org/project/pypurge/)

<!-- License -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

# 🧹 pypurge — Safe & Powerful Python Project Cleaner

**pypurge** is a production-grade Python cleanup utility designed to safely remove auto-generated files, caches, virtualenv leftovers, test artifacts, temporary files, and clutter — **without putting your system at risk.**

Think of it as a **precision broom for Python projects**.  
No more `find . -name __pycache__ -delete` or risky scripts — **clean confidently, with safety rails.**

---

## 🚀 Quick Start

### Prerequisites
*   Python 3.8+
*   `rich` (UI), `pathspec` (Gitignore), `jsonschema` (Validation) — *installed automatically*

### Installation

```bash
pip install pypurge
```

### Usage

**Clean current project interactively:**
```bash
pypurge
```

**Preview everything — no deletions:**
```bash
pypurge --preview
```

---

## ✨ Key Features

*   **🛡️ Safety-first Design**: Prevents accidental root-level deletion and protects system directories.
*   **🎯 Targeted Cleanup**: Smartly handles `__pycache__`, `.pytest_cache`, `build/`, `dist/`, `.egg-info`, and more.
*   **🧠 Smart Preview**: Shows detailed counts, groups, and disk usage before you confirm deletion.
*   **🪄 Configuration Wizard**: Easily setup exclusions with `pypurge --init`.
*   **📦 Atomic Backups**: Create a zip backup with SHA256 manifest before cleaning (`--backup`).
*   **🪪 Concurrency Safety**: Stale lock & lockfile protection to avoid multi-process conflicts.
*   **🕒 Age-based Filtering**: Delete only items older than N days (`--older-than`).
*   **🧹 Virtualenv Purge**: Optional cleaning of virtual environments (`--clean-venv`).
*   **⚙️ Highly Configurable**: Use CLI arguments or `.pypurge.json` for persistent settings.
*   **🤖 CI/CD Ready**: Supports non-interactive modes (`--yes`, `--quiet`, `--log-format json`).
*   **🛡️ Gitignore Awareness**: Respects `.gitignore` rules (including nested ones) to avoid cleaning untracked files (`--no-gitignore` to disable).
*   **🐚 Shell Completions**: Native auto-completion for `bash`, `zsh`, and `fish` to speed up CLI usage.

---

## ⚙️ Configuration & Advanced Usage

While `pypurge` works great out of the box, you can fine-tune its behavior with command-line arguments or a configuration file.

### Shell Completions

You can generate shell completion scripts to make using `pypurge` even easier.

**Bash:**
```bash
pypurge --completions bash > /etc/bash_completion.d/pypurge
# or source directly
source <(pypurge --completions bash)
```

**Zsh:**
```bash
pypurge --completions zsh > ~/.zfunc/_pypurge
# Ensure ~/.zfunc is in your fpath
```

**Fish:**
```bash
pypurge --completions fish > ~/.config/fish/completions/pypurge.fish
```

### CLI Arguments

| Argument | Short | Description | Default |
| :--- | :--- | :--- | :--- |
| `root...` | | Directories to clean. | `.` (current directory) |
| `--preview` | `-p` | Preview targets without deleting anything. | `False` |
| `--yes` | `-y` | Skip the interactive confirmation prompt. | `False` |
| `--quiet` | `-q` | Suppress all output except for critical errors. | `False` |
| `--clean-venv` | | Include virtual environment folders (`.venv`, `venv`) in the scan. | `False` |
| `--exclude <pattern>` | | Exclude files/directories matching a glob or `re:` pattern. | (none) |
| `--older-than <days>` | | Only target files older than `N` days. | `0` (all ages) |
| `--age-type <type>` | | Age metric: `mtime` (modified), `atime` (accessed), `ctime` (created). | `mtime` |
| `--force` | | Attempt to `chmod` files to ensure deletion. | `False` |
| `--backup` | | Create a `.zip` backup of all targets before deletion. | `False` |
| `--backup-dir <path>` | | Specify a directory to store backups. | (root of scan) |
| `--backup-name <name>` | | Set a reproducible base name for backup archives. | (auto-generated) |
| `--no-color` | | Disable colored output. | `False` |
| `--delete-symlinks` | | Also delete symbolic links (the link itself, not the target). | `False` |
| `--config <path>` | | Path to a `.pypurge.json` configuration file. | (auto-detect) |
| `--allow-broad-root` | | **DANGEROUS**: Allow running in broad directories like `/` or `$HOME`. | `False` |
| `--allow-root` | | **DANGEROUS**: Allow running as the `root` user. | `False` |
| `--lockfile <name>` | | Name of the lockfile to prevent concurrent runs. | `.pypurge.lock` |
| `--lock-stale-seconds <N>` | | Time in seconds before a lock is considered stale. | `86400` (24h) |
| `--log-file <path>` | | Path to a file for logging output. | (none) |
| `--log-format <format>` | | Log format: `text` or `json`. | `text` |
| `--no-rotate-log` | | Disable log file rotation. | `False` |
| `--interactive` | | Force interactive pretty output (colors). | `False` |
| `--version` | `-v` | Show the application version and exit. | `False` |
| `--init` | | Run the configuration wizard. | `False` |
| `--no-gitignore` | | Do not respect .gitignore files (enabled by default). | `False` |
| `--completions` | | Generate shell completion script (`bash`, `zsh`, `fish`). | (none) |

### Configuration File (`.pypurge.json`)

You can create a `.pypurge.json` file in the root of your project to define custom patterns and exclusions. Use `pypurge --init` to generate one.

**Advanced Validation:**
The configuration file is validated against a strict schema. `exclude_patterns` supports regex patterns prefixed with `re:`. These are compiled and validated at runtime to prevent invalid regex errors.

```json
{
  "exclude_dirs": [".git", "node_modules"],
  "exclude_patterns": ["re:.*migrations.*", "data/"],
  "dir_groups": {
    "CustomData": ["temp_run/", "scratch/"]
  },
  "file_groups": {
    "Logs": ["*.log"]
  }
}
```

---

## 🏗️ Architecture

The project follows a modular structure to separate concerns:

```
src/pypurge/
├── cli.py             # Main entry point, argument parsing
└── modules/
    ├── args.py        # Argument parsing logic
    ├── backup.py      # Atomic backup logic
    ├── completions.py # Shell completion scripts
    ├── config.py      # Configuration schema and validation
    ├── config_wizard.py # Interactive configuration generator
    ├── deletion.py    # Safe file/directory removal
    ├── locking.py     # Cross-process lock management
    ├── logging.py     # Logging setup
    ├── safety.py      # Guards against dangerous operations
    ├── scan.py        # Core target scanning logic
    ├── ui.py          # Rich terminal output
    └── utils.py       # Helper functions
```

**Core Logic Flow:**
1.  **Parse Arguments**: `cli.py` handles user input and configuration.
2.  **Safety Checks**: `safety.py` ensures we aren't running in a dangerous context (e.g., root directory).
3.  **Acquire Lock**: `locking.py` prevents concurrent runs in the same directory.
4.  **Scan**: `scan.py` identifies files and directories to be deleted based on predefined and custom patterns.
5.  **Confirm**: The user is presented with a `rich` preview (via `ui.py`) and prompted to proceed.
6.  **Backup (Optional)**: `backup.py` creates an atomic archive of targets.
7.  **Delete**: `deletion.py` removes the targets.
8.  **Release Lock**: The lock is released.

---

## 🗺️ Roadmap

Our vision for `pypurge` is just getting started. We have ambitious plans for new features, integrations, and AI-powered capabilities.

To see the full, detailed plan, please check out our official [**Project Roadmap**](ROADMAP.md).

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) (if available) or simply fork the repository and submit a Pull Request.

---

## 🪪 License

MIT © Dhruv
