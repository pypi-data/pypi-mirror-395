import os
from pathlib import Path
from pypurge.modules.scan import scan_for_targets

def test_scan_priorities_and_gitignore(fs):
    root = Path("/project")
    fs.create_dir(root)

    # .gitignore content
    # ignores ignored_dir/ and *.ignored and *.pyc
    fs.create_file(root / ".gitignore", contents="ignored_dir/\n*.ignored\n*.pyc\n")

    # --- Case 1: Exclude Patterns vs Targets ---
    # "important.log" is a target (e.g. *.log), but explicitly excluded in exclude_patterns.
    # Exclude (Priority 1) should win.
    fs.create_file(root / "important.log")

    # --- Case 2: Targets vs Gitignore ---
    # "trash.pyc" is in gitignore (*.pyc), but is a target (*.pyc).
    # Target (Priority 2) should win over Gitignore (Priority 3).
    fs.create_file(root / "trash.pyc")

    # --- Case 3: Gitignore Only ---
    # "random.ignored" is in gitignore (*.ignored), not a target.
    # Gitignore should win (ignore it).
    fs.create_file(root / "random.ignored")

    # --- Case 4: Directory in Gitignore (with trailing slash) ---
    # "ignored_dir/" in gitignore.
    # ignored_dir should be skipped.
    fs.create_dir(root / "ignored_dir")
    fs.create_file(root / "ignored_dir" / "nested.file") # Should not be scanned

    # --- Case 5: Directory Target vs Gitignore ---
    # "clean_me/" is in gitignore (let's add it dynamically or assume behavior)
    # Let's say we have another gitignore rule "clean_me/"
    # But clean_me is a target.
    # Target should win.
    fs.create_dir(root / "clean_me")
    with open(root / ".gitignore", "a") as f:
        f.write("clean_me/\n")

    dir_groups = {"Clean": ["clean_me"]}
    file_groups = {"Logs": ["*.log"], "Pyc": ["*.pyc"]}
    exclude_dirs = set()
    exclude_patterns = [("glob", "important.log")] # Explicit user exclusion

    # Add a file in ignored_dir that would match a target if scanned
    fs.create_file(root / "ignored_dir" / "bad.log") # matches *.log target

    targets = scan_for_targets(
            root_path=root,
            dir_groups=dir_groups,
            file_groups=file_groups,
            exclude_dirs=exclude_dirs,
            exclude_patterns=exclude_patterns,
            older_than_sec=0,
            age_type="mtime",
            delete_symlinks=False,
            use_gitignore=True
    )

    all_targets = [p for sublist in targets.values() for p in sublist]

    # 1. important.log should NOT be in targets (Exclude > Target)
    assert root / "important.log" not in all_targets

    # 2. trash.pyc should be in targets (Target > Gitignore)
    assert root / "trash.pyc" in all_targets

    # 3. random.ignored should NOT be in targets (Gitignore)
    assert root / "random.ignored" not in all_targets

    # 4. ignored_dir should NOT be in targets (Gitignore)
    # And we should verify we didn't scan inside?
    # bad.log inside ignored_dir should NOT be in targets.
    assert root / "ignored_dir" / "bad.log" not in all_targets

    # 5. clean_me should be in targets (Target > Gitignore)
    assert root / "clean_me" in all_targets
