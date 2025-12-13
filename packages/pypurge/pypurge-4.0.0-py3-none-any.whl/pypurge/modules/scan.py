# src/pypurge/modules/scan.py

import fnmatch
import os
import re
from collections import defaultdict
from pathlib import Path
import pathspec

from .utils import is_old_enough


def load_gitignore_patterns(path: Path) -> list[str]:
    """
    Loads .gitignore patterns from a specific path as a list of strings.
    """
    gitignore_path = path / ".gitignore"
    if gitignore_path.exists():
        try:
            with open(gitignore_path, "r") as f:
                return f.read().splitlines()
        except Exception:
            pass
    return []


def scan_for_targets(
    root_path: Path,
    dir_groups: dict,
    file_groups: dict,
    exclude_dirs: set,
    exclude_patterns: list,
    older_than_sec: int,
    age_type: str,
    delete_symlinks: bool,
    use_gitignore: bool = True,
) -> dict:
    targets = defaultdict(list)

    # State for nested .gitignore support
    # Maps directory path -> list of accumulated patterns
    active_patterns: dict[Path, list[str]] = {}
    # Maps directory path -> compiled PathSpec
    active_specs: dict[Path, pathspec.PathSpec] = {}

    if use_gitignore:
        # Initialize root patterns
        root_patterns = load_gitignore_patterns(root_path)
        active_patterns[root_path] = root_patterns
        if root_patterns:
            active_specs[root_path] = pathspec.PathSpec.from_lines("gitwildmatch", root_patterns)

    # Pre-calculate regex for excludes to save time
    compiled_excludes = []
    for pt, pat in exclude_patterns:
        if pt == "re":
            compiled_excludes.append(("re", pat))
        else:
            compiled_excludes.append(("glob", pat))

    for root, dirs, files in os.walk(root_path, topdown=True, followlinks=False):
        current_path = Path(root)

        try:
            rel_root = current_path.relative_to(root_path)
        except Exception:
            rel_root = Path(".")

        # Update gitignore context for this directory
        spec = None
        if use_gitignore:
            if current_path != root_path:
                parent = current_path.parent
                parent_patterns = active_patterns.get(parent, [])
                local_patterns = load_gitignore_patterns(current_path)

                if not local_patterns:
                    active_patterns[current_path] = parent_patterns
                    active_specs[current_path] = active_specs.get(parent)
                else:
                    rewritten = []
                    prefix = str(rel_root).replace(os.sep, "/") + "/"
                    if prefix == "./": prefix = ""

                    for p in local_patterns:
                        p = p.strip()
                        if not p or p.startswith("#"):
                            continue

                        is_negated = p.startswith("!")
                        if is_negated:
                            p = p[1:]

                        if p.startswith("/"):
                            new_p = "/" + prefix + p[1:]
                        else:
                            new_p = p

                        if is_negated:
                            rewritten.append("!" + new_p)
                        else:
                            rewritten.append(new_p)

                    combined = parent_patterns + rewritten
                    active_patterns[current_path] = combined
                    active_specs[current_path] = pathspec.PathSpec.from_lines("gitwildmatch", combined)

            spec = active_specs.get(current_path)

        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        # Directories
        for d in list(dirs):
            d_path = current_path / d
            rel_path = rel_root / d
            rel_str = str(rel_path)

            # 0. Symlink Safety (Priority 0)
            if d_path.is_symlink() and not delete_symlinks:
                continue

            # 1. Check exclude patterns (Priority 1)
            if any(
                (pt == "re" and pat.search(rel_str))
                or (pt == "glob" and fnmatch.fnmatch(rel_str, pat))
                for pt, pat in compiled_excludes
            ):
                dirs.remove(d)
                continue

            # 2. Check targets (Priority 2)
            matched = False
            for g, pats in dir_groups.items():
                for pat in pats:
                    try:
                        if fnmatch.fnmatch(d, pat) or fnmatch.fnmatch(rel_str, pat):
                            if older_than_sec and not is_old_enough(d_path, older_than_sec, age_type):
                                matched = True
                                break
                            targets[g].append(d_path)
                            matched = True
                            break
                    except Exception:
                        continue
                if matched:
                    break

            if matched:
                if d in dirs:
                    dirs.remove(d)
                continue

            # 3. Check gitignore (Priority 3)
            if spec:
                 if spec.match_file(rel_str):
                     dirs.remove(d)
                     continue
                 if spec.match_file(rel_str + "/"):
                     dirs.remove(d)
                     continue

        # Files
        for f in files:
            f_path = current_path / f
            rel_path = rel_root / f
            rel_str = str(rel_path)

            # 0. Symlink Safety
            if f_path.is_symlink() and not delete_symlinks:
                continue

            # 1. Excludes
            if any(
                (pt == "re" and pat.search(rel_str))
                or (pt == "glob" and fnmatch.fnmatch(rel_str, pat))
                for pt, pat in compiled_excludes
            ):
                continue

            # 2. Targets
            matched = False
            for g, pats in file_groups.items():
                for pat in pats:
                    try:
                        if fnmatch.fnmatch(f, pat) or fnmatch.fnmatch(rel_str, pat):
                            if older_than_sec and not is_old_enough(f_path, older_than_sec, age_type):
                                matched = True
                                break
                            targets[g].append(f_path)
                            matched = True
                            break
                    except Exception:
                        continue
                if matched:
                    break

            if matched:
                continue

            # 3. Gitignore
            if spec and spec.match_file(rel_str):
                continue

    return targets
